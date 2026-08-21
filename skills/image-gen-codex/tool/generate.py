#!/usr/bin/env python3
"""Subscription-only bridge from an agent to Codex's built-in $imagegen skill.

Generates exactly one PNG per invocation through the Codex desktop app's built-in
image generation, authenticated by an existing ChatGPT subscription. No OpenAI API
key is used or accepted. The result is validated (full PNG chunk-stream check) and a
provenance manifest is written next to it.

Configuration (no code edits needed):
  --output-root DIR      Project root that outputs and references must stay within.
                         Default: env IMAGEGEN_OUTPUT_ROOT, else the current dir.
  --allowed-subdir NAME  Required output area under the root (outputs must live here).
                         Default: env IMAGEGEN_OUTPUT_SUBDIR, else "generated".

Stdlib only. Requires Python 3.10+.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import zlib
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_SUBDIR = "generated"


class BridgeError(RuntimeError):
    """Raised when the subscription-backed image generation contract is violated."""


def discover_codex(executable: str | None = None) -> Path:
    """Find Codex without hard-coding its versioned desktop-app directory."""
    if executable:
        candidate = Path(executable).expanduser().resolve()
        if candidate.is_file():
            return candidate
        raise BridgeError(f"Codex executable not found: {candidate}")

    on_path = shutil.which("codex") or shutil.which("codex.exe")
    if on_path:
        return Path(on_path).resolve()

    # Windows desktop app: %LOCALAPPDATA%\OpenAI\Codex\bin\<version>\codex.exe
    local_appdata = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local"))
    candidates = list((local_appdata / "OpenAI/Codex/bin").glob("*/codex.exe"))
    # macOS/Linux CLI installs usually land on PATH (handled above); also try ~/.codex/bin.
    candidates += list((Path.home() / ".codex/bin").glob("*/codex"))
    candidates = [path for path in candidates if path.is_file()]
    if candidates:
        return max(candidates, key=lambda path: path.stat().st_mtime).resolve()

    raise BridgeError(
        "Codex was not found. Install/open the Codex desktop app or put codex on PATH."
    )


def require_chatgpt_login(executable: Path) -> str:
    """Refuse image generation unless Codex is using included ChatGPT access."""
    result = subprocess.run(
        [str(executable), "login", "status"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
        check=False,
    )
    status = "\n".join(
        part.strip() for part in (result.stdout, result.stderr) if part and part.strip()
    )
    if result.returncode != 0 or "Logged in using ChatGPT" not in status:
        raise BridgeError(
            "Codex is not authenticated through the ChatGPT subscription. "
            "Run `codex login` and choose Sign in with ChatGPT; API-key login is rejected."
        )
    return "Logged in using ChatGPT"


def build_codex_prompt(request: str, output: Path) -> str:
    """Create a constrained Codex task that stays on built-in subscription imagegen."""
    return f"""Use the $imagegen skill and its built-in image generation tool.

Image request:
{request.strip()}

Requirements:
- Use built-in image generation under the active ChatGPT subscription.
- Do not use the API-key fallback, OPENAI_API_KEY, or scripts/image_gen.py.
- Generate exactly one PNG for this job.
- Save or copy the final image to this exact absolute path:
  {output}
