---
name: visual-canon-builder
description: Build imagegen-ready visual canon kits from character, faction, worldbuilding, costume, item, environment, game-asset notes, or one or more reference images. Use when Codex needs to analyze visual references, ask canon-critical clarification questions, document observed visual facts, create a lightweight visual knowledge graph with provenance, validation shapes, proportion/view-projection rules, and produce safe `$imagegen` prompt packs without directly generating images.
---

# Visual Canon Builder

## Overview

Use this skill to convert creative notes and visual references into a practical visual canon system. The output should help `$imagegen` create consistent characters, factions, props, sprites, story illustrations, or concept art by making the canon explicit before any image generation happens.

This skill does not generate or edit images, call image APIs, run image CLIs, train LoRAs, or operate ControlNet/IP-Adapter. If the user also wants images, first produce an `$imagegen`-ready prompt pack, then hand off to `$imagegen` using that pack.

This is a lightweight ontology-inspired skill, not a full RDF/OWL/SHACL implementation. Still, use semantic concepts deliberately: entities have classes and individuals, fields act as properties, relationships are graph triples, observations become provenance-backed assertions, and validation rules behave like SHACL-style shapes.

## Workflow

1. Identify the asset target: character, faction, costume, item, environment, UI icon set, skill effect, sprite, or scene.
2. If images are provided, create an `Image Inventory` first. If the user gives local image paths, inspect them before analysis; if images are already attached, analyze them directly.
3. Extract canon rules from notes and images:
   - `immutable`: must never change.
   - `allowed_variation`: can change by scene, pose, season, damage, emotion, camera, or asset type.
   - `forbidden`: must not appear.
   - `canon_references`: approved reference images, sheets, palettes, or notes.
   - `semantic_mapping`: mapping from YAML fields to class, individual, property, relation, constraint, and provenance concepts.
   - `relations`: graph-like subject/predicate/object triples such as `Image_001 depicts CHR_001`.
   - `canon_assertions`: individual claims with source, confidence, and confirmation state.
   - `proportion_model`: normalized width, height, depth, and limb measurements.
   - `view_spec`: requested view angle and camera constraints.
   - `validation_shapes`: SHACL-like rules with target, path, constraint, severity, and message.
   - `imagegen_execution`: downstream `$imagegen` mode, input roles, output requirements, and handoff status.
4. Separate observed facts from inference. Mark hidden, ambiguous, or conflicting details as `needs_confirmation` instead of inventing them.
5. Ask only canon-critical clarification questions: which image is canon, which differences are intended variants, and which details are forbidden drift.
6. Write a compact visual ontology with English keys and Korean-friendly values/examples.
7. Compile one or more `$imagegen` prompt packs using the schema below. Put only confirmed canon assertions in `Confirmed constraints`; keep uncertain, inferred, role-ambiguous, or source-ambiguous facts in `Provisional constraints` or `Unresolved questions`.
8. Add a validation checklist and canon promotion rule so generated images do not become canon automatically.

For fuller copy/paste templates, read `references/visual-canon-template.md`. For image-to-canon analysis, read `references/image-analysis-to-canon.md`. For semantic mapping, assertion provenance, and shape rules, read `references/semantic-canon-model.md`. For regression goals and manual sample tests, read `references/v3.1-goals-and-manual-tests.md`.

## Image Analysis To Canon

When one or more images are provided, use this pipeline before ontology writing:

1. `Image Inventory`: label each image as `canon candidate`, `reference image`, `variant`, `edit target`, `style reference`, or `forbidden example`.
2. `Observed Visual Facts`: list visible silhouette, palette, face, costume, props, materials, markings, view angle, and camera distortion.
3. `Consistent Elements`: identify features repeated across multiple images; these become `immutable` candidates.
4. `Variant Elements`: identify pose, expression, lighting, weathering, camera, or outfit changes; these become `allowed_variation` candidates.
5. `Conflicts And Unknowns`: record contradictory or hidden details as `needs_confirmation`.
6. `Clarifying Questions`: ask only the questions needed to decide canon, variants, forbidden drift, or hidden dimensions.

Do not treat a stylized or perspective-distorted image as a measurement source unless the user confirms it is a reference sheet. Strong perspective images should become `scene-specific perspective` references, not canon measurement sources.

Image roles gate canon promotion. Repetition alone is not enough: repeated details in two `style reference` images must not outrank a single declared `canon candidate`. If image roles conflict or are unknown, keep the affected facts out of `immutable` and ask.

## Confirmation And Handoff Gates

Treat `observed` and `confirmed canon` as different states:

