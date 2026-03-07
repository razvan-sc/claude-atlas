"""Configuration loader for Atlas MCP server."""

import base64
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AtlasConfig:
    """Configuration for connecting to the Atlassian Atlas API."""

    email: str
    api_token: str
    subdomain: str
    cloud_id: str = ""

    @property
    def base_url(self) -> str:
        """Return the GraphQL endpoint URL for this Atlas instance."""
        return f"https://{self.subdomain}.atlassian.net/gateway/api/graphql"

    @property
    def auth_header(self) -> str:
        """Return the Basic auth header value."""
        credentials = f"{self.email}:{self.api_token}".encode()
        return f"Basic {base64.b64encode(credentials).decode()}"

    @property
    def container_ari(self) -> str:
        """Return the ARI used as containerId for project searches."""
        return f"ari:cloud:townsquare::site/{self.cloud_id}"

    @property
    def hostname(self) -> str:
        """Return the full Atlassian hostname."""
        return f"{self.subdomain}.atlassian.net"


_REQUIRED_FIELDS = ("email", "api_token", "subdomain")


def load_config(path: Path | None = None) -> AtlasConfig:
    """Load Atlas configuration from a JSON file.

    Args:
        path: Path to config file. Defaults to ~/.atlas/config.json.

    Returns:
        AtlasConfig instance with validated fields.

    Raises:
        FileNotFoundError: If the config file does not exist.
        ValueError: If required fields are missing or empty.
    """
    if path is None:
        path = Path.home() / ".atlas" / "config.json"

    if not path.exists():
        raise FileNotFoundError(
            f'Config file not found at {path}. Create it with: '
            f'{{"email": "...", "api_token": "...", "subdomain": "..."}}'
        )

    data = json.loads(path.read_text())

    missing = [f for f in _REQUIRED_FIELDS if f not in data or not data[f]]
    if missing:
        raise ValueError(f"Missing or empty config fields: {', '.join(missing)}")

    return AtlasConfig(
        email=data["email"],
        api_token=data["api_token"],
        subdomain=data["subdomain"],
        cloud_id=data.get("cloud_id", ""),
    )
