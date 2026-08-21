---
name: image-gen-codex
description: Generate or edit PNG images through Codex's built-in $imagegen using an existing ChatGPT subscription, with no OpenAI API key or separate image API. Use when the user asks to generate an image, ad visual, carousel card, lifestyle scene, product mockup, or image variant via Codex. Saves to a configured output directory, validates the PNG, and writes a provenance manifest.
version: 1.0.0
---

# Image Gen via Codex — subscription bridge (no API key)

Drive the Codex desktop app's built-in `$imagegen` from an agent, authenticated by an existing ChatGPT subscription. Run `tool/generate.py`: it discovers the Codex executable, requires `Logged in using ChatGPT`, strips `OPENAI_API_KEY` from the child process, invokes built-in `$imagegen`, validates the PNG, and writes a `.manifest.json` sidecar.

This skill is model-family-specific: Codex `$imagegen` renders with the **GPT-Image** model. Nothing here calls a paid image API.

## Hard rules

0. **Do not model-render trademarks or trade dress you do not own.** Image models render third-party logos/marks inaccurately, and even a pixel-correct logo dropped into your own layout can misrepresent that brand's usage standards (clear-space, sizing, co-brand rules you don't control). Reference an outside brand as **plain text in your own typography** (e.g. "Available at [Retailer]"), never as a rendered mark or a background engineered to imitate its trade dress. Rendering a brand you own (your own wordmark as flat text on your own packaging) is fine. If a request seems to require someone else's logo, stop and confirm with the user first.
1. **Subscription only.** Never use an OpenAI API key or a paid fallback. The bridge rejects non-ChatGPT login and strips `OPENAI_API_KEY`.
2. **Outputs stay in the configured area.** Every output is a `.png` below `<output-root>/<allowed-subdir>/` (default `generated/`). The bridge refuses paths outside it. Copy the generated image into the project — don't leave it only in Codex's private output cache.
3. **Non-destructive.** Use a new descriptive filename. Do not pass `--force` unless the user explicitly asked to replace that exact file.
4. **Preserve reference/official assets.** When you attach a product render or brand asset as a reference, tell Codex not to alter its packaging, labels, logos, proportions, or colors. Keep the source asset files untouched.
5. **One asset per invocation.** For a batch, run the bridge once per requested asset/variant (Codex's built-in mode is one-image-per-run). The bridge tolerates several concurrent runs.
6. **Generating a file is not permission to publish it.** Uploading, posting, or activating the creative on any platform is a separate action — gate it on the user's explicit confirmation per your environment's rules.

## Invocation

Short prompt:

```bash
python tool/generate.py \
  --prompt "Create a clean editorial product lifestyle image. No text or watermark." \
  --output "generated/lifestyle/hero-01.png"
```

Long production prompt from a UTF-8 file, with reference images:

```bash
python tool/generate.py \
  --prompt-file "generated/carousel/prompts/card-01.txt" \
  --image "assets/product-render.png" \
  --image "assets/style-reference.png" \
  --output "generated/carousel/card-01.png"
```

Repeat `--image` for multiple references. Images attach to the initial Codex prompt in the order given; name their roles in the prompt as Image 1, Image 2, etc. Outputs and references must live inside the output root (see Configuration).

## Configuration

- `--output-root DIR` (or env `IMAGEGEN_OUTPUT_ROOT`): the project root that outputs and references must stay within. Default: current working directory.
- `--allowed-subdir NAME` (or env `IMAGEGEN_OUTPUT_SUBDIR`): the required output area under the root. Default: `generated`.
- `--codex PATH`: explicit Codex executable; normally auto-discovered.
- `--timeout SECONDS`: generation timeout (default 600).

## Prompt contract

Use the smallest useful production spec:

```text
Use case: <ad / social / hero / mockup / etc.>
Asset type: <carousel card / static / hero / etc.>
Primary request: <single visual goal>
Input images: Image 1 = product render, preserve exactly; Image 2 = style reference only
Scene/backdrop: <setting>
Subject: <hero subject>
Style/medium: <photorealistic / editorial / illustration>
Composition/framing: <aspect / composition / negative space>
Lighting/mood: <lighting>
Color palette: <palette>
Text (verbatim): "<exact text>" or "No text"
Constraints: preserve product packaging and labels; no invented claims; no watermark
Avoid: altered logo, garbled package copy, extra products, distorted hands, others' trademarks
```

For production-critical typography, exact product placement, flat geometric graphics, or pixel-matched layouts, generate only the non-critical visual layer with the model and compose the exact elements deterministically afterward (e.g. an HTML/headless-browser text layer). Reference images **guide** the model; they do not guarantee unchanged dimensions, geometry, or perfectly uniform colors. Always inspect package labels and human anatomy before accepting an output.

## Required workflow

1. Read the relevant brief/brand rules. Completion: the prompt cites the correct constraints.
2. Confirm every reference exists and label each reference's role. Completion: no ambiguous image inputs.
3. Choose a new path under `<allowed-subdir>/<job>/`. Completion: the path does not already exist.
4. Run the bridge. Completion: exit code 0 and JSON reports `auth: Logged in using ChatGPT`.
5. Inspect the PNG visually. Completion: subject, product fidelity, composition, text, and avoid-list pass.
6. Read the `.manifest.json`. Completion: dimensions, byte size, SHA-256, prompt, references, and Codex executable are recorded.
7. For a rejected output, iterate with one targeted prompt change and a new filename. Completion: prior variants remain available for comparison.

## Failure handling

- **Codex not found:** open/update the Codex desktop app, or put `codex` on PATH. The bridge auto-discovers the versioned desktop executable; never hard-code the version folder.
- **Not authenticated through ChatGPT:** run `codex login` and choose **Sign in with ChatGPT**. Do not switch to API-key auth.
- **Timeout:** rerun once with `--timeout 900`. If it fails again, report the Codex error; do not substitute an API.
- **Output exists:** choose a versioned filename. Do not overwrite silently.
- **Invalid/missing PNG:** treat the run as failed even if Codex exited 0. Inspect Codex output and retry with a new filename.
- **Transparent background:** the built-in model does not guarantee native transparency. Prefer a clean solid backdrop or deterministic local background removal; do not use an API fallback.

## Verification

```bash
python -m unittest tool/test_generate.py -v
python tool/generate.py --help
```

A live smoke test must additionally produce a PNG and manifest under the output area and be visually inspected.

## Self-improvement

Read `LEARNINGS.md` before non-trivial runs. When a run reveals a reproducible Codex/imagegen quirk or recovery step not covered here, append a dated, evidence-backed entry and bump the changelog.

## Changelog

- v1.0.0 — Subscription-only agent -> Codex `$imagegen` bridge: auto-discovery, ChatGPT-login guard, `OPENAI_API_KEY` strip, full PNG-chunk validation, provenance manifest, configurable output root/subdir, reference-image attach via stdin-piped prompt.
