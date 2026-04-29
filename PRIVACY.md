## Privacy Policy

Last updated: 2026-04-29

`knowledge-control-datasets` is a Dify tool plugin that calls the Dify Knowledge Base API selected by the user through `api_base`.

### Data Processed

This plugin processes only the data needed to run the selected tool:

- Provider credentials: `api_base` and the Dify workspace `api_key`.
- Tool inputs: dataset IDs, dataset names, descriptions, permission settings, retrieval settings, model names, tag IDs, and retrieval queries.
- API responses returned by the configured Dify API, such as dataset metadata and retrieval results.

### Data Collection and Storage

The plugin author does not collect, receive, store, or sell user data. Credentials are stored by the Dify plugin runtime according to Dify's credential handling. The plugin does not create its own external database or analytics service.

The plugin declares a small local storage permission in `manifest.yaml`, but the current implementation does not persist user content, credentials, API responses, or logs in plugin storage.

### Data Sharing

The plugin sends requests only to the `api_base` configured by the user. By default, this is `https://api.dify.ai/v1`; for self-hosted Dify, users may configure their own Dify API endpoint. No data is intentionally sent to the plugin author or to unrelated third parties.

### Retention

The plugin does not retain data independently. Dataset data, API keys, and API request history are governed by the user's Dify workspace, configured Dify instance, and related infrastructure.

### Security

The plugin uses the provided API key only as an HTTP Bearer token when calling the configured Dify API. Users should grant only the permissions required for dataset management and should rotate or revoke API keys if they are no longer needed.

### User Control

Users can remove or update the plugin credentials in Dify at any time. Users can also point `api_base` to a self-hosted Dify endpoint to keep requests within their own infrastructure.

### Contact

For privacy or security questions, contact: starswherevip@gmail.com
