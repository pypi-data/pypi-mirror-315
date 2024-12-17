#!/usr/bin/env -S poetry run python
"""This is a script which uses the ONVIF protocol to discover RTSP cameras
on the local network.
It tries to guess the username/password for each camera.
It then prints out the RTSP URLs for each camera.
"""
import os
import time
import traceback
import logging

import typer
from onvif import ONVIFCamera
from wsdiscovery.discovery import ThreadedWSDiscovery as WSDiscovery
import onvif

app = typer.Typer()

# Create a logger instance for this module
logger = logging.getLogger(__name__)

def onvif_discover(verbose:bool = True) -> list[str]:
    """Use WSDiscovery to find ONVIF devices.
    Returns a list of IP addresses of ONVIF devices.
    """
    device_ips = set()
    logger.debug("Starting WSDiscovery for ONVIF devices")
    wsd = WSDiscovery()
    #wsd.addSourceAddr("")  # maybe to pick the right interface?
    wsd.start()
    ret = wsd.searchServices()
    for service in ret:
        xaddr = service.getXAddrs()[0]
        # each service has a bunch of QName's == qualified names
        qnames = service.getTypes()
        for qname in qnames:
            # the qname's we care about are 
            # - http://www.onvif.org/ver10/network/wsdl:NetworkVideoTransmitter
            # - http://www.onvif.org/ver10/device/wsdl:Device
            if "onvif" in str(qname):
                logger.debug(f"Found ONVIF service {qname} at {xaddr}")
                # xaddr will be like "http://10.44.2.95/onvif/device_service"
                ip = xaddr.split("//")[1].split("/")[0]
                device_ips.add(ip)   
    wsd.stop()
    return list(device_ips)

def find_token(profile: "onvif.client.ONVIFProfile") -> str:
    """Find the token for an onvif profile."""
    try:
        # In my experience, it seems to be just ".token"
        return profile.token
    except AttributeError:
        pass
    try:
        # Docs often say it's suppoed to by "._token"
        return profile._token
    except AttributeError:
        logger.warning(f"Failed to find profile token for {profile}")
        raise


def enumerate_rtsp_urls(ip: str, username: str = "admin", password: str = "admin") -> list[str]:
    """Fetch RTSP URLs from an ONVIF device, given a username/password.
    Returns [] if the device is unreachable or the credentials are wrong.
    """
    #TODO: we should include more metadata in the response somehow.
    # Things like the resolution are pretty useful.
    # Maybe we should return a dict with the IP, username, password, and RTSP URL?
    rtsp_urls = []
    try:
        try:
            # Assuming port 80, adjust if necessary
            cam = ONVIFCamera(ip, 80, username, password)
            # Create media service
            media_service = cam.create_media_service()
            # Get profiles
            profiles = media_service.GetProfiles()
            # For each profile, get the RTSP URL
            for profile in profiles:
                reqobj = media_service.create_type('GetStreamUri')
                reqobj.ProfileToken = find_token(profile)
                reqobj.StreamSetup = {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}}
                uri = media_service.GetStreamUri(reqobj)
                rtsp_urls.append(uri.Uri)
        except onvif.exceptions.ONVIFError as e:
            msg = str(e).lower()
            if "auth" in msg:  # looks like a bad login - give up.
                return []
            else:
                raise  # something else
    except Exception as e:
        logger.error(f"Error fetching RTSP URL for {ip}: {e}", exc_info=True)

    # Now insert the username/password into the URLs
    for i, url in enumerate(rtsp_urls):
        rtsp_urls[i] = url.replace("rtsp://", f"rtsp://{username}:{password}@")
    return rtsp_urls


DEFAULT_CREDENTIALS = [
    ("admin", "admin"),
    ("admin", ""),
    ("", ""),
    ("root", "camera"),
    ("root", "root"),
    ("admin", "12345"),
    ("admin", "123456"),
    ("admin", "password"),
    ("user", "user"),
    ("root", "pass"),
]

def guess_rtsp_logins(ips: list[str]) -> list[str]:
    """Tries guessing common username/password combinations for ONVIF devices.
    Returns a list of RTSP URLs that are discovered.
    """
    # TODO: add the username/pass into the URL
    found_urls = []
    remaining_ips = ips.copy()

    for username, password in DEFAULT_CREDENTIALS:
        # Outer loop on creds so we slow down how fast we hit
        # any device.
        if not remaining_ips:  # Stop if no IPs left
            break
        logger.debug(f"Trying {username}:{password} on {len(remaining_ips)} IPs")
        for ip in remaining_ips[:]:  # copy the list for safe removal during iteration
            out = enumerate_rtsp_urls(ip, username, password)
            if out:
                found_urls.extend(out)
                remaining_ips.remove(ip)  # Remove IP if credentials were successful
            else:
                time.sleep(2)
    no_credentials_urls = generate_no_credentials_urls(remaining_ips)
    found_urls.extend(no_credentials_urls)
    return found_urls


def generate_no_credentials_urls(ips: list[str]) -> list[str]:
    """Generate RTSP URLs for ONVIF devices where we didn't figure out the 
    credentials, so we don't lose them.
    """
    return [f"rtsp://username:unknown_password@{ip}/onvif1" for ip in ips]

@app.command()
def discover_cameras(verbose: bool = True) -> list[str]:
    """Returns a list of RTSP URLs for ONVIF cameras on the network."""
    camera_ips = onvif_discover(verbose)
    logger.info(f"Found {len(camera_ips)} ONVIF devices - trying default credentials")
    rtsp_urls = guess_rtsp_logins(camera_ips)
    logger.info(f"Found {len(rtsp_urls)} streams:")
    for url in rtsp_urls:
        logger.info(url)
    return rtsp_urls

@app.command()
def climain(verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output")):
    if verbose:
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')
        logger.debug("Verbose output enabled")
    else:
        logging.basicConfig(level=logging.INFO, format='%(message)s')
    app()

if __name__ == "__main__":
    climain()