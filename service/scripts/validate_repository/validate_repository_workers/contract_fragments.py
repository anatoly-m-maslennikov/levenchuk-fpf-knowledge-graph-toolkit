"""Check required and forbidden literal contract fragments."""


def missing_fragments(text: str, fragments: list[str], label: str) -> list[str]:
    return [
        f"{label} is missing contract text: {fragment}"
        for fragment in fragments if fragment not in text
    ]


def present_forbidden_fragments(text: str, fragments: list[str], label: str) -> list[str]:
    return [
        f"{label} retains forbidden contract text: {fragment}"
        for fragment in fragments if fragment in text
    ]
