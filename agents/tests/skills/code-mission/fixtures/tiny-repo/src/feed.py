import json
from pathlib import Path


STORIES_PATH = Path(__file__).resolve().parents[1] / "data" / "stories.json"


def load_stories(path=STORIES_PATH):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def build_feed(page=1):
    return load_stories()
