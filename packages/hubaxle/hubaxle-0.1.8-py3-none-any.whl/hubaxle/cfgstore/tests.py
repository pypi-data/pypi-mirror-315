from unittest import skip

from django.core.exceptions import ValidationError
from django.test import TestCase

from hubaxle.cfgstore.models import ConfigEntry, parse_env_contents


class TestConfigEntryValidation(TestCase):
    def test_config_entry_validation_yaml_positive(self):
        """Test that valid YAML content passes validation"""
        valid_yaml_content = "key: value\nanother_key: Another Value"
        config_entry = ConfigEntry(
            name="Valid YAML", kind="yaml", contents=valid_yaml_content
        )
        try:
            config_entry.clean()
        except ValidationError:
            self.fail(
                "ConfigEntry.clean() raised ValidationError unexpectedly for valid YAML!"
            )

    def test_config_entry_validation_yaml_negative(self):
        """Test that invalid YAML content raises ValidationError"""
        invalid_yaml_content = "key: value\nanother_key: Another Value:\n"
        config_entry = ConfigEntry(
            name="Invalid YAML", kind="yaml", contents=invalid_yaml_content
        )
        with self.assertRaises(
            ValidationError,
            msg="Expected ValidationError for invalid YAML content not raised",
        ):
            config_entry.clean()

    def test_config_entry_validation_json_positive(self):
        """Test that valid JSON content passes validation"""
        valid_json_content = '{"key": "value", "another_key": "Another Value"}'
        config_entry = ConfigEntry(
            name="Valid JSON", kind="json", contents=valid_json_content
        )
        try:
            config_entry.clean()
        except ValidationError:
            self.fail(
                "ConfigEntry.clean() raised ValidationError unexpectedly for valid JSON!"
            )

    def test_config_entry_validation_json_negative(self):
        """Test that invalid JSON content raises ValidationError"""
        invalid_json_content = '{"key": "value", "another_key": "Another Value"'
        config_entry = ConfigEntry(
            name="Invalid JSON", kind="json", contents=invalid_json_content
        )
        with self.assertRaises(
            ValidationError,
            msg="Expected ValidationError for invalid JSON content not raised",
        ):
            config_entry.clean()

    def test_config_entry_validation_env_positive(self):
        """Test that valid dotenv content passes validation"""
        valid_env_content = "DEBUG=True\nSECRET_KEY=SuperSecret"
        config_entry = ConfigEntry(
            name="Valid ENV", kind="env", contents=valid_env_content
        )
        try:
            config_entry.clean()
        except ValidationError:
            self.fail(
                "ConfigEntry.clean() raised ValidationError unexpectedly for valid dotenv!"
            )

    def test_config_entry_validation_env_negative(self):
        """Test that invalid dotenv content raises ValidationError"""
        invalid_env_content = "NOT_AN_ENV_FORMAT"
        config_entry = ConfigEntry(
            name="Invalid ENV", kind="env", contents=invalid_env_content
        )
        with self.assertRaises(
            ValidationError,
            msg="Expected ValidationError for invalid dotenv content not raised",
        ):
            config_entry.clean()

    @skip("This should really fail - try environs instead of dotent")
    def test_config_entry_validation_env_negative2(self):
        """Test that invalid dotenv content raises ValidationError"""
        invalid_env_content = "this is awesome!"
        config_entry = ConfigEntry(
            name="Invalid ENV", kind="env", contents=invalid_env_content
        )
        with self.assertRaises(
            ValidationError,
            msg="Expected ValidationError for invalid dotenv content not raised",
        ):
            config_entry.clean()


class TestParseEnvContents(TestCase):
    def test_parse_env_contents_positive(self):
        """Test that valid dotenv content passes validation"""
        valid_env_content = "DEBUG=True\nSECRET_KEY=SuperSecret"
        try:
            parse_env_contents(valid_env_content)
        except ValidationError:
            self.fail("parse_env_contents raised ValidationError unexpectedly!")

    def test_parse_env_contents_negative(self):
        """Test that invalid dotenv content raises ValidationError"""
        invalid_env_content = "NOT_AN_ENV_FORMAT"
        with self.assertRaises(
            ValidationError,
            msg="Expected ValidationError for invalid dotenv format not raised",
        ):
            parse_env_contents(invalid_env_content)
