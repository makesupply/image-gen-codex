# Changelog

All notable changes to image-gen-codex.

## v1.2.2 — round-2 research ingest

Narrower follow-up research on the questions v1.2.1 left unmeasured. Firm findings promoted into `realism-formula.md` (marked `[R2]`), everything else parked in its §15 test queue with concrete protocols. Condensed record with confidence tags: `skills/image-gen-codex/references/research-notes-2026-09.md`.

- **Codex routing is documented** (`realism-formula.md` §2, `prompt-craft.md` §0, `LEARNINGS.md`): OpenAI's Codex docs state built-in image generation uses `gpt-image-2`, invoked by natural language or `$imagegen`, drawing on general Codex usage limits, with **no** exposed fields for size, quality, input fidelity, reference count, masks, quotas, or concurrency. A prose size is therefore a request, not a parameter; observed exports of 1254x1254 and 1080x1350 remain unexplained by any public source, and the provenance manifest is the record.
- **Positive state beats negation** (§8): controlled DALL-E 3 lineage research found plain negation handled poorly. Every critical constraint now goes into the prompt body as a desired physical state; the `Avoid:` line is an echo, never the mechanism. A pattern and a self-check against the Realism Block are included.
- **Bounded refine + local mask-composite** (§9a): the refine prompt enumerates identity, facial landmarks, hands, clothing, background, product silhouette, package colors, logo placement, printed characters, camera, crop, depth of field, white balance, exposure, and shadow direction as preserved; because prompt-only preservation leaks and Codex exposes no mask, the accepted region is composited over the original locally (Pillow recipe, optional).
- **Placement-native, grain-free masters** (§2, §4, §9b; `prompt-craft.md` §2): 1080x1350 for 4:5, 1080x1920 for 9:16, 1080x1080 for 1:1. No platform publishes its served compression, so realism is judged on served test assets, and grain becomes a tested variant rather than a default.
- **Local upscalers** (§9c, §11): SwinIR and HAT confirmed as the only defensible Apache-2.0 deterministic baselines, still unproven on identity and printed text; if trialed, face restoration off, judged after downsampling, rejected on any change to face landmarks, fingers, container outline, cap geometry, logo placement, or printed characters.
- **Skin tone** (§7b): an exact Monk number is a measurement anchor, not a control; a copy-ready clause pairs it with descriptive complexion, undertone, neutral white balance, controlled highlights, and open shadows.
- **§15 rewritten** as nine concrete tests (export dimensions and edit resampling, surviving exclusions, edit leakage rate, phrase ablations, served-transcode survival with clean vs grain variants, grain parameters, Monk compliance, upscaler acceptance, cross-engine protocol).

## v1.2.1 — round-1 research ingest

Six-question desk research on the realism layer's open questions, folded in and marked `[R]`.

- **Engine envelope** (§2): gpt-image-1 / 1.5 / 1-mini output 1024x1024, 1024x1536, 1536x1024, or auto; gpt-image-2 accepts flexible sizes (edges divisible by 16, aspect at most 3:1, 655,360 to 8,294,400 pixels, max edge under 3840, above 2560x1440 experimental); `quality` is effort and `size` is pixels. Prose negatives are an unverified secondary constraint. GPT editing over-modifies irrelevant regions (GIE-Bench 2025), so refine prompts enumerate preserved regions. No head-to-head macro skin / hair benchmark exists across engines; Nano Banana's perceptual detail includes hallucinated texture and GPT-Image-1's known artifacts are over-smooth skin and oily sheen.
- **Hair as geometry** (§5): parting line with a scalp strip, root-to-tip flow, strand groups with irregular gaps, perimeter flyaways, no painted highlight band; matte / satin / wet-look surface physics; a beard clause with follicle spacing, taper, and a sparse-to-dense gradient; a measurable curl fragment (mixed diameter, partial ringlets, no repeating corkscrews), described never by ethnicity.
- **Skin tone** (§7b): Monk Skin Tone plus undertone plus localized pigmentation, with cues for deep, medium, and pale tones; state the tone every time because GPT Image defaults cluster lighter and lighting shifts apparent tone.
- **Delivery-size lens** (§4): one-pixel detail dies in platform recompression, several-pixel cues survive; micro-texture supports realism and the several-pixel cues carry it at 1080 px.
- **Refine and grain** (§9): preservation-first refine wording; resample with Lanczos and downscale once rather than generative enhancement; grain only after the final downscale, luminance-only, sigma about 1.0-2.0 (the earlier 4-6 on the generated size withdrawn); SwinIR / HAT / Real-ESRGAN order with CodeFormer / GFPGAN excluded on identity work.

## v1.2.0 — the realism layer

- **Added `skills/image-gen-codex/references/realism-formula.md`**: a physics-level skin and hair prompting layer for GPT-Image via Codex, expanded from a publicly shared "Realism Formula" macro-skin master prompt (attributed; its text not reproduced).
  - §1 decomposes the 14-clause master prompt into physical mechanisms (raking 45-degree light reveals relief, sebum sits on convex surfaces, subsurface color fights uniform tone, zero sharpening kills halos, lifted blacks and soft rolloff give the film tonal curve) and explains why each clause beats loose phrasing.
  - §2 adapts Nano Banana 2 assumptions to GPT-Image: no negative field (prose Avoid line), no 4K (generate at native size, texture survives downscale not upscale), no paid upscaler (Codex refine pass or local grain), JSON keys dropped, grain said once.
  - §3 the copy-ready **Realism Block** with a slot guide.
  - §4 the **distance ladder** (R1 macro, R2 close-up, R3 half-body / selfie, R4 environmental) with per-rung skin, hair, light, and grain vocabulary and what to drop; an eyes clause and an R3 block.
  - §5 the **Hair Realism Block** (strand logic, light logic, scalp, flyaways, color variation), a product-finish physics table for common styling finishes, curl-pattern vocabulary by ringlet size, beard and fade clauses.
  - §6 product-in-hand physical accuracy that keeps the label fence.
  - §7 slot libraries: grooming body parts, undertone-first skin tones, and a firewalled imperfection vocabulary (identity marks allowed, skin conditions banned).
  - §8 merged Avoid line; §9 two-pass refine protocol; §10 six worked examples; §11 QA tell-list.
  - §12 an 8-image A/B validation on Codex: the formula won all four pairs (beard macro, close-up portrait, matte-clay part line, UGC selfie). Evidence corrections recorded: macro words at selfie distance are ignored rather than producing leather; matte clay needs stronger physics wording; output size follows the prose aspect but not always the stated pixels.
- **`prompt-craft.md`** gained the raking-light row (§3), a §4 pointer paragraph, and a §14 line.
- **`SKILL.md`** points at the realism layer from the prompt-craft section; **`LEARNINGS.md`** records the validation findings.

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
