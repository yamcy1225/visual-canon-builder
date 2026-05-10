---
name: visual-canon-builder
description: Build imagegen-ready visual canon kits from character, faction, worldbuilding, costume, item, environment, or game-asset notes. Use when Codex needs to turn creative settings into a structured visual ontology, immutable/variable/forbidden rules, canon reference guidance, validation checklists, and `$imagegen` prompt packs for consistent image generation without directly generating images.
---

# Visual Canon Builder

## Overview

Use this skill to convert creative notes into a practical visual canon system. The output should help `$imagegen` create consistent characters, factions, props, sprites, story illustrations, or concept art by making the canon explicit before any image generation happens.

This skill does not generate or edit images, call image APIs, run image CLIs, train LoRAs, or operate ControlNet/IP-Adapter. If the user also wants images, first produce an `$imagegen`-ready prompt pack, then hand off to `$imagegen` using that pack.

## Workflow

1. Identify the asset target: character, faction, costume, item, environment, UI icon set, skill effect, sprite, or scene.
2. Extract canon rules from the user's notes:
   - `immutable`: must never change.
   - `allowed_variation`: can change by scene, pose, season, damage, emotion, camera, or asset type.
   - `forbidden`: must not appear.
   - `canon_references`: approved reference images, sheets, palettes, or notes.
   - `validation_checks`: pass/fix/reject criteria after generation.
3. Write a compact visual ontology with English keys and Korean-friendly values/examples.
4. Compile one or more `$imagegen` prompt packs using the schema below.
5. Add a validation checklist and canon promotion rule so generated images do not become canon automatically.

For fuller copy/paste templates, read `references/visual-canon-template.md`.

## Ontology Shape

Prefer YAML-like blocks for canon. Keep the ontology specific enough to guide images, but do not invent unsupported lore.

```yaml
entity_type: Character
id: CHR_001
name: Liora
version: 1.0.0

visual_core:
  silhouette:
    value: slim_vertical
    immutable: true
  face:
    eye_shape: almond
    eye_color: pale_gold
    unique_mark: mole_under_left_eye
  palette:
    primary: deep_indigo
    secondary: antique_silver
    accent: pale_gold

immutable:
  - pale_gold almond eyes
  - mole under left eye
  - slim vertical silhouette
  - crescent emblem on collar

allowed_variation:
  - sleeve wrinkles
  - dust and light fabric damage in battle scenes
  - minor accessory count

forbidden:
  - red scarf
  - round glasses
  - bulky armor
  - changed eye color

canon_references:
  - front view sheet
  - side view sheet
  - face close-up
  - color palette
  - forbidden examples

validation_checks:
  identity:
    - 눈 색이 pale_gold인가?
    - 왼쪽 눈 아래 점이 유지되는가?
  costume:
    - 초승달 문장이 칼라에 있는가?
    - 왼쪽 어깨 망토가 비대칭으로 유지되는가?
  forbidden:
    - 붉은 스카프, 둥근 안경, 무거운 갑옷이 생기지 않았는가?
```

## `$imagegen` Prompt Pack

When the user wants an image or an image prompt, compile the canon into this `$imagegen`-compatible schema. Use only fields that help. Put canon-preserving rules in `Constraints`; put prohibited drift in `Avoid`.

```text
Use case: <stylized-concept | illustration-story | identity-preserve | sketch-to-render | logo-brand | background-extraction | other imagegen taxonomy slug>
Asset type: <character concept sheet, sprite cutout, faction banner, item icon, scene illustration, etc.>
Primary request: <the user's requested image>
Input images: <Image 1: reference image; Image 2: edit target; Image 3: style reference> (optional)
Scene/backdrop: <environment or flat chroma-key background when needed>
Subject: <main subject and canon identity>
Style/medium: <illustration, concept art, anime, painterly, game sprite, etc.>
Composition/framing: <front view, 3/4 view, full body, close-up, sheet layout, etc.>
Lighting/mood: <lighting and tone>
Color palette: <canon palette>
Materials/textures: <cloth, metal, skin, hair, prop materials>
Text (verbatim): "<exact text if needed>"
Constraints: <immutable canon rules and must-keep details>
Avoid: <forbidden rules, drift risks, watermark, unwanted text>
```

Use these `$imagegen` taxonomy slugs when they fit:
- `stylized-concept`: character concepts, costume sheets, props, faction visuals, world art.
- `illustration-story`: narrative scenes, key art, comics, story moments.
- `identity-preserve`: edits or variants where a provided character image must stay recognizable.
- `sketch-to-render`: line art, rough designs, silhouettes, or thumbnails converted into polished art.
- `background-extraction`: sprite/cutout/transparent-background requests.
- `logo-brand`: faction marks, emblems, sigils, or vector-friendly explorations.

## Chroma-Key Cutout Guidance

For sprite or transparent-background requests, prepare the prompt for `$imagegen`'s built-in-first chroma-key workflow:

```text
Scene/backdrop: flat solid #00ff00 background; perfectly uniform chroma-key field for background removal
Constraints: full subject visible, crisp separated edges, generous padding, no cast shadow, no contact shadow, no reflection, no background texture, do not use #00ff00 anywhere in the subject
Avoid: shadows, floor plane, gradients, key-color clothing or effects, watermark, extra text
```

If the subject contains hair, fur, smoke, glass, liquid, translucent effects, or heavy reflections, note that `$imagegen` may need its native transparency fallback rather than simple chroma-key cleanup.

## Validation And Canon Promotion

Always include a post-generation checklist:

- `pass`: satisfies immutable identity, proportion, palette, and forbidden checks.
- `fix`: mostly correct but needs a targeted regeneration or edit.
- `reject`: violates immutable or forbidden rules.

Use this canon status flow:

```text
generated -> reviewed -> corrected -> approved -> canon
```

Do not treat a generated image as canon just because it looks good. Only approved outputs can enter `canon_references`; rejected outputs can be kept as `forbidden examples` when useful.

## Output Contract

Return these sections unless the user asks for a narrower artifact:

1. `Visual Canon Ontology`
2. `$imagegen Prompt Pack`
3. `Validation Checklist`
4. `Canon Promotion Notes`

Keep outputs concise enough to be pasted into `$imagegen`, but include all immutable and forbidden rules needed to prevent visual drift.
