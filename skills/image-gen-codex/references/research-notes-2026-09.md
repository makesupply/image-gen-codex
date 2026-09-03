# Research notes — photorealistic skin and hair on GPT-Image / Codex (2026-09-03)

Two rounds of desk research were run with Perplexity Deep Research against the open questions in `realism-formula.md`. This file is the condensed record: what each question returned, with the dossiers' own confidence tags, and what changed in the skill because of it. The raw dossiers are not included; every claim below carries the confidence the dossier assigned, and "no evidence found" is recorded where the research came up empty. Sources named in the dossiers: OpenAI's image-generation prompting guide and API reference (2026-04), OpenAI's Codex documentation, GIE-Bench (2025), a GPT restoration study (2025-05), the HairPort editing prompt (2026-06), strand-based hair-generation and hair-capture literature, a GPT-Image-2 social-media dataset study (2026-04) and detection benchmark (2026-06), a skin-tone fidelity study (2026-04), a GPT Image 1.5 vs Gemini Flash 2.5 tone study (2026-02), Nano Banana Pro / 2 restoration studies (2025-12, 2026-04), the MultiBanana benchmark, RealGen (2025-11), and controlled DALL-E 3 negation research.

## Round 1 — six questions

| Question | Finding | Confidence | Where it went |
|---|---|---|---|
| Engine envelope | gpt-image-1 / 1.5 / 1-mini return 1024x1024, 1024x1536, 1536x1024, or auto. gpt-image-2 accepts flexible sizes: both edges divisible by 16, long:short at most 3:1, 655,360 to 8,294,400 total pixels, max edge under 3840; above 2560x1440 is experimental. `quality` = rendering effort, `size` = pixels. gpt-image-2 is OpenAI's recommended model for photorealism and identity-sensitive editing, with high input fidelity by default. | High | §2 |
| Prose negatives | No negative-conditioning channel verified; no controlled with/without test found. Keep a short observable `Avoid:` line as a secondary constraint only. | Low | §2, §8 |
| Refinement | GPT text-guided editing follows instructions well but alters irrelevant regions, geometry, counts, perspective. Enumerate every preserved region; inspect at 200 percent; keep the original. | Medium | §9 |
| Hair | Describe hair as geometry, organization, visibility, material: parting line + narrow scalp strip, root-to-tip flow, strand groups with irregular gaps, perimeter flyaways, restrained frizz, no painted highlight band; matte / satin / wet-look surface physics; beards emerge from visible skin with follicle spacing and a sparse-to-dense gradient; curls as mixed-diameter clumps with partial ringlets. Describe curls in measurable terms, never ethnicity. | Medium (physical grounding); Low (GPT-specific reliability) | §5, §15 |
| Recompression | No platform-specific survival study exists. General compression behavior: one-pixel detail dies first; several-pixel cues survive. Micro-texture supports realism, it does not carry it at 1080 px. Add grain after the final downscale, luminance-only, sigma about 1.0-2.0, preview after an approximate encode. | Medium (principle); Low (grain numbers) | §4, §9b, §15 |
| Skin tone | Monk Skin Tone (1-10) beats Fitzpatrick for visible tone. GPT Image 1.5 defaults cluster toward lighter tones with less prompt-driven variation than Nano Banana; lighting and grading shift apparent tone by more than a Monk step. Structure: Monk number + undertone + localized pigmentation + capillary warmth; tone-specific cues for deep / medium / pale. | High (Fitzpatrick limits); Medium (bias, structure); Low (compliance) | §7b |
| Local enhancement | No generative enhancer adds real detail deterministically. Default: generate at the largest reliable size, Lanczos resample, downscale once, grain at final size. If 2x is unavoidable: conservative SwinIR / HAT first, Real-ESRGAN second; never CodeFormer / GFPGAN on identity or label work; check licenses per checkpoint. No comparison against Magnific exists. | Medium | §9b-9c |
| Engine comparison | No controlled macro skin / hair head-to-head across GPT-Image-2, Nano Banana, Flux, Midjourney. Nano Banana's perceptual detail includes hallucinated texture; GPT-Image-1's known artifacts are over-smooth skin and oily sheen (RealGen), matching the §12 baselines; GPT-Image won several multi-reference composition tests. | Medium | §2, §15 |

## Round 2 — eight narrower questions

| Question | Finding | Confidence | Where it went |
|---|---|---|---|
| Codex routing | OpenAI's Codex documentation states built-in image generation uses gpt-image-2, invoked by natural language or `$imagegen`, drawing on general Codex usage limits. No desktop fields are exposed for size, quality, input fidelity, reference count, masks, quotas, or concurrency. | High | §2 |
| Codex dimensions | No public evidence explains observed exports such as 1254x1254 or 1080x1350. Treat the integration as a natural-language wrapper and log every exported raster (the manifest does). | Unresolved | §2, §15 |
| Platform processing | Meta and TikTok publish upload dimensions, formats, and acceptance requirements; no first-party source publishes served quality, chroma subsampling, sharpening, enhancement, or bitrate. Use placement-native canvases and judge served test assets. | Unresolved after upload | §4 |
| Upscaling | SwinIR and HAT are defensible Apache-2.0 deterministic baselines. No benchmark proves preservation of portrait identity and printed label text; no comparable Windows runtime table. | Conservative baseline only | §9c |
| Cross-engine realism | No four-way GPT-Image / Nano Banana / FLUX / Midjourney benchmark for pore topology, vellus hair, beard emergence, strand separation, reference identity, printed text. General leaderboards must not be presented as microtexture evidence. | No exact benchmark | §2, §15 |
| Negation | Controlled DALL-E 3 research found poor handling of plain negation. Express important constraints as positive physical target states; prose exclusions remain secondary. | Lineage evidence | §8 |
| Descriptor ablations | No controlled GPT-Image ablation for `visible pores`, `vellus hair`, `strand separation`, `matte finish`. Internal test variables. | Unmeasured | §15 |
| Skin tone | MST is a useful measurement framework, but no controlled evidence that an exact MST number maps to that output in GPT Image 1.5 / 2 or Nano Banana across lighting. Use a number plus descriptive tone, undertone, neutral lighting, and review. | Scale is not exact control | §7b |
| Grain | Some studies indicate well-matched noise can improve perceived texture and viewers cite grain as an authenticity cue; no controlled AI-portrait study establishes a grain recipe that survives social-platform encoding. | Incomplete | §9b, §15 |
| Identity drift | Editing benchmarks show strong aggregate GPT Image 2 performance but not zero drift. Prompt-only preservation can leak; narrow masking plus compositing the accepted region over the original is the strongest supported workflow. | Composite to enforce | §9a, §11 |

## What changed in the skill because of the research

- **Engine facts:** the size envelope and the Codex routing are documented; the Codex wrapper exposes no controls and its export sizes are unexplained, so the prompt states the size and the manifest is the record. Master at placement-native canvases (1080x1350, 1080x1920, 1080x1080).
- **Constraints:** critical constraints go in as positive physical states; the Avoid line is an echo, not a mechanism.
- **Hair:** geometry vocabulary, matte / satin / wet-look physics, follicle-gradient beard, mixed-diameter curl clumps.
- **Skin tone:** Monk number + undertone + local pigmentation, paired with a lighting and white-balance clause; state the tone every time because of the lighter-default bias.
- **Delivery:** several-pixel cues carry realism at 1080 px; masters stay grain-free until a served-transcode test proves grain helps.
- **Edits and enhancement:** bounded refine prompt that enumerates preserved regions; local mask-composite of the accepted region; resample-then-downscale rather than generative enhancement; SwinIR / HAT only, face restoration off, strict rejection criteria; never CodeFormer / GFPGAN on identity work.
- **Engine decision:** unchanged. No evidence justifies a second engine.

## Still unmeasured (the §15 test queue)

Codex export dimensions and whether edits resample · exclusions that survive positive-state conversion · identity-edit leakage rates · skin and hair phrase ablations · served platform encoding and survival thresholds · grain benefit after encode · Monk-number compliance · upscaler acceptance on faces and labels · a cross-engine macro benchmark. None of these is a rule until a batch on this engine confirms it.
