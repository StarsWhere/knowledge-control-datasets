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


class DatasetUpdateTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator:
        try:
            client = DifyClient(self.runtime.credentials)
            dataset_id = tool_parameters["dataset_id"]
            body: dict[str, Any] = {}
            for key in (
                "name",
                "description",
                "indexing_technique",
                "permission",
                "provider",
                "external_knowledge_api_id",
                "external_knowledge_id",
                "embedding_model",
                "embedding_model_provider",
            ):
                if tool_parameters.get(key) is not None:
                    body[key] = tool_parameters.get(key)

            partial_members = _csv_to_list(tool_parameters.get("partial_member_list"))
            if partial_members is not None:
                body["partial_member_list"] = partial_members

            retrieval_model = _build_retrieval_model(tool_parameters)
            if retrieval_model:
                body["retrieval_model"] = retrieval_model

            summary_setting = _build_summary_setting(tool_parameters)
            if summary_setting:
                body["summary_index_setting"] = summary_setting

            data = client.request("PATCH", f"/datasets/{dataset_id}", json=body)
            result = {"data": data}
            result.update(suggest_models(client))
            yield self.create_json_message(result)
        except Exception as e:
            yield self.create_text_message(f"Error: {e}")
