# Look Packages — camera, lens, and film stock as *visible outcomes* (the look layer)

**v1.0.** Read this alongside `prompt-craft.md` §4a (camera-hardware framing) and `realism-formula.md` §4 (the distance ladder) before any production prompt that has to carry a *look*: a hero, a carousel plate, a lifestyle still, a night scene, a product demonstration. `realism-formula.md` is the physics of skin and hair; this file is the **optics and the tonal curve** — what the lens, the sensor, and the stock would have done to the frame, written so the engine can build it.

> **Authoring rule (unchanged):** every copy-ready line below is ASCII-only (straight quotes, hyphens, no bullets or accents) so it pastes cleanly through any stdin encoding. Keep it that way when you copy one out.

**Source:** adapted from Promptwise's publicly shared *Field Guide 01 — 5 Camera & Lens Setups for AI Video* (a lead magnet) on camera and lens setups for AI *video* prompting (five named setups, each paired with the visible result it produces and a fix for when it fails; attributed, its text not reproduced). Everything about camera *movement* belongs to video and is left out (§7). What transfers to stills is the look system and four practice rules, validated on Codex `$imagegen` in §6.

---

## 0. The idea in one line, and why it matters here

The guide's premise: a camera name gives the model a cue, but the prompt must *also* state the result you want to see. Every setup in it pairs the gear with the **visible consequence** (fine grain, gentle highlights, oval background lights, a sharply focused face) and, in its practice pages, with the **physical cause** (small lamps far behind the subject; which side of the face the window lights). That is exactly the principle the realism layer already runs on for skin ("say what the light DOES"), applied one level up to optics and tone. `prompt-craft.md` §4a used to list camera bodies and lenses as bare names; this file replaces that with packages that carry the result and the cause.

The guide also warns that these are creative directions, not simulations of real equipment, and that different models interpret the same wording differently. True of this engine too — a package is a strong prior, not a parameter. Judge the output, not the wording.

---

## 1. The rule — NAME + RESULT + CAUSE, never the name alone

Every look line in a production prompt has three parts:

1. **NAME** — camera + lens (+ stock): loads the prior. `ARRICAM LT with a Cooke S4/i 50mm lens, Kodak VISION3 500T film look`.
2. **RESULT** — two to four things the viewer can *see*: `fine organic grain, a gradual roll-off into the highlights, texture that stays visible in skin and fabric weave`.
3. **CAUSE** — the physical arrangement that produces the result: `soft side light from the window on the left: the left cheek lit, the right side falling into open shadow with gentle shadow edges`.

A bare name (`shot on ARRI`) is a taste word in a costume; a result without a cause (`beautiful bokeh`) is a wish. Write all three and the engine has something to build.

---

## 2. The five packages (copy-ready, ASCII)

Each package: when to use it, the ladder rung it serves, what to ask for, one copy-ready stills line, and the fix the guide gives when it fails.

### L1 — THE FILM LOOK · ARRICAM LT + Cooke S4/i 50mm · Kodak VISION3 500T (daylight-corrected)

**Use for:** tactile portraits, lived-in interiors, any frame where skin, fabric, and surfaces should feel touchable: window-lit hero plates, founder stills, bedroom and bathroom scenes. **Rung:** R2 (also R1 with the raking light from `realism-formula.md` §3).

**Ask for:** fine organic grain · gradual transitions into bright highlights · texture that stays visible in skin and materials.

```
Photorealistic. ARRICAM LT with a Cooke S4/i 50mm lens, Kodak VISION3 500T film look,
daylight-corrected color: fine organic grain, a gradual roll-off into the bright window
highlights, texture that stays visible in the skin and in the fabric weave of the [GARMENT].
Soft side light from the window on the [LEFT/RIGHT] shapes the face: the near cheek lit, the far
side of the face falling into open shadow with gentle shadow edges.
```

**Why it works:** side light gives pores and weave something to show; the film shoulder keeps the window from clipping. **Grain adds texture to the image; it does not repair a smooth, poorly lit face** — if the skin is flat, fix the light angle or the skin inventory, not the grain.
**If everything looks blurry:** replace any "soft image" wording with `sharp eyes, gentle highlight roll-off and fine grain`. Soft highlights never require an out-of-focus subject (§3b).
**Stock note:** 500T is tungsten-balanced. State `daylight-corrected color` for a neutral daylight read; warmth is a creative choice you write (`a faint warm cast`), never an automatic film effect. Because the package already says `fine organic grain`, **drop the separate grain sentence** from the realism block — grain is said once (`realism-formula.md` §1 clause 9).

