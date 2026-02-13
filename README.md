## knowledge-control-datasets

Knowledge-control-datasets is the dataset management tool plugin in the `knowledge-control` series. It exposes the Dify “数据集/知识库” API as a set of small, composable tools: list, create, update, delete, inspect details, and test retrieval. Each action is a separate tool to keep user prompts simple and predictable.

**Author:** starswhere  
**Version:** 0.0.1  
**Type:** Dify Tool Plugin (Python 3.12)

### What it does
- Manage datasets in a workspace: create, update, delete, view detail, list all.
- Test retrieval against a dataset with optional rerank settings.

### Tools (one action per tool)
- `datasets-list`: List datasets with keyword/tag filter and pagination.
- `datasets-create`: Create a dataset; supports permission, indexing, embedding model, retrieval/rerank settings, summary index.
- `dataset-detail`: Get dataset detail by ID.
- `dataset-delete`: Delete a dataset by ID.
- `dataset-update`: Update dataset fields (same options as create).
- `dataset-retrieve`: Test search/retrieve chunks from a dataset.

### Credentials (provider-level)
- `api_base` (optional): Defaults to `https://api.dify.ai/v1`. Point this to your self-hosted Dify API if needed.
- `api_key` (required): Workspace API Key with dataset permissions.

### Key behaviors / defaults
- Embedding & rerank models: fields are optional. If left blank, Dify uses the workspace/dataset defaults.
- Rerank mode options (dropdown): `rerank_all` (rerank all retrieved items) or `rerank_top_k` (rerank only top_k). Leaving it empty keeps the dataset’s existing setting.
- Retrieval options (search_method, top_k, score_threshold, rerank_enable) are optional; unset values do not override existing dataset settings.

### Quick start (local debug)
1) Install deps in your venv: `pip install -r requirements.txt`  
2) Configure credentials in Dify when adding the plugin (api_base/api_key).  
3) Run locally for debug: `python -m main` (or your IDE’s run command).  
4) In Dify, call the tool you need; no aggregator is required.

### Typical workflows
- **Create a dataset**: In `datasets-create`, fill name and optional settings; leave embedding/rerank fields empty to use workspace defaults or fill them directly if you know the model ids.  
- **Tune retrieval**: Use `dataset-update` to change `search_method`, `top_k`, `rerank_enable/mode`, thresholds.  
- **Test**: Use `dataset-retrieve` with a query to verify retrieval quality before wiring into an app.

### Known limitations
- Dify tool forms are static; embedding/rerank fields cannot be auto-populated—enter model names manually or leave blank for defaults.
- Network access is required from the plugin runtime to reach your `api_base`.

### Repo layout (key files)
- `provider/knowledge-control-datasets.yaml` — provider definition & credentials schema.
- `tools/*.yaml` — per-tool schemas and labels.
- `tools/*.py` — per-tool implementations.
- `tools/common.py` — shared HTTP client and helpers.

### Part of the knowledge-control family
This plugin focuses on datasets/knowledge bases. Other `knowledge-control` series plugins will manage adjacent capabilities; they can be installed independently.
