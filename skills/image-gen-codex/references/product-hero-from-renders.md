# Product-Accurate Hero from Real Renders

The reliable way to place a REAL product into an AI-generated lifestyle or hero scene at high definition, without the model inventing generic packaging. Read this before any people-plus-product hero, group lifestyle shot, or product-in-scene composition.

## The core rule

**Attach the real product render as an image reference; generate the people and the scene from text.**

The GPT-Image family reproduces an *attached* product far more faithfully than one it conjures from a description. Describe-only prompts return plausible-but-generic packaging — the right silhouette, wrong everything-else — which reads as "not our product." So split the job:

- Every product that must be recognizable -> one real render attached as `--image` (Image 1..N).
- People, wardrobe, setting, lighting, mood -> described in text; the engine renders these well from words.
- Restate each product's identity in the prompt anyway. The engine leans on the text over the reference for identity, so name the exact form, the label wording to keep, and the relative size of each attached product — never "same as the reference."

## Sourcing the renders

- Use your **canonical, high-resolution** product renders — clean, front-facing, transparent or solid background. Higher input resolution yields crisper labels in the output.
- **Verify each render visually before you use it.** Render libraries are frequently mislabeled (a file named for one SKU can hold another). Open it and confirm it is the product you think it is.
- The bridge only accepts references **inside the output root**, so copy any external render into a job folder under `<allowed-subdir>/` first. (Search tools also may not see files outside the working tree — reference them by absolute path when copying in.)
- Respect the ~5-image reference cap: one render per product. With more products than slots, attach the ones that must read as exact and describe the rest.

## Prompt structure that lands

- **Name each product** in the input-images list: its exact form (foam-pump bottle, lotion-pump bottle, trigger-spray, screw-lid jar, tube, ...), the label wording to preserve, and its size **relative to the others** (call out the tallest and the shortest). Correct relative proportions are what make a product row read as real rather than pasted.
- **Reserve the overlay zone.** If text will be laid over the image afterward, state which side stays clean and empty (~40%) and cluster the subjects on the opposite side; keep the products in a lower foreground row on clean blocks.
- **Preservation fence** on every attached render: "keep the label / wordmark / colors / proportions intact" paired with "add no new text, logos, or watermarks."
- Generate the people fresh from the written description.

## Fidelity limits (know before you promise)

- Reference-guided generation gets you ~95%: correct shapes, correct label copy, correct proportions.
- It will **not pixel-lock small label micro-text** — a wordmark or fine print can garble on some runs, and it varies run to run. Inspect every label on every output.
- For **pixel-perfect** packaging, generate the scene, then composite the official product PNG over the model's product deterministically (Pillow or an HTML/headless layer) instead of trusting the model with the fine print.

## High-definition output + exact aspect

- `$imagegen` **ignores a requested pixel size** (the manifest records what you actually got). Generate at the aspect that suits the subject, then reach the exact target size deterministically.
- **To reach a wider target aspect:** extend the *clean background* side by edge-replicating the uniform edge column (Pillow), then resample to the exact pixels. Extend **only** a side that is empty background — extending a side that contains a subject smears it into horizontal streaks.
- **For a tall/portrait placement that crops to a fixed box:** bake the empty margin **into the generated frame** — subjects in the middle band, the product row in the lower third, a large clean band on top. A fixed-aspect crop discards any padding added afterward, so the clear space an overlay needs must exist in the render itself.

## QA before you accept

- Labels legible and correctly spelled; wordmark intact; no invented copy.
- Product forms and **relative proportions** match the real lineup.
- Hands and anatomy clean; no extra or duplicate products; nothing floating.
- No trademark you don't own is rendered (Hard Rule 0); the reserved overlay zone is genuinely clear.
- Read the manifest for the true dimensions; upscale or refine only per the `realism-formula.md` ladder.
