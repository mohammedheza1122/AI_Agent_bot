# Supabase Manager

Configures and exposes environment variables for client-side apps using Supabase.

## Module: `supabase_manager`

### Class: `SupabaseManager`

- **__init__()**
  - **Parameters**: none
  - **Behavior**: Creates a Supabase `Client` using `SUPABASE_PROJECT_URL` and `SUPABASE_SERVICE_ROLE_KEY`.

- **setup_database(app_name: str, table_schema: dict | None = None) -> dict**
  - **Parameters**:
    - `app_name`: Used to name or namespace resources (future use)
    - `table_schema`: Optional schema description for table creation (not implemented yet)
  - **Returns**: `{ "NEXT_PUBLIC_SUPABASE_URL": str, "NEXT_PUBLIC_SUPABASE_ANON_KEY": str }`
  - **Notes**: Do not expose service role keys to clients in production.

### Usage

```python
from supabase_manager import SupabaseManager

sm = SupabaseManager()
keys = sm.setup_database("task_app")
# keys => {"NEXT_PUBLIC_SUPABASE_URL": ..., "NEXT_PUBLIC_SUPABASE_ANON_KEY": ...}
```

### Notes
- In production, use a true anon key for public clients; do not expose service role keys.
- Extend `setup_database` to create tables using SQL or REST as needed.
