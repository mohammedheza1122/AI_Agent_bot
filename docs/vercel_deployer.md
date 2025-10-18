# Vercel Deployer

Creates a Vercel project connected to GitHub and returns the deployment URL.

## Module: `vercel_deployer`

### Class: `VercelDeployer`

- **__init__()**
  - **Parameters**: none
  - **Behavior**: Sets base API URL and `Authorization` header using `VERCEL_API_TOKEN`.

- **deploy(repo_url: str, project_name: str, env_vars: dict) -> str**
  - **Parameters**:
    - `repo_url`: Full GitHub repository URL
    - `project_name`: Vercel project name (used in final URL)
    - `env_vars`: Dict of environment variables to set across targets
  - **Returns**: Deployment URL string (computed placeholder)
  - **Raises**: Exception when project creation fails (non-200/201 response)

### Usage

```python
from vercel_deployer import VercelDeployer

vd = VercelDeployer()
url = vd.deploy(
    repo_url="https://github.com/you/task_app",
    project_name="task_app",
    env_vars={"NEXT_PUBLIC_SUPABASE_URL": "...", "NEXT_PUBLIC_SUPABASE_ANON_KEY": "..."}
)
print(url)
```

### Notes
- The function currently returns a formatted URL; consider polling `/v13/deployments` to confirm readiness.
- Ensure `VERCEL_API_TOKEN` is configured.
