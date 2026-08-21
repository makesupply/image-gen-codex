# Prompt Craft — reasoning layer for Codex `$imagegen`

Read this before writing any **production** image prompt. It is the craft/reasoning layer the base `SKILL.md` prompt-contract does not carry: how to fill each field for photorealism, illustration, spatial composition, and product/subject fidelity. Distilled and de-duplicated from three open image-prompting skills (an ad-prompt library, a photoreal product/portrait reference set, and a GPT-Image prompting skill), then generalized.

> **Encoding:** this bridge sends prompts to Codex as UTF-8, so any Unicode is fine. If you run an older bridge or a Codex build that reads stdin in the system locale, keep the actual prompt string ASCII-only (straight quotes, hyphens not em-dashes) to avoid a Windows cp1252 failure. The copy-ready blocks below are ASCII-clean either way.

---

## 0. Model reality — what `$imagegen` actually is

**Codex `$imagegen` renders with the GPT-Image model family.** You generally cannot swap models — treat its strengths and weaknesses as your operating envelope, not a menu.

**Native strengths (lean into these):**
- Legible **text, wordmarks, and typography-led layouts** — big bold headlines render cleanly; diagram/table/UI grammar is well-trained.
- A flat brand **wordmark as text** renders reliably.

**Documented weaknesses (compensate hard):**
- **Photoreal handheld objects, flatlay product photography with rich material rendering, and aspirational lifestyle photography with naturalistic lighting.** The model defaults to a slightly *smoother/more illustrated* look. For any realism target, load the imperfection + skin + texture blocks (§4) heavier than feels necessary.
- **Reference cap ~5 images, and it blends multiple references less smoothly.** Budget references; put the strongest identity signal first.
- **It leans on the TEXT description more than the reference image for identity.** Vague descriptors ("soft features", "same as reference") drift across angles. **Restate the full, specific description every time** — verbose text beats a terse "match the reference."
- **Dense small text garbles** even with guard suffixes. "The fix is fewer words, not more rules." Route dense copy to a deterministic text layer (§11).

**Practical corollary:** treat model-rendered text as safe **only** for a single large headline/wordmark. Everything dense (claims, prices, ingredient lists, multi-line copy, logos) goes to a deterministic layer (e.g. HTML composed over a model-generated background plate).

---

## 1. The brief method — structure beats style words

**Core thesis:** a strong prompt reads like a **visual brief, not a pile of style words.** The #1 failure is opening with taste words ("cinematic, premium, high-end") and leaving format/subject/composition undefined.

**The 8-slot brief order** — fill in this sequence:
1. **Image type / format** (poster, product hero, flatlay, lifestyle still, carousel card, editorial spread) — decide FIRST; it loads the model's spatial grammar.
2. **Core subject** — one clear focal point, with pose/action/state.
3. **Composition / layout** — the actual spatial arrangement (center + periphery, regions, grid, split).
4. **Supporting modules** — 2-5 structural elements around the subject (annotation lines, callouts, product row) that create hierarchy.
5. **Visual tone** — a control layer used AFTER 1-4, always translated (§8).
6. **Material / texture** — named surfaces and how they handle light (a primary realism lever).
7. **Typography / labeling** — plan the copy + hierarchy here, then route dense text to a deterministic layer (§11).
8. **Aspect ratio** — always close the prompt with an explicit ratio.

**Weak-prompt upgrade checklist** (turn any loose ask into a filled brief, in order): clarify image type -> define subject -> define composition -> add modules -> translate vague taste words -> add materials/labels/typography -> choose aspect ratio.

**Prompt-body discipline** (for any standalone creative):
- **Line 1 = canvas declaration:** ratio + WxH + "standalone image, edge-to-edge" + background color as a hex.
- **Describe regions in vertical order with explicit height budgets:** "Top (~12% height): ...", "Center: ...", "Bottom (~10% height): ...". Percentages force predictable layout.
- **Typography spelled out per block:** font feel + weight + size feel + color + alignment.
- **Close with an aesthetic gestalt sentence**, then the negative/exclusion line.

---

## 2. Canvas & spatial control

- **Vertical-region % budgeting** is the core layout lever — pre-allocate the canvas top-to-bottom by percentage. The model obeys layout far better when regions are named and sized.
- **84% safe zone:** all text, headlines, CTAs, wordmarks, and key focal subjects fit within the central 84% (~8% padding every edge). Backgrounds and dividers may bleed; text/focal elements may NOT. **If a tall subject doesn't fit, scale it DOWN — never crop a headline.**
- **Match the aspect ratio to the focal subject's proportions.** Tall content on a 1:1 canvas clips. Ratios in use: `1:1` (feed square), `4:5` (feed portrait, 1080x1350), `9:16` (Stories/Reels/vertical), `2:3` (tall product/board), `16:9` (landscape/board).
- **Reserve negative space for any text overlay.** Generous negative space also carries "premium/restrained."
- **Name reference roles by index:** "the product in image_ref[0]", "the lighting/mood from image_ref[1]". Improves placement and identity. (~5-ref cap.)
- **Depth / foreground-background separation:** request it, don't hope for it — "shallow depth of field on the background", "the product slightly overlaps the prop column, creating depth", "soft drop shadow".
- **Product hero sizing:** give the product an explicit frame fraction — "the product occupies roughly 45-55% of the frame, centered."
- **Deliberate off-kilter realism:** small rotations sell "hand-arranged" — "slightly rotated counter-clockwise about 5 degrees", "tilted ~3 degrees, hand-arranged feel."
- **Angle/height vocabulary:** eye-level, slightly-low upward, high-angle/top-down, low-angle, cross-section. Long lens (85mm+) compresses/flatters; wide/fisheye (12-18mm) exaggerates near objects and curves edges.

---

## 3. Lighting recipes (fill as: time-of-day + source direction + quality)

| Recipe phrasing | When to use |
|---|---|
| Three-point (key 45 deg + fill at 1/2 key + rim behind + eye/catchlight) | Default portrait/headshot; separates subject from background |
| Softbox key / soft diffused / "soft commercial studio lighting" | E-commerce even illumination, "no harsh glare" |
| Rim / backlight ("dramatic backlight, rim lighting highlighting edges") | Subject-background separation, hair-edge, premium product spotlight |
| Ring flash / ring light | Catchlights in eyes; high-key macro |
| Golden hour / warm side window light | Warm nostalgic lifestyle, "morning routine", film look |
| Harsh direct on-camera flash (blown highlights, strong falloff) | Candid/UGC realism |
| Bright fresh daylight / high-key | Clean commercial, crisp high contrast |
| Even diffuse overhead softbox | Flatlays, product-on-surface |
| Uneven ambient indoor, one side of face in shadow | UGC authenticity (deliberately imperfect) |
| Cinematic museum/plinth pool of light | Prestige/artifact product shots |

**Consistency principle (for edits/composites):** the environment light must match the subject's existing light — same direction, shadow quality, and color temperature, or the composite reads fake.

---

## 4. Photorealism levers (weight these heavier — GPT-Image renders smoother than reality)

**4a. Camera-hardware framing** — the strongest realism anchor is naming the capture device:
- UGC/candid: `Raw iPhone front-camera selfie video frame grab.` Add `iPhone front camera wide-angle lens distortion on the extended arm`.
- Editorial/product: name a body + lens + aperture — `Sony A7III / Canon EOS R5 / Hasselblad`, `85mm f/1.4` (portrait compression), `50mm f/1.8` (clean lookbook), `35mm f/2.8` (environmental), `macro 120mm f/4` (product detail).
- DOF rule: shallow (f/1.4-f/2.8) for portraits/hero; deep (f/5.6-f/11) for full-product-in-focus.
- Film/grade: `Kodak Portra 400` (warm, nostalgic, natural skin, subtle grain); "clean cinematic color grading with subtle warmth."

