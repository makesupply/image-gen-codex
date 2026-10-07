# Changelog

All notable changes to image-gen-codex.

## v1.5.1 — pin the Codex agent model

Bridge fix. `codex exec` runs on the `model` in the user's global `~/.codex/config.toml`. With Codex CLI 0.146.0 and a global default of `gpt-6.1-sol`, every job failed in about five seconds with `400 invalid_request_error: The 'gpt-6.1-sol' model is not supported when using Codex with a ChatGPT account.` The bridge never passed a model, so it inherited the rejected default.

- **`tool/generate.py`**: new `--model MODEL` (or env `IMAGEGEN_CODEX_MODEL`), passed to `codex exec` as `-m`. Unset keeps Codex's own default, so existing setups behave exactly as before. This is the Codex agent that calls the built-in image tool; images still render with GPT-Image.
- **`tool/test_generate.py`**: a test that `-m` is added only when a model is given (19 tests).
- **Verified live**: nine of nine concurrent `$imagegen` renders with `--model gpt-5.6-sol`, all `Logged in using ChatGPT`, valid PNGs and manifests. `gpt-5.5` is also accepted on the same login.
- **`SKILL.md`** 1.5.1 (Configuration, Failure handling, changelog), **`README.md`** (configuration, troubleshooting, test count), **`LEARNINGS.md`** entry.

## v1.5.0 — look packages

The look layer: camera, lens, and film stock as visible outcomes, not bare names. Adapted from a publicly shared field guide on camera and lens setups for AI video (attributed; its text not reproduced; camera-movement guidance left out). No bridge code changed.

- **Added `skills/image-gen-codex/references/look-packages.md`.**
  - §1 The rule: NAME + visible RESULT + physical CAUSE. A bare camera name is a taste word in a costume; a result without a cause is a wish.
  - §2 Five packages, each with when to use it, the ladder rung, what to ask for, a copy-ready stills line, and the fix when it fails: L1 film look (ARRICAM LT / Cooke S4/i 50mm / VISION3 500T daylight-corrected — grain, gradual highlight roll-off, texture in skin and fabric; "if blurry: sharp eyes, gentle roll-off, fine grain"), L2 clean natural detail (Sony VENICE 2 / ZEISS Supreme Prime 50mm T2.8 — name the two or three surfaces that matter; "if clinical: natural edge detail, subtle skin variation, soft side light"), L3 anamorphic character (RED V-RAPTOR / Laowa Proteus 45mm 2x — one flare tied to a practical near the frame edge, vertically oval bokeh from distant lights outside the focus plane), L4 portrait separation (Laowa Argus spherical — eyes precisely focused, lamps meters behind as rounded highlights; "create distance, not just blur"), L5 natural depth (ALEXA Mini LF / Signature Prime 47mm T2.8 — moderate depth of field, the background recognizable but softly separated; "keep some of the world in the shot"). The phone package is unchanged.
  - §3 Practice rules: describe the cause, not the effect (a table of effect words and their buildable conditions); the three kinds of softness (light, background, highlight roll-off) are separate and none requires blurry eyes; choose the focus target in every prompt, with the product-demonstration rule (the label the sharpest point, the face a close second, moderate depth of field); assign each reference a job and say what not to take from it; fix one thing at a time and judge a phrase on more than one result; positive wording (`deep charcoal shadows retain subtle texture`); state the white balance rather than letting a stock imply it.
  - §4 Symptom-to-lever table. §5 Integration map (ladder rungs, capture modes incl. a `night` mode, shot-intent look aliases, templates). §6 Five A/B pairs on Codex, same subject / framing / size per pair, only the look wording changed: 5/5 to the packages (window-lit portrait, in-hand product demo with a real render, phone selfie with the three-softness rewrite only, anamorphic night street, natural-depth outdoor court). §7 Not adopted: camera movement (video only).
