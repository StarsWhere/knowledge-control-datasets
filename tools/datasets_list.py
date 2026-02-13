from __future__ import annotations

from collections.abc import Generator
from typing import Any

import os, sys
sys.path.append(os.path.dirname(__file__))

from dify_plugin import Tool

from common import DifyClient, _csv_to_list, suggest_models


class DatasetsListTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator:
        try:
            client = DifyClient(self.runtime.credentials)
            params = {
                "keyword": tool_parameters.get("keyword"),
                "tag_ids": _csv_to_list(tool_parameters.get("tag_ids")),
                "include_all": tool_parameters.get("include_all"),
                "page": tool_parameters.get("page"),
                "limit": tool_parameters.get("limit"),
            }
            data = client.request("GET", "/datasets", params=params)
            result = {"data": data}
            result.update(suggest_models(client))
            yield self.create_json_message(result)
        except Exception as e:
            yield self.create_text_message(f"Error: {e}")