**4b. Imperfection block** (include 4-5 for UGC — defeats the "AI influencer" look):
`slight motion blur on hair strands` - `slightly overexposed highlights on forehead and nose` - `visible image grain and noise` - `wide-angle lens distortion on the extended arm` - `slightly off-center framing, tilted a few degrees` - `washed out flat color grading` - `soft focus, nothing tack sharp` - `uneven ambient indoor lighting` - `caught mid-blink or mid-word, not a perfect expression`.

**4c. Skin-realism block** (pick 3-4, place INLINE with the character description, not in the imperfection block):
`natural skin with visible pores` - `slight unevenness in skin tone` - `minor undereye shadows` - `a hint of shine on the nose and forehead from natural oils` - `slight pinkness on cheeks and nose` - `minor skin texture variation` - `the kind of skin you see on a real person's unfiltered front camera`.
- **Hard guardrail:** never use `acne, pimples, breakouts, blemishes, redness` or anything that reads as a skin condition. Goal is "real person, not retouched" — NOT "person with skin problems."

**4d. Texture cues the model specifically needs** (it renders smoother than reality — always append):
`visible skin texture, fine hair flyaways catching light, subtle pores` - `individual hair strands catching light` - `individual eyelashes visible`. When output looks flat/plasticky, regen with explicit texture clauses.

**4e. Material vocabulary for product surfaces** — name the material and its optical behavior: matte finish, glossy sheen, brushed-metal lid, wet-look gel, glass-bottle refraction, `satin foil reflectivity`, `subsurface scattering on skin`.

**4f. Identity / face preservation** (the model leans on text over the reference):
- State preservation in the FIRST sentence: `Keep the facial features of the person in the uploaded image exactly consistent.`
- Specify what CAN change (outfit, environment, pose, expression) while locking the face — otherwise it over-freezes or drifts.
- For a specific real person: `CRITICAL CHARACTER LIKENESS: the subject is the exact same person in the reference photos. Match the face exactly: [describe features]. Maintain the exact facial proportions, eye shape, and skin tone. Do not generalize.`

**4g. Anti-polish negative line** (append to any realism target):
`No retouching, no beauty filter, no studio lighting, not a professional photo, not overly polished, not perfectly composed, not tack sharp. No airbrushed skin, no flawless complexion.`

**4h. Commit sentence:** end UGC prompts with `This must look like an unedited frame pulled from a real iPhone selfie video, NOT a professional photo. Raw, unpolished, authentically amateur.`

---

## 5. Product & commercial staging

- **E-commerce isolation recipe:** pure white (RGB 255,255,255) or subtle gradient-gray background + **a soft realistic contact shadow directly beneath the product** (never skip — without it the product looks pasted-on) + soft commercial studio lighting + centered with spacing + "color-corrected, brand new, no scratches/dust."
- **Editorial/luxury:** product on dark water/surface with reflections and ripples, `droplets on product surface`, `chilled (visible condensation)`, golden-hour or dramatic backlight, shallow DOF, "sharp focus on product label", "8K, luxury advertising quality."
- **e-commerce vs editorial split:** e-comm = even light, no drama, centered, "clean lookbook aesthetic"; editorial = dramatic light, props/water/florals, rich saturation, mist/haze.
- **Packaging/label fidelity when attaching an official render:** `Preserve the product from image_ref[0] with extreme accuracy. Keep the label, wordmark, colors, and proportions perfectly intact. No new text, logos, or watermarks added.`

---

## 6. Edit / preservation grammar (attach an official render, don't let the model redraw it)

Every edit uses a **preserve list + a "don't touch" fence.**

Skeleton:
```
Use image_ref[0] as the base. Preserve everything about the product exactly:
label artwork, wordmark, colors, proportions, shape, and finish.
Only change: [the background / the scene / the lighting environment].
Do NOT change: the product, its label, its color, or its geometry.
No new text, no new logos, no watermarks, no extra product copies.
```

Reusable fences:
- `global_restrictions: no new characters, no clothing changes, no location-type changes, no text/logos/watermarks added.`
- Background swap keeping product identical: `Keep the product exactly as in image_ref[0]. Replace the background completely with [scene]. Do not relight the product. Clean precise cutout, no halos, product casts an appropriate contact shadow onto the new surface.`
- Clutter/hand removal: `Remove the hand/clutter, keep the product completely untouched, fill with realistic background that matches grain, focus depth, lighting, and color temperature. No smudges or clone-stamp marks.`

**Pair "keep the label intact" with "no new text/logos added"** on every product edit — so the model neither edits the label nor invents a badge or third-party mark.

---

## 7. JSON-for-complexity (structured JSON for multi-element scenes)

Use JSON when there are multiple subjects, detailed wardrobe/accessory specs, precise element placement, or specific camera/lighting rigs. Canonical top-level keys:
`subject` (with `face: {preserve_original: true}` or an `identity_preservation` block) - `photography` (`camera{model,sensor}`, `lens{focal_length,aperture,effect}`, `settings{shutter,iso,white_balance}`) - `lighting` (`key/fill/rim/eye_light`, each with `type,position,intensity,effect`) - `background` (`type,color(hex),gradient,vignette` or `setting,elements[],foreground_props[]`) - `rendering_requirements` (`skin,fabric,hair,eyes,overall`) - `composition` (`framing,gaze,depth_of_field,focus_point`) - `color_grading` - `negative` (`content,style`).
Best practice: keep identity rules at the top; exact hex colors; start simple and add one element at a time. For a coherent multi-card set, define 3-6 **Visual Anchors** (traits that stay constant), then vary only one variable per card while holding lighting + grade + technical specs constant.

---

## 8. Taste-word -> visual translation (never ship an untranslated taste word)

| Taste word | Concrete direction |
|---|---|
| premium / high-end | restrained layout, limited palette, clean type, premium materials, generous negative space |
| cinematic | low-angle framing, dramatic lighting, foreground/background depth, emotional tension, reflective surfaces |
| tech / modern | glass panels, metal textures, cool lighting, precision spacing |
| editorial / magazine | strong headline placement, clean grid, short support text, controlled palette |

---

## 9. Ad-specific rules

