from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Heading:
    level: int
    text: str
    line: int


@dataclass(frozen=True)
class GraphProfile:
    key: str
    label: str
    id_field: str
    default_source: str
    default_output: str
    pattern_roots: tuple[str, ...]
    multi_root_relations: bool

    @property
    def index_files(self) -> tuple[str, str, str]:
        return (
            f"{self.label} - Index",
            f"{self.label} - Relation Index",
            f"{self.label} - Term Index",
        )


FPF_PROFILE = GraphProfile("fpf", "FPF", "fpf_id", "FPF-Spec.md", "FPF-Knowledge-Graph", tuple("ABCDEFGHIJK"), False)
NPF_PROFILE = GraphProfile("npf", "NPF", "npf_id", "Narrativization-and-Narrative-Studies-Principles-Framework.md", "NPF-Knowledge-Graph", ("NSTD",), True)
PROFILES = {profile.key: profile for profile in (FPF_PROFILE, NPF_PROFILE)}


@dataclass
class Page:
    kind: str
    heading: Heading
    start: int
    end: int
    body: list[str]
    page_name: str = ""
    parent_hub: str = ""
    framework_id: str = ""
    title: str = ""
    page_type: str = ""
    status: str = "generated"
    normativity: str = ""
    terms: list[str] = field(default_factory=list)
    relations: dict[str, list[str]] = field(default_factory=dict)