```yaml
confirmation_gate:
  confirmed_when:
    - confidence: user_confirmed
    - confidence: observed
      source_role: approved canon source
    - confidence: observed
      source_role: canon candidate
      request_context: clearly_declared_as_canon
  provisional_when:
    - confidence: observed
      source_role: reference image
    - confidence: observed
      source_role: canon candidate
      request_context: not_yet_approved
    - confidence: inferred
    - confidence: low_confidence
  blocked_when:
    - identity_critical_conflict_unresolved
    - left_right_asymmetry_conflict_unresolved
    - canon_source_conflict_unresolved
    - proportion_required_but_missing_reference_dimension
```

Set `$imagegen` handoff status from canon risk:

```yaml
handoff_status_rules:
  ready:
    - all identity-critical assertions are confirmed
    - all required view/proportion locks are confirmed or not needed
    - no reject or blocked validation shape is unresolved
  provisional:
    - one usable canon candidate exists but is not yet approved
    - only non-critical style, material, accessory, or atmosphere details remain inferred
    - requested image can be drafted without pretending provisional facts are canon
    - output can proceed if uncertainty is explicitly named in Provisional constraints
  blocked:
    - no usable canon candidate exists
    - multiple canon candidates conflict on identity-critical facts
    - face identity, subject-left/right details, required text, faction mark, or core proportions are required for the requested output and unresolved or conflicting
```

## Semantic Mapping And Provenance

Map the practical YAML output to ontology concepts:

```yaml
semantic_mapping:
  class: entity_type
  individual: id
  property: nested visual/proportion/style fields
  relation: subject-predicate-object records under relations
  constraint: validation_shapes
  provenance: canon_assertions source/confidence fields
```

Use `relations` when a fact connects entities:

```yaml
relations:
  - subject: CHR_001
    predicate: hasFaction
    object: FCT_MoonArchive
  - subject: Image_001
    predicate: depicts
    object: CHR_001
  - subject: CHR_001_Battle
    predicate: variantOf
    object: CHR_001
```

Use `canon_assertions` for claims that may later be audited or revised:

```yaml
canon_assertions:
  - id: ASSERT_001
    subject: CHR_001
    predicate: hasEyeColor
    object: pale_gold
    source_image_id: Image_001
    source_role: approved canon source
    confidence: observed
    canon_status: confirmed
    asserted_by: visual-canon-builder
    derived_from: image_analysis_001
    needs_confirmation: false
```

Validation should include both human-readable checklist items and SHACL-like `validation_shapes`:

```yaml
validation_shapes:
  - target: CHR_001
    path: face.eye_color
    constraint: equals pale_gold
    severity: reject
    message: 눈 색이 pale_gold가 아니면 정본 위반이다.
```

## Ontology Shape

Prefer YAML-like blocks for canon. Keep the ontology specific enough to guide images, but do not invent unsupported lore.

