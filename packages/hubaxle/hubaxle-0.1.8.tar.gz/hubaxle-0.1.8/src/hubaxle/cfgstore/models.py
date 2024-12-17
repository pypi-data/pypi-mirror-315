import json
import os
from pathlib import Path

import yaml
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import models

from .envkind import parse_env_contents


class ConfigEntry(models.Model):
    """Represents a config file used by the runtime container.

    These currently exist in both the database and the filesystem,
    which is a bad practice - the duplication leads to confusion and does no good.
    We should simplify this so they're only on the filesystem.
    """

    name = models.CharField(max_length=255, unique=True)
    kind = models.CharField(
        max_length=4,
        choices=[
            ("yaml", "YAML"),
            ("json", "JSON"),
            ("env", "Environment variables"),
            ("text", "Any text"),
        ],
    )
    contents = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Config Entry"
        verbose_name_plural = "Config Entries"

    def __str__(self):
        return f"ConfigEntry(name={self.name}, kind={self.kind})"

    def path_on_disk(self) -> Path:
        """Where the actual file on disk is corresponding to this entry"""
        storage_path = Path(apps.get_app_config("cfgstore").storage_path)
        return storage_path / self.name

    def clean(self):
        self.check_contents_type()

    def check_contents_type(self):
        """Validates that the `contents` match the `kind`"""
        if self.kind == "json":
            try:
                json.loads(self.contents)
            except json.JSONDecodeError as e:
                raise ValidationError(f"Invalid JSON: {e}")
        elif self.kind == "yaml":
            try:
                yaml.safe_load(self.contents)
            except yaml.YAMLError as e:
                raise ValidationError(f"Invalid YAML: {e}")
        elif self.kind == "env":
            parse_env_contents(self.contents)
        elif self.kind == "text":
            pass  # No validation needed
        else:
            raise ValidationError(f"Unknown kind: {self.kind}")

    def save(self, *args, **kwargs):
        self.check_contents_type()
        super().save(*args, **kwargs)
        self.save_file()

    def save_file(self):
        """Saves the contents to a file in the filesystem"""
        file_path = self.path_on_disk()
        with open(file_path, "w") as f:
            f.write(self.contents)
        # update the mtime of the file to match the updated_at field
        when = self.updated_at.timestamp()
        os.utime(file_path, (when, when))

    def delete(self, *args, **kwargs):
        self.delete_file()
        super().delete(*args, **kwargs)

    def delete_file(self):
        """Deletes the file from the filesystem"""
        file_path = self.path_on_disk()
        os.remove(file_path)

    def reload(self):
        """Reloads the contents from the file on disk"""
        # TODO: make this more efficient using timestamps
        file_path = self.path_on_disk()
        with open(file_path, "r") as f:
            new_contents = f.read()
        if self.contents != new_contents:
            self.contents = new_contents
            self.save()  # Save the new contents to the database

    @classmethod
    def save_all(cls):
        entries = cls.objects.all()
        for entry in entries:
            entry.save()

    @classmethod
    def reload_all(cls):
        entries = cls.objects.all()
        for entry in entries:
            entry.reload()
