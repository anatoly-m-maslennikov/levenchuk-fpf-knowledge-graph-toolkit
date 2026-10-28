from __future__ import annotations

import re

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)\s*$")
CODE_FENCE_RE = re.compile(r"^\s*(```|~~~)")
ID_ROOT = r"[A-Z][A-Z0-9-]*"
SECTION_ID = rf"{ID_ROOT}\.(?:Reference|Sources):[A-Za-z0-9][A-Za-z0-9-]*(?:\.[A-Za-z0-9][A-Za-z0-9-]*)*"
FRAMEWORK_ID = rf"(?:{SECTION_ID}|{ID_ROOT}(?:\.[A-Za-z0-9][A-Za-z0-9-]*)+)"
SINGLE_ROOT_ID = rf"(?:{SECTION_ID}|[A-Z](?:\.[A-Za-z0-9][A-Za-z0-9-]*)+)"
ID_START_RE = re.compile(rf"^(?P<id>{FRAMEWORK_ID})\s*(?:[-–—:]|$)\s*(?P<title>.*)$")
ID_RE = re.compile(rf"(?<![\w/`|#])({FRAMEWORK_ID})(?![\w/`-])")
BACKTICK_ID_RE = re.compile(rf"`({FRAMEWORK_ID})`")
SINGLE_ROOT_ID_RE = re.compile(rf"(?<![\w/`|#])({SINGLE_ROOT_ID})(?![\w/`-])")
SINGLE_ROOT_BACKTICK_ID_RE = re.compile(rf"`({SINGLE_ROOT_ID})`")
RELATION_TOKEN_RE = re.compile(r"(?<![\w/\\#:-])[A-Z](?:[A-Za-z0-9.:\\-]|[ \t]*/[ \t]*)*")
RELATION_ID_RE = re.compile(rf"{FRAMEWORK_ID}(?::[A-Za-z0-9][A-Za-z0-9.-]*)?")
QUALIFIED_RELATION_ID_RE = re.compile(r"^(.+)-(?:family|compatible|selected|admitted|qualified)$")
RANGE_RELATION_ID_RE = re.compile(rf"^(?P<start>{ID_ROOT}(?:\.[A-Za-z0-9]+)+)-(?P<end>{ID_ROOT}(?:\.[A-Za-z0-9]+)+)$")
U_TERM_RE = re.compile(r"(?<![\w/`])U\.[A-Za-z][A-Za-z0-9]*(?:\.[A-Za-z][A-Za-z0-9]*)?(?![\w/`])")
LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
REL_LABEL = r"Builds on|Coordinates with|Used by|See also|Depends on|Extends|Related|Uses(?: \(via Extensions\))?|Publishes to|Constrains"
REL_LABEL_RE = re.compile(rf"^({REL_LABEL})(?::\s*|\s+|$)(.*)$", re.I)
BOLD_REL_LABEL_RE = re.compile(rf"^\s*(?:-\s+)?\*\*({REL_LABEL}):?\*\*\s*(.*)$", re.I)
BULLET_RE = re.compile(r"^\s*-\s+(.*)$")
FRONTMATTER_STATUS_RE = re.compile(r"^>\s*\*\*Status:\*\*\s*(.+)$", re.M)
FRONTMATTER_NORM_RE = re.compile(r"^>\s*\*\*Normativity:\*\*\s*(.+)$", re.M)
BAD_FILENAME_CHARS = '<>:"/\\|?*'
MAX_NAME = 170
INDEX_DIR = "00_Index"
HUBS_DIR = "00_Hubs"
