import json
from pathlib import Path


def load_regulations() -> dict:
    regulations_file = Path(__file__).resolve().parent.parent / "knowledge" / "regulations.json"
    with regulations_file.open("r", encoding="utf-8") as file:
        result = json.load(file)
    return result


# regulations = load_regulations()
# print(regulations["product"]["price"])