- **Hooks** (big legible type is the model's strength): "5 Reasons Why", "How it started / How it's going", "POV: your morning routine", "Ditch the [competitor category] for good."
- **Product-in-hand:** `natural grip with fingertips` avoids the classic AI unnatural-hand failure. If hands break: `anatomically correct hand, five fingers, no extra limbs`. Avoid `studio lighting, floating product, unnatural hand pose`.
- **UGC reference order (cap ~5):** `[character_hero, product, style_ref_1, style_ref_2, style_ref_3]` — character hero first (strongest identity signal), 3 style refs is the sweet spot.
- **CTA styling (trademark-safe):** a plain colored bar/pill, full-width, plain sans-serif text left-aligned, a simple `>` arrow. This is the safe pattern for "Available at [Retailer]" as **plain text** — no third-party logo, no imitation of a brand's trade dress. (See §12.)

---

## 10. Reusable formulas (compose fast)

- **F1 UGC selfie:** `[camera hardware] + [framing] + [character desc w/ inline skin cues] + [action with product] + [expression] + [outfit] + [setting] + [imperfection block] + [anti-polish negatives]`.
- **F2 Person + product still:** `[person] + [interaction verb] + [product] + setting + camera + lighting + "clearly visible, in-focus, natural grip" + style + avoid-list`.
- **F3 Fresh-prompt anchors:** subject/pose - lighting + time of day - lens/framing - palette/mood - composition (thirds/leading lines) - negative space for text - reference roles by index - standalone-creative scope.
- **F4 Canvas-region:** canvas declaration -> top region (% + content + type) -> middle -> bottom (CTA/wordmark) -> gestalt sentence -> exclusion line.
- **F5 Character-identity anchor block:** see §4f.

---

## 11. Safety suffixes — hard-append to production prompts

Three always-on guards that fix recurring rendering failures. Append the relevant ones to any production prompt:

**NO-CHROME** (keeps the render a clean standalone image, not a fake screenshot):
```
Render only the standalone image itself, not a screenshot of how it displays in-feed.
Exclude device chrome, platform brand-row (avatar/handle/Sponsored), caption text, link-card
footer, like/comment/share counts and buttons, nav/tab bars, and Story chrome. Just the image.
```
**SAFE-ZONE:**
```
All text, headlines, CTAs, wordmarks, and key focal subjects must fit within the central 84% of
the canvas (about 8% padding from every edge). Backgrounds and dividers may bleed; text and focal
elements may not touch or extend off any edge. If a tall subject does not fit, scale it DOWN; never
crop a headline or cut off the top/bottom of a product.
```
**TEXT-FIDELITY:**
```
Inside any body-text block, plain words only: no emoji, no unicode glyphs, no special characters
mid-sentence. Render the exact count of elements specified; do not invent extra lines or items.
```

> These reduce failure but do NOT make dense text reliable. Dense copy, claims, prices, and logos still go to a deterministic text layer, not the model.

---

## 12. Firewall (three patterns to keep OUT of the model)

The source skills freely do three things worth firewalling for commercial work. Take the *method*, firewall the *behavior*:

1. **Trademarks / trade dress you do not own — do not model-render.** Sources render publication/retailer wordmarks, "AS SEEN ON" logo rows, fake-search marks, mastheads, and storefront signage as credibility props. Reference an outside brand as **plain text in your own typography** ("Available at [Retailer]") — never a rendered mark or a background engineered to imitate its trade dress. Your OWN wordmark as flat text on your own packaging is fine.
2. **Fabricated store / shelf / OOH-placement scenes.** Sources stage storefronts, shelves, wayfinding, subway/billboard placements. If authenticity matters, an AI-rendered store scene is a credibility killer (and risks rendering other brands' signage in the background). Keep proposal-board mechanics (label specs, icon sets, color system) but strip the store-space perspective, signage, and floor-stickers.
3. **Dense text / UI / tables baked into the image.** Sources rely on the model to render dense labels, threads, tables, receipts, calendars. That garbles (a model limit, §0). Mine those templates for **layout and art direction only**; render the dense text/tables/logos in a deterministic layer over a model-generated plate. Model-rendered text is OK only for a single large headline/wordmark.
4. **Tabloid / surveillance / fake-news realism cues — off-brand for commercial work.** Harvest only the clean-realism subset (`candid photo, flash photography, imperfect framing, motion blur, street photography`). Drop `paparazzi, surveillance still, tabloid, fake-news, cursed image`.

---

## 13. Starter template catalog (copy-ready, ASCII-clean)

Fill the `[BRACKETS]`, attach a clean product render as `image_ref[0]`, and keep the label-preservation fence from §6. These favor the model's strengths (big type, clean hero) or compensate for its weaknesses (heavy texture cues on flatlay/lifestyle).

**T-Hero — bold typography hero (native model strength):**
```
1:1 static image, 1080x1080, edge-to-edge, standalone. Background: deep brand color with a subtle
darker radial vignette. Top 60 percent: a huge bold condensed sans-serif statement in cream
off-white, stacked on three uppercase lines, left-aligned with a consistent 10 percent left margin:
"[LINE ONE]" / "[LINE TWO]" / "[LINE THREE]." Tight letter-spacing and line-height. Bottom-right
(about 28 percent of canvas, inside the safe zone): a clean editorial photo of the product from
image_ref[0], slightly tilted, faint soft drop shadow, colors and wordmark preserved exactly.
Lower-left, cream sans-serif three short lines: "[BENEFIT ONE]" / "[BENEFIT TWO]" / "Available at
[Retailer]." Brutalist-meets-premium typography; the type makes the point, the product punctuates it.
No third-party logos, no store imagery, no platform chrome.
```

**T-Flatlay — daily-kit flatlay (compensate with texture cues):**
```
Top-down 1:1 flatlay product photograph, 1080x1080, deep matte surface, edge-to-edge, subtle texture.
Centerpiece: the product from image_ref[0], wordmark preserved exactly. Surrounding everyday-carry
items with negative space between them: [ITEM 1] (top-left), [ITEM 2] (top-right), [ITEM 3] (right),
[ITEM 4] (bottom-right), [ITEM 5] (bottom-left), [ITEM 6] (left). Thin white hairline annotation lines
extend to small white sans-serif labels near the edges but inside the safe zone: [ITEM 1] "[LABEL]",
... . Soft cinematic top-down light from upper-left, gentle shadows under each object, visible material
texture on leather and metal, subtle sheen on the product, light image grain. Premium editorial
aesthetic. No third-party logos, no store imagery.
```

**T-BeforeAfter — two-panel split (native strength: clean type + contrast):**
```
1:1 static image, 1080x1080, edge-to-edge, split down the center by a 2px white vertical divider.
LEFT half "[BEFORE LABEL]": muted grey-beige background, bold black uppercase sans-serif title at top,
below it a photo of [BEFORE STATE], dull dim light. RIGHT half "[AFTER LABEL]": warm bright cream
background, same title font, [AFTER STATE with the product from image_ref[0] in the lower corner,
wordmark preserved]. Identical camera angle and identical title placement on both halves so the eye
reads the contrast. Natural skin with visible pores where a person appears. No logos overlay, no store
imagery, no platform chrome.
```

**T-UGC — candid selfie realism (load imperfection + skin blocks):**
```
Raw iPhone front-camera selfie video frame grab, 4:5 vertical, 1080x1350. A [age/description] person,
front-facing selfie angle slightly above eye level, holding up the product from image_ref[0] with a
natural grip with fingertips, product clearly visible and in focus with wordmark preserved, giving a
genuine relaxed half-smile mid-word. Setting: a real [ROOM] in warm morning window light, one side of
the face slightly in shadow. Natural skin with visible pores, a hint of shine on the nose and forehead,
minor undereye shadows. Slight motion blur on hair strands, slightly overexposed highlights on the
forehead, visible image grain, wide-angle lens distortion on the extended arm, slightly off-center
tilted framing, washed-out flat color grading, soft focus. This must look like an unedited frame from a
real iPhone selfie video, not a professional photo: raw, unpolished, authentically amateur. No
retouching, no beauty filter, no studio lighting, no airbrushed skin. No text, no logos, no store imagery.
```

**T-Annotated — feature callouts on a clean hero (native strength):**
```
1:1 static image, 1080x1080, edge-to-edge, soft warm off-white background. Top (about 12 percent
height): a row of five small black stars and one italic dark-serif quote line in quotes (max 80 chars).
Center: a clean editorial hero of the product from image_ref[0], upright and slightly tilted, soft
shadow beneath, product about 50 percent of the frame, label and wordmark preserved exactly. Four to
five thin black hand-drawn arrow lines curve outward from the product to feature labels in the white
space, clean black sans-serif: "[FEATURE 1]", "[FEATURE 2]", "[FEATURE 3]", "[FEATURE 4]", "[FEATURE 5]".
Bottom (about 10 percent height): the brand wordmark centered. Editorial product photography, soft
daylight, neutral premium palette. No third-party logos, no store imagery.
```

**T-StillLife — editorial flat-lay spread (compensate with texture cues):**
```
4:5 editorial still-life, 1080x1350, top-down composition on a warm concrete surface. Arranged objects
with negative space between them: the product from image_ref[0] (label and wordmark preserved), plus
[PROP 1], [PROP 2], [PROP 3], [PROP 4]. Each object has a fine thin annotation line to a short label
describing its use or benefit. Clean thin sans-serif body with one serif headline. Restrained palette of
brand neutrals plus one accent. Even diffuse overhead softbox light, gentle contact shadows, visible
material texture on fabric and metal, light grain. Feels like a magazine feature spread. No store imagery,
no third-party logos.
```

---

## 14. One-line operating summary

Decide the **format first**, build the **8-slot brief**, budget the canvas by **vertical % inside the 84% safe zone**, and — because GPT-Image renders *smoother than reality* — load the **imperfection + skin + texture blocks** heavier for anything photoreal, **restate the full description over the reference** for identity, keep the **label-preservation fence** on every attached product render, append the **three safety suffixes**, and **firewall** every third-party trademark, fabricated store scene, and dense-text block out to plain text or a deterministic layer.
