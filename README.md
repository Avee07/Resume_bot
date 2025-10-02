# Resume Parser Telegram Bot

This project is a minimal Telegram bot in Python that accepts resume files (PDF/DOCX), extracts text, and returns a parsed JSON summary. It's a starter implementation with simple parsing logic; for production use you'll likely want to plug in a more advanced parser or ML service.

Files added:
- `bot.py` - main Telegram bot
- `parser_utils.py` - simple text extraction and resume-to-JSON logic
- `requirements.txt` - Python dependencies
- `run.sh` - helper to run the bot

Quick start
1. Create a virtualenv and install deps:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Set your Telegram bot token as an environment variable:

```bash
export TG_BOT_TOKEN="<your-telegram-bot-token>"
```

3. Run the bot:

```bash
./run.sh
```

Usage
- Send the bot a resume as a document (PDF or DOCX). The bot will reply with a JSON file containing extracted fields (name, email, phone, skills, education, experience) using heuristics.

Notes
- This is a minimal implementation focused on infrastructure. Parsing is heuristic-based and won't be perfect. You can replace `parser_utils.parse_resume_text` with any parser or an external API for better results.
# Resume_bot
Resume bot that can auto-apply resume
