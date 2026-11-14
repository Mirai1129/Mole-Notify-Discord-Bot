# Mole-Notify-Discord-bot

A nextcord bot using the cog + extension pattern, loosely modeled on the
[python-discord/bot](https://github.com/python-discord/bot) project structure.


## Running

```bash
uv sync            # or: pip install -r requirements.txt
cp .env.example .env   # then fill in DISCORD_BOT_TOKEN
python -m src.main
```

Running as `python -m src.main` (rather than `python src/main.py`) is what
makes the `from src....` imports work correctly no matter which directory
you launch from — the `-m` flag runs it as part of the `src` package.

## Adding a new cog

1. Create a new file in `src/commands/`, e.g. `src/commands/ping.py`.
2. Define a `Cog` subclass (usually `BotCore` from `src.core.Core`) with your
   commands on it.
3. Add a module-level `setup(bot)` function that does `bot.add_cog(...)`.
4. That's it — `walk_extensions()` finds it automatically on next startup, or
   run `!ext load src.commands.ping` while the bot is running (owner only).
