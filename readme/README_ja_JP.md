## knowledge-control-datasets プラグイン概要

`knowledge-control-datasets` は `knowledge-control` シリーズの「ナレッジベース/データセット管理」用ツールプラグインです。Dify のデータセット API を、一覧・作成・更新・削除・詳細取得・検索テストの小さなツールに分割し、シンプルに扱えるようにしました。

**作者**：starswhere  
**バージョン**：0.0.1  
**タイプ**：Dify ツールプラグイン（Python 3.12）

### 機能
- ナレッジの作成 / 更新 / 削除 / 詳細取得 / 一覧。
- 検索テスト（必要に応じてリランク設定）。

### ツール一覧（1 アクション=1 ツール）
- `datasets-list`：キーワード/タグでナレッジ一覧を取得。
- `datasets-create`：ナレッジ作成。権限、索引方式、埋め込みモデル、検索/リランク設定、サマリ索引を指定可能。
- `dataset-detail`：ID で詳細取得。
- `dataset-delete`：ID で削除。
- `dataset-update`：各種設定を更新。
- `dataset-retrieve`：ナレッジに対して検索テスト。

### 資格情報（プロバイダ共通）
- `api_base`（任意）：デフォルト `https://api.dify.ai/v1`。自ホスト環境では変更してください。  
- `api_key`（必須）：ワークスペースの API Key（データセット権限が必要）。

### デフォルト挙動
- 埋め込み/リランクモデルは未入力でも可。未入力ならワークスペース/ナレッジのデフォルトを使用。必要に応じてモデル名を直接入力。  
- リランクモード（プルダウン）：`rerank_all`（全件リランク） / `rerank_top_k`（top_k のみ）。未入力なら既存設定を保持。  
- 検索パラメータ（search_method, top_k, score_threshold, rerank_enable など）は任意。未入力なら既存値を上書きしない。

### すぐ試す手順
1) 仮想環境で依存インストール：`pip install -r requirements.txt`  
2) Dify でプラグイン追加時に `api_base` / `api_key` を設定。  
3) ローカルデバッグ：`python -m main`。  
4) Dify 上で必要なツールだけ呼び出せば OK（アグリゲーター不要）。

### 典型フロー
- **作成**：`datasets-create` で名称と必要項目を入力。モデルは空ならデフォルト、またはモデル名を直接入力。  
- **調整**：`dataset-update` で search_method / top_k / rerank の有無やモードを変更。  
- **検証**：`dataset-retrieve` でクエリを投げて品質確認。

### 制約
- Dify のツールフォームは静的なため、モデルの動的プルダウンは提供できません。モデル名を直接入力するか、未入力でデフォルトに任せてください。  
- ランタイムから `api_base` へのネットワーク到達性が必要です。

### 主要ファイル
- `provider/knowledge-control-datasets.yaml`：プロバイダ定義と資格情報フォーム。  
- `tools/*.yaml`：各ツールのスキーマ。  
- `tools/*.py`：ツール実装。  
- `tools/common.py`：HTTP クライアントと共通ロジック。

### knowledge-control シリーズについて
本プラグインはナレッジ領域を担当し、他のシリーズプラグインと組み合わせても単体でも利用できます。
