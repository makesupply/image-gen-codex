# Changelog

All notable changes to image-gen-codex.

## v1.1.0

- **Added the prompt-craft reasoning layer** (`skills/image-gen-codex/references/prompt-craft.md`): how to prompt the GPT-Image model well.
  - Model reality: native strengths (legible type, wordmarks, clean hero, diagram/table layouts) and weaknesses to compensate for (photoreal handheld/flatlay/lifestyle renders smoother than reality; ~5-image reference cap; leans on the text description over the reference for identity; dense text garbles).
  - The 8-slot "visual brief" method + a weak-prompt upgrade checklist.
  - Canvas control: vertical %-height regions inside a central 84% safe zone; aspect-ratio-to-subject matching.
  - Photorealism levers: camera-hardware framing, the imperfection block, the skin-realism block (with the "never render skin conditions" guardrail), texture cues, lighting recipe table.
  - Product staging, an edit/preservation grammar (attach an official render without letting the model redraw it), JSON-for-complexity, a taste-word -> visual translation table.
  - Three always-on safety suffixes and a copy-ready template catalog (hero, flatlay, before/after, UGC, annotated, still-life).
  - A firewall section: keep third-party trademarks, fabricated store/shelf scenes, and dense text OUT of the model (plain text or a deterministic layer instead).
- **Wired the craft layer into `SKILL.md`** (new "Prompt craft" section + prompt-contract pointer + workflow step 1).

## v1.0.0

- Initial subscription-only agent -> Codex `$imagegen` bridge.
  - Auto-discovery of the versioned Codex desktop executable (or `codex` on PATH / explicit `--codex`).
  - ChatGPT-login guard; strips `OPENAI_API_KEY` from the child process; refuses API-key auth.
  - Prompt piped on stdin (UTF-8) so the variadic `-i/--image` parser can't swallow it.
  - Full PNG chunk-stream validation (signature, IHDR, IDAT decompress, IEND, per-chunk CRC).
  - Provenance manifest sidecar (`.manifest.json`).
  - Configurable output root/subdir; outputs and references constrained to the project.
  - Self-contained skill (SKILL.md + LEARNINGS.md + tool/) with 18 stdlib unit tests.
