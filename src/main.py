import json
from pathlib import Path

from .Blackjack import PlayRound


def load_settings(ruleset_name="standard.json"):
    """
    Load a ruleset JSON from the settings folder.
    """
    repo_root = Path(__file__).resolve().parent.parent
    settings_path = repo_root / "settings" / ruleset_name

    with open(settings_path, "r") as f:
        return json.load(f)


def main():
    settings = load_settings("standard.json")
    PlayRound(settings)


if __name__ == "__main__":
    main()
