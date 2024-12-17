import base64
from typing import Any
from django.contrib.auth.models import User
from django.http import FileResponse
from django.urls import reverse
from rest_framework.test import APITestCase
import yaml

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def make_simple_test_user() -> dict:
    username = "test-user"
    password = "test-password"
    user = User.objects.create_user(username=username, password=password)
    credentials = base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')
    auth_header = f'Basic {credentials}'
    return user, password, auth_header

class TestAuth(APITestCase):
    def setUp(self):
        self.user, self.password, self.auth_header = make_simple_test_user()

    def test_get_secret_auth(self):
        response = self.client.get('/api/v1/secrets')
        self.assertEqual(response.status_code, 401)
        response = self.client.get('/api/v1/secrets', HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, 200)

        # endpoints currently should not respond to session based requests
        self.client.login(username='test', password='test')
        response = self.client.get('/api/v1/secrets')
        self.assertEqual(response.status_code, 401)

class TestAPI(APITestCase):
    def setUp(self):
        self.user, self.password, self.auth_header = make_simple_test_user()

    def test_secrets(self):
        response = self.client.get('/api/v1/secrets', HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])
        response = self.client.post('/api/v1/secrets', {"name": "test", "value": "test"}, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/api/v1/secrets', HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.data[0]['name'], "test")
        self.assertEqual(response.data[0]['value'], "test")
        self.assertTrue("id" in response.data[0].keys())

    def test_config(self):
        response = self.client.get(reverse("appconfig-retrieve-update"), HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, 200)
        with open(Path(__file__).parent / "test_config.yaml", "r") as f:
            yaml_str = f.read()
            response = self.client.put(reverse("appconfig-retrieve-update"), {"kind": "yaml", "contents": yaml_str}, HTTP_AUTHORIZATION=self.auth_header)
        response = self.client.get(reverse("appconfig-retrieve-update"), HTTP_AUTHORIZATION=self.auth_header)
        yaml_content = yaml.safe_load(response.data["contents"])
        self.assertEqual(yaml_content, {'test': {'much': 1, 'test': 2}, 'yams': {'yams': {'yams': {'itsallyams': {'yamyam': {'yeah': {'y': {'a': {'m': {'YAM!': 'so many yams'}}}}}}}}}})