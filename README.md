# image-gen-codex

Generate and edit images from an AI agent through **Codex's built-in `$imagegen`**, using an existing **ChatGPT subscription** — with **no OpenAI API key** and no separate paid image API.

It is a small, dependency-free (Python stdlib only) skill: a bridge script that drives the Codex desktop app, enforces subscription-only auth, validates the PNG, and writes a provenance manifest — plus a `SKILL.md` an agent loads to know how and when to use it.

## Why

- **No extra cost / no keys.** Reuses the ChatGPT subscription you already pay for; the bridge refuses API-key auth and strips `OPENAI_API_KEY` from the child process.
- **Verified output.** Every result is checked as a structurally complete PNG (full chunk-stream + checksums), and a `.manifest.json` records dimensions, byte size, SHA-256, the prompt, references, and the Codex executable used.
- **Safe by construction.** Outputs are constrained to a configured directory, overwrites are refused by default, and reference images must stay inside the project.

## Requirements

- **Codex desktop app** installed and signed in with **Sign in with ChatGPT** (not an API key). Or `codex` on PATH.
- **Python 3.10+** (uses `X | None` type syntax and `Path.is_relative_to`). No pip installs — stdlib only.

## Layout

```
image-gen-codex/
├── README.md
├── LICENSE
└── skills/
    └── image-gen-codex/          # the installable skill (self-contained)
        ├── SKILL.md              # how/when an agent uses it
        ├── LEARNINGS.md          # reproducible Codex quirks + fixes
        └── tool/
            ├── generate.py       # the bridge (run this)
            └── test_generate.py  # unit tests (stdlib unittest)
```

## Install

1. Copy `skills/image-gen-codex/` into your agent's skills directory (for Claude Code: `.claude/skills/image-gen-codex/`).
2. Ensure the agent's runtime is Python 3.10+ and the Codex desktop app is authenticated with ChatGPT.
3. Verify:
   ```bash
   python skills/image-gen-codex/tool/test_generate.py -v
   python skills/image-gen-codex/tool/generate.py --help
   ```

## Usage

```bash
# Simple
python tool/generate.py \
  --prompt "Clean editorial product lifestyle image. No text or watermark." \
  --output "generated/lifestyle/hero-01.png"

# With reference images (product render + style reference)
python tool/generate.py \
  --prompt-file "generated/carousel/prompts/card-01.txt" \
  --image "assets/product-render.png" \
  --image "assets/style-reference.png" \
  --output "generated/carousel/card-01.png"
```

Outputs land under `<output-root>/<allowed-subdir>/` (default `<cwd>/generated/`). Configure with `--output-root` / `--allowed-subdir` or the env vars `IMAGEGEN_OUTPUT_ROOT` / `IMAGEGEN_OUTPUT_SUBDIR`.

## License

MIT — see [LICENSE](LICENSE).
