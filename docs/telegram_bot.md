# Telegram Bot Commands

Exposes chat commands that orchestrate generation, repository creation, Supabase setup, and Vercel deployment.

## Module: `telegram_bot`

### Commands

- **/start** → `start_command`
  - Sends a welcome message and usage instruction.

- **/create_app "<app_name>" "<description>"** → `create_app_command`
  - End-to-end flow:
    1. Generate code with Gemini
    2. Save files to a temp directory
    3. Setup Supabase and get env keys
    4. Create and push a GitHub repo
    5. Trigger Vercel deployment
  - **Example**:
    - `/create_app "Task App" "A simple task list with Supabase storage"`

### Handlers

- **start_command(update, context)**
  - Sends guidance on how to use the bot.

- **create_app_command(update, context)**
  - Parses args, runs the full pipeline, reports progress, and cleans up temp files.

### Configuration

Set the following in `config.py` or environment:

- `TELEGRAM_BOT_TOKEN`: Token for the Telegram bot
- `GEMINI_API_KEY`: Google Gemini API key
- `TEMP_CODE_DIR`: Writable directory for generated files
- `SUPABASE_PROJECT_URL`: Supabase project URL
- `SUPABASE_SERVICE_ROLE_KEY`: Supabase service role key (do not expose to clients)
- `GITHUB_TOKEN`: GitHub PAT with `repo` scope
- `GITHUB_USERNAME`: GitHub username/owner
- `VERCEL_API_TOKEN`: Vercel API token

### Running the bot

```python
from telegram_bot import main

if __name__ == "__main__":
    main()
```

### Error handling
- If generation fails, the bot informs the user and exits.
- Temporary directories are cleaned up regardless of success.

### Notes
- Ensure required secrets are set in `config.py` and environment.
- `TEMP_CODE_DIR` must be writable.
