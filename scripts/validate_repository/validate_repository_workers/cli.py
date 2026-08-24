"""Command-line adapter for repository integration validation."""

import json
import sys

from ..validate_repository import validate_repository


def main() -> int:
    result = validate_repository()
    errors = result.pop("errors")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0
