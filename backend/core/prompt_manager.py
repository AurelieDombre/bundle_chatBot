# Gestions des prompts
from pathlib import Path

# Récupère les prompts dans le dossier
PROMPT_DIR = Path("prompts")

# Charge les prompts
def load_prompt(name: str):
    path = PROMPT_DIR / name
    return path.read_text(encoding="utf-8")