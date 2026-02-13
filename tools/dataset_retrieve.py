from __future__ import annotations

from collections.abc import Generator
from typing import Any

import os, sys
sys.path.append(os.path.dirname(__file__))

from dify_plugin import Tool

from common import DifyClient, _build_retrieval_model, suggest_models


class DatasetRetrieveTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator:
        try:
            client = DifyClient(self.runtime.credentials)
            dataset_id = tool_parameters["dataset_id"]
            body: dict[str, Any] = {"query": tool_parameters["query"]}
            retrieval_model = _build_retrieval_model(tool_parameters)
            if retrieval_model:
                body["retrieval_model"] = retrieval_model
            data = client.request("POST", f"/datasets/{dataset_id}/retrieve", json=body)
            result = {"data": data}
            result.update(suggest_models(client))
            yield self.create_json_message(result)
        except Exception as e:
            yield self.create_text_message(f"Error: {e}")
