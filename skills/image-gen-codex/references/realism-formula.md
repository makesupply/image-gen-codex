# Realism Formula — physics-level skin and hair prompting for GPT-Image (Codex `$imagegen`)

Read this alongside `prompt-craft.md` §4 (photorealism levers) before any production prompt whose subject is a **person, skin, hair, beard, or a product held against skin**. `prompt-craft.md` tells you *which* levers exist; this file is the *physics-level* recipe for the realism ones, scaled to every shot distance you actually use, and extended to the thing the source never covers: **hair**.

> **Authoring note:** every copy-ready block below is kept ASCII-only (straight quotes, hyphens, no bullets or accents). This bridge sends prompts as UTF-8, so that is portability for older locale-bound Codex builds, not a requirement.

**Source and attribution.** The starting point was a publicly shared prompt carousel titled *"Realism Formula — The prompts. The system."* (invideo, April 2026): one JSON master prompt for extreme-macro skin realism written for Google's Nano Banana 2, six worked body-part examples, a Magnific AI upscale step, and a Kling animate step. The carousel invites reuse of its master prompt; its text is not reproduced here beyond the clause-by-clause analysis in §1, and the adapted block in §3 is this skill's own wording.

**Research markers.** Two rounds of desk research (Perplexity Deep Research, 2026-09-03) were run against this file's open questions and are summarized in `research-notes-2026-09.md` with the dossiers' own confidence tags. Findings folded in below are marked **[R]** (round 1) and **[R2]** (round 2). Anything the research left unmeasured sits in §15 as a test queue, not as a rule.

---

## 0. What the source is, and what to take from it

The carousel's domain is narrow and precise: **extreme macro skin photography** ("skin fills 85% of frame") on Nano Banana 2 at 4K, with a separate `negative_prompt` field and a paid detail-enhancement pass. That is not this skill's stack and not most teams' shot list. What transfers is the **physics**: the formula works because every clause names a physical cause (light angle, oil on convex surfaces, subsurface color, tonal curve) rather than a taste word.

**Taken:** the 14-clause fixed block and why each clause works (§1), the three-slot structure (§3), the negative list (§8), the *conservative* second-pass idea (§9).
**Adapted:** engine differences Nano Banana 2 -> Codex `$imagegen` / GPT-Image (§2); a **distance ladder** so the formula stops being macro-only (§4); a **Hair Realism Block** the source has no equivalent for (§5); product-in-scene physical accuracy (§6); grooming body-part and skin-tone slot libraries (§7).
**Not adopted:** the carousel cover's likeness of a real person (never generate a recognizable real person who has not consented), text-in-skin tattoos (dense text garbles), and the skin-*condition* imperfections the master prompt lists as options (`keloid`, `acne scarring`) — the guardrail in `prompt-craft.md` §4c stands: imperfections are identity marks, never conditions (§7c). The tool chain (invideo, Magnific, Kling) is not adopted.

---

## 1. Decomposition — what each clause of the master prompt does physically

The master prompt is one fixed paragraph with three tweakable slots (`body_part`, `skin_tone`, `imperfections[]`). Read it as 14 mechanisms, not as a vibe:

| # | Clause (source wording, quoted for analysis) | Mechanism — why it beats loose phrasing | Keep / adapt |
|---|---|---|---|
| 1 | `Extreme macro photograph of [BODY_PART].` | Declares **format + framing first** (the 8-slot rule). "Macro" loads the macro-photography prior: shallow DOF, lens compression, resolving power. | Keep; the format word changes per ladder rung (§4). |
| 2 | `[SKIN_TONE] skin.` | Tone as its **own sentence** so every later gradient (melanin, flush, sheen) is computed relative to a stated baseline instead of a default. | Keep; use the §7b vocabulary. |
| 3 | `Photorealistic, shot on medium format film.` | Capture-device anchor (`prompt-craft` §4a). Medium format = smooth tonal gradation + high resolving power; "film" = grain + highlight shoulder prior. Beats "8K", which pulls toward digital over-sharpness. | Keep for R1-R2; swap to a phone anchor for R3 (§4). |
| 4 | `Raking side-top light at 45 degrees reveals every pore as a 3D crater with its own micro-shadow.` | **The key clause.** Texture is a function of light angle: frontal/soft light fills pores (flat), raking light casts micro-shadows that make relief visible. It also states the light's *visible consequence*, not just its position — a general principle: say what the light DOES. | Keep; at R2 add a soft fill so the face is not half-black; at R3-R4 the raking language goes away. |
| 5 | `Shallow depth of field - critical sharpness in the center, gentle optical falloff at edges.` | DOF as a **sharpness distribution**. Uniform edge-to-edge sharpness is the CGI tell; naming where sharpness lives gives the model permission to soften. | Keep; move the sharp point to the eyes at R2. |
| 6 | `Visible: individual pore openings with depth, vellus peach fuzz catching sidelight, natural sebum sheen (uneven, concentrated on convex surfaces), subsurface color variation (veins, capillary flush, melanin gradients), micro-wrinkles between major features.` | A **named micro-feature inventory**. Pores *with depth* (not dots); vellus hair (the #1 realism carrier at macro); sebum **uneven and on convex surfaces** (oil sits on high points: nose, forehead, cheekbones — physically reasoned, so the model places it right); subsurface color variation (fights *uniform tone*, the #1 AI tell); micro-wrinkles (the fine crosshatch). | Keep at R1; localize at R2; reduce to "soft suggestion" at R3; drop at R4. |
| 7 | `[IMPERFECTION] rendered with full physical accuracy - casting micro-shadow, distinct texture from surrounding skin.` | A feature must **interact with light** (cast shadow) and have **its own material**. Same physical-logic rule as the reference-image guidance in `LEARNINGS.md` ("nothing floats"). | Keep; this is also how to describe the product in a skin scene (§6). |
| 8 | `Skin fills 85% of frame.` | Explicit **frame-fill percentage** (the "product occupies 45-55%" analog). | Keep; the percentage is the ladder rung. |
| 9 | `Fine organic film grain throughout.` | Grain as a texture unifier; "organic" steers away from digital color noise. | Keep, say it once. GPT-Image over-delivers when grain is mentioned twice. |
| 10 | `Zero digital sharpening - all sharpness is optical.` | Kills the **sharpening halo**, a top AI tell. | Keep, always. |
| 11 | `Lifted blacks - shadow detail preserved inside every pore.` | Tonal-curve instruction: no crushed shadows, so pore interiors keep detail; also the film look. | Keep. |
| 12 | `Soft highlight rolloff - specular sheen never clips.` | No blown whites; the sheen keeps skin color inside it; film shoulder. On **deep skin tones the specular highlight is the main texture carrier**, so this clause matters most there. | Keep. |
| 13 | `No makeup, no retouching, no smoothing, no filters.` | Process negatives in prose (the engine has no negative field, §2). | Keep. |
| 14 | `The skin must look uncomfortably real - a dermatological study shot by a cinematographer.` | The **commit sentence**: two priors fused (clinical accuracy + cinematic light). Same job as the UGC "unedited phone frame" commit line. | Keep at R1-R2; at R3 use the UGC commit line instead. |

**Negative list** (`airbrushed, smooth skin, uniform tone, beauty lighting, ring light, porcelain, digital sharpening halos, symmetrical pore patterns, CGI, plastic, silicone, flat lighting, text, logos, watermarks`): note the three groups — *surface failures* (airbrushed / porcelain / plastic / silicone), *texture killers* (beauty lighting, ring light, flat lighting — soft frontal light erases relief), and *AI artifacts* (sharpening halos, **symmetrical pore patterns** = tiled texture). Merged into §8.

**Upscale block** (Magnific: preset Low, 2x, creativity -3, hdr 0, resemblance 3, fractality 0, prompt "Add micro pores, micro hairs and sharp skin texture"): the settings are deliberately **conservative** — minimum hallucination, maximum resemblance. The lesson is not "buy Magnific"; it is *a second pass must add detail without re-imagining*. The substitute in §9 honors that.

---

## 2. Engine adaptation — Nano Banana 2 -> Codex `$imagegen` (GPT-Image)

This skill has one engine (`prompt-craft.md` §0). Differences that change how the formula is written:

| Source assumes | This engine | What to do |
|---|---|---|
| A separate `negative_prompt` field | No negative field | Fold negatives into one **`Avoid:`** sentence at the end of the prompt. Keep it short and specific (10-16 items); a long negative list dilutes the positive brief. **[R]** No verified negative-conditioning channel exists for GPT Image and no controlled with/without test was found: the Avoid line is a secondary natural-language constraint, never the mechanism that fixes a weak positive description. **[R2]** Controlled research on the DALL-E 3 lineage found plain negation handled poorly, so every constraint that matters goes in as a positive physical state (§8). |
| 4K output | **[R]** API docs (2026-04, high confidence): gpt-image-1 / 1.5 / 1-mini return 1024x1024, 1024x1536, 1536x1024, or auto; **gpt-image-2 accepts flexible sizes** (both edges divisible by 16, long:short at most 3:1, 655,360 to 8,294,400 total pixels, max edge under 3840; anything above 2560x1440 is experimental). `quality` changes rendering effort, `size` changes pixels. **[R2] Codex routing is documented: built-in image generation uses `gpt-image-2`** (OpenAI Codex docs; high confidence), invoked by natural language or `$imagegen`, drawing on general Codex usage limits. The docs expose **no** desktop fields for `size`, `quality`, input fidelity, reference count, masks, quotas, or concurrency, so the integration is a natural-language wrapper and a prose size is a request, not a parameter. **Export dimensions remain unexplained:** this bridge has returned 1024x1024, 1254x1254, and 1080x1350 for prose-stated sizes (one machine, 2026-09-03), none divisible by 16, and no public source accounts for it (§15); with no size stated at all (2026-09-03, bare one-word prompts) it returned 1024x1536 and 863x1823, so an unstated size is a lottery. The manifest beside every PNG records the prompt (with the requested size), the references, the actual width x height, bytes, and SHA-256, which is the per-generation logging the research asks for. | State the aspect ratio and pixel size in the prompt (the bridge has no size flag) and read the manifest every time. Ask for texture **at generation**, not after; texture survives *downscale* far better than *upscale*. If Codex ever exposes size control, generate at 2K-class (2560x1440 or the portrait equivalent) and downscale once to the 1080 px master (§9b). **[R2]** Master at the placement-native canvas: 1080x1350 for 4:5 feed, 1080x1920 for 9:16 vertical, 1080x1080 for square. |
| Magnific detail pass | No paid tools (this skill is subscription-only) | Two-pass refine through Codex with a preservation fence, or the resample-then-grain ladder. Never sharpen. §9. **[R]** Generative refinement is not deterministic: benchmarks (GIE-Bench 2025, restoration studies 2025) show GPT editing alters irrelevant regions, geometry, counts, and perspective. Enumerate every region that must stay unchanged, inspect for global drift at 200 percent, keep the original for compositing. |
| `"model"`, `"resolution"`, `"upscale"` JSON keys | Not consumed | Drop them. Keep the *slot idea* (`subject.body_part / skin_tone / imperfections`), not the braces — prose works for a single-subject realism shot; JSON is for multi-element scenes (`prompt-craft` §7). |
| Grain-tolerant renderer | GPT-Image renders "grain" heavier than asked | Say `fine organic film grain` **once**. At R3 say `phone-sensor noise` instead. |
| Smoother-than-reality is not its default | It IS GPT-Image's (`prompt-craft` §0) | This formula is the compensation. Load it fully at R1-R2. |
| Reference blending is strong | ~5-ref cap, leans on text over the reference for identity | For a specific person, the identity anchor block (`prompt-craft` §4f) goes **first**, then the realism block. **[R]** API docs describe gpt-image-2 identity preservation as robust with high input fidelity by default; the Codex wrapper exposes none of that and a live run showed reference drift, so keep the anchor block and restate the description. |
| A second engine would be better at skin | **[R]** No controlled head-to-head macro skin / hair benchmark exists across GPT-Image-2, current Nano Banana, Flux, and Midjourney (2026-09-03; **[R2]** re-confirmed). Nano Banana scores well on perceptual texture but that includes *hallucinated* high-frequency detail; GPT-Image-1 was criticized for overly smooth skin and oily facial sheen (RealGen, 2025-11), which is exactly what the baseline pairs in §12 showed. | A second engine is not justified by evidence. If it is ever considered, run the §15 cross-engine test protocol first: same references, prompt, aspect, size, crop, and generation count per engine, scored across multiple outputs. |

---

## 3. The Realism Block (RB) — the fixed core, copy-ready

Fill the `[SLOTS]`, keep the rest verbatim. Skin-only; add the Hair block (§5) when hair or beard is in frame; add the product fence (§6 / `prompt-craft` §6) when a product is in frame.

```
[SHOT] of [BODY_PART]. [SKIN_TONE] skin. [SCENE_DETAIL: what is in frame, from where to where,
plus anything worn or held]. Photorealistic, shot on medium format film. Raking side-top light at
45 degrees reveals every pore as a small crater with its own micro-shadow. Shallow depth of field:
critical sharpness at [FOCUS_POINT], gentle optical falloff toward the edges. Visible: individual
pore openings with depth, vellus peach fuzz catching the sidelight, natural sebum sheen that is
uneven and concentrated on convex surfaces, subsurface color variation (faint veins, capillary
flush, melanin gradients), micro-wrinkles between the major features. [FEATURE] rendered with full
physical accuracy, casting its own micro-shadow, with a texture distinct from the surrounding skin.
Skin fills [FILL] percent of the frame, [BACKGROUND]. Fine organic film grain throughout. Zero
digital sharpening: all sharpness is optical. Lifted blacks: shadow detail preserved inside every
pore. Soft highlight rolloff: specular sheen never clips. No makeup, no retouching, no smoothing,
no filters. The skin must look uncomfortably real, like a dermatological study shot by a
cinematographer. Avoid: airbrushed, smooth skin, uniform tone, beauty lighting, ring light,
porcelain, digital sharpening halos, symmetrical or repeating pore patterns, CGI, plastic,
silicone, flat lighting, text, logos, watermarks. [ASPECT].
```

Slot guide:
- `[SHOT]` — `Extreme macro photograph` (R1) / `Close-up portrait photograph` (R2). R3-R4 use the ladder variants in §4, not this block.
- `[BODY_PART]` — from §7a.
- `[SKIN_TONE]` — from §7b, always with an undertone word.
- `[SCENE_DETAIL]` — the source's examples all add 1-3 concrete sentences here (what is worn, what is at the frame edge, the background color). Do the same; it is where the shot stops being generic.
- `[FOCUS_POINT]` — `the center of the frame` (R1) / `the eyes and the near cheek` (R2).
- `[FEATURE]` — the one identity mark or the beard / hair (§7c). Restate it here even though it is already in `[SCENE_DETAIL]`; the source repeats on purpose.
- `[FILL]` — `85` at R1, `70` at R2.
- `[BACKGROUND]` — `softly blurred neutral warm background` / `plain dark neutral background, softly blurred`.
- `[ASPECT]` — `Square 1:1 image, 1080x1080` / `Portrait 4:5 image, 1080x1350`.

---

## 4. The distance ladder — scale the texture to the shot (the main expansion)

The source is macro-only. Applied unchanged at half-body it does not help: in the 2026-09-03 validation (§12, pair 04) the engine mostly **ignored** the macro inventory at selfie distance and the result drifted *more polished*, because the words that carry realism at that distance (phone-sensor noise, motion softness, flat grade, lens distortion) were missing. On other engines the same mistake produces leather skin. Either way the rule holds: *the texture vocabulary must match what a real lens would see from where the camera stands.* Four rungs:

| Rung | Frame | Camera anchor | Skin language | Hair language | Light | Grain | DROP |
|---|---|---|---|---|---|---|---|
| **R1 Macro** | one feature fills 85%+ | `Extreme macro photograph ... medium format film` (or `100mm macro lens at f/4`) | full RB inventory | follicle level: each hair grows from visible skin and casts a shadow | raking side-top 45 deg | fine organic film grain | expression, environment |
| **R2 Close-up portrait** | face fills the frame, ~70% | `Close-up portrait ... medium format film` or `85mm f/1.4-f/2` | RB inventory **localized**: pores as tiny craters *on the nose, cheeks, forehead*; sheen *on the T-zone*; flush *on cheeks and nose*; micro-wrinkles *at the eye corners and across the forehead*; plus the eyes clause below | strand level for beard, brows, hairline; scalp regrowth dots on a shaved head | raking key 45 deg **with a soft fill** so texture reads without half the face going black | fine grain | "every pore", "dermatological" is optional |
| **R3 Half-body / UGC selfie** | head + shoulders (+ raised arm) | `Raw phone front-camera selfie video frame grab` or `35-50mm` | tone unevenness, T-zone shine, faint under-eye shadows, `the soft suggestion of pore texture on the nose and cheeks without exaggerated detail`, 1-2 identity marks | clumps / ringlets with gaps, frizz halo, flyaways against the light | window light with one side of the face in shadow; or harsh on-camera flash (candid phone-camera angle) | `phone-sensor grain and noise` | ALL crater / vellus / veins / "dermatological" language |
| **R4 Environmental** | full body, scene | `35mm f/2.8, environmental` | almost none: `natural skin, not retouched`; hands anatomically correct | silhouette level: hair mass with a few loose strands, flyaways rim-lit | one consistent source; contact shadows under every object | light grain | all skin micro-language; realism is carried by fabric weave, surface wear, clutter, and light consistency |

**Look package per rung (`look-packages.md`):** the ladder sets the *texture* vocabulary; the package sets the *optics and tonal curve*, written as camera + lens + stock = name + visible result + physical cause, never a bare camera name. R1 -> L1 film look with the raking light (or the 100mm macro anchor); R2 -> L1 (film, window-lit plates), L4 (portrait separation, hero cards: eyes precisely focused, lamps meters behind as rounded highlights) or L2 (clean natural detail, whenever the label is in frame); R3 -> the phone package (unchanged) or L2 for a waist-up product demonstration; R4 -> L5 natural depth: `Moderate depth of field; the background remains recognizable but softly separated` replaces the habitual `softly blurred background` whenever the setting carries part of the message. Two rules ride with every package: name the **focus target** (the eyes for a portrait; the label first for a product demonstration), and keep the **three kinds of softness** apart (soft light = gentle shadow edges, soft background = defocus, soft highlight roll-off = gradual transition into the bright areas; none of them requires blurry eyes). When a package already states grain (L1), drop the separate grain sentence: grain is said once.

**Eyes clause (R2 only, copy-ready):** `Eyes: [COLOR] iris with visible radial fibers, one small natural catchlight, individual short eyelashes, fine under-eye texture.` One catchlight, never a ring — a ring-shaped catchlight is the ring-light tell the negative list bans.

**R3 block (copy-ready, replaces the RB at selfie distance; pair with the imperfection block from `prompt-craft` §4b):**
```
Skin at this distance: natural unevenness in tone, a hint of shine on the nose and forehead from
natural oils, faint under-eye shadows, the soft suggestion of pore texture on the nose and cheeks
without exaggerated detail, one or two small marks like a mole or a healed nick that read as a
real person. Lifted blacks and soft highlight rolloff like a phone HDR frame. Visible phone-sensor
grain and noise. No retouching, no beauty filter, no airbrushed skin, no flawless complexion, no
exaggerated pore detail.
```

**Choosing the rung:** decide by *what the image needs the viewer to feel*. Product-benefit close-ups (beard oil on a beard, clay texture in hair, curl definition) are R1-R2 — the texture IS the message. Spokesperson talking-head stills are R2. Candid / UGC / testimonial frames are R3. Lifestyle and environment are R4. Never write an R1 block for an R3 shot because "more realism is better"; it is not, it is a different lens.

**Delivery-size lens [R] (2026-09-03, medium confidence for the principle, no platform-specific thresholds yet):** platform re-encoding destroys one-pixel detail first (very fine pores, tiny vellus hairs away from high-contrast edges, one-pixel flyaways, fine random film grain, subtle chroma mottling) and keeps several-pixel cues (directional side light, broad pore relief, wrinkles and creases, localized sebum sheen, scalp at the part, curl-clump separation, silhouette flyaways, beard-density gradients, larger tone variation). For a 1080 px social image, micro-texture *supports* realism and the several-pixel cues *carry* it. So at R1-R2 the non-negotiables are light direction, relief that spans several output pixels, sheen placement, and strand-group separation; the vellus-hair and film-grain clauses are stills-only polish that costs nothing but should not be relied on. **[R2]** Meta and TikTok publish upload dimensions, formats, and acceptance requirements only; no first-party source publishes served JPEG / WebP quality, chroma subsampling, sharpening, or bitrate. So: master at the placement-native canvas (1080x1350 for 4:5, 1080x1920 for 9:16, 1080x1080 for 1:1), keep the master grain-free, and judge realism on a *served* test asset, never on the upload.

---

## 5. Hair Realism Block (HRB) — absent from the source

Hair fails in GPT-Image the same way skin does, one level up: it renders as a **smooth mass** (helmet, painted, plastic sheen) unless the prompt states strand logic and light logic. Every styling product changes hair's *surface physics*, so the product finish must be described as a material, not a product name.

**5a. Core block (copy-ready; insert after the skin inventory):**
```
Hair as geometry, not a mass: a clearly readable parting line with a narrow strip of visible scalp
that has its own pore texture; directional root-to-tip strand flow; separated strand groups with
small irregular gaps between them, varying in thickness, direction, and length; fine perimeter
flyaways and short baby hairs at the temples and hairline catching the light; restrained natural
frizz. Rim and raking light skims across the hair so highlights follow the strand direction and
each group casts a micro-shadow on the strands beneath it, never forming one solid painted
highlight band. [FINISH sentence from 5b]. Natural color variation within the hair: a few lighter
and grayer strands, darker roots, no uniform color fill. Avoid: helmet-like single mass, painted
hair, uniform strands, plastic sheen, blurry hair mass, a single glossy highlight band, perfectly
even hairline.
```
**[R]** The geometry vocabulary (parting line, scalp strip, root-to-tip flow, strand *groups* with irregular gaps, perimeter flyaways, no painted highlight band) comes from hair-reconstruction research and the HairPort editing prompt (medium confidence). Its GPT-specific reliability is untested beyond the §12 pair, so treat individual phrase choices as A/B candidates (§15). The shorter first-version wording ("strand by strand ... visible gaps") is what §12 validated; this version adds organization terms without removing any of it.

**5b. Product-finish vocabulary — state the surface physics, not the product name:**

| Finish | Surface physics to state | Strand behavior | Avoid |
|---|---|---|---|
| Matte clay | `dry, diffuse, chalky, light-absorbing, no wet shine, no highlight on any individual strand` (validated 2026-09-03: "dry, diffuse, no wet shine" alone still left a satin sheen). **[R]** physics wording: `diffuse low-luster surface, broad soft reflections, minimal specular streaking, dry strand separation, no oily highlight band` | separated pieces and clumps, piecey texture, holds shape without shine | wet look, glossy, satin sheen, oily highlight band |
| Pomade (classic shine) | `controlled satin-to-gloss sheen, broad soft highlights running along the comb grooves`. **[R]** satin wording: `controlled medium luster, narrow soft reflections that follow the strand flow, individual fibers still visible inside the highlights, no mirror-like glare` | slicked, comb grooves visible, strands aligned but individually visible inside the highlight | plastic helmet, mirror gloss |
| Matte paste with thickening fibers (thin hair) | `matte finish, strands look slightly thicker, scalp less visible` | lift at the root, strands separated, subtle fiber texture | painted-on density, visible product |
| Curl cream | `soft sheen on defined ringlets, hydrated not wet` | ringlets and clumps with visible gaps, frizz tamed but a few loose strands, root-to-tip definition. **[R]** clump physics: `curl clumps of mixed diameter and irregular spacing, several partial ringlets rather than identical complete spirals, denser roots and looser tips, occasional crossed and escaped strands, no repeating corkscrew pattern` | glued, crunchy, wet-gel, identical repeated corkscrews |
| Mousse | `light hold, airy, faint sheen` | volume, defined but soft | crunchy, stiff |
| Sea salt spray | `matte, slightly gritty, tousled` | separated, wind-moved, texture concentrated at the ends | uniform strands, shine |
| Gel (wet look) | `high gloss, wet, sharp narrow highlights`. **[R]** wet-look wording: `cohesive damp clumps with darker local value, thin sharper specular lines aligned with strand direction, small gaps between clumps, visible moisture weight, no plastic shell or uniformly glossy mass` | strands clumped into wet ribbons | dry frizz, plastic shell |
| Beard oil | `soft conditioned sheen on each hair, the skin beneath moisturized` | individual hairs glossy and lying flatter | greasy blob, single shine patch |
| Beard balm | `low sheen, shaped edges` | hairs shaped, edges defined, still individual | |
| Hair / beard powder concealer | `matte powder finish on the scalp or hairline` | hairline looks denser, strands unchanged, slight powder softness at the edge | visible residue, painted line |

**5c. Curl pattern vocabulary:** describe by **ringlet size and clump behavior**, never by ethnicity.
- Wavy (2A-2C): `loose S-waves` -> `defined S-waves with some clumping`.
- Curly (3A-3C): `loose spirals about the width of a marker` -> `springy curls about the width of a pencil, defined clumps with visible gaps`.
- Coily (4A-4C): `tight coils the width of a crochet needle, dense, springy` -> `zig-zag coils, very dense, shrinkage visible`.
Always add: `a soft frizz halo of loose strands catching the light` and `root-to-tip definition` when the product story is definition.
**[R] Curl fragment (medium confidence, copy-ready):** `Curl structure: springy curl clumps with mixed diameter and irregular spacing; several partial ringlets rather than identical complete spirals; visible separation between clumps; a light frizz halo at the outer silhouette; denser roots and looser tips; occasional crossed and escaped strands; no repeating corkscrew pattern.` Describe curls only in measurable terms (ringlet diameter, clump size, density, direction, root lift, shrinkage, perimeter frizz, moisture level); never use ethnicity as a proxy for hair geometry.

**5d. Beard clause (copy-ready; [R] upgraded with follicle spacing, taper, and the density gradient):** `Beard rendered strand by strand: individual tapered hairs emerge from visible skin with readable follicle spacing and varied growth direction, lower density on the upper cheeks increasing gradually through the jaw and chin, mixed lengths and curvature, a few gray and stray hairs, skin and pores visible between the hairs, no solid painted beard shape.`

**5e. Fade / shaved-head clause (copy-ready):** `Skin fade: hair length graduates from bare skin at the temple to a few millimeters above, individual regrowth dots visible in the faded zone with the scalp skin between them, a crisp line-up edge at the hairline with a few tiny stray hairs.` For a shaved head: `Scalp stubble as individual dots of regrowth with the scalp skin visible between them.`

---

## 6. Product-surface realism — the physical-accuracy clause applied to the product

When the product is in the skin scene (hand holding a tin, fingers with product, product against a beard), two things are true at once: the **label is fenced** (`prompt-craft` §6: keep the label, wordmark, colors, proportions intact; no new text, logos, watermarks) and the **product must obey the same physics as the skin** (source clause 7).

Copy-ready add-on:
```
The product from image_ref[0] rendered with full physical accuracy: it sits in the hand with a
real grip, fingertips pressing slightly into the skin around it, it casts a contact shadow onto
the palm and fingers, and its surface reflects the same raking light as the skin. [PRODUCT SURFACE:
open tin with a finger trough swept through the pomade and a soft satin sheen / matte granular
clay surface, dry, no shine / cream with soft peaks and a faint sheen]. A trace of product on the
fingertips with its own sheen. Keep the label, wordmark, colors, and proportions from image_ref[0]
perfectly intact. No new text, no new logos, no watermarks, no extra product copies.
```
The product itself stays brand-new (no scratches, no dust — the e-commerce rule). The *skin and product surface* carry the realism; the *packaging* carries fidelity.

**Focus target for a product demonstration (`look-packages.md` §3c):** at R2-R3 the portrait rungs' shallow, eyes-first depth of field lets the label go soft — in-hand plates inherit exactly that. For any frame where the product is being shown or used, write the priority: `Moderate depth of field chosen for a product demonstration: the face and the product label both stay readable; the label is the sharpest point in the frame and the eyes a close second; only the far wall softens.` Pair it with L2 (clean natural detail) and name the product surface as one of the two or three surfaces that matter. At R1 the macro rule stands (critical sharpness on the product surface or the wordmark).

---

## 7. Slot libraries

**7a. Body-part slots (grooming-adapted).** The source's ears / forehead / lips / neck / eye / finger become:

| Slot | Use it for | Scene-detail cues |
|---|---|---|
| hairline and side part | pomade, clay, paste, powder concealer | part line, comb grooves, scalp visible along the part, baby hairs |
| temple and fade | barber / fade shots, powder concealer | graduated length, regrowth dots, line-up edge |
| nape | fade, line-up | tapered hair into bare neck skin, vellus hair on the neck |
| jawline and beard line | beard oil, balm, filler pencil | cheek-line edge, sparse-to-dense gradient, skin between hairs |
| chin and goatee | spokesperson close-ups, beard products | goatee density, gray strands, lip line above |
| ear and fade | barber context | helix / tragus / lobe, hair graduating above and behind the ear |
| hand holding the tin | any product-in-hand macro | grip, knuckle creases, nail edges, contact shadow (§6) |
| fingertips with product | texture demos | product on fingertips, sheen, finger-pad ridges |
| forehead (application) | applying product to the hairline | fingers at the hairline, product trace, forehead lines |
| eye | R2 stills | the eyes clause (§4) |
| lips, neck | rarely; never with text tattoos | |

**7b. Skin-tone vocabulary.** The source's five (`deep brown-black / warm medium brown / olive-tan / light beige-pink / pale with pink undertones`) plus an undertone axis. Describe **color and undertone**, never ethnicity-as-color:
`deep brown-black with cool undertones` · `deep brown-black with warm undertones` · `rich dark brown` · `warm medium brown` · `golden tan` · `olive-tan` · `light beige with neutral undertones` · `light beige-pink` · `pale with pink undertones` · `pale with yellow undertones`.
Two physically-true additions that read as real: **melanin gradients** are darker on knuckles, elbows, and around the eyes and lighter on the palms; and **the realism carrier shifts with tone** — on deep tones it is the specular sheen (so "soft highlight rolloff, never clips" matters most), on pale tones it is capillary flush and visible veins.

**[R] Monk anchor + undertone + local variation (medium confidence for the principle, low for model-specific compliance):** the Monk Skin Tone scale (1-10) describes *visible* tone better than Fitzpatrick, which was built around sun response and is thin on darker tones. GPT Image 1.5 defaults cluster toward lighter tones with less prompt-driven variation than Nano Banana, and lighting or grading can shift apparent tone by more than one Monk step. So **state the tone explicitly every time**, pair it with an undertone word, and never treat the number as deterministic. Copy-ready structure (ASCII):
```
Skin tone: approximately Monk [1-10], with a [warm / cool / neutral / olive / red-golden] undertone.
Preserve natural local variation rather than one flat color: slightly deeper pigmentation around the
eyes, mouth, hairline, knuckles, finger joints, and beard area; restrained capillary warmth on the
cheeks, nose, ears, and fingertips; subtle value changes across planes facing toward and away from
the light. Do not render the skin as one flat color.
```
Tone-specific cues: **deep tones** keep highlight color and texture instead of raising exposure (colored specular reflections, rich shadow chroma, darker joint and periorbital pigmentation; never lift the face until it goes gray or desaturated); **medium tones** get undertone-specific transitions, localized warmth, and subtle sun-exposed variation, never generic orange grading; **pale tones** get translucent variation, localized capillary flush, faint veins only where anatomically plausible, subtle freckles when appropriate, never uniform pink.

**[R2] The Monk number is a measurement anchor, not a control knob:** no controlled evidence shows that stating an exact MST number reproduces that tone in GPT Image 1.5 / 2 or Nano Banana across lighting. Pair the number with descriptive complexion words, the undertone, neutral white balance, controlled highlights, and open shadows, then review the output. Copy-ready control clause (ASCII):
```
An adult with deep brown skin, approximately Monk Skin Tone 7, with a neutral-warm golden-red
undertone. Preserve the deep brown local skin color in the midtones. Use soft neutral daylight,
restrained contrast, neutral white balance, and no stylized color grade. Keep highlights controlled
so they do not wash the complexion lighter, and keep shadows open enough to preserve hue.
```
Swap the tone words and the number per subject; keep the lighting and white-balance sentences, they are what stops the drift.

**7c. Imperfection vocabulary — firewalled.** Imperfections are **identity marks**, not conditions.
- **Allowed (state size where it helps):** `a raised mole about 4mm` · `a small freckle cluster` · `a healed thin scar about 15mm` · `fine lines at the eye corners` · `three horizontal forehead lines` · `fine under-eye texture` · `vertical lip lines` · `vellus hair` · `stubble regrowth dots` · `slight unevenness in tone` · `capillary flush on the nose and cheeks` · `a sun-darkened forehead` · `a small healed shaving nick` · `naturally thin hair at the crown with the scalp showing through` (allowed only when the product story IS thinning hair, e.g. a thickening paste or powder concealer).
- **Banned in brand creative:** `acne, pimples, breakouts, acne scarring, keloid, blemishes, redness as a condition, rash, eczema, dandruff flakes, bald patches` (outside the thinning-hair story). Same rule as `prompt-craft` §4c; the source lists `keloid` and `acne scarring` as options and this skill does not import them.

---

## 8. The merged Avoid line (copy-ready)

Skin: `Avoid: airbrushed, smooth skin, uniform tone, beauty lighting, ring light, porcelain, digital sharpening halos, symmetrical or repeating pore patterns, CGI, plastic, silicone, flat lighting, text, logos, watermarks.`
Hair add-on: `helmet hair, painted hair, uniform strands, plastic sheen, blurry hair mass, perfectly even hairline.`
UGC add-on (R3): `no studio lighting, not a professional photo, not perfectly composed, not tack sharp, no exaggerated pore detail.`
The standing safety suffixes (`prompt-craft` §11) still apply to any ad-creative canvas; the Avoid line does not replace them.

**[R] Observable-exclusion variant:** `Avoid: a beauty-filter finish, waxy or porcelain skin, uniform stamped pores, oily full-face gloss, ring-light catchlights, painted beard shapes, helmet-like hair, repeated identical curls, aggressive sharpening, crushed shadows.` Every item names something you can *see* in the output, which is what a natural-language constraint can act on. Use whichever list is shorter for the shot. The Avoid line is a secondary constraint, not a verified negative channel (§2).

**[R2] Positive state beats negation (controlled DALL-E 3 lineage research found plain negation handled poorly):** every constraint that matters must exist in the prompt body as a *desired physical state*; the Avoid line only echoes it. Pattern: `Use soft off-axis window light. Keep the catchlights broad and irregular. Do not use a circular frontal catchlight.` The first two sentences do the work; the third is the echo. Check the RB the same way: `ring light` in the Avoid line is backed by `one small natural catchlight` and `raking side-top light` in the body; `airbrushed` is backed by the pore inventory; `helmet hair` is backed by the strand-group sentences. An Avoid item with no positive counterpart in the body is a wish, not an instruction.

Two more positive forms (`look-packages.md` §3f): `Deep charcoal shadows retain subtle texture: shadow detail preserved inside every pore and between the curls` for blocked-up blacks (the positive form of "lifted blacks / no crushed shadows"), and `The eyes are the sharpest point in the frame; all sharpness is optical` in place of any `soft focus` / `not tack sharp` wording — the three kinds of softness (light, background, highlight roll-off) are separate physical conditions and none of them requires blurry eyes.

---

## 9. Two-pass refine protocol (the Magnific substitute)

The source's upscale settings say: *add micro-detail, change nothing else*. Two ways to do that on this stack, both **only when the first pass is already right** in composition, identity, and product fidelity. Never refine to rescue a bad first pass; regenerate with one targeted change instead (SKILL.md workflow step 7).

**[R] What the research changed here:** "change nothing else" is not something the engine can literally do. Text-guided GPT editing is strong at following the instruction but prone to altering *irrelevant* regions, geometry, object counts, and perspective (GIE-Bench 2025; restoration studies 2025; medium confidence). So the refine prompt must **enumerate every region that stays unchanged**, the pass must be inspected for global drift at 200 percent, and the original must be kept for compositing. No local tool adds *real* pore or strand information deterministically either, so the default path for size is resample-then-downscale, not generative enhancement (9b), and grain belongs at the final 1080 px size, not in the generation.

**9a. Codex refine pass (attach the first pass as `image_ref[0]`):**
```
python tool/generate.py --prompt-file "<job>/prompts/refine.txt" --image "<job>/<first-pass>.png" --output "<job>/<first-pass>-refined.png"
```
`refine.txt` (copy-ready, ASCII; **[R2]** bounded and enumerated):
```
Edit the attached image_ref[0] rather than regenerating it. Edit only the skin and hair surface of
the subject. Add subtle, irregular microtexture consistent with the existing focus and lighting:
irregular pore size and spacing, shallow pore depth in the existing raking light, short vellus
hairs, separated hair strands, natural tonal variation. Preserve the person's identity, facial
landmarks, eyes, nose, mouth, ears, hairline, beard boundary, hands, clothing, background, product
silhouette, package colors, logo placement, and every printed character exactly. Keep camera
position, crop, depth of field, white balance, exposure, and shadow direction unchanged. Zero
digital sharpening, no halos. Do not smooth, do not retouch, do not add text, logos, or
watermarks. Same aspect ratio and size as image_ref[0].
```
Caveat from `LEARNINGS.md` and the [R] benchmarks: references guide, they do not pixel-lock, and edits over-modify. Compare the pair at 200 percent on eyes, nostrils, lips, beard boundary, hairline, fingers, product silhouette, and every printed character; if identity, label typography, geometry, or the count and placement of small objects drifts, discard the refine and keep the first pass. Use a **new filename** (never `--force`). The preservation wording follows the documented pattern of naming the edit region and enumerating what must not change; it reduces drift, it does not guarantee zero drift.

**[R2] Composite to enforce it:** Codex exposes no mask, and prompt-only preservation leaks, so the strongest supported workflow is to take *only the accepted region* from the refine pass and composite it over the original locally. Paint a soft mask PNG (white = take from the refine, black = keep the original), then (optional helper; needs Pillow):
```
python - <<EOF
from PIL import Image, ImageFilter
orig = Image.open(r"<job>/<first-pass>.png").convert("RGB")
edit = Image.open(r"<job>/<first-pass>-refined.png").convert("RGB").resize(orig.size, Image.LANCZOS)
mask = Image.open(r"<job>/<first-pass>-mask.png").convert("L").resize(orig.size).filter(ImageFilter.GaussianBlur(12))
Image.composite(edit, orig, mask).save(r"<job>/<first-pass>-composited.png")
EOF
```
The resize exists because the refine may come back on a different canvas (§2). Everything outside the mask is the original by construction, so labels, hands, and background cannot drift. Judge the composite at 200 percent as before, and save it as a new versioned file.

**9b. Resample, then grain at final size (local, free, reversible) [R]:** no local tool adds *real* pore or strand information deterministically, so the default ladder is: generate at the largest size the bridge will return -> if the image is already clean, resample with Lanczos (never a generative face restorer) -> downscale **once** to the 1080 px delivery master -> add restrained **luminance-only** grain at that final size (sigma about 1.0-2.0 on 8-bit, grain diameter 1-2 px, lighter in smooth backgrounds and highlights) -> preview after an approximate platform re-encode. Grain baked into the generation at full size mostly dies in recompression; grain added at 1080 px is what the viewer actually sees, and keeping it luminance-only stops chroma compression from turning it into colored crawl. The sigma range is a low-confidence starting point for A/B (§15), not a rule. **[R2] Masters stay grain-free.** Causal evidence that grain improves perceived realism *after* platform encoding is incomplete, so the delivery master is the clean downscaled file; a grain variant is produced only for a served-transcode test and adopted only if the served version wins. Save every step as a new versioned file. Optional helper (needs Pillow + NumPy):
```
python - <<EOF
from PIL import Image; import numpy as np
src = r"<job>/<first-pass>.png"; dst = r"<job>/<first-pass>-1080-grain.png"
im0 = Image.open(src).convert("RGB"); W = 1080; H = round(im0.height * W / im0.width)
im = np.asarray(im0.resize((W, H), Image.LANCZOS)).astype(np.float32)   # downscale ONCE, first
rng = np.random.default_rng(7); noise = rng.normal(0, 1.5, im.shape[:2])[..., None]  # luminance-only, sigma 1.5
Image.fromarray(np.clip(im + noise, 0, 255).astype(np.uint8)).save(dst)
EOF
```
It is cosmetic; it cannot add pores or strands.

**9c. Local upscalers, only if a 2x enlargement is ever unavoidable [R] [R2]:** conservative restoration models at low strength only: SwinIR (Apache-2.0 repository) or HAT first, Real-ESRGAN (BSD-3 repository; can invent texture and over-sharpen faces) second. Never CodeFormer or GFPGAN on identity- or label-bearing work; they are face-restoration models whose learned priors alter identity-bearing features. Check the license at the exact repository *and checkpoint* version before commercial use. Round 2 confirmed SwinIR and HAT as the defensible deterministic baselines and found no benchmark proving identity or printed-text preservation and no Windows runtime table. If trialed: disable any face-restoration option, downsample to delivery size before judging, and reject the result if any face landmark, finger, bottle or tin outline, cap geometry, logo placement, or printed character changed. No controlled comparison against Magnific's low-creativity / high-resemblance preset exists (§15); this is the order to try in, not a current workflow.

---

## 10. Worked examples (grooming, copy-ready, ASCII)

**E1 — Beard macro (R1). Validated 2026-09-03 (§12, pair 01).**
```
Extreme macro photograph of a man's jawline and short beard, from the ear to the chin. Warm
medium brown skin. The beard fills the lower two thirds of the frame with the bare cheek skin
above it. Photorealistic, shot on medium format film. Raking side-top light at 45 degrees
reveals every pore as a small crater with its own micro-shadow. Shallow depth of field: critical
sharpness at the center of the frame, gentle optical falloff toward the edges. Visible: individual
pore openings with depth, vellus peach fuzz catching the sidelight, natural sebum sheen that is
uneven and concentrated on convex surfaces, subsurface color variation (faint veins, capillary
flush, melanin gradients), micro-wrinkles between the major features. The beard rendered with
full physical accuracy: individual hairs of different lengths and curvature growing out of
visible skin, each casting its own micro-shadow, sparser at the cheek line and denser at the
chin, a few gray strands, skin and pores visible between the hairs. Skin and beard fill 85
percent of the frame, softly blurred neutral warm background. Fine organic film grain throughout.
Zero digital sharpening: all sharpness is optical. Lifted blacks: shadow detail preserved inside
every pore and between the hairs. Soft highlight rolloff: specular sheen never clips. No makeup,
no retouching, no smoothing, no filters. The skin must look uncomfortably real, like a
dermatological study shot by a cinematographer. Avoid: airbrushed, smooth skin, uniform tone,
beauty lighting, ring light, porcelain, digital sharpening halos, symmetrical or repeating pore
patterns, helmet-like beard, CGI, plastic, silicone, flat lighting, text, logos, watermarks.
Square 1:1 image, 1080x1080.
```

**E2 — A specific real person (spokesperson or founder) with identity anchor (R2). Attach 2-3 clean reference photos as `image_ref[0..2]`, character hero first. Only for a person who has consented to being generated.**
```
CRITICAL CHARACTER LIKENESS: the subject is the exact same person as in image_ref[0], image_ref[1],
and image_ref[2]. Match the face exactly: [describe from the references: head shape, hair or
shaved head, facial hair shape and density, brow shape, eye shape and spacing, nose, mouth, skin
tone]. Maintain the exact facial proportions, facial-hair style, and skin tone. Do not generalize.
Close-up portrait photograph of this person, [SKIN_TONE] skin, looking straight into the camera
with a calm, direct expression, face filling the frame from the top of the head to just below the
chin. Photorealistic, shot on medium format film. Raking side-top key light at 45 degrees with a
soft fill so the skin texture reads across the whole face: pores visible as tiny craters with
their own micro-shadows on the nose, cheeks, and forehead; vellus peach fuzz on the cheeks and
ears catching the sidelight; natural sebum sheen, uneven and concentrated on the forehead, nose
bridge, and chin; subsurface color variation with faint capillary flush on the cheeks and nose and
melanin gradients across the face; micro-wrinkles at the corners of the eyes and across the
forehead. [FACIAL HAIR: the 5d beard clause, or omit]. [HAIR: the 5a block or the 5e shaved-head
clause]. Eyes: [COLOR] iris with visible radial fibers, one small natural catchlight, individual
short eyelashes, fine under-eye texture. Shallow depth of field: critical sharpness on the eyes
and the near cheek, gentle optical falloff at the ears and the back of the head. Fine organic
film grain throughout. Zero digital sharpening: all sharpness is optical. Lifted blacks: shadow
detail preserved inside every pore. Soft highlight rolloff: the specular sheen on the forehead
and nose never clips. No makeup, no retouching, no smoothing, no filters. Plain dark neutral
background, softly blurred. Avoid: airbrushed, smooth skin, uniform tone, beauty lighting, ring
light, porcelain, digital sharpening halos, symmetrical or repeating pore patterns, CGI, plastic,
silicone, flat lighting, helmet-like beard, text, logos, watermarks. Portrait 4:5 image, 1080x1350.
```
Never render tattoo text; if a tattooed area is in frame, say `tattoos as soft abstract shapes, no legible letters`. Never a third-party mark.

**E3 — Styled hair, part line macro, matte clay (R1). Validated 2026-09-03 (§12, pair 03).**
```
Extreme close-up photograph of the top and side of a man's head: dark hair styled with a matte
clay and combed to the side with a clean side part, the hairline and temple visible at the lower
edge of the frame, warm medium brown skin. Hair rendered strand by strand, never as a solid mass:
individual hairs separate and overlap with visible gaps between them, varying in thickness,
direction, and length; the comb has left visible grooves and slightly separated clumps. Matte
clay finish as a physical surface: dry, diffuse, no wet shine, no specular highlights, texture
held in soft separated pieces. Raking light from the upper side skims across the hair so each
strand carries its own thin highlight and casts a micro-shadow on the strands beneath it.
Flyaways and baby hairs at the hairline and temple catch the light. Scalp faintly visible along
the part with its own pore texture and a few dots of regrowth. Natural color variation within the
hair: a few lighter and grayer strands, darker roots, no uniform color fill. Temple skin: pores
visible as tiny craters with micro-shadows, vellus peach fuzz catching the sidelight, natural
sebum sheen uneven at the forehead edge. Photorealistic, shot on medium format film. Shallow
depth of field: critical sharpness on the part line, gentle optical falloff at the back of the
head. Fine organic film grain throughout. Zero digital sharpening: all sharpness is optical.
Lifted blacks: shadow detail preserved between the strands. Soft highlight rolloff: highlights
never clip. No retouching, no smoothing, no filters. Hair and skin fill 85 percent of the frame,
softly blurred neutral background. Avoid: helmet hair, painted hair, uniform strands, plastic
sheen, blurry hair mass, wet gel look, perfectly even hairline, airbrushed skin, CGI, text,
logos, watermarks. Square 1:1 image, 1080x1080.
```
Swap the finish sentence from §5b for pomade, paste, or powder. For a fully matte read, use the stronger `chalky, light-absorbing, no highlight on any individual strand` wording (§5b).

**E4 — Curl definition close-up, curl cream (R2).**
```
Close-up photograph of the side and crown of a young man's head with springy 3B curls about the
width of a pencil, warm medium brown skin at the temple and ear, hair filling about 75 percent of
the frame. Hair rendered strand by strand, never as a solid mass: ringlets and clumps with visible
gaps between them, root-to-tip definition, a soft frizz halo of loose strands catching the light,
a few strands loose from the clumps. Curl cream finish as a physical surface: soft sheen on the
defined ringlets, hydrated not wet, no crunch, no gel gloss. Rim light from behind and above plus
a raking side light so each curl carries its own thin highlight and casts a micro-shadow on the
curls beneath it. Baby hairs at the hairline and temple catch the light. Natural color variation:
darker roots, a few lighter strands at the ends, no uniform color fill. Temple skin: soft
suggestion of pore texture, natural sebum sheen at the forehead edge, vellus hair catching the
sidelight. Photorealistic, shot on medium format film. Shallow depth of field: critical sharpness
on the curls nearest the camera, gentle optical falloff toward the back of the head. Fine organic
film grain throughout. Zero digital sharpening: all sharpness is optical. Lifted blacks: shadow
detail preserved between the curls. Soft highlight rolloff: highlights never clip. No retouching,
no smoothing, no filters. Softly blurred warm neutral background. Avoid: helmet hair, painted
hair, uniform strands, plastic sheen, blurry hair mass, wet gel look, crunchy curls, airbrushed
skin, CGI, text, logos, watermarks, store or shelf imagery. Square 1:1 image, 1080x1080.
```

**E5 — Hand holding the product tin, macro (R1 + product fence). Attach the official render as `image_ref[0]`.**
```
Extreme macro photograph of a man's hand holding the open product tin from image_ref[0], warm
medium brown skin, the tin and the fingers filling 85 percent of the frame, thumb on the rim and
fingertips underneath. Photorealistic, shot on medium format film. Raking side-top light at 45
degrees reveals every pore and knuckle crease as a small crater or fold with its own micro-shadow.
Shallow depth of field: critical sharpness on the product surface and the nearest fingertip,
gentle optical falloff at the wrist. Visible on the hand: individual pore openings with depth,
vellus hair on the back of the fingers catching the sidelight, natural sebum sheen uneven on the
knuckles, subsurface color variation (faint veins on the back of the hand, darker knuckles,
lighter finger pads), fine knuckle creases and nail edges with a natural cuticle. The product from
image_ref[0] rendered with full physical accuracy: it sits in the hand with a real grip, the
fingertips press slightly into the skin around it, it casts a contact shadow onto the palm and
fingers, and its surface reflects the same raking light as the skin. Open tin with a finger trough
swept through the product and a soft satin sheen, a trace of product on one fingertip with its own
sheen. Keep the label, wordmark, colors, and proportions from image_ref[0] perfectly intact. No new
text, no new logos, no watermarks, no extra product copies. Fine organic film grain throughout.
Zero digital sharpening: all sharpness is optical. Lifted blacks: shadow detail preserved inside
every pore and under the tin. Soft highlight rolloff: the sheen on the product and the skin never
clips. No retouching, no smoothing, no filters. Softly blurred neutral background. Avoid:
airbrushed, smooth skin, uniform tone, beauty lighting, ring light, porcelain, digital sharpening
halos, symmetrical or repeating pore patterns, CGI, plastic, silicone, flat lighting, extra
fingers, distorted hand, floating product, altered label, garbled package copy, added text or
logos. Square 1:1 image, 1080x1080.
```
Inspect the label and the hand before accepting (SKILL.md workflow step 5).

**E6 — UGC selfie (R3, candid phone-camera angle). Validated 2026-09-03 (§12, pair 04).**
```
Raw phone front-camera selfie video frame grab, 4:5 vertical, 1080x1350. A man in his early 20s,
warm medium brown skin, short dark curly hair, front-facing selfie angle slightly above eye level,
head and shoulders and one raised arm in frame, giving a relaxed half-smile mid-word. Setting: a
real bathroom in warm morning window light, one side of the face slightly in shadow. Skin at this
distance: natural unevenness in tone, a hint of shine on the nose and forehead from natural oils,
faint under-eye shadows, the soft suggestion of pore texture on the nose and cheeks without
exaggerated detail, one or two small marks like a mole or a healed nick that read as a real
person. Hair: curls defined as individual ringlets and clumps with visible gaps, a frizz halo of
loose strands catching the window light, natural color variation, not a solid mass. Slight motion
blur on the hair edges, slightly overexposed highlights on the forehead, visible phone-sensor grain
and noise, wide-angle lens distortion on the extended arm, slightly off-center tilted framing,
washed-out flat color grading, soft focus, nothing tack sharp. Lifted blacks and soft highlight
rolloff like a phone HDR frame. This must look like an unedited frame from a real phone selfie
video, not a professional photo: raw, unpolished, authentically amateur. No retouching, no beauty
filter, no studio lighting, no airbrushed skin, no flawless complexion, no exaggerated pore detail.
No text, no logos, no watermark.
```
**Look-layer update:** E6 stays as the validated record. For production, replace `soft focus, nothing tack sharp` with the R3 three-softness line (`look-packages.md` §3b: the eyes the sharpest point, motion softness only on the hair edges and the raised hand, a gentle highlight roll-off where the light hits the forehead) and `not tack sharp` with `no digital sharpening` — validated as pair 03 of the look-package batch (`look-packages.md` §6).

---

## 11. QA checklist — the AI tells to inspect before accepting a realism output

Look for these at 100% zoom before the output leaves the generated folder:
- **Repeating / tiled pore pattern** (the same pore cluster twice) — regenerate.
- **Sharpening halos** (bright rims along edges) — the prompt said zero sharpening; if present, regenerate, do not "fix" with blur.
- **Clipped speculars** (pure white patches on the forehead / nose / product) — highlight rolloff failed.
- **Plastic / porcelain / uniform tone** — the inventory did not land; add the `[SCENE_DETAIL]` concreteness and re-run; on deep tones check the sheen has color inside it.
- **Ring-shaped catchlight** — ring-light tell.
- **Helmet hair / painted beard / hairs merging into a mass**, **a perfectly even hairline** — HRB missing or overridden by a "clean" word elsewhere in the prompt.
- **Leather skin, or on this engine a polished drift, at R3-R4** — you wrote an R1 block for a selfie; the pore words are ignored and the phone-artifact words are missing. Step down the ladder.
- **Grain rendered as color noise / heavy speckle** — grain was mentioned twice or at R3 with "film" instead of "phone sensor".
- **Missing contact shadows** under the product or hand; **floating** anything.
- **Hands**: count fingers, check the grip; **label**: read every word against the reference render.
- **Over-symmetry** (mirror-perfect face) and **no identity marks** — add one mark from §7c.
- **Blurry eyes at R2-R3** — a softness conflation (`soft focus`, `not tack sharp`, "soft image"); rewrite with the eyes as the focus target (`look-packages.md` §3b). **Soft label in an in-hand frame** — the product-demonstration focus rule is missing (§6). **Background mush at R4** when the setting carries the message — ask for moderate depth of field, recognizable but softly separated (L5). **Flare with no source, or round bokeh where oval was asked** — L3 needs one practical near the frame edge and distant lights outside the focus plane.
- **After any refine, upscale, or composite [R2]:** compare against the original at 200 percent on face landmarks, fingers, product or tin outline, cap geometry, logo placement, and every printed character. Any change = reject that pass; composite only the accepted region over the original instead (§9a).

---

## 12. Validation on Codex `$imagegen` (2026-09-03)

Eight images, four A/B pairs, same subject and framing per pair, run through this bridge in two waves of four concurrent jobs (about five minutes total, no rate-limit errors). **A = the pre-existing `prompt-craft.md` §4 phrasing, B = this file's block.** Manifests recorded prompt, size, bytes, and SHA-256 beside each PNG.

| Pair | Shot | A (baseline) | B (this file) | Result |
|---|---|---|---|---|
| 01 | Beard macro (R1) | §4a-4d cues, film-stock name, 85mm | RB + beard clause | **B wins decisively.** A: softened skin, beard as fine painted strokes, a smeared artifact on the jaw. B: pores as craters with micro-shadows, sebum sheen on the cheekbone, follicle-level beard growing from visible skin, gray strands, vellus hair. Reads as a real macro. |
| 02 | Close-up portrait (R2) | three-point + skin block | RB localized + eyes + goatee + scalp | **B wins.** A: clean studio headshot, rim-light halo around the head, skin slightly smoothed. B: localized pores on nose / cheeks / forehead, T-zone sheen that does not clip, scalp regrowth dots, expression lines, strand-level goatee; softer warmer light, no halo. Less flattering, more real. |
| 03 | Styled hair, matte clay part (R1) | "individual strands catching light" | HRB + matte-clay finish | **B wins hardest.** A: glossy helmet hair, uniform strands, painted part line, wet look despite "matte clay" in the prompt. B: strand-by-strand with gaps, scalp visible along the part with pore texture, baby hairs at the temple, gray strands. Matte read only partial: a satin sheen remained. |
| 04 | UGC selfie (R3) | **macro block misapplied** at selfie distance | R3 ladder block | **B wins; hypothesis corrected.** A did not turn to leather: the engine ignored most of the macro inventory and produced a *polished* selfie (clean skin, no sensor noise, arm tucked behind the head). B reads as a real phone frame: wide-angle arm distortion, tilted framing, washed flat grade, sensor noise, ringlets with gaps, tone unevenness and T-zone shine. |

**What the batch changed in this file:** §4's ladder rationale (macro words at selfie distance are *wasted, not harmful* on this engine; the phone-artifact block carries R3), §5b's matte clay row (add `chalky, light-absorbing, no highlight on any individual strand` for a fully matte read), and §11's tell-list. Output sizes followed the prose aspect but not always the stated pixels: the four 4:5 asks came back exactly 1080x1350; the four 1:1 asks (stated as 1024x1024) came back 1024x1024 twice and 1254x1254 twice. Read the manifest, never assume the size.

---

## 13. Research log — two rounds, 2026-09-03

A six-question brief and a narrower eight-question follow-up were run through Perplexity Deep Research against this file's open questions. The findings, with the dossiers' own confidence tags, are summarized in `research-notes-2026-09.md`; the firm ones are folded in above as **[R]** and **[R2]**. In one paragraph: gpt-image-2's size envelope is documented and Codex's routing to it is documented, but the Codex wrapper exposes no controls and its export sizes are unexplained; prose negatives are an unverified secondary constraint and plain negation is handled poorly, so constraints go in as positive states; GPT editing over-modifies irrelevant regions, so refine prompts enumerate preserved regions and the accepted region is composited locally; hair is described as geometry and material; several-pixel cues carry realism at 1080 px and masters stay grain-free at placement-native canvases; Monk plus undertone beats Fitzpatrick but the number is an anchor, not a control; SwinIR / HAT are the only defensible local upscalers and remain unproven on identity and text; no controlled cross-engine macro benchmark exists, so a second engine is not evidence-justified.

---

## 14. Integration — where this plugs into the skill

- `look-packages.md` sits one level above this file: the optics and tonal curve per rung (L1 film / L2 clean / L3 anamorphic / L4 separation / L5 depth, each as name + visible result + cause), the focus-target rule for product demonstrations (§6 here), and the three-softness rule. The texture inventory, the HRB, and the fence are unchanged by it.
- `prompt-craft.md` §3 lighting table carries the **raking side-top 45 deg (texture reveal)** recipe; §4 points here for the full block; §13 templates `T-UGC` and `T-BeforeAfter` take the R3 block and the HRB respectively.
- Spokesperson / founder stills -> **E2** (identity anchor first, then RB at R2), only with the person's consent.
- Cut-out plates for composited layouts -> R2 / R3 with the HRB; any third-party mark stays in the deterministic layer (Hard Rule 0).
- Candid / UGC lanes -> **R3 only**; never R1 language on a selfie.
- Packaging / how-to icon sets -> §6 physical-accuracy clause plus the reference-image guidance in `LEARNINGS.md`.
- Firewall unchanged: no third-party trademarks or trade dress, no fabricated store / shelf / OOH scenes, dense text to the deterministic layer, no likeness of a real person without consent.

---

## 15. Experimental queue — tests to run before anything here becomes a rule

Round 2 either answered the desk-researchable questions or confirmed that no public evidence exists for them, so everything left here is **a test to run on this engine**, with the protocols round 2 specified. Run each the way §12 was run (same subject, framing, and size; A = current block, B = candidate; several outputs per arm, not one favorable pick) and promote a finding only after the batch confirms it.

1. **Codex export dimensions** — routing is settled (gpt-image-2, §2); what is not is what the wrapper does with a prose size. Generate each standard ratio (1:1, 4:5, 9:16, plus 1536x1536 and 2560x1440 asks) five times with the size stated in prose; record every actual raster from the manifests; then run one iterative edit on each and check whether the edit resamples. If 2K-class output ever appears, the §9b ladder starts there.
2. **Exclusions that survive positive-state conversion** — first rewrite every critical Avoid item as a positive physical state (§8); for the exclusions that remain, run identical prompts with and without them, multi-sample (at least ten per arm), scored on the §11 tell-list.
3. **Identity-edit leakage** — save source / edit pairs for the §9a bounded refine; isolate the intended edit region; measure change in the protected regions (face landmarks, hands, label glyphs); composite whenever protected pixels must stay fixed. Report the leakage rate, not one example.
4. **Skin and hair phrase ablation** — baseline vs `visible pores` vs `visible pores + sparse vellus hair in grazing light`, at least 20 generations per arm, blinded scoring; then the hair variants: first-version "strand by strand" vs the [R] geometry block, matte wording variants (chalky / light-absorbing vs diffuse low-luster), beard first-version vs [R] follicle wording, curl fragment vs the E4 curl sentence.
5. **Platform transcode survival, clean vs grain** — upload a clean master and a grain variant of one R1 and one R3 still as private / unpublished drafts on each platform (with the account owner's approval; drafts only, never activated); retrieve the *served* assets; compare edges, fine hair, skin texture, and label glyphs at 100 percent and at phone size. This single test answers both the survival-threshold and the grain-benefit questions; until it runs, masters stay grain-free (§9b) and the §4 lens stands on general compression behavior only.
6. **Grain parameters, only after item 5 shows grain helps** — sigma 1.0 / 1.5 / 2.0 luminance-only at 1080 px, judged on served assets.
7. **Monk-number compliance** — the same scene, light, and white balance with Monk 3, 6, and 9 stated using the §7b control clause; measure whether the output tracks the number and how far a lighting change shifts it.
8. **Upscaler acceptance** — build crops containing eyes, beard roots, curls, hands, tin or bottle edges, and printed labels; compare SwinIR and HAT at 2x with face restoration disabled, judged after downsampling to delivery size on identity and glyph fidelity; only if a 2x need ever appears.
9. **Cross-engine macro test** — only if a second engine is ever considered. Protocol: identical references, prompt, aspect, size, crop, and generation count per engine; score pore topology, vellus hair, beard emergence, strand separation, identity retention, and label text across all outputs. Copy-ready test prompt (ASCII):
```
Close beauty portrait photographed at natural viewing distance with a 90 mm macro lens look.
Preserve realistic facial proportions and optical falloff. Raking soft side-top light at
approximately 45 degrees reveals shallow pore relief without hard sharpening. Skin has nonuniform
pore size, short vellus hairs, localized capillary warmth, subtle subsurface color variation, and
restrained uneven sebum sheen only on convex planes. Hair has a readable part line, narrow visible
scalp, directional root-to-tip flow, separated strand groups, a few perimeter flyaways, and no
solid helmet-like mass. Facial hair emerges as individual tapered hairs from visible skin, with a
sparse-to-dense transition from upper cheek to jaw and chin. Soft highlight rolloff, lifted but
colored blacks, fine luminance grain, no digital sharpening. Avoid a beauty-filter finish, waxy or
porcelain skin, uniform pore stamps, oily full-face gloss, ring-light catchlights, painted beard
shapes, identical curl spirals, and a single glossy highlight band across the hair.
```