### L2 — CLEAN, NATURAL DETAIL · Sony VENICE 2 + ZEISS Supreme Prime 50mm T2.8

**Use for:** contemporary portraits, **products and product-in-hand**, interiors — clear detail without an aggressively sharpened image. In-hand plates, e-commerce lifestyle, group heroes, any frame where the label must read. **Rung:** R2-R3.

**Ask for:** natural skin tones · readable surface detail · a gentle transition from the focused subject into the background.

```
Photorealistic. Sony VENICE 2 with a ZEISS Supreme Prime 50mm lens at T2.8: natural skin tones,
readable surface detail, a gentle transition from the focused subject into the background, clean
digital rendering with natural edge detail and no digital over-sharpening. The surfaces that
matter: [SURFACE 1: the skin with its pores], [SURFACE 2: the matte-black bottle with its
low-sheen plastic and crisp printed label], [SURFACE 3: the glazed ceramic of the sink].
Soft daylight from the window on the [LEFT/RIGHT] with a gentle fill, restrained contrast.
```

**Name the surfaces that matter — two or three.** `skin, the matte-black container, the brushed-metal lid` is more specific than "hyper-detailed everything", and it tells the engine where to spend its resolution. For a product shot the product surface is always one of the three.
**If the result looks clinical:** add `natural edge detail, subtle skin variation and soft side light` — keep the useful detail while killing the exaggerated local contrast.

### L3 — ANAMORPHIC CHARACTER · RED V-RAPTOR + Laowa Proteus 45mm 2x anamorphic (blue flare)

**Use for:** night streets, lit interiors, and any scene with bright **practical** lights that belong in it — a lamp, a car's tail lights, apartment windows, a barber station's bulbs, a venue queue. **Rung:** R2-R4. If your pipeline has capture modes (window / flash / macro), this is a fourth, `night`.

**Ask for:** horizontal flare linked to a light source in frame · vertically oval background highlights · natural facial proportions (correctly desqueezed).

```
Photorealistic. RED V-RAPTOR with a Laowa Proteus 45mm 2x anamorphic lens, blue-flare version,
Super 35 sensor crop, correctly desqueezed with natural facial proportions. The [PRACTICAL: tungsten
streetlamp / warm lamp] near the [LEFT/RIGHT] frame edge throws one brief thin horizontal blue
flare across the [upper left] of the frame; the [DISTANT LIGHTS: apartment windows and tail
lights far down the block], well outside the focus plane, render as vertically oval bokeh. Soft
warm practical light from [SOURCE beside the subject] keeps the face clearly readable: the near
cheek lit, the far side of the face in open shadow with gentle shadow edges.
```

**Give the flare a reason to exist:** a bright practical near the frame edge; keep the streak brief and thin so the face stays readable. **If the oval bokeh is missing:** add small, distant lights outside the focus plane — `anamorphic` alone does not tell the engine *where* the lens character should appear.
**Firewall:** no readable lettering, no signage, no bar or shop names, no third-party marks (Hard Rule 0 and the no-fabricated-placement rule). Write the positive state: `no readable lettering or signage anywhere` in the scene sentence *and* in the Avoid line.

### L4 — PORTRAIT SEPARATION · RED V-RAPTOR + Laowa Argus spherical, wide aperture

**Use for:** close portraits where the **eyes** carry the scene and the background becomes soft pools of light: hero-card anchors, the finished / payoff plate, founder close-ups. **Rung:** R2.

**Ask for:** precisely focused eyes · shallow depth of field · predominantly rounded highlights near the center of the image.

```
Photorealistic. RED V-RAPTOR with a Laowa Argus spherical lens look, wide aperture and shallow
depth of field. The eyes remain precisely focused. Small warm lamps several meters behind the
subject become large, soft, predominantly rounded highlights near the center of the frame. Gentle
side light preserves skin texture.
```

**Create distance, not just blur:** place the person close to the camera and the lights well behind them, and *say so* — tell the engine how the scene is arranged, not only that the background is blurry. **If the face or the hands lose focus:** choose the priority. Portrait = eyes sharp. **Product demonstration = more depth of field so the face and the product both stay readable** (§3c) — the rule in-hand plates usually miss.

### L5 — NATURAL DEPTH · ARRI ALEXA Mini LF + ARRI Signature Prime 47mm T2.8

**Use for:** environmental portraits — the person matters but the room, court, street, or loft still tells part of the story. R4 lifestyle frames and every "real setting" (a wall, a court, a loft, a skatepark, a barbershop). **Rung:** R3-R4.

**Ask for:** natural fine detail · smooth tonal transitions · soft separation that leaves the surrounding space recognizable.

```
Photorealistic. ARRI ALEXA Mini LF with an ARRI Signature Prime 47mm lens at T2.8: natural fine
detail, smooth tonal transitions, soft separation that leaves the surrounding space recognizable.
Keep some of the world in the shot: [THE DOORWAY / WINDOW / CORRIDOR / COURT LINES] behind the
subject remain recognizable but softly separated. Moderate depth of field; the background does not
disappear. The eyes are the sharpest point in the frame.
```

**Keep some of the world in the shot:** a doorway, a window, or a corridor gives the portrait depth; the background does not have to vanish for the subject to stand out. **If the background turns to mush:** `Moderate depth of field; the background remains recognizable but softly separated.` This replaces the habitual `softly blurred background` whenever the setting is part of the message.

### Phone package (unchanged, for completeness)

R3 selfie and flash plates keep the phone anchor from `realism-formula.md` §4 (`Raw phone front-camera selfie video frame grab`, phone-sensor grain, wide-angle arm distortion). It is already a NAME + RESULT + CAUSE package. What §3b changes for it: **the eyes are still the sharpest point** — a phone locks focus on a face; the softness lives in the moving hand and the hair edges, not in the eyes.

---

## 3. Practice rules (the generalizable craft)

### 3a. Describe the CAUSE, not the effect

| Instead of (effect word) | Write (visible condition the engine can build) |
|---|---|
| beautiful bokeh | `small lamps several meters behind the subject, well outside the focus plane` |
| dramatic light | `the window on the left lights the near cheek; the far side of the face falls into open shadow` |
| subject separation | `the subject close to the camera, the background several meters back` (distance, then aperture) |
| lens flare | `a bright practical near the left frame edge` (the flare needs a source) |
| moody / cinematic | the lighting side + the shadow quality + one practical in frame (`prompt-craft.md` §8 table) |
| crisp / sharp | `the eyes are the sharpest point in the frame; all sharpness is optical, no digital sharpening` |

A specific source, distance, or focus target is more useful than another adjective.

### 3b. Separate the THREE kinds of softness

- **Soft light** = gentle shadow edges (a large or diffused source).
- **Soft background** = defocus (distance + aperture).
- **Soft highlight roll-off** = a gradual transition into the bright areas (the film shoulder; `realism-formula.md` clause 12).

**None of them requires blurry eyes.** The old UGC wording `soft focus, nothing tack sharp` conflated all three and invited a blurry face. Copy-ready replacement (any rung):
```
Three kinds of softness kept apart: soft light means gentle shadow edges, a soft background means
defocus, soft highlight roll-off means a gradual transition into the bright [WINDOW / FLASH
HOTSPOT]; none of them softens the eyes. The eyes are the sharpest point in the frame.
```
At R3 (phone): `The eyes are the sharpest point in the frame, as a phone front camera locks focus on a face; slight motion softness only on the hair edges and the raised hand; a gentle highlight roll-off where the light hits the forehead, bright but not clipped.`

### 3c. Choose the FOCUS TARGET, every prompt

Name what must stay sharp. The engine distributes sharpness; if you do not assign it, it chooses.
- **Portrait / anchor / finished:** `the eyes are the sharpest point in the frame`.
- **Product demonstration / in-hand / action:** `Moderate depth of field chosen for a product demonstration: the face and the product label both stay readable; the label is the sharpest point in the frame and the eyes a close second; only the far wall softens.`
- **Macro / texture beat:** `critical sharpness on [the part line / the curl clumps / the wordmark]` (`realism-formula.md` §3).
- **Environmental:** eyes sharp, background `recognizable but softly separated` (L5).

### 3d. Assign each reference a JOB — and say what NOT to take from it

The guide: use one reference for identity and another for the setting and light, say so explicitly, and do not accidentally import a character sheet's background or pose. `prompt-craft.md` §2 names roles by index; this adds the **exclusion**. Copy-ready:
```
Image 1 = identity only: this exact face, hair and skin tone; do not take its background, pose,
clothing or lighting. Image 2 = the product, preserve exactly (label, wordmark, colors,
proportions intact; no new text, logos or watermarks). Image 3 = light and setting only; do not
import its people, pose or products.
```
Pairs with the preservation fence (`prompt-craft.md` §6) and the identity anchor (§4f).

