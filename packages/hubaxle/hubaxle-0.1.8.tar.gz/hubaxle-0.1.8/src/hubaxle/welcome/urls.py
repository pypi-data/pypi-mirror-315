from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage_view, name="homepage"),
    path("views/discovery", views.camera_discovery_view, name="camera_discovery"),
    path("views/apps", views.apps_view, name="apps"),
    path("api/system_status", views.system_status_api, name="system_status_api"),
    path("launch/<int:app_num>", views.launch_view, name="launch_app"),
]
