"""Run one isolated structured Codex evaluation turn."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess


def _prepare_codex_home(target: Path) -> Path:
    source = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).resolve()
    authentication = source / "auth.json"
    if not authentication.is_file():
        raise ValueError(f"Codex file-based authentication is unavailable: {authentication}")
    target.mkdir(parents=True, exist_ok=True)
    target.chmod(0o700)
    link = target / "auth.json"
    if link.is_symlink() and link.resolve() == authentication:
        return target
    if link.exists() or link.is_symlink():
        raise ValueError(f"isolated Codex authentication link conflicts: {link}")
    link.symlink_to(authentication)
    return target


def _timeout_error(exc: subprocess.TimeoutExpired, timeout: float) -> RuntimeError:
    stderr = exc.stderr if isinstance(exc.stderr, str) else ""
    stdout = exc.stdout if isinstance(exc.stdout, str) else ""
    detail = (stderr or stdout)[-4000:]
    suffix = f": {detail}" if detail else ""
    return RuntimeError(f"Codex evaluation timed out after {timeout:g}s{suffix}")


def run_codex(
    prompt: str, schema: Path, output: Path, root: Path, *,
    executable: str, model: str | None, timeout: float, state_home: Path,
) -> dict[str, object]:
    resolved = shutil.which(executable)
    if resolved is None:
        raise ValueError(f"Codex CLI not found: {executable}")
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        resolved, "-a", "never", "exec", "--ephemeral", "--ignore-user-config", "--ignore-rules",
        "-s", "read-only", "-C", str(root),
        "--output-schema", str(schema), "--output-last-message", str(output), "-",
    ]
    if model:
        command[4:4] = ["--model", model]
    environment = dict(os.environ)
    environment["PYTHONPYCACHEPREFIX"] = str(root / ".runtime" / "pycache")
    environment["CODEX_HOME"] = str(_prepare_codex_home(state_home))
    try:
        completed = subprocess.run(
            command, input=prompt, text=True, capture_output=True, check=False,
            timeout=timeout, cwd=root, env=environment,
        )
    except subprocess.TimeoutExpired as exc:
        raise _timeout_error(exc, timeout) from exc
    if completed.returncode:
        detail = completed.stderr[-4000:] or completed.stdout[-4000:]
        raise RuntimeError(f"Codex evaluation failed ({completed.returncode}): {detail}")
    try:
        value = json.loads(output.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Codex did not write valid structured output: {output}") from exc
    if not isinstance(value, dict):
        raise RuntimeError("Codex structured output must be a JSON object")
    return value
