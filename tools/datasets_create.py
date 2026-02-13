from __future__ import annotations

from collections.abc import Generator
from typing import Any

import os, sys
sys.path.append(os.path.dirname(__file__))

from dify_plugin import Tool

from common import (
    DifyClient,
    _build_retrieval_model,
    _build_summary_setting,
    _csv_to_list,
    suggest_models,
)


class DatasetsCreateTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator:
        try:
            client = DifyClient(self.runtime.credentials)
            body: dict[str, Any] = {
                "name": tool_parameters["name"],
                "description": tool_parameters.get("description"),
                "indexing_technique": tool_parameters.get("indexing_technique"),
                "permission": tool_parameters.get("permission"),
                "provider": tool_parameters.get("provider"),
                "external_knowledge_api_id": tool_parameters.get("external_knowledge_api_id"),
                "external_knowledge_id": tool_parameters.get("external_knowledge_id"),
                "embedding_model": tool_parameters.get("embedding_model"),
                "embedding_model_provider": tool_parameters.get("embedding_model_provider"),
            }
            partial_members = _csv_to_list(tool_parameters.get("partial_member_list"))
            if partial_members:
                body["partial_member_list"] = partial_members

            retrieval_model = _build_retrieval_model(tool_parameters)
            if retrieval_model:
                body["retrieval_model"] = retrieval_model

            summary_setting = _build_summary_setting(tool_parameters)
            if summary_setting:
                body["summary_index_setting"] = summary_setting

            data = client.request("POST", "/datasets", json=body)
            result = {"data": data}
            result.update(suggest_models(client))
            yield self.create_json_message(result)
        except Exception as e:
            yield self.create_text_message(f"Error: {e}")
