import json
import os
import time
from typing import Dict

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from framegrab import AutodiscoverMode, RTSPDiscovery

from hubaxle.gldiscover import discover_cameras

from .diagnostics import get_all_diagnostics  # Import the function


def get_or_initiate_camera_discovery() -> Dict[str, any]:
    """
    Checks for existing camera discovery results and returns them if they are recent.
    If no recent results are found, initiates a new camera discovery process if one is not already running.
    Returns a dictionary containing the discovery results or process metadata, including a waiting flag and timestamp.

    Returns:
        Dict[str, any]: A dictionary with discovery results or process metadata.
    """
    lock_file = 'camera_discovery.lock'
    results_file = 'camera_discovery_results.json'
    current_time = time.time()

    if os.path.exists(results_file):
        results_mtime = os.path.getmtime(results_file)
        if current_time - results_mtime < 1800:  # Less than 30 minutes old
            with open(results_file, 'r') as file:
                rtsp_urls = json.load(file)
            return {'rtsp_urls': rtsp_urls, 'timestamp': results_mtime, 'waiting': False}

    if os.path.exists(lock_file):
        lock_mtime = os.path.getmtime(lock_file)
        if current_time - lock_mtime > 600:  # Lock is more than 10 minutes old
            os.remove(lock_file)
        else:
            return {'waiting': True, 'timestamp': lock_mtime}

    with open(lock_file, 'w') as file:
        file.write('')

    pid = os.fork()
    if pid == 0:  # Child process
        try:
            rtsp_urls = discover_cameras(verbose=False)
            with open(results_file, 'w') as file:
                json.dump(rtsp_urls, file)
        finally:
            os.remove(lock_file)
        os._exit(0)
    else:
        return {'waiting': True, 'timestamp': current_time}

def system_status_api(request: HttpRequest) -> JsonResponse:
    """
    API view to provide system status in JSON format.
    """
    
    system_info = get_all_diagnostics()
    return JsonResponse(system_info)

def camera_discovery_view(request: HttpRequest) -> JsonResponse:
    """
    Discover RTSP devices using the ONVIF protocol.

    Args:
        request: The HTTP request object.

    Returns:
        A JsonResponse containing the discovered devices' IP addresses and ports.
    """
    discovered_devices = RTSPDiscovery.discover_onvif_devices(auto_discover_mode=AutodiscoverMode.ip_only)
    devices_info = [{"ip": device.ip, "port": device.port} for device in discovered_devices]
    return JsonResponse(devices_info, safe=False)

@login_required()
def apps_view(request: HttpRequest) -> render:
    """
    View function for the apps page.

    Args:
        request: The HTTP request object.

    Returns:
        A render response for the apps page.
    """
    
    return render(request, 'apps.html')

def launch_view(request: HttpRequest, app_num: int) -> render:
    """
    View function for launching an app.

    Args:
        request: The HTTP request object.
        app_num: The number ID of the app to launch.

    Returns:
        A render response for the app launch page.
    """
    
    return render(request, 'launch.html', {"app_num": app_num})

def homepage_view(request: HttpRequest) -> render:
    """
    View function for the homepage. This function gathers system information using the get_all_diagnostics method.
    
    Args:
        request (HttpRequest): The HTTP request object.
    
    Returns:
        render: A Django render response with the system information.
    """
    system_info = get_all_diagnostics()  # Use the existing method to gather system info
    
    # Default service linked to from the homepage
    context = {"service_name": os.environ.get("DEFAULT_LOGS_SERVICE_NAME")}
    context.update({"system_info": system_info})
    return render(request, 'homepage.html', context)
