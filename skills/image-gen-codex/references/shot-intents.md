# Shot intents — shorthand aliases that expand into full briefs (never model commands)

**What this is.** A shorthand layer for the user: they can type `/macro`, `/floating`, `/flatlay`, `/candid` plus a product or subject, and the agent expands the intent into a full 8-slot brief (`prompt-craft.md` §1) with the right template, the realism blocks (`realism-formula.md`), the preservation fence, the safety suffixes, and the firewall already applied. The alias selects the template; it never replaces the brief.

**What this is not.** Neither ChatGPT nor Codex has image "slash commands". A word like `/floating` typed into ChatGPT is plain text that the model reads as a one-word style hint; inside Codex, `/` commands are CLI features (`/model`, `/status`, ...), not image directives, and this bridge embeds the prompt inside its own task text and pipes it on stdin, so a leading slash is never parsed as a command. Validity verdict and the evidence batch are in §5.

**Provenance.** Adopted 2026-09-03 from a public "100 ChatGPT slash hacks for product images" lead-magnet document (no author of record, no OpenAI affiliation; it sells a course). The only thing worth keeping from it is the *idea* of short intent names for common shot types, which is how a creative director already talks. Every mapping below points at a template this skill already owns; the document's own descriptions were not imported.

> Copy-ready blocks are kept ASCII-only for portability; this bridge sends UTF-8.

---

## 1. How the agent expands an intent

`/<intent> <subject or product> [modifiers]` -> the agent:
1. Looks the intent up in §2-§4. Blocked intents stop with the reason. Gated intents apply their condition first.
2. Picks the template it maps to (`prompt-craft.md` §13 catalog, or the realism blocks) and fills the 8-slot brief: type -> subject -> composition -> modules -> tone -> material -> typography -> aspect ratio.
3. Applies the standing rules: label-preservation fence on any attached render (`prompt-craft` §6), the three safety suffixes (§11), Hard Rule 0 (no third-party marks, plain text only), no fabricated store / shelf / OOH scenes, dense text to a deterministic text layer, the Realism Block at the right distance rung when skin or hair is in frame.
4. Writes the prompt to `<allowed-subdir>/<job>/prompts/<name>.txt` and runs the bridge with the product render attached as `image_ref[0]`.
5. Inspects against `prompt-craft` §10 / `realism-formula` §11 before delivering.

Modifiers the user may add and how they map: `4:5` / `9:16` / `1:1` -> aspect and placement-native master size; `dark` / `light` -> backdrop family; `hand` -> product-in-hand (`realism-formula` §6, R1); `face` -> R2 with the Realism Block; `phone` -> R3 UGC block; a retailer or marketplace name -> a plain-text availability line only, never a mark.

---

## 2. Accepted intents (map directly to something this skill already does well)

