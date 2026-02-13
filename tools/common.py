from __future__ import annotations

from typing import Any, Optional

import requests


class DifyClient:
    """Thin wrapper around Dify API calls."""

    def __init__(self, credentials: dict[str, Any]) -> None:
        api_key = credentials.get("api_key")
        if not api_key:
            raise ValueError("Missing api_key in provider credentials.")
        api_base = credentials.get("api_base") or "https://api.dify.ai/v1"
        self.api_base = api_base.rstrip("/")
        self.api_key = api_key

    def request(self, method: str, path: str, params: dict | None = None, json: dict | None = None) -> Any:
        url = f"{self.api_base}{path}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        resp = requests.request(method, url, headers=headers, params=params, json=json, timeout=30)
        if resp.status_code == 204:
            return None
        if not resp.ok:
            raise RuntimeError(f"{resp.status_code}: {resp.text}")
        if resp.text:
            return resp.json()
        return None

    def list_models(self, model_type: str) -> list[str]:
        """Return flat list like provider:model for a given model type."""
        try:
            data = self.request("GET", f"/workspaces/current/models/model-types/{model_type}")
        except Exception:
            return []
        models: list[str] = []
        if isinstance(data, dict):
            items = data.get("data") or data.get("models") or []
        elif isinstance(data, list):
            items = data
        else:
            items = []
        for group in items:
            provider = group.get("provider") or group.get("provider_name")
            for m in group.get("models", []):
                name = m.get("model") or m.get("name") or m.get("model_name")
                if provider and name:
                    models.append(f"{provider}:{name}")
                elif name:
                    models.append(str(name))
        return models


def _csv_to_list(value: Optional[str]) -> Optional[list[str]]:
    if not value:
        return None
    return [item.strip() for item in value.split(",") if item.strip()]


def _build_retrieval_model(params: dict[str, Any]) -> Optional[dict[str, Any]]:
    retrieval: dict[str, Any] = {}
    search_method = params.get("retrieval_search_method")
    if search_method:
        retrieval["search_method"] = search_method
    if params.get("retrieval_top_k") is not None:
        retrieval["top_k"] = int(params["retrieval_top_k"])
    if params.get("retrieval_score_threshold_enabled") is not None:
        retrieval["score_threshold_enabled"] = bool(params["retrieval_score_threshold_enabled"])
    if params.get("retrieval_score_threshold") is not None:
        retrieval["score_threshold"] = float(params["retrieval_score_threshold"])
    if params.get("reranking_enable") is not None:
        retrieval["reranking_enable"] = bool(params["reranking_enable"])
    if params.get("reranking_mode"):
        retrieval["reranking_mode"] = params["reranking_mode"]
    rerank_provider = params.get("reranking_provider_name")
    rerank_model = params.get("reranking_model_name")
    rerank_model_dict: dict[str, Any] = {}
    if rerank_provider:
        rerank_model_dict["provider_name"] = rerank_provider
    if rerank_model:
        rerank_model_dict["model_name"] = rerank_model
    if rerank_model_dict:
        retrieval["reranking_model"] = rerank_model_dict
    return retrieval if retrieval else None


def _build_summary_setting(params: dict[str, Any]) -> Optional[dict[str, Any]]:
    summary: dict[str, Any] = {}
    if params.get("summary_enabled") is not None:
        summary["enabled"] = bool(params["summary_enabled"])
    if params.get("summary_model_provider_name"):
        summary["model_provider_name"] = params["summary_model_provider_name"]
    if params.get("summary_model_name"):
        summary["model_name"] = params["summary_model_name"]
    if params.get("summary_prompt"):
        summary["prompt_template"] = params["summary_prompt"]
    return summary if summary else None


def suggest_models(client: DifyClient) -> dict[str, Any]:
    return {
        "available_embedding_models": client.list_models("text-embedding"),
        "available_rerank_models": client.list_models("rerank"),
    }


def drop_none(d: dict[str, Any]) -> dict[str, Any]:
    """Shallow remove None values to avoid sending nulls to Dify API."""
    return {k: v for k, v in d.items() if v is not None}
