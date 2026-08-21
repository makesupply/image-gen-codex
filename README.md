# image-gen-codex

Generate and edit images from an AI agent through **Codex's built-in `$imagegen`**, using an existing **ChatGPT subscription** — with **no OpenAI API key** and no separate paid image API.

Two parts, one self-contained skill folder:

1. **The bridge** (`tool/generate.py`) — drives the Codex desktop app, enforces subscription-only auth, validates the PNG, writes a provenance manifest. Python stdlib only, zero pip installs.
2. **The prompt-craft layer** (`references/prompt-craft.md`, v1.1.0) — the *reasoning* an agent needs to write good prompts for photorealism, composition, and product fidelity on the GPT-Image model, plus copy-ready templates and safety suffixes.

`SKILL.md` ties them together: it tells an agent when to use the skill, how to invoke the bridge, and points at the craft layer.

## Why

- **No extra cost / no keys.** Reuses the ChatGPT subscription you already pay for; the bridge refuses API-key auth and strips `OPENAI_API_KEY` from the child process.
- **Verified output.** Every result is checked as a structurally complete PNG (full chunk-stream + checksums), and a `.manifest.json` records dimensions, byte size, SHA-256, the prompt, references, and the Codex executable used.
- **Better prompts, not just plumbing.** The craft layer encodes what the GPT-Image family is good and bad at, so the agent compensates for its weak spots (photoreal lifestyle, identity drift) instead of discovering them shot by shot.
- **Safe by construction.** Outputs are constrained to a configured directory, overwrites refused by default, references must stay inside the project, and the skill firewalls third-party trademarks and dense text out of the model.

## Requirements

- **Codex desktop app** installed and signed in with **Sign in with ChatGPT** (not an API key). Or `codex` on PATH.
- **Python 3.10+** (uses `X | None` type syntax and `Path.is_relative_to`). No pip installs — stdlib only.
- An OS where Codex runs. Executable auto-discovery covers Windows (`%LOCALAPPDATA%\OpenAI\Codex\bin\<version>\codex.exe`), `codex` on PATH, and `~/.codex/bin`; otherwise pass `--codex`.

## Layout

```
image-gen-codex/
├── README.md
├── LICENSE
├── CHANGELOG.md
└── skills/
    └── image-gen-codex/              # the installable skill (self-contained — copy this folder)
        ├── SKILL.md                  # how/when an agent uses it
        ├── LEARNINGS.md              # reproducible Codex quirks + fixes
        ├── references/
        │   └── prompt-craft.md       # the prompt reasoning layer (read before production prompts)
        └── tool/
            ├── generate.py           # the bridge (run this)
            └── test_generate.py      # unit tests (stdlib unittest)
```

## Wiring it into an agent — what's needed

This ships as a standard "skill folder," so wiring is: put the folder where your agent looks for skills, make sure the runtime and Codex are ready, and verify.

**1. Place the skill folder.**
Copy `skills/image-gen-codex/` into your agent's skills directory. Examples:
- **Claude Code:** `.claude/skills/image-gen-codex/` (project-level) or the user-level skills dir.
- **Hermes / a custom agent:** whatever directory that agent scans for skills. The unit of install is the whole `image-gen-codex/` folder (SKILL.md + LEARNINGS.md + references/ + tool/) — keep it intact so `tool/` and `references/` stay relative to `SKILL.md`. Confirm the exact skills path from that agent's own config; this repo does not assume one.

**2. Make the runtime ready.**
- The agent must be able to run `python` (3.10+). If your agent uses a dedicated virtualenv, confirm that interpreter is 3.10+; no packages need installing (stdlib only). If `python` on the agent's PATH is a different/older interpreter, call the skill with the correct interpreter explicitly (e.g. an absolute path to the 3.10+ python).
- The **Codex desktop app must be installed and logged in with ChatGPT** on the machine the agent runs on. The bridge will refuse to run otherwise (by design).

**3. Point outputs somewhere sane.**
Outputs land under `<output-root>/<allowed-subdir>/`, default `<cwd>/generated/`. Set them for your project once via env so the agent doesn't have to pass them every call:
```bash
export IMAGEGEN_OUTPUT_ROOT="/path/to/your/project"
export IMAGEGEN_OUTPUT_SUBDIR="generated"      # or "_creatives/Generated", "assets/img", etc.
```
(or pass `--output-root` / `--allowed-subdir` per call.)

**4. Verify (do this once after wiring).**
```bash
python skills/image-gen-codex/tool/test_generate.py -v   # 18 tests, no Codex needed
python skills/image-gen-codex/tool/generate.py --help
# then one real smoke generation (needs Codex + ChatGPT login):
python skills/image-gen-codex/tool/generate.py \
  --prompt "A single ceramic mug on a plain white background. No text." \
  --output "generated/smoke/mug-01.png"
```
Success = exit 0, JSON reporting `auth: Logged in using ChatGPT`, and a valid PNG + `.manifest.json` at the output path.

**5. Tell the agent it exists.**
Make sure your agent actually loads `SKILL.md` (most skill-aware agents do this automatically once the folder is in the skills directory). The description line in `SKILL.md` is what triggers the agent to reach for it on image requests.

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

For anything beyond a quick render, read `references/prompt-craft.md` first: decide the image format, build the 8-slot brief, keep text/subjects inside the 84% safe zone, and add the imperfection/skin/texture cues the GPT-Image model needs for photoreal work.

## How it works (internals)

1. **Discover Codex** without hard-coding its versioned directory.
2. **Guard auth** — run `codex login status`; proceed only if it contains `Logged in using ChatGPT`. Strip `OPENAI_API_KEY` from the child environment.
3. **Build a constrained task** that pins Codex to built-in `$imagegen`, names the exact output path, and requires a `RESULT: <path>` line.
4. **Pipe the prompt on stdin** (as UTF-8) so Codex's variadic `-i/--image` parser can't swallow it.
5. **Validate** the returned file as a structurally complete PNG (signature, IHDR, IDAT decompress, IEND, per-chunk CRC).
6. **Write a manifest** (`.manifest.json`) with dimensions, bytes, SHA-256, prompt, references, and the Codex executable.

## Troubleshooting

- **"Codex was not found."** Open/update the Codex desktop app, or put `codex` on PATH, or pass `--codex /path/to/codex`.
- **"not authenticated through the ChatGPT subscription."** Run `codex login`, choose **Sign in with ChatGPT**. API-key login is rejected on purpose.
- **Timed out.** Rerun once with `--timeout 900`.
- **"Output must be below ..."** The output path is outside `<output-root>/<allowed-subdir>`. Fix the path or set `--allowed-subdir`.
- **Non-ASCII prompt errors on an old build.** This bridge sends UTF-8; if you hit `input is not valid UTF-8` on a locale-bound Codex build, keep the prompt ASCII-only.
- **Transparent background looks wrong.** The built-in model doesn't guarantee native transparency — use a clean solid backdrop or remove the background deterministically afterward.

## License

MIT — see [LICENSE](LICENSE). Prompt-craft techniques were distilled from public agent skills and generalized; no proprietary data is included.
