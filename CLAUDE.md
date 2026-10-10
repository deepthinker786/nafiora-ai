# Nafiora AI Assistant: project rules for Claude Code

Full-stack AI assistant by Nafeesa: `api/` (FastAPI, Python 3.13, uv), `web/` (Next.js 16),
`agent/` (LiveKit voice worker). Features: chat, voice, photos, files + Library (Gemini RAG).

## Skills (in .claude/skills)
- `fullstack-ai-assistant`: the base template and `scripts/scaffold.py`; already merged with the three below.
- `add-photos`, `livekit-voice-mode`, `add-files-library`: installers, already applied here.
  Do NOT run them again on this project; a second run can duplicate edits.
Read a skill's SKILL.md and review what it changes before running any script.

## Rules
- Keep API keys only in `api/.env` and `agent/.env` (never commit them, never print them).
- LiveKit values must be identical in `api/.env` and `agent/.env`; use `python sync_voice_env.py`.
- Routes stay thin; logic goes in `services/` and the provider registry.
- Run `cd api && uv run ruff check . && uv run ruff format --check . && uv run pytest` and
  `cd web && npm run typecheck` before saying a change is done.
- Keep the UI to one accent colour and no gradients.