### 3e. Fix ONE thing at a time; compare on the same scene; judge a phrase on more than one result

If the skin looks flat, adjust the light or the skin description (not the grain, not the camera name). If the bokeh is missing, adjust focus and background distance. When comparing packages, hold the subject, framing, size, and everything else constant (`realism-formula.md` §12 / §15 protocol), and try more than one result before judging a phrase — one favorable pick is not evidence.

### 3f. Write FOR THE MODEL: positive wording

The guide's example for video is `locked camera` rather than `no camera movement`; for blocked-up shadows, `deep charcoal shadows retain subtle texture`. That is this skill's positive-state rule (`realism-formula.md` §8): every constraint exists in the body as a desired physical state, the Avoid line only echoes it. Two positive forms now in use:
- `Deep charcoal shadows retain subtle texture: shadow detail preserved inside every pore and [between the curls / under the hand / in the black leather].` (the positive form of "lifted blacks / no crushed shadows")
- `The eyes are the sharpest point in the frame; all sharpness is optical.` (the positive form of "no blur / no digital sharpening")

### 3g. State the white balance; never let the stock imply it

`daylight-corrected color`, `neutral white balance`, or `a faint warm cast by choice`. A stock name (Portra, 500T) carries a temperature prior the engine may or may not apply; the realism layer's tone clause (`realism-formula.md` §7b) already says neutral white balance so the complexion holds — keep the two consistent.

---

## 4. Symptom -> lever (troubleshooting, merged with the realism tell-list)

| What you see | Which lever (and only that one) |
|---|---|
| Blurry face / soft eyes | §3b: replace any "soft image / soft focus / not tack sharp" with sharp eyes + gentle highlight roll-off + fine grain |
| Clinical, over-crisp, etched edges | L2 fix: `natural edge detail, subtle skin variation and soft side light`; confirm `no digital over-sharpening` |
| Background is mush; setting unreadable | L5: `moderate depth of field; the background remains recognizable but softly separated`; name the doorway / window / court lines |
| No bokeh / no separation | §3a + L4: put small distant lights outside the focus plane; state subject-close, lights-far |
| Flat, waxy skin | Light angle or skin inventory (`realism-formula.md` §3-4), never more grain, never a camera name |
| Product label soft in an in-hand shot | §3c: product-demo focus rule, label the sharpest point, moderate DoF |
| Flare with no source / random streaks | L3: one practical near the frame edge; keep the streak brief; or remove the anamorphic package |
| Round bokeh in a night scene that should be anamorphic | Add distant small lights outside the focus plane; say `vertically oval bokeh`; say where they sit |
| Frame too warm / orange | §3g: `daylight-corrected color, neutral white balance`; warmth only by explicit choice |
| Crushed black shadows | §3f positive form: `deep charcoal shadows retain subtle texture` |
| Grain as colored speckle | Grain said twice (package + realism block) or "film" at phone distance: say it once; at R3 say phone-sensor noise |

---

## 5. Integration map

- **Distance ladder (`realism-formula.md` §4):** R1 -> L1 with the raking light (or the 100mm macro anchor); R2 -> L1 (film, window plates) or L4 (separation, hero cards) or L2 (clean, whenever the label is in frame); R3 -> the phone package (or L2 for a waist-up product demo); R4 -> L5.
- **Capture modes, if your pipeline has them:** `window` -> L1 (anchor, finished) / L2 (in-hand); `flash` -> phone package (unchanged); `macro` -> L1 at R1 with raking light; **`night` (new) -> L3**. An in-hand builder should carry the product-demo focus rule (§3c).
- **Shot intents (`shot-intents.md` §2):** look aliases `/film`, `/clean`, `/anamorphic` (`/night`), `/separation`, `/depth` select a package; they are modifiers like `/golden_hour`, combined with a shot intent. `/nightlife` now expands through L3.
- **Templates (`prompt-craft.md` §13):** T-UGC loses `soft focus`; product scenes take L2 with the named surfaces.
- **Not changed:** the Realism Block inventory, the Hair Realism Block, the preservation fence, the safety suffixes, Hard Rule 0, the no-fabricated-placement rule, the text-layer rule.

---

## 6. Validation on Codex `$imagegen` (five A/B pairs)

