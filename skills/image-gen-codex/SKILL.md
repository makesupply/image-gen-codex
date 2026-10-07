---
name: image-gen-codex
description: Generate or edit PNG images through Codex's built-in $imagegen using an existing ChatGPT subscription, with no OpenAI API key or separate image API. Use when the user asks to generate an image, ad visual, carousel card, lifestyle scene, product mockup, or image variant via Codex. Saves to a configured output directory, validates the PNG, and writes a provenance manifest.
version: 1.5.1
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
- `--model MODEL` (or env `IMAGEGEN_CODEX_MODEL`): the Codex agent model, passed to `codex exec` as `-m`. Default: Codex's own configured default. The image still renders with GPT-Image; this only picks the agent that calls `$imagegen`. Set it when the global default is a model the ChatGPT backend rejects (see Failure handling).
- `--timeout SECONDS`: generation timeout (default 600).

## Prompt craft (read before writing any production prompt)

`references/prompt-craft.md` is the reasoning layer behind the contract below — how to fill each field for photorealism, illustration, spatial composition, and product fidelity. Read it before any production creative. The five things it changes about how you prompt:

- **`$imagegen` renders with the GPT-Image model family.** Native strengths: legible big type, wordmarks, clean hero/product-on-white, diagram/table layouts. Documented weaknesses to compensate for: photoreal handheld/flatlay/lifestyle rendering (it renders *smoother than reality* — load the imperfection/skin/texture cues heavier), a ~5-image reference cap, and it **leans on the text description over the reference for identity** (restate the full description every time; never "same as reference").
- **Structure beats style words.** Decide the image *format* first, then fill the 8-slot brief (type -> subject -> composition -> modules -> tone -> material -> typography -> aspect ratio). Never open with taste words.
- **Control the canvas** with vertical %-height regions inside the central **84% safe zone**; match the aspect ratio to the subject's proportions; scale a tall subject down rather than crop a headline.
- **Preservation fence on every attached product render:** "keep the label/wordmark/colors/proportions intact" **paired with** "no new text, logos, or watermarks added" — so the model neither edits the label nor invents a badge or third-party mark.
- **Firewall (see Hard Rule 0):** never model-render a trademark you don't own, a fabricated store/shelf scene, or dense text — those go to plain text or a deterministic text layer (e.g. HTML over a model-generated plate). Model-rendered text is safe only for a single large headline/wordmark.

`references/prompt-craft.md` also carries copy-ready templates (hero, flatlay, before/after, UGC, annotated, still-life) and the three always-on safety suffixes to append.

`references/realism-formula.md` (v1.2) is the **physics-level realism layer** for any person, skin, hair, beard, or product-in-hand shot. Read it before any realism prompt. It carries: the **Realism Block** (raking 45-degree texture-reveal light; pore / vellus / sebum / subsurface inventory; film grain said once; zero digital sharpening; lifted blacks; soft highlight rolloff; a prose `Avoid:` line because the engine has no negative field), the **distance ladder** (R1 macro / R2 close-up / R3 selfie / R4 environmental — never write macro language for a selfie; on this engine it is ignored and the frame drifts polished), the **Hair Realism Block** with surface physics for common styling finishes (matte clay, pomade, thickening paste, curl cream, mousse, salt spray, gel, beard oil / balm, powder concealer) plus curl-pattern, beard, and fade clauses, the product-in-hand physical-accuracy add-on, firewalled slot libraries (body parts, skin tones with a Monk anchor, imperfections = identity marks never conditions), the two-pass refine protocol with a local mask-composite step (no paid tools), six worked examples, a QA tell-list, an 8-image A/B validation on Codex (4/4 pairs won), and a test queue for everything still unmeasured. Two rounds of desk research behind it are condensed in `references/research-notes-2026-09.md` with confidence tags: Codex's built-in image generation is documented as `gpt-image-2` with no exposed size / quality / mask controls, so a prose size is a request and the manifest is the record; critical constraints go in as positive physical states rather than negation; micro-detail edits are enforced by compositing the accepted region over the original; masters are placement-native and grain-free.

`references/shot-intents.md` (v1.3) is the **shorthand layer**: the user can type `/macro`, `/floating`, `/flatlay`, `/candid` and the like plus a product or subject, and the agent expands the intent into a full 8-slot brief with the right template, the realism blocks, the preservation fence, the safety suffixes, and the firewall already applied. Aliases are intent labels, never model commands: neither ChatGPT nor Codex has image slash commands, and this bridge embeds the prompt inside its own task text on stdin, so a leading slash is inert. The file lists accepted intents with their template mappings, gated intents with the condition that makes them safe (before/after as labeled concept only, cutaways as illustration only, variants only if they exist, packaging only if real, dense text to the text layer, endorsements only from real consenting people), blocked intents with the nearest accepted alternative (fabricated store / shelf / billboard scenes, fabricated testimonials, meme backgrounds, platform-UI imitation), and the off-brand style intents that stay in concept lanes. Its §5 carries the validity verdict with a four-image evidence batch: bare one-word prompts returned uncontrolled canvases and broke label fidelity; the expansions returned 1080x1080 exactly with the label intact.

`references/product-hero-from-renders.md` (v1.0) is the **product-accurate hero SOP** — the repeatable way to place a REAL product into an AI lifestyle/hero scene at high definition. The core rule: attach the real product render(s) as `--image` references and generate the people and scene from text; the engine reproduces an attached product far more faithfully than one it invents, which is what stops products from coming back generic. It covers sourcing and visually verifying the renders, per-product identity + relative-proportion prompting under the ~5-image cap, the fidelity limit (labels ~95%; composite the official PNG for pixel-perfect), and reaching an exact output aspect deterministically (edge-extend the clean side; bake the clear overlay margin into the frame for fixed-crop placements). Read it before any people-plus-product hero or product-in-scene shot.

`references/look-packages.md` (v1.0) is the **look layer** — camera, lens, and film stock written as NAME + visible RESULT + physical CAUSE, never a bare camera name (a bare name is a taste word in a costume). Five packages with copy-ready stills lines and the fix when each fails: **L1 film look** (ARRICAM LT + Cooke S4/i 50mm, VISION3 500T daylight-corrected — window-lit hero plates, founder stills), **L2 clean natural detail** (Sony VENICE 2 + ZEISS Supreme Prime 50mm T2.8 — product-in-hand and any frame where the label must read; name the two or three surfaces that matter), **L3 anamorphic character** (RED V-RAPTOR + Laowa Proteus 45mm 2x — night and practical-light scenes: one flare tied to a source near the frame edge, vertically oval bokeh at distance), **L4 portrait separation** (Laowa Argus spherical — eyes precisely focused, lamps meters behind as rounded highlights; "create distance, not just blur"), **L5 natural depth** (ALEXA Mini LF + Signature Prime 47mm T2.8 — environmental frames: moderate depth of field, the background recognizable but softly separated, "keep some of the world in the shot"). The practice rules that came with them: describe the **cause** not the effect (small lamps far behind the subject, not "beautiful bokeh"); the **three kinds of softness** — soft light, soft background, soft highlight roll-off — are separate conditions and none of them requires blurry eyes (so `soft focus, nothing tack sharp` is gone from the UGC wording); name the **focus target** in every prompt, with the **product-demonstration rule** (moderate depth of field so the face and the label both stay readable, the label first) that in-hand plates usually miss; give each reference a **job** and say what not to take from it; fix one thing at a time and judge a phrase on more than one result; **positive wording** (`deep charcoal shadows retain subtle texture`); state the **white balance** instead of letting a stock name imply it. Plus a symptom-to-lever table, the mapping onto the distance ladder / capture modes / shot-intent look aliases (`/film`, `/clean`, `/anamorphic`, `/separation`, `/depth`), and a five-pair A/B batch on Codex (§6, 5/5 to the packages). Adapted from a publicly shared camera-and-lens field guide for AI video (attributed; camera movement left out).

## Prompt contract

Use the smallest useful production spec (see `references/prompt-craft.md` for how to fill each field well):

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

