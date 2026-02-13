from __future__ import annotations

from typing import Any

import requests
from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class KnowledgeControlDatasetsProvider(ToolProvider):
    """Provider definition for knowledge-control-datasets: validates api_base/api_key."""

    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        api_key = credentials.get("api_key")
        if not api_key:
            raise ToolProviderCredentialValidationError("api_key is required.")
        api_base = (credentials.get("api_base") or "https://api.dify.ai/v1").rstrip("/")
        try:
            resp = requests.get(
                f"{api_base}/datasets",
                params={"limit": 1},
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=15,
            )
            if resp.status_code not in (200, 401, 403, 404):
                resp.raise_for_status()
            if resp.status_code in (401, 403):
                raise ToolProviderCredentialValidationError("API key is invalid or lacks permission.")
        except ToolProviderCredentialValidationError:
            raise
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))

    # OAuth not implemented for this plugin. If needed, add flows above and update provider YAML.
