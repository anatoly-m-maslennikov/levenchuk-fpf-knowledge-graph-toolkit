from __future__ import annotations

import re

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)\s*$")
CODE_FENCE_RE = re.compile(r"^\s*(```|~~~)")
ID_ROOT = r"[A-Z][A-Z0-9-]*"
ID_START_RE = re.compile(rf"^(?P<id>{ID_ROOT}(?:\.[A-Za-z0-9][A-Za-z0-9-]*)+)\s*(?:[-–—:]|$)\s*(?P<title>.*)$")
ID_RE = re.compile(rf"(?<![\w/`|#])({ID_ROOT}(?:\.[A-Za-z0-9][A-Za-z0-9-]*)+)(?![\w/`-])")
BACKTICK_ID_RE = re.compile(rf"`({ID_ROOT}(?:\.[A-Za-z0-9][A-Za-z0-9-]*)+)`")
SINGLE_ROOT_ID_RE = re.compile(r"(?<![\w/`|#])([A-Z](?:\.[A-Za-z0-9][A-Za-z0-9-]*)+)(?![\w/`-])")
SINGLE_ROOT_BACKTICK_ID_RE = re.compile(r"`([A-Z](?:\.[A-Za-z0-9][A-Za-z0-9-]*)+)`")
QUALIFIED_RELATION_ID_RE = re.compile(r"^(.+)-(?:family|compatible|selected)$")
RANGE_RELATION_ID_RE = re.compile(rf"^(?P<start>{ID_ROOT}(?:\.[A-Za-z0-9]+)+)-(?P<end>{ID_ROOT}(?:\.[A-Za-z0-9]+)+)$")
U_TERM_RE = re.compile(r"(?<![\w/`])U\.[A-Za-z][A-Za-z0-9]*(?:\.[A-Za-z][A-Za-z0-9]*)?(?![\w/`])")
LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
REL_LABEL_RE = re.compile(r"^(Builds on|Coordinates with|Used by|See also|Depends on|Extends|Related):\s*(.*)$", re.I)
BOLD_REL_LABEL_RE = re.compile(r"^\s*-\s+\*\*(Builds on|Coordinates with|Used by|See also|Depends on|Extends|Related):\*\*\s*(.*)$", re.I)
BULLET_RE = re.compile(r"^\s*-\s+(.*)$")
FRONTMATTER_STATUS_RE = re.compile(r"^>\s*\*\*Status:\*\*\s*(.+)$", re.M)
FRONTMATTER_NORM_RE = re.compile(r"^>\s*\*\*Normativity:\*\*\s*(.+)$", re.M)
BAD_FILENAME_CHARS = '<>:"/\\|?*'
MAX_NAME = 170
INDEX_DIR = "00_Index"
HUBS_DIR = "00_Hubs"
