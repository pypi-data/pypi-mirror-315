from django.db import models

from pathlib import Path
from hubaxle.cfgstore.models import ConfigEntry

class BaseModel(models.Model):
    """Base model for all glhub models."""

    name = models.CharField(max_length=100, unique=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Secret(BaseModel):
    """A secret stored in the database."""

    value = models.CharField(max_length=200)

    def __str__(self):
        return f"secret {self.name} ({str(self.value)[8:]})"

class CameraConfig(ConfigEntry):
    """A camera configuration stored in the database."""
    rtsp_url = models.CharField(max_length=200)