1. Read the relevant brief/brand rules and — for any production creative — `references/prompt-craft.md`, and for any frame that carries a look (hero, plate, lifestyle, night scene, product demonstration) `references/look-packages.md`. Completion: the prompt cites the correct constraints and is built as an 8-slot brief, not a pile of style words.
2. Confirm every reference exists and label each reference's role. Completion: no ambiguous image inputs.
3. Choose a new path under `<allowed-subdir>/<job>/`. Completion: the path does not already exist.
4. Run the bridge. Completion: exit code 0 and JSON reports `auth: Logged in using ChatGPT`.
5. Inspect the PNG visually. Completion: subject, product fidelity, composition, text, and avoid-list pass.
6. Read the `.manifest.json`. Completion: dimensions, byte size, SHA-256, prompt, references, and Codex executable are recorded.
7. For a rejected output, iterate with one targeted prompt change and a new filename. Completion: prior variants remain available for comparison.

## Failure handling

- **Codex not found:** open/update the Codex desktop app, or put `codex` on PATH. The bridge auto-discovers the versioned desktop executable; never hard-code the version folder.
- **Not authenticated through ChatGPT:** run `codex login` and choose **Sign in with ChatGPT**. Do not switch to API-key auth.
- **"The '<model>' model is not supported when using Codex with a ChatGPT account" (400, fails in seconds):** the global Codex default model is one the ChatGPT backend does not serve. Pass `--model` (or set `IMAGEGEN_CODEX_MODEL`) to a model your login accepts (verified 2026-10-06: `gpt-5.6-sol`, `gpt-5.5`). Do not switch to API-key auth.
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