Five A/B pairs, same subject, framing, size, and realism scaffolding; **A = the previous wording (`prompt-craft.md` §4 / `realism-formula.md`), B = A with the package + practice rules substituted and nothing else changed**. Two waves of five concurrent jobs, about four and a half minutes, every canvas exactly as asked (1080x1080 for the square asks, 1080x1350 for the 4:5 selfie), manifests recording prompt, size, bytes and SHA-256.

| Pair | Shot | A (previous) | B (this file) | Result |
|---|---|---|---|---|
| 01 | R2 window-lit close portrait in a bedroom (curly hair, suede jacket over a charcoal tee) | window-light realism block + shallow DoF + "softly blurred" | L1 film look + three-softness + "recognizable but softly separated" | **B wins clearly.** A: clean, even, slightly digital; flat window light; skin smooth. B: a film tonal curve (the window rolls off instead of clipping), visible organic grain, the suede nap and the tee weave readable, pores and freckles on the lit cheek, the far side of the face in open shadow with detail, eyes razor sharp; the shelf, posters and plant still readable behind him. |
| 02 | R3 in-hand product demonstration, a real matte-black pump-bottle render attached (sandy crop, cream hoodie, bathroom) | window-light block + shallow DoF on the eyes | L2 clean detail + named surfaces + product-demo focus rule | **B wins.** A: bright and over-clean, the window blown, hair a smooth mass. B: natural skin tones with freckles and pores, strand-separated hair, the bottle label crisp and the face readable at once, the towel and shower glass recognizable but separated, a more natural grip. The front label text was legible in both arms; the render's vertical side wordmark came back as a partial stroke in both, which is the known fidelity ceiling (`product-hero-from-renders.md`), not a package effect. |
| 03 | R3 phone selfie, bathroom window light | the UGC wording incl. `soft focus, nothing tack sharp` | three-softness rewrite only (nothing else changed) | **B wins.** A: the whole face slightly hazy, eyes soft, the frame reads "filtered". B: eyes and brows crisp as a phone focus lock would make them, the forehead hotspot bright but rolled off, sensor grain visible, the shower curtain, window, plant and sink all there; still unmistakably a phone frame. Confirms the guide: soft highlights never required a blurry subject. |
| 04 | Night street with practicals (two-block cut, leather moto jacket) | "practical-light recipe" prose | L3 anamorphic (flare with a source, oval bokeh at distance) | **B wins.** A: a good generic night portrait: warm lamp, round bokeh, but a glossy, slightly plastic skin sheen. B: the streetlamp carries one thin horizontal blue flare at the top-left, the tail lights and windows stretch into vertically oval pools, a blue-black sky against the warm window fill, pores and a controlled sheen on the face. The lens character appeared because the prompt said where it should: a practical near the edge, lights outside the focus plane. |
| 05 | R4 outdoor court, environmental (skin fade + curls, plain jersey) | `35mm f/2.8, environmental` + "softly blurred" | L5 natural depth + "keep some of the world in the shot" | **B wins narrowly.** Both arms kept the court legible: on this engine the R4 default was never mush. A: warmer golden rim light, the building behind him softer. B: the court lines, the fence and the open doorway all recognizable with smooth tonal transitions, the subject still separated; a cleaner look, slightly less golden. B meets the brief more fully; A's light is as good. One watch item: B put a cross pendant on an unspecified chain, so write `a plain silver chain, no pendant` when jewelry is unspecified. |

**Score: 5/5 pairs to B** (three clearly, one clear, one narrow). What the batch changed in this skill: `prompt-craft.md` §2/§3/§4a/§4b/§4g/§13/§14 and `realism-formula.md` §4/§6/§8/§10/§11/§14 carry the rules above; grain is said once per prompt (a package that carries grain replaces the realism block's grain sentence).

---

## 7. Not adopted (and where it goes instead)

- **Camera movement** (shoulder-mounted handheld, "restrained handheld breathing", the camera responding to an action, late focus pulls): video-only. If you also prompt video models, the guide's rule there is also positive wording: `locked camera` rather than `no camera movement`, and a still shot can be the right choice.
- **Any third-party prompting tool:** not adopted; this skill stays on the subscription-only Codex bridge (Hard Rule 1).
- **Image-to-video "let the starting image do its job"** (describe only what changes): the stills analogue is already the edit grammar (`prompt-craft.md` §6) — edits name the change and fence the rest.
