# GitHub Manager

Creates a new repository and pushes generated code files.

## Module: `github_manager`

### Class: `GitHubManager`

- **__init__()**
  - **Parameters**: none
  - **Behavior**: Authenticates with GitHub using `GITHUB_TOKEN` and loads user `GITHUB_USERNAME`.

- **create_and_push(local_app_path: str, repo_name: str) -> str**
  - **Parameters**:
    - `local_app_path`: Root directory of generated files
    - `repo_name`: Repository name (will be created under the configured user)
  - **Returns**: Repository HTML URL as `str`
  - **Raises**: On creation failure, reuses existing repo; individual file upload errors are printed and ignored.

### Usage

```python
from github_manager import GitHubManager

gm = GitHubManager()
repo_url = gm.create_and_push("/tmp/task_app", "task_app")
print(repo_url)
```

### Notes
- Skips dotfiles during upload.
- If files already exist, upload errors are printed and ignored; adjust for idempotency as needed.