- v1.5.1 — Bridge fix: `--model` / `IMAGEGEN_CODEX_MODEL` pins the Codex agent model (`codex exec -m`). A global Codex default the ChatGPT backend does not serve (seen: `gpt-6.1-sol` on Codex CLI 0.146.0) failed every run in seconds with a 400; the bridge never passed a model, so it inherited it. Unset keeps Codex's default, so existing setups are unchanged. Images still render with GPT-Image. 19 tests; verified live with `gpt-5.6-sol` (nine of nine concurrent renders, all `Logged in using ChatGPT`).
- v1.5.0 — Added `references/look-packages.md`, the look layer, adapted from a publicly shared field guide on camera and lens setups for AI video (attributed; its text not reproduced; camera-movement guidance left out). The rule: camera + lens + stock written as NAME + visible RESULT + physical CAUSE, never a bare camera name. Five packages (L1 film look, L2 clean natural detail, L3 anamorphic character with practicals, L4 portrait separation, L5 natural depth), each with a copy-ready stills line and the fix when it fails; practice rules (describe the cause not the effect; the three kinds of softness never require blurry eyes; name the focus target, with the product-demonstration rule that keeps the label and the face both readable; give each reference a job and an exclusion; fix one thing at a time; positive wording such as `deep charcoal shadows retain subtle texture`; state the white balance); a symptom-to-lever table; and the mapping onto the distance ladder, capture modes (a `night` mode) and shot-intent look aliases. Validated 5/5 on Codex (window-lit film-look portrait, in-hand product demo with a real render, phone selfie with the three-softness rewrite only, anamorphic night street, natural-depth outdoor court). Coupled edits: `prompt-craft.md` §2/§3/§4a/§4b/§4g/§13/§14 (the `soft focus, nothing tack sharp` wording is gone), `realism-formula.md` §4/§6/§8/§10/§11/§14, `shot-intents.md` §1-2, LEARNINGS entry.
- v1.4.0 — Added `references/product-hero-from-renders.md`, the product-accurate hero SOP. The repeatable win: attach the real product render as an image reference and generate the people/scene from text — describe-only prompts return generic packaging, whereas an attached render is reproduced ~95% faithfully (residual label micro-text glitches per run; composite the official PNG for pixel-perfect). Also covers sourcing/verifying renders (libraries are often mislabeled — confirm visually), per-product identity + relative-proportion prompting under the ~5-image cap, and reaching an exact output aspect deterministically (edge-extend the clean side; bake the clear overlay margin into the generated frame for fixed-crop placements). Wired into the Prompt-craft references block.
- v1.3.0 — Added `references/shot-intents.md`, the shorthand layer. A public "100 ChatGPT slash hacks for product images" document was checked; verdict: the "commands" are one-word prompts (neither ChatGPT nor Codex has image slash commands; this bridge embeds the prompt in its task text on stdin, so a leading slash is inert). Kept the idea of intent labels, mapped every usable one onto an existing template (`prompt-craft.md` §13 catalog or `realism-formula.md` blocks), gated the risky ones (before/after as labeled concept, cutaways as illustration, variants only if real, packaging only if real, dense text to the text layer, endorsements only from real consenting people), blocked the rule-breakers (fabricated store / shelf / billboard scenes, fabricated testimonials, meme backgrounds, platform-UI imitation), and parked the off-brand styles in concept lanes. Evidence batch (4 images, same product render): bare `/floating` and `/macro` returned uncontrolled canvases (1024x1536, 863x1823), a black void with no shadow, a cropped wordmark, and garbled side print; the expansions returned 1080x1080 exactly and matched their briefs. `realism-formula.md` §2 notes that an unstated size returns an arbitrary canvas; LEARNINGS entry added.
- v1.2.2 — Round-2 research ingest (condensed in `references/research-notes-2026-09.md`). Codex built-in image generation is documented as `gpt-image-2` with no exposed size / quality / fidelity / reference-count / mask / quota controls (export sizes such as 1254x1254 and 1080x1350 remain unexplained; the manifest is the record). Critical constraints now go in as positive physical states, with the Avoid line as an echo only. The refine pass is bounded by an enumerated preservation prompt and enforced by a local mask-composite of the accepted region (Pillow recipe). Masters are placement-native (1080x1350 / 1080x1920 / 1080x1080) and kept grain-free until a served-transcode test says otherwise. SwinIR / HAT are the only defensible local upscaler baselines, face restoration off, judged after downsampling, with strict rejection criteria. The Monk number is an anchor, not a control, paired with a lighting / white-balance clause. The experimental queue was rewritten as concrete test protocols.
- v1.2.1 — Round-1 research ingest: gpt-image-2 size envelope per OpenAI docs; prose negatives as an unverified secondary constraint; GPT editing over-modifies irrelevant regions, so preservation regions are enumerated; hair described as geometry (parting line, scalp strip, root-to-tip flow, strand groups, perimeter flyaways) with matte / satin / wet-look surface physics, a follicle-gradient beard clause, and mixed-diameter curl clumps; Monk-plus-undertone skin-tone structure with tone-specific cues; a delivery-size lens (several-pixel cues carry realism at 1080 px, one-pixel detail dies in recompression); resample-then-grain-at-final-size ladder; local-upscaler order with CodeFormer / GFPGAN excluded on identity work.
- v1.2.0 — Added `references/realism-formula.md`, the physics-level skin / hair realism layer, expanded from a publicly shared "Realism Formula" macro-skin master prompt (attributed; not reproduced): 14-clause decomposition of why the formula works, Nano-Banana-to-GPT-Image adaptation (prose Avoid line, generate at native size, Codex refine pass or local grain instead of a paid upscaler), the Realism Block, the distance ladder, the Hair Realism Block with product-finish physics, product-in-hand physical accuracy, firewalled body-part / skin-tone / imperfection slot libraries, six worked examples, a QA tell-list, and an 8-image A/B validation on Codex (4/4 pairs won; macro words at selfie distance are ignored, not harmful; matte clay needs "chalky, light-absorbing, no highlight on any strand"). `prompt-craft.md` gained the raking-light row (§3), a §4 pointer, placement-native master sizes (§2), and a §14 line.
- v1.1.0 — Added `references/prompt-craft.md`, the prompt reasoning/craft layer: model-reality strengths/weaknesses of the GPT-Image family, the 8-slot brief method, canvas/84%-safe-zone spatial control, photorealism imperfection/skin/texture blocks, lighting recipes, product staging, edit/preservation grammar, JSON-for-complexity, taste-word translation, three safety suffixes, and a copy-ready template catalog. Wired into the prompt contract + workflow step 1.
- v1.0.0 — Subscription-only agent -> Codex `$imagegen` bridge: auto-discovery, ChatGPT-login guard, `OPENAI_API_KEY` strip, full PNG-chunk validation, provenance manifest, configurable output root/subdir, reference-image attach via stdin-piped prompt.