- Create the parent directory if needed.
- Do not overwrite unrelated files.
- Verify the destination exists and is a valid PNG before finishing.
- Finish with exactly: RESULT: {output}
"""


def verify_png(path: Path) -> dict[str, int]:
    """Validate the complete PNG chunk stream and return dimensions using only stdlib."""
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise BridgeError(f"Generated output is missing or unreadable: {path}") from exc
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise BridgeError(f"Generated output is not a valid PNG: {path}")

    position = 8
    width = height = 0
    seen_ihdr = False
    seen_iend = False
    idat_parts: list[bytes] = []

    while position < len(data):
        if len(data) - position < 12:
            raise BridgeError(f"Generated PNG is truncated: {path}")
        length = struct.unpack(">I", data[position : position + 4])[0]
        chunk_end = position + 12 + length
        if chunk_end > len(data):
            raise BridgeError(f"Generated PNG is truncated: {path}")

        chunk_type = data[position + 4 : position + 8]
        chunk_data = data[position + 8 : position + 8 + length]
        stored_crc = struct.unpack(">I", data[position + 8 + length : chunk_end])[0]
        computed_crc = zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF
        if stored_crc != computed_crc:
            raise BridgeError(f"Generated PNG has an invalid chunk checksum: {path}")

        if not seen_ihdr:
            if chunk_type != b"IHDR" or length != 13:
                raise BridgeError(f"Generated PNG is missing a valid first IHDR chunk: {path}")
            width, height = struct.unpack(">II", chunk_data[:8])
            seen_ihdr = True
        elif chunk_type == b"IHDR":
            raise BridgeError(f"Generated PNG contains multiple IHDR chunks: {path}")

        if chunk_type == b"IDAT":
            idat_parts.append(chunk_data)
        elif chunk_type == b"IEND":
            if length != 0:
                raise BridgeError(f"Generated PNG has an invalid IEND chunk: {path}")
            seen_iend = True
            position = chunk_end
            break

        position = chunk_end

    if not seen_iend or position != len(data):
        raise BridgeError(f"Generated PNG is truncated or has data after IEND: {path}")
    if width <= 0 or height <= 0:
        raise BridgeError(f"Generated PNG has invalid dimensions: {path}")
    if not idat_parts:
        raise BridgeError(f"Generated PNG has no image data: {path}")
    try:
        zlib.decompress(b"".join(idat_parts))
    except zlib.error as exc:
        raise BridgeError(f"Generated PNG has invalid compressed image data: {path}") from exc
    return {"width": width, "height": height}


def resolve_output(
    root: Path,
    requested: str | Path,
    allowed_subdir: str = DEFAULT_SUBDIR,
    force: bool = False,
) -> Path:
    """Constrain outputs to <root>/<allowed_subdir> and avoid clobbering."""
    root = root.resolve()
    requested = Path(requested)
    output = (requested if requested.is_absolute() else root / requested).resolve()
    allowed = (root / allowed_subdir).resolve()
    if not output.is_relative_to(allowed):
        raise BridgeError(f"Output must be below {allowed} ({allowed_subdir}).")
    if output.suffix.lower() != ".png":
        raise BridgeError("Output filename must end in .png")
    if output.exists() and not force:
        raise BridgeError(
            f"Output already exists; choose a new filename or pass --force: {output}"
        )
    return output


def resolve_references(root: Path, requested: list[Path]) -> list[Path]:
    """Allow only existing image references inside the project root (avoids data leaks)."""
    root = root.resolve()
    allowed_suffixes = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
    resolved: list[Path] = []
    for item in requested:
        path = (item if item.is_absolute() else root / item).expanduser().resolve()
        if not path.is_relative_to(root):
            raise BridgeError(f"Reference images must stay inside the project root: {path}")
        if not path.is_file():
            raise BridgeError(f"Reference image not found: {path}")
        if path.suffix.lower() not in allowed_suffixes:
            raise BridgeError(f"Unsupported reference image type: {path}")
        resolved.append(path)
    return resolved


def build_command(
    executable: Path,
    references: list[Path],
    last_message: Path,
) -> list[str]:
    """Build a shell-free Codex command; the prompt is piped separately on stdin."""
    command = [
        str(executable),
        "exec",
        "--sandbox",
        "workspace-write",
        "--output-last-message",
        str(last_message),
    ]
    for reference in references:
        command.extend(["-i", str(reference)])
    return command


def require_result_path(final_message: str, output: Path) -> Path:
    """Require one parseable RESULT line that names the verified output."""
    result_lines = [
        line.removeprefix("RESULT:").strip()
        for line in final_message.splitlines()
        if line.strip().startswith("RESULT:")
    ]
    if len(result_lines) != 1 or not result_lines[0]:
        raise BridgeError("Codex final message must contain exactly one RESULT: <path> line")
    reported = Path(result_lines[0]).expanduser().resolve()
    if reported != output.resolve():
        raise BridgeError(
            f"Codex RESULT path did not match the requested output: {reported} != {output}"
        )
    return reported


def write_manifest(
    output: Path,
    request: str,
    references: list[Path],
    executable: Path,
    auth_status: str,
    png_info: dict[str, int],
) -> Path:
    """Write a reproducibility and provenance sidecar next to the generated PNG."""
    payload = {
        "schema": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generator": "Codex built-in $imagegen",
        "auth": auth_status,
        "request": request,
        "references": [str(path) for path in references],
        "output": str(output),
        "width": png_info["width"],
        "height": png_info["height"],
        "bytes": output.stat().st_size,
        "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "codex_executable": str(executable),
    }
    manifest = output.with_suffix(".manifest.json")
    manifest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return manifest


def run_generation(
    root: Path,
    request: str,
    output: Path,
    references: list[Path],
    executable: Path,
    timeout: int,
) -> dict[str, object]:
    """Invoke subscription-backed Codex, then verify and record the result."""
    auth_status = require_chatgpt_login(executable)
    output.parent.mkdir(parents=True, exist_ok=True)
    prompt = build_codex_prompt(request, output)
    with tempfile.NamedTemporaryFile(
        prefix="codex-imagegen-last-",
        suffix=".txt",
        dir=output.parent,
        delete=False,
    ) as handle:
        last_message = Path(handle.name)

    command = build_command(executable, references, last_message)
    env = os.environ.copy()
    env.pop("OPENAI_API_KEY", None)
    try:
        result = subprocess.run(
            command,
            cwd=root,
            env=env,
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
        final_message = (
            last_message.read_text(encoding="utf-8", errors="replace").strip()
            if last_message.exists()
            else ""
        )
    except subprocess.TimeoutExpired as exc:
        raise BridgeError(f"Codex image generation timed out after {timeout} seconds") from exc
    finally:
        last_message.unlink(missing_ok=True)

    if result.returncode != 0:
        details = (result.stderr or result.stdout or "").strip()
        raise BridgeError(f"Codex image generation failed ({result.returncode}): {details}")

    require_result_path(final_message, output)
    png_info = verify_png(output)
    manifest = write_manifest(
        output=output,
        request=request,
        references=references,
        executable=executable,
        auth_status=auth_status,
        png_info=png_info,
    )
    return {
        "output": str(output),
        "manifest": str(manifest),
        "width": png_info["width"],
        "height": png_info["height"],
        "auth": auth_status,
        "final_message": final_message,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate one PNG through Codex built-in $imagegen using ChatGPT subscription auth."
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--prompt", help="Image-generation request text")
    source.add_argument("--prompt-file", type=Path, help="UTF-8 file containing the request")
    parser.add_argument("--output", required=True, help="PNG path below <output-root>/<allowed-subdir>/")
    parser.add_argument(
        "--image",
        action="append",
        default=[],
        type=Path,
        help="Reference/edit image to attach; repeat for multiple images",
    )
    parser.add_argument(
        "--output-root",
        help="Project root that outputs/references must stay within (default: $IMAGEGEN_OUTPUT_ROOT or cwd)",
    )
    parser.add_argument(
        "--allowed-subdir",
        help=f"Required output area under the root (default: $IMAGEGEN_OUTPUT_SUBDIR or '{DEFAULT_SUBDIR}')",
    )
    parser.add_argument("--codex", help="Explicit codex executable; normally auto-discovered")
    parser.add_argument("--timeout", type=int, default=600, help="Generation timeout in seconds")
    parser.add_argument("--force", action="store_true", help="Allow replacing the named output")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root_arg = args.output_root or os.environ.get("IMAGEGEN_OUTPUT_ROOT") or os.getcwd()
    root = Path(root_arg).expanduser().resolve()
    allowed_subdir = (
        args.allowed_subdir or os.environ.get("IMAGEGEN_OUTPUT_SUBDIR") or DEFAULT_SUBDIR
    )
    try:
        request = (
            args.prompt
            if args.prompt is not None
            else args.prompt_file.read_text(encoding="utf-8")
        )
        if not request.strip():
            raise BridgeError("Prompt cannot be empty")
        references = resolve_references(root, args.image)
        output = resolve_output(root, args.output, allowed_subdir=allowed_subdir, force=args.force)
        executable = discover_codex(args.codex)
        summary = run_generation(
            root=root,
            request=request,
            output=output,
            references=references,
            executable=executable,
            timeout=args.timeout,
        )
    except (BridgeError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
