from __future__ import annotations

from collections.abc import Generator
from typing import Any

import os, sys
sys.path.append(os.path.dirname(__file__))

from dify_plugin import Tool

from common import DifyClient


class DatasetDeleteTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator:
        try:
            client = DifyClient(self.runtime.credentials)
            dataset_id = tool_parameters["dataset_id"]
            client.request("DELETE", f"/datasets/{dataset_id}")
            yield self.create_text_message(f"Dataset {dataset_id} deleted.")
        except Exception as e:
            yield self.create_text_message(f"Error: {e}")
