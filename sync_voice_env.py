"""Copy the LiveKit / voice values from api/.env into agent/.env.

Voice only works when api/.env and agent/.env hold the SAME LIVEKIT_URL,
LIVEKIT_API_KEY, LIVEKIT_API_SECRET, VOICE_AGENT_NAME and VOICE_AGENT_TOKEN.
Fill in api/.env once, then run:

    python sync_voice_env.py

Creates agent/.env from agent/.env.example if it is missing. Other lines in
agent/.env are left untouched. Standard library only.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

KEYS = (
    "LIVEKIT_URL",
    "LIVEKIT_API_KEY",
    "LIVEKIT_API_SECRET",
    "VOICE_AGENT_NAME",
    "VOICE_AGENT_TOKEN",
)


def read_values(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        values[key.strip()] = value.strip()
    return values


def sync(root: Path) -> list[str]:
    """Return the keys copied. Raises SystemExit with a friendly message on problems."""
    api_env = root / "api" / ".env"
    agent_env = root / "agent" / ".env"
    if not api_env.is_file():
        raise SystemExit("api/.env not found. Run: copy api\\.env.example api\\.env, then fill in LIVEKIT_*.")
    if not agent_env.is_file():
        example = root / "agent" / ".env.example"
        if not example.is_file():
            raise SystemExit("agent/.env.example not found; is this the project folder?")
        shutil.copyfile(example, agent_env)

    source = read_values(api_env)
    missing = [k for k in ("LIVEKIT_URL", "LIVEKIT_API_KEY", "LIVEKIT_API_SECRET") if not source.get(k)]
    if missing:
        raise SystemExit(f"Fill these in api/.env first: {', '.join(missing)}")

    lines = agent_env.read_text(encoding="utf-8").splitlines()
    copied: list[str] = []
    for key in KEYS:
        value = source.get(key)
        if not value:
            continue
        new_line = f"{key}={value}"
        for i, line in enumerate(lines):
            if line.split("=", 1)[0].strip() == key and not line.lstrip().startswith("#"):
                lines[i] = new_line
                break
        else:
            lines.append(new_line)
        copied.append(key)
    agent_env.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return copied


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent
    copied = sync(root)
    print("Copied to agent/.env: " + ", ".join(copied))
    print("Now run:  cd agent  &&  uv run python voice_agent.py dev")
    return 0


if __name__ == "__main__":
    sys.exit(main())