```yaml
entity_type: Character
id: CHR_001
name: Liora
version: 1.0.0

semantic_mapping:
  class: Character
  individual: CHR_001
  properties:
    - visual_core
    - proportion_model
    - projection_rules
  relation_model: relations
  constraint_model: validation_shapes
  provenance_model: canon_assertions

relations:
  - subject: CHR_001
    predicate: hasFaction
    object: FCT_MoonArchive
  - subject: Image_001
    predicate: depicts
    object: CHR_001
  - subject: CHR_001_Battle
    predicate: variantOf
    object: CHR_001

orientation_conventions:
  left_right_basis: subject_left_subject_right
  mirror_validation: required_for_asymmetric_marks
  example: mole_under_subject_left_eye

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

canon_assertions:
  - id: ASSERT_001
    subject: CHR_001
    predicate: hasEyeColor
    object: pale_gold
    source_image_id: Image_001
    source_role: approved canon source
    confidence: observed
    canon_status: confirmed
    asserted_by: visual-canon-builder
    derived_from: image_analysis_001
    needs_confirmation: false
  - id: ASSERT_002
    subject: CHR_001
    predicate: hasBodyDepthSide
    object: needs_confirmation
    source_image_id: Image_001
    source_role: canon candidate
    confidence: needs_confirmation
    canon_status: unresolved
    asserted_by: visual-canon-builder
    derived_from: hidden_side_depth
    needs_confirmation: true

proportion_model:
  units: height_units
  measurement_protocol:
    basis: orthographic_reference_sheet
    full_height_includes: body_top_to_sole_without_hair_hat_or_weapon
    landmarks:
      head_height: chin_to_skull_top_excluding_hair_volume
      shoulder_width_front: subject_left_shoulder_outer_to_subject_right_shoulder_outer
      arm_length: shoulder_joint_to_wrist
      leg_length: hip_joint_to_ankle
    tolerance:
      strict_identity_sheet: 3_percent
      dynamic_scene: 8_percent
    calibration_status: uncalibrated
    tolerance_applies: false
    calibration_evidence:
      pixel_crop: needs_calibration
      normalized_landmarks: needs_calibration
      measured_by: needs_calibration
    tolerance_valid_when:
      - calibrated_reference_sheet
      - pixel_normalized_landmarks
      - full_body_uncropped
      - camera_low_distortion_or_orthographic
    fallback_when_uncalibrated: use_descriptive_or_low_confidence_proportions
    do_not_measure_from:
      - wide_angle_perspective
      - foreshortened_action_pose
      - cropped_body
      - heavy_cloak_or_flared_costume_only
  anatomical_proportion:
    full_height: 1000
    head_height: 154
    head_width_front: 120
    head_depth_side: needs_confirmation
    arm_length: 390
    leg_length: 540
  costume_silhouette_envelope:
    shoulder_width_front: 260
    shoulder_depth_side: needs_confirmation
    torso_width_front: 210
    torso_depth_side: needs_confirmation
    hip_width_front: 230
    hip_depth_side: needs_confirmation
    body_depth_side: needs_confirmation
    costume_or_shell_depth_side: needs_confirmation
  confidence:
    full_height: observed
    side_depths: needs_confirmation

projection_rules:
  formula_type: orthographic_envelope_estimate
  width_formula_per_landmark: projected_width = abs(front_width * cos(yaw)) + abs(side_depth * sin(yaw))
  compute_per_landmark:
    - head
    - shoulder
    - torso
    - hip
    - costume_envelope
  do_not_collapse_to_single_width: true
  yaw_direction_convention:
    positive_yaw_reveals: subject_right
    negative_yaw_reveals: subject_left
  default_reference_camera: orthographic
  valid_when:
    - yaw_only_turnaround
    - pitch_is_0
    - roll_is_0
    - low_clothing_bulk
  invalid_or_low_confidence_when:
    - pitch_or_roll_present
    - strong_perspective
    - foreshortened_pose
    - arms_or_weapon_extend_silhouette
    - cloak_or_skirt_flare_changes_envelope
  distortion_constraints:
    - neutral camera height
    - no wide-angle distortion
    - long-lens or orthographic look for proportion sheets

view_spec:
  view_type: three_quarter
  yaw: 45
  yaw_direction: positive_reveals_subject_right
  visible_side: subject_right
  pitch: 0
  roll: 0
  camera_mode: orthographic
  fixed_canvas_height: 1000
  derived_projected_widths:
    head: needs_head_depth_confirmation
    shoulder: needs_shoulder_depth_confirmation
    torso: needs_torso_depth_confirmation
    hip: needs_hip_depth_confirmation
    costume_envelope: needs_body_depth_confirmation
  numeric_width_check: invalid_until_side_depth_confirmed
  asymmetry_validation_required: true

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

validation_shapes:
  - target: CHR_001
    path: face.eye_color
    constraint: equals pale_gold
    severity: reject
    message: 눈 색이 pale_gold가 아니면 정본 위반이다.
  - target: CHR_001
    path: proportion_model.body_depth_side
    constraint: must_not_be_confirmed_from_front_only_image
    severity: needs_confirmation
    message: 정면 이미지만으로 측면 깊이를 확정하지 않는다.
  - target: CHR_001
    path: orientation_conventions.left_right_basis
    constraint: equals subject_left_subject_right
    severity: fix
    message: 비대칭 표식은 viewer-left가 아니라 subject-left/right로 기록한다.
```

## `$imagegen` Prompt Pack

When the user wants an image or an image prompt, compile the canon into this `$imagegen`-compatible schema. Use only fields that help. Put confirmed canon-preserving rules in `Confirmed constraints`; put helpful but unresolved guidance in `Provisional constraints`; put prohibited drift in `Avoid`.

```text
Use case: <current $imagegen taxonomy slug>
Asset type: <character concept sheet, sprite cutout, faction banner, item icon, scene illustration, etc.>
Primary request: <the user's requested image>
Handoff status: <ready | provisional | blocked>
Imagegen execution: mode=<generate | edit>; input_roles=<reference image/edit target/style reference>; output_aspect=<ratio or size>; transparent_required=<true | false>; variants=<count>; postprocess=<none | chroma-key removal | native transparency fallback>
Input images: <Image 1: reference image; Image 2: edit target; Image 3: style reference> (optional)
Scene/backdrop: <environment or flat chroma-key background when needed>
Subject: <main subject and canon identity>
Style/medium: <illustration, concept art, anime, painterly, game sprite, etc.>
Composition/framing: <front view, 3/4 view, full body, close-up, sheet layout, etc.>
View/proportion lock: <camera mode, yaw direction, visible side, pitch/roll, fixed height, per-landmark derived projected widths, distortion constraints>
Lighting/mood: <lighting and tone>
Color palette: <canon palette>
Materials/textures: <cloth, metal, skin, hair, prop materials>
Text (verbatim): "<exact text if needed>"
Confirmed constraints: <user-confirmed canon, approved-canon-source facts, or clearly declared canon-candidate facts only>
Provisional constraints: <useful but unresolved details; label source role and do not present as hard canon>
Unresolved questions: <canon-critical blockers or needs_confirmation items>
Avoid: <confirmed forbidden rules, request-local prohibitions, drift risks, watermark, unwanted text>
```

