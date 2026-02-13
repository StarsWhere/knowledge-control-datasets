## knowledge-control-datasets 插件说明

`knowledge-control-datasets` 是 `knowledge-control` 系列中负责“知识库/数据集”管理的工具插件，把 Dify 的数据集 API 拆成多个易用的小工具：列出、创建、更新、删除、查看详情、检索测试。每个动作独立成一个工具，避免复杂聚合。

**作者**：StarsWhere  
**版本**：0.0.1  
**类型**：Dify 工具插件（Python 3.12）

### 功能概览
- 管理知识库：创建 / 更新 / 删除 / 详情 / 列表。
- 检索测试：对知识库执行检索并可选重排。

### 工具列表（单一动作）
- `datasets-list`：按关键字/标签分页列出知识库。
- `datasets-create`：创建知识库，支持权限、索引方式、嵌入模型、检索/重排设置、摘要索引。
- `dataset-detail`：根据 ID 获取详情。
- `dataset-delete`：根据 ID 删除。
- `dataset-update`：更新知识库字段（与创建选项一致）。
- `dataset-retrieve`：检索/测试查询。

### 凭证（提供方级）
- `api_base`（可选）：默认 `https://api.dify.ai/v1`，自托管请改为自己的地址。
- `api_key`（必填）：工作区 API Key，需具备数据集权限。

### 行为与默认值
- 嵌入/重排模型字段可留空，留空则使用工作区/知识库默认；如需手选，直接填写模型名称。
- 重排模式下拉：`rerank_all`（重排全部候选）/ `rerank_top_k`（仅重排 top_k）。不填则沿用知识库当前配置。
- 检索参数（search_method、top_k、score_threshold、rerank_enable 等）都是可选，未填写不会覆盖现有设置。

### 快速开始（本地调试）
1) 在虚拟环境安装依赖：`pip install -r requirements.txt`  
2) 在 Dify 添加插件时填写 `api_base` / `api_key`。  
3) 本地运行调试：`python -m main`（或 IDE 运行）。  
4) 在 Dify 调用对应工具即可，无需聚合工具。

### 常见流程
- **创建知识库**：在 `datasets-create` 中填写名称及可选项，嵌入/重排模型可留空使用默认，或直接填写模型名称。  
- **调整检索**：用 `dataset-update` 修改 `search_method`、`top_k`、`rerank` 开关/模式、分数阈值。  
- **验证效果**：用 `dataset-retrieve` 带查询文本测试检索质量。

### 已知限制
- Dify 工具表单目前是静态的，无法自动填充动态下拉；需手动填写模型名称或留空使用默认。  
- 插件运行环境需能访问 `api_base`。

### 目录提示
- `provider/knowledge-control-datasets.yaml`：提供方定义与凭证表单。  
- `tools/*.yaml`：各工具参数/标签。  
- `tools/*.py`：各工具实现。  
- `tools/common.py`：HTTP 客户端与共用方法。

### 关于 knowledge-control 系列
本插件专注知识库能力，系列中的其他插件将覆盖相关功能，可按需独立安装。
