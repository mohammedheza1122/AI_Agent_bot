# Gemini Code Generator

Provides code generation using Gemini and saves structured file outputs to disk.

## Module: `gemini_generator`

### Class: `CodeGenerator`

- **__init__()**
  - **Parameters**: none
  - **Behavior**: Initializes the Gemini client and selects model `gemini-2.5-pro`.

- **generate_app_code(app_description: str, app_name: str) -> str | None**
  - **Parameters**:
    - `app_description`: High-level description of the desired app
    - `app_name`: Human-readable app title
  - **Returns**: Raw text bundle from Gemini or `None` on failure
  - **Raises**: Logs exceptions and returns `None`

- **save_code_files(gemini_output: str, app_name: str) -> str**
  - **Parameters**:
    - `gemini_output`: Text bundle with `START/END FILE` markers
    - `app_name`: Used to create an output folder under `TEMP_CODE_DIR`
  - **Returns**: Absolute path to the created app directory
  - **Raises**: `ValueError` when markers are not found in the output

### Usage

```python
from gemini_generator import CodeGenerator

code_generator = CodeGenerator()
output = code_generator.generate_app_code(
    app_description="A simple task list app with dark theme using localStorage.",
    app_name="Task App"
)

if not output:
    raise RuntimeError("Gemini generation failed")

app_dir = code_generator.save_code_files(output, "task_app")
print(f"Files saved under: {app_dir}")
```

### Notes
- `generate_app_code` returns the raw text produced by Gemini; validate before saving.
- `save_code_files` expects the special markers `--- START FILE: <name> ---` and `--- END FILE: <name> ---`.