If canon-critical conflicts remain, set `Handoff status` to `blocked` or `provisional`. Never move unresolved details into `Confirmed constraints`; keep them in `Provisional constraints` or `Unresolved questions`.

Descriptive prompt fields such as `Subject`, `Style/medium`, `Color palette`, and `Materials/textures` may summarize provisional image evidence, but they must label it as provisional or reference-derived when it is not confirmed. Reserve `Text (verbatim)` for text the user explicitly requested, user-confirmed, or supplied by an approved canon source; otherwise put visible but unconfirmed text in `Provisional constraints` and ask. Reserve `Avoid` for confirmed forbidden drift or request-local exclusions, not for locking unresolved canon.

For proportion-critical requests, compute `derived_projected_widths` per landmark or silhouette envelope from the canon measurement model:

```text
projected_width = abs(front_width * cos(yaw)) + abs(side_depth * sin(yaw))
front yaw 0: projected_width = front_width
side yaw 90: projected_width = side_depth
three-quarter yaw 45: projected_width = 0.707 * front_width + 0.707 * side_depth
```

Run the formula separately for head, shoulder, torso, hip, and costume/accessory envelopes when those dimensions matter. Use `orthographic`, `neutral camera height`, and `no wide-angle distortion` for reference sheets and turnarounds. For dynamic scenes, phrase the lock as "maintain canon proportions with low-distortion perspective" rather than forcing exact sheet measurements.

Use active `$imagegen` taxonomy slugs when they fit. If the active taxonomy is unavailable, use a plain use-case label and avoid claiming the slug is current. Examples that were current at authoring time:
- Generate: `photorealistic-natural`, `product-mockup`, `ui-mockup`, `infographic-diagram`, `scientific-educational`, `ads-marketing`, `productivity-visual`, `logo-brand`, `illustration-story`, `stylized-concept`, `historical-scene`.
- Edit: `text-localization`, `identity-preserve`, `precise-object-edit`, `lighting-weather`, `background-extraction`, `style-transfer`, `compositing`, `sketch-to-render`.

## Chroma-Key Cutout Guidance

For sprite or transparent-background requests, prepare the prompt for `$imagegen`'s built-in-first chroma-key workflow:

```text
Scene/backdrop: flat solid #00ff00 background; perfectly uniform chroma-key field for background removal
Confirmed constraints: full subject visible, crisp separated edges, generous padding, no cast shadow, no contact shadow, no reflection, no background texture, do not use #00ff00 anywhere in the subject
Avoid: shadows, floor plane, gradients, key-color clothing or effects, watermark, extra text
```

If the subject contains green canon colors, choose a different key such as `#ff00ff`. If the subject contains hair, fur, smoke, glass, liquid, translucent effects, or heavy reflections, note that `$imagegen` may need its native transparency fallback rather than simple chroma-key cleanup.

## Validation And Canon Promotion

Always include a post-generation checklist:

- `pass`: satisfies immutable identity, proportion, palette, and forbidden checks.
- `fix`: mostly correct but needs a targeted regeneration or edit.
- `reject`: violates immutable or forbidden rules.

Add these proportion-specific checks when a `proportion_model` or `view_spec` exists:
- 전체 키가 `fixed_canvas_height`에 맞는가?
- 머리:몸 비율과 limb length가 정본 범위 안에 있는가?
- 측면/3/4뷰의 폭이 투영 규칙과 크게 어긋나지 않는가?
- 어깨, 골반, 머리 폭이 시점 변화에 맞게 자연스럽게 줄거나 넓어졌는가?
- 원근 때문에 손, 얼굴, 무기만 과도하게 커지지 않았는가?

Use this canon status flow:

```text
generated -> reviewed -> corrected -> approved -> canon
```

Do not treat a generated image as canon just because it looks good. Only approved outputs can enter `canon_references`; rejected outputs can be kept as `forbidden examples` when useful.

## Output Contract

Return these sections unless the user asks for a narrower artifact:

1. `Image Inventory` when images are provided
2. `Observed Visual Facts` when images are provided
3. `Conflicts And Unknowns` when anything is hidden, contradictory, or uncertain
4. `Clarifying Questions` when canon-critical decisions are blocked
5. `Visual Canon Ontology`
6. `Semantic Relations And Provenance`
7. `Validation Shapes`
8. `$imagegen Prompt Pack`
9. `Validation Checklist`
10. `Canon Promotion Notes`

Keep outputs concise enough to be pasted into `$imagegen`, but include all immutable and forbidden rules needed to prevent visual drift.
