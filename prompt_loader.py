import os
from functools import lru_cache
from pathlib import Path

PROMPTS_DIR = Path(os.getenv("PROMPTS_DIR", Path(__file__).resolve().parent / "prompts"))


@lru_cache(maxsize=16)
def _read_prompt_file(name: str) -> str:
    path = PROMPTS_DIR / name
    if not path.is_file():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    return path.read_text(encoding="utf-8").strip()


def load_knowledge_prompt() -> str:
    return _read_prompt_file("knowledge.txt")


def load_system_prompt() -> str:
    template = _read_prompt_file("system.txt")
    return template.replace("{{UNIVERSITY_KNOWLEDGE}}", load_knowledge_prompt())


def load_greeting_prompt() -> str:
    return _read_prompt_file("greeting.txt")


def reload_prompts() -> None:
    _read_prompt_file.cache_clear()
