"""Command-line adapter for the script architecture gate."""

import json

from ..validate_script_architecture import validate_script_architecture


def main() -> int:
    result = validate_script_architecture()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["errors"] else 0
