import base64
import json
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from hubaxle.api.models import CameraConfig
from hubaxle.cfgstore.models import ConfigEntry

class TestCameraConfig(TestCase):
    def test_camera_config(self):
        """Test basic creation of a CameraConfig"""
        valid_yaml_content = "key: value\nanother_key: Another Value"
        _ = CameraConfig(name="MyCamera", rtsp_url="rtsp://notarealurl", kind="yaml", contents=valid_yaml_content)

class TestAPIViews(APITestCase):

    def setUp(self):
        # TODO: Basic auth is pretty akward here
        self.username = "username"
        self.password = "password"
        self.user = User.objects.create(username=self.username)
        self.user.set_password(self.password)
        self.user.save()
        self.credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(self.credentials.encode('utf-8')).decode('utf-8')
        self.client.credentials(HTTP_AUTHORIZATION=f'Basic {encoded_credentials}')

        self.valid_yaml_content = "key: value\nanother_key: Another Value"
        CameraConfig.objects.create(name="Camera1", rtsp_url="rtsp://notarealurl", kind="yaml", contents=self.valid_yaml_content)
        CameraConfig.objects.create(name="Camera2", rtsp_url="rtsp://notarealurl", kind="yaml", contents="{}")
        ConfigEntry.objects.create(name="app_config", kind="yaml", contents="{}")

    def test_get_config(self):
        response = self.client.get(
            reverse("appconfig-retrieve-update")
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("name"), "app_config")
        self.assertEqual(response.data.get("kind"), "yaml")

    def test_put_config(self):
        response = self.client.put(
            reverse("appconfig-retrieve-update"),
            {
                "kind" : "json",
                "contents" : json.dumps({})
            },
            "json",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse("appconfig-retrieve-update")
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("kind"), "json")

    def test_patch_config(self):
        response = self.client.patch(
            reverse("appconfig-retrieve-update"),
            {
                "contents" : self.valid_yaml_content,
            },
            "json",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse("appconfig-retrieve-update")
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("kind"), "yaml")
        self.assertEqual(response.data.get("contents"), self.valid_yaml_content)

    def test_get_cameras(self):
        headers = {"HTTP_AUTHORIZATION": f"Basic {self.credentials}", "AUTHORIZATION": f"Basic {self.credentials}"}
        response = self.client.get(
            reverse("camera-list"),
            **headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        for camera in response.data:
            camera["name"] in ["Camera1", "Camera2"]
