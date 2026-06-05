"""Backward-compatible exports. Edit agent prompts in the prompts/ folder."""

from prompt_loader import load_greeting_prompt, load_system_prompt

NDEJJE_UNIVERSITY_SYSTEM_PROMPT = load_system_prompt()
