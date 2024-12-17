import socket
import os
import psutil
from groundlight import Groundlight 
from groundlight.client import ApiTokenError, GroundlightClientError


def get_groundlight_service_info() -> dict:
    """
    Gathers info about connectivity to groundlight.  This includes:
    - Endpoint being used  (from env var GROUNDLIGHT_ENDPOINT)
    - Username 
    - Is an API token configured? (from env var GROUNDLIGHT_API_TOKEN)
    If this fails, it will also include info about the error that occurred.
    
    TODO: 
        - Run a DNS check on the endpoint's host, and see what it resolves to
        - Open a TCP socket to the host and see if anything is listening
        https://chat.openai.com/share/e/1775e7ac-9f25-407b-804b-e7613e48e79d
    """
    out = {}
    
    api_token = os.getenv("GROUNDLIGHT_API_TOKEN")
    out["API Token Configured"] = "Yes" if api_token else "No"

    try:
        sdk_client = Groundlight()
        username = sdk_client.whoami()
        endpoint = sdk_client.endpoint
        out["Groundlight Username"] = username
        out["Groundlight Endpoint"] = endpoint
    except ApiTokenError as e:
        out["Reported Error"] = str(e)
        
    except GroundlightClientError as e:
        out["Reported Error"] = str(e)
        
    return out 


def get_system_info() -> dict:
    """Returns a dictionary containing system information"""
    out = {}

    # Get local IP address
    try:
        hostname = socket.gethostname()
        out["Hostname / Container ID"] = hostname
    except Exception as e:
        out["Hostname / Container ID"] = f"Unavailable: {e}"
    
    try:
        local_ip = socket.gethostbyname(hostname)
    except Exception as e:
        local_ip = "Unavailable"
    out["Local IP Address"] = local_ip
    
    # Get uptime
    try:
        with open("/proc/uptime", "r") as f:
            uptime_seconds = float(f.readline().split()[0])
            days, remainder = divmod(uptime_seconds, 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            out["Uptime"] = f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"
    except Exception as e:
        out["Uptime"] = f"Unavailable: {e}"
    
    # Get load average
    try:
        load1, load5, load15 = os.getloadavg()
        out["CPU Load Average (1 min)"] = f"{load1:.3f}"
        out["CPU Load Average (5 min)"] = f"{load5:.3f}"
        out["CPU Load Average (15 min)"] = f"{load15:.3f}"
    except Exception as e:
        out["CPU Load Average"] = f"Unavailable: {e}"

    out["CPU Cores"] = os.cpu_count()
    try:
        out["Total RAM"] = f"{psutil.virtual_memory().total / 1024 / 1024:.0f} MB"
    except Exception as e:
        out["Total RAM"] = f"Unavailable: {e}"
    
    try:
        out["Free Disk Space"] = f"{psutil.disk_usage('/').free / 1024 / 1024 :.0f} MB"
    except Exception as e:
        out["Free Disk Space"] = f"Unavailable: {e}"

    # CPU architecture
    try:
        out["CPU Architecture"] = os.uname().machine
    except Exception as e:
        out["CPU Architecture"] = f"Unavailable: {e}"

    return out


def get_all_diagnostics() -> dict:
    """Returns a dictionary containing all diagnostics"""
    out = {}

    # merge all the diagnostics
    out.update(get_groundlight_service_info())
    out.update(get_system_info())
    return out

