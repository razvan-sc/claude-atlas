"""Tests for atlas.config module."""

import base64
import json
from pathlib import Path

import pytest

from atlas.config import AtlasConfig, load_config


class TestAtlasConfig:
    """Tests for the AtlasConfig dataclass."""

    def test_base_url_uses_subdomain(self):
        config = AtlasConfig(email="user@example.com", api_token="tok123", subdomain="mysite")
        assert config.base_url == "https://mysite.atlassian.net/gateway/api/graphql"

    def test_auth_header_is_basic_base64(self):
        config = AtlasConfig(email="user@example.com", api_token="tok123", subdomain="mysite")
        expected = "Basic " + base64.b64encode(b"user@example.com:tok123").decode()
        assert config.auth_header == expected


class TestLoadConfig:
    """Tests for the load_config function."""

    def test_loads_valid_config(self, tmp_path: Path):
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({
            "email": "user@example.com",
            "api_token": "tok123",
            "subdomain": "mysite",
        }))
        config = load_config(config_file)
        assert config.email == "user@example.com"
        assert config.api_token == "tok123"
        assert config.subdomain == "mysite"

    def test_raises_file_not_found_when_missing(self, tmp_path: Path):
        missing = tmp_path / "nonexistent.json"
        with pytest.raises(FileNotFoundError, match="Config file not found"):
            load_config(missing)

    def test_raises_value_error_when_field_missing(self, tmp_path: Path):
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({"email": "user@example.com"}))
        with pytest.raises(ValueError):
            load_config(config_file)

    def test_raises_value_error_when_field_empty(self, tmp_path: Path):
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({
            "email": "",
            "api_token": "tok123",
            "subdomain": "mysite",
        }))
        with pytest.raises(ValueError):
            load_config(config_file)