- **`prompt-craft.md`**: §2 depth bullet now describes the cause ("create distance, not just blur"); §3 gains the practical-lights / anamorphic row; §4a rewritten as look packages with the focus-target DOF rule and an explicit white-balance line; §4b and §4g drop `soft focus, nothing tack sharp` / `not tack sharp` for "the eyes stay the sharpest point"; §13 T-UGC updated; §14 summary extended.
- **`realism-formula.md`**: §4 gains the look-package-per-rung note (R4 takes "recognizable but softly separated"); §6 gains the product-demonstration focus rule; §8 gains two positive forms; §10 E6 carries the three-softness production note; §11 gains the blurry-eyes / soft-label / background-mush / sourceless-flare tells; §14 lists the new file.
- **`shot-intents.md`**: look aliases `/film`, `/clean`, `/anamorphic` (`/night`), `/separation`, `/depth` as modifiers; `/nightlife` expands through L3; `/streetstyle` through L5.
- **`SKILL.md`**: version 1.5.0, a look-layer paragraph in the prompt-craft section, workflow step 1, changelog entry. **`README.md`**: layout tree and a "Look packages" section. **`LEARNINGS.md`**: the batch's reproducible findings.

## v1.4.0 — product-accurate hero

The repeatable method for putting a real product into an AI scene at high definition, without the model inventing generic packaging.

- **Added `skills/image-gen-codex/references/product-hero-from-renders.md`.**
  - Core rule: attach the real product render as an `--image` reference and generate the people/scene from text; the engine reproduces an attached product far more faithfully than one it invents (describe-only prompts return generic packaging).
  - Sourcing: canonical high-resolution renders, verified visually (libraries are often mislabeled), copied inside the output root, one render per product under the ~5-image cap.
  - Prompting: name each product's exact form, label wording, and size relative to the others; reserve a clean overlay side and cluster subjects opposite; preservation fence on every render.
  - Fidelity limit: reference-guided ~95%; small label micro-text can garble per run — inspect every label, and composite the official PNG for pixel-perfect packaging.
  - High definition + exact aspect: `$imagegen` ignores a requested pixel size, so extend the clean background side to a wider aspect (edge-replicate; never a side with a subject), and bake the clear margin into the generated frame for placements that crop to a fixed box.
- **SKILL.md** version bumped to v1.4.0; the new reference is wired into the Prompt-craft block.

## v1.3.0 — shorthand intents

A shorthand layer that turns short intent names into full briefs, built after checking a popular "ChatGPT slash hacks" document and finding that its "commands" are one-word prompts. No bridge code changed.

- **Added `skills/image-gen-codex/references/shot-intents.md`.**
  - §1 How the agent expands `/<intent> <subject> [modifiers]`: look up the intent, pick the mapped template, fill the 8-slot brief, apply the preservation fence, safety suffixes, Hard Rule 0, the no-fabricated-placement rule, the text-layer rule, and the Realism Block at the right distance rung; modifiers for aspect, backdrop family, product-in-hand, face, phone, and plain-text availability lines.
  - §2 Accepted intents mapped to templates this skill already owns: hero and luxury, floating and levitating, macro and material, flatlay and bundle, lifestyle family, candid and UGC and POV, aspirational and street and nightlife, ad-concept family (plate only, text to the text layer), problem/solution as two plates, reel cover, unboxing with real packaging, splash and smoke, orbit and gravity with real objects, museum plinth, scale indicator, lighting-only intents, giant and miniature as concept, loop as a still.
  - §3 Gated intents with the condition that makes them safe: before/after as labeled concept only; exploded, cutaway, cross-section, transparent, blueprint as illustration only; 360 as a deterministic multi-angle composite; color variants only if real; packaging and gift box only if real; infographic, value-prop, offer, comparison with all text in the text layer; marketplace hero without naming the marketplace; testimonial and social proof only with real consenting people.
  - §4 Blocked intents with the nearest alternative: storefront, shelf display, billboard and 3D billboard (fabricated placement), green screen (meme and third-party content), duet style (platform UI), trend hop and challenge ad, soundwave. Off-brand style intents parked in concept lanes.
  - §5 Validity verdict and a four-image evidence batch on Codex with the same product render: bare `/floating` returned an unrequested 1024x1536 portrait of the bottle on a black void with no surface or shadow; bare `/macro` returned 863x1823, a size in no documented list, with the wordmark cropped and side print garbled; the two expansions returned 1080x1080 exactly and matched their briefs.
  - §6 Worked expansions for `/floating` and `/macro`, copy-ready.
- **`realism-formula.md` §2**: an unstated size returns an arbitrary canvas; always state aspect and pixels.
- **`LEARNINGS.md`**: the one-word-prompt lottery, the unstated-size behavior, and the fact that a leading `/` is inert in this bridge (`codex exec` reads the prompt as plain instructions).
- **`SKILL.md`**: version 1.3.0, a shorthand-layer paragraph in the prompt-craft section, changelog entry. **`README.md`**: layout tree and a "Shorthand intents" section.

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