| Intent | Maps to | Expansion notes |
|---|---|---|
| `/producthero`, `/hero_product`, `/luxury` | T-Hero (`prompt-craft` §13) | Product 45-55 percent of frame, softbox key + rim, contact shadow, premium backdrop family from your brand system; "luxury" = the same hero with a darker backdrop and a tighter palette, not gold props |
| `/floating`, `/levitating` | T-Hero + levitation module | Product hovers one hand-height above the surface, level, with a soft diffuse drop shadow beneath (larger and softer than a contact shadow); optional suspended droplets at mixed depths; whole product sharp (f/5.6). Worked example §6 |
| `/macro`, `/productcloseup`, `/material`, `/asmr_shot` | `realism-formula` §6 product-surface block at R1 | Raking side-top light, label print grain, satin sheen rolloff, real contact shadow, critical sharpness on the wordmark; brand-new surface. Worked example §6 |
| `/flat_lay`, `/kit_layflat`, `/bundle_shot` | T-Flatlay | Top-down, even overhead softbox, grid or radial arrangement, only real companion products (attach each render), no invented accessories |
| `/lifestyle`, `/morningroutine`, `/workspace`, `/travel`, `/dayinmylife` | T-Hero in an environment, R4 | Golden-hour or window light recipe, product in use or at rest in a believable scene, environment clutter carries realism; person present -> R2/R3 blocks |
| `/candid`, `/ugc_ad`, `/pov_ad` | T-UGC, R3 | Raw phone front-camera frame, imperfection block, R3 skin block, Hair Realism Block if hair shows; `pov_ad` = first-person hands holding the product, phone lens distortion |
| `/aspirational`, `/streetstyle`, `/nightlife` | T-Hero in an environment, R3/R4 | Aspirational = elevated environment without status props that imply claims; nightlife = practical-light recipe, tungsten and neon spill, no bar signage or third-party marks |
| `/scrollstopper`, `/adcreative`, `/social_ad`, `/conversion_ad`, `/product_drop`, `/productlaunch`, `/viral_ad` | T-Hero plate + deterministic text layer | The model renders the plate only; any headline, price, or CTA goes to the text layer; "viral" and "conversion" are not visual instructions, so the agent asks for the one concept before expanding |
| `/problem_solution` | Two-plate concept | Two clean plates (problem state, product state) composed deterministically side by side; never a results claim; no before/after skin or hair transformation implied as fact |
| `/reelcover` | 9:16 plate + text-layer headline | 1080x1920 master, subject in the central safe zone, headline typography deterministic |
| `/unboxing` | T-StillLife with the real packaging | Only the real box or sleeve (attach its render); hands per R1 product-in-hand |
| `/splash`, `/smoke` | T-Hero + effect module | Water splash or smoke as a physical element with a light source; product fence stays; effect never covers the label |
| `/orbit`, `/gravity` | T-Hero + suspended-elements module | Real companion objects only (ingredient sprigs, water, the product's own components), all with consistent light direction and shadows |
| `/museum` | T-StillLife, cinematic plinth pool of light | Plinth, single pool of light, dark environment; no invented placards or third-party marks |
| `/scale_indicator` | T-StillLife with a universal reference object | A hand or an everyday object (pen, key) for true relative size |
| `/minimalist`, `/darksome`, `/golden_hour`, `/botanical`, `/mirror_reflection`, `/prism`, `/vibe_check` | Lighting / backdrop recipes (`prompt-craft` §3) | These are lighting and backdrop choices, not shot types; combine with a shot intent above |
| `/giant`, `/miniature` | T-Hero, scale concept | Concept lane only; product fence stays; environment must be obviously staged, never a store or a street with real signage |
| `/loop_visual` | Still only | For a still it is a symmetric or radial composition; the video half is out of scope for this bridge |

---

## 3. Gated intents (allowed only with the condition applied)

| Intent | Condition | Why |
|---|---|---|
| `/beforeafter` | Concept illustration only, labeled as such in the text layer; never a results claim; the same real product in both plates | An AI before/after presented as an outcome is a deceptive-advertising exposure |
| `/exploded`, `/cutaway`, `/crosssection`, `/transparent`, `/blueprint` | Illustration lane only, never a claim about what is inside the product; not for regulated content (ingredients, claims) | Invented internals misrepresent the product |
| `/360product` | Three or four separately generated angles composed deterministically; never one generation "showing multiple angles" | The model cannot keep one product consistent across angles in a single frame |
| `/color_variant` | Only variants that exist, each attached as its own real render | Invented variants are nonexistent products |
| `/packaging`, `/gift_box` | Only the real packaging (attach it); no invented boxes, sleeves, or ribbons around the product | Reference-image guidance in `LEARNINGS.md`: depict the real product, never one from memory |
| `/infographic_ad`, `/value_prop`, `/offer_ad`, `/comparison` | The model renders the plate; every data point, benefit, price, and comparison label goes to the deterministic text layer | Dense model-rendered text garbles and cannot be verified; comparisons naming a competitor are a legal review item |
| `/amazon_hero` -> use `/marketplace_hero` | White-background primary image; never name or evoke the marketplace | Third-party brand reference (Hard Rule 0) |
| `/testimonial`, `/socialproof` | Only with a real, consenting person and their real words in the text layer; the model never generates the endorser | Fabricated endorsements are a compliance exposure |

---

## 4. Blocked intents (do not expand; say why and offer the nearest accepted intent)

| Intent | Reason | Offer instead |
|---|---|---|
| `/storefront`, `/shelf_display`, `/billboard`, `/billboard3d` | Fabricated store, shelf, and OOH scenes are firewalled (`prompt-craft` §12): they read as fake and misrepresent placement | `/producthero` with a plain-text availability line in the text layer |
| `/greenscreen` | Meme or third-party backgrounds carry copyright and identity risk | `/candid` or `/vibe_check` |
| `/duet_style` | Imitates platform UI in an ad | `/candid` |
| `/trend_hop`, `/challenge_ad` | Undefined trend and IP dependence; nothing a still can carry | `/scrollstopper` with a named concept |
| `/soundwave` | Not a still-image intent | none |

**Off-brand style intents** (`/cyberpunk`, `/vaporwave`, `/scifi`, `/fantasy`, `/retro_vintage`, `/futuristic`, `/surreal`, `/underwater`, `/fire`, `/ice`, `/desert`, `/jungle`, `/storm`, `/snowfall`, `/sand_dune`, `/neon_glow`, `/glitch`, `/papercraft`, `/claymation`, `/neon_noir`, `/pixel_art`, `/clay_render`, `/hologram`, `/maximalist`) are not blocked, but they sit outside most brand systems. The agent expands them only for an explicitly labeled concept lane, never for a retail or e-commerce lane, and never with a person unless the realism blocks apply.

---

## 5. Validity verdict and evidence

**Verdict.** The "slash hacks" are one-word prompts wearing a command costume. They contain no mechanism: no aspect ratio, no lighting, no composition, no preservation fence, no product description, so the engine falls back to its defaults for everything the word does not say. On this engine the defaults are the things this skill exists to override (smoother-than-reality rendering, drifting product labels, invented text). The names are useful as *intent labels* because the user and the agent share them; the descriptions in the document are not prompts and were not imported.

**Evidence batch (2026-09-03).** The same official product render (a glossy black pump bottle with white printed label text) attached in all four runs, one concurrent wave of about two and a half minutes. Two bare "hack" prompts exactly as the document instructs ("upload your product, type a slash hack"), two expansions from §6.

| Run | Prompt | Canvas | Result |
|---|---|---|---|
| 01 | `/floating` bare | 1024x1536 (unrequested portrait) | Bottle on a black void with a rim glow. No surface, no shadow, nothing to float above; "floating" read as "no context". Label intact. Not usable as a hero. |
| 02 | `/macro` bare | 863x1823 (a size in no documented list) | Tight crop of the pump collar on black; the wordmark is cut off at the right edge and the small side print on the bottle turned to gibberish. Not usable: label fidelity failed. |
| 03 | `/floating` expanded (§6) | 1080x1080 as asked | Bottle level above a warm off-white surface, soft diffuse drop shadow beneath, suspended droplets at mixed depths, rim separation, label fully intact and readable. Matches the brief line for line. |
| 04 | `/macro` expanded (§6) | 1080x1080 as asked | Dark slate surface, raking light, each collar rib carrying its own highlight and micro-shadow, gloss reflections rolling off, both wordmark words fully readable. Matches the brief. |

**What the batch shows.** The bare word controls nothing that matters: canvas size is a lottery (two runs, two non-standard sizes), the scene is whatever the engine's dark default is, and label fidelity is unprotected (a cropped wordmark and garbled side print are the exact failures the preservation fence exists to prevent). The expansions hit the requested size both times and kept the label because the brief said so. The list's value is the vocabulary, not the prompts.

---

## 6. Worked expansions (the §5 prompts, copy-ready, ASCII)

**`/floating <product>` ->**
```
Use case: ads-marketing. Asset type: square social static, product hero. Primary request: the product
from image_ref[0] floating in mid-air above a clean surface, a premium studio product shot.
Image 1 = the official product render, preserve exactly: keep the label text, wordmark, colors,
proportions, and closure geometry intact; no new text, logos, or watermarks added.
Scene: a seamless warm off-white studio backdrop with a matte tabletop; the product hovers about one
hand-height above the surface, perfectly upright and level, casting a soft diffuse drop shadow
directly beneath it that is slightly larger and softer than a contact shadow. A few tiny droplets of
water suspended in the air around it at different depths, some sharp, some out of focus.
Composition: product centered, occupying about 55 percent of the frame height, generous negative
space above and below, everything inside the central 84 percent safe zone. Camera at product
mid-height, 85mm lens, f/5.6 so the whole product is sharp.
Lighting: large softbox key from the upper left, soft fill from the right, a thin rim light from behind
to separate the product edge from the backdrop; highlights roll off softly, no clipped whites on the
label text.
Material: [PRODUCT MATERIAL from the reference: container body finish, closure finish, how the label
is printed or applied; e.g. glossy black plastic pump bottle with a ribbed pump collar, white text
printed directly on the body, two soft vertical reflections of the softbox on the gloss].
Palette: warm neutrals from the backdrop and the product's own colors only.
Text: No text beyond the label already on the product.
Constraints: preserve product packaging and label text exactly; no invented claims; no watermark;
photorealistic, not CGI-glossy; fine film grain.
Avoid: altered wordmark, garbled label text, extra products, duplicate containers, distorted
geometry, harsh hard-edged shadow, floating without a shadow, any third-party marks, added text,
watermarks.
Square 1:1 image, 1080x1080.
```

**`/macro <product>` ->**
```
Use case: ads-marketing. Asset type: square social static, product macro detail. Primary request: an
extreme macro photograph of the product from image_ref[0], showing the label print texture, the
closure, and the surface finish.
Image 1 = the official product render, preserve exactly: keep the label text, wordmark, colors,
proportions, and closure geometry intact; no new text, logos, or watermarks added.
Scene: the product stands on a dark matte slate surface; the frame is filled by the upper third of the
container and its closure, cropped tight so the top of the wordmark is fully readable while the
container outline runs off the bottom of the frame.
Photorealistic, shot on medium format film with a 120mm macro lens at f/4. Raking side-top light at 45
degrees reveals the physical surfaces: [the label print: e.g. white lettering printed directly on
glossy black plastic with a slightly raised matte ink edge against the gloss]; the clean brand-new
surface with soft reflections of the light source; [the closure: e.g. each rib of the pump collar
catching a thin highlight and casting a micro-shadow on the next rib]; the closure edge catching a thin
rim highlight; a real contact shadow where the closure meets the container shoulder. Shallow depth of
field: critical sharpness on the wordmark and the nearest closure detail, gentle optical falloff toward
the far side. Fine organic film grain throughout. Zero digital sharpening: all sharpness is optical.
Lifted blacks: shadow detail preserved under the closure edge. Soft highlight rolloff: the gloss never
clips to pure white.
Text: No text beyond the label already on the product.
Constraints: preserve product packaging and label text exactly; no invented claims; no watermark; not
CGI-glossy.
Avoid: altered wordmark, garbled label text, extra products, distorted closure geometry, plastic CGI
look, symmetrical repeating texture, digital sharpening halos, added text, logos, or watermarks.
Square 1:1 image, 1080x1080.
```
