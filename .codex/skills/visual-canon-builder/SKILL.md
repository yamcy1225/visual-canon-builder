---
name: visual-canon-builder
description: Build user-friendly, imagegen-ready visual canon kits from character, faction, worldbuilding, costume, item, environment, game-asset notes, or one or more reference images, especially when preserving identity, original style, proportions, palette, line language, and preventing visual drift matters. Use when Codex needs to analyze visual references, run a compact evidence interview before canon lock, let the user approve/revise/reject canon candidates in plain language, document observed visual facts, create a lightweight visual knowledge graph with provenance, validation shapes, proportion/view-projection rules, generation contracts, evaluation loops, and safe `$imagegen` edit/reference prompt packs without directly generating images.
---

# Visual Canon Builder

## Overview

Use this skill to convert creative notes and visual references into a practical visual canon system. The output should help `$imagegen` create consistent characters, factions, props, sprites, story illustrations, or concept art by making the canon explicit before any image generation happens.

This skill does not generate or edit images, call image APIs, run image CLIs, train LoRAs, or operate ControlNet/IP-Adapter. If the user also wants images, first produce an `$imagegen`-ready prompt pack, then hand off to `$imagegen` using that pack.

This is a lightweight ontology-inspired skill, not a full RDF/OWL/SHACL implementation. Still, use semantic concepts deliberately: entities have classes and individuals, fields act as properties, relationships are graph triples, observations become provenance-backed assertions, and validation rules behave like SHACL-style shapes.

## Workflow

1. Identify the asset target: character, faction, costume, item, environment, UI icon set, skill effect, sprite, or scene.
2. If images are provided, create an `Image Inventory` first. If the user gives local image paths, inspect them before analysis; if images are already attached, analyze them directly.
3. Before locking canon, run User-Friendly Evidence Interview Mode: start with a short user-facing review, split current conversation inputs into `Evidence Cards`, connect them to `Candidate Assertions`, emit an `Approval Review Pack`, and require explicit user approval before any candidate assertion becomes `confirmed`.
4. Extract canon rules from notes and images:
   - `immutable`: must never change.
   - `allowed_variation`: can change by scene, pose, season, damage, emotion, camera, or asset type.
   - `forbidden`: must not appear.
   - `canon_references`: approved reference images, sheets, palettes, or notes.
   - `evidence_cards`: current-conversation image/note snippets used as temporary RAG evidence.
   - `retrieval_trace`: links from evidence cards to candidate assertions.
   - `semantic_mapping`: mapping from YAML fields to class, individual, property, relation, constraint, and provenance concepts.
   - `relations`: graph-like subject/predicate/object triples such as `Image_001 depicts CHR_001`.
   - `canon_assertions`: individual claims with source, confidence, and confirmation state.
   - `style_fidelity_model`: line quality, rendering depth, stylization level, detail density, and forbidden style drift.
   - `style_canon`: identity-bound visual treatment, including line, rendering, color, lighting, texture, camera, and composition language.
   - `generation_contract`: task sensitivity, reference policy, change budget, invariant restatement, allowed mutations, and forbidden mutations.
   - `evaluation_contract`: drift taxonomy, pass/fix/reject rules, retry policy, and next-prompt patch requirements.
   - `reference_preserve_mode`: when generated output must preserve a specific source cell's silhouette, proportions, and style rather than reinterpret the character.
   - `source_cell_asset`: cropped or isolated source-cell image required when exact preservation is expected.
   - `proportion_model`: normalized width, height, depth, and limb measurements.
   - `view_spec`: requested view angle and camera constraints.
   - `validation_shapes`: SHACL-like rules with target, path, constraint, severity, and message.
   - `imagegen_execution`: downstream `$imagegen` mode, input roles, output requirements, and handoff status.
5. Separate observed facts from inference. Mark hidden, ambiguous, unapproved, or conflicting details as `needs_confirmation`, `pending_user_approval`, or `keep_provisional` instead of inventing or prematurely confirming them.
6. Ask only canon-critical clarification questions through the Interactive Clarification Loop: create a `question_queue` with stable IDs, mark each question `blocking_for_ready` and `blocking_for_provisional`, then continue with a provisional ontology and `$imagegen` prompt pack unless a hard-stop condition applies.
7. Write a compact visual ontology with English keys and Korean-friendly values/examples.
8. For identity-sensitive or style-sensitive requests, treat the prompt pack as a generation contract: prefer `edit` or reference-image handoff, state what can change, restate invariants every time, and avoid text-only generation unless the user wants loose inspiration or no reference exists.
9. Compile one or more `$imagegen` prompt packs using the schema below. Put only user-approved canon assertions in `Confirmed constraints`; keep pending, inferred, role-ambiguous, or source-ambiguous facts in `Provisional constraints` or `Unresolved questions`.
10. Add a validation checklist, drift taxonomy, prompt-patch loop, and canon promotion rule so generated images do not become canon automatically.

For fuller copy/paste templates, read `references/visual-canon-template.md`. For image-to-canon analysis, read `references/image-analysis-to-canon.md`. For identity-bound style extraction, read `references/style-canon-model.md`. For edit/reference handoff policy and prompt contracts, read `references/generation-contract.md`. For generated-result review, drift taxonomy, and next-prompt patches, read `references/evaluation-loop.md`. For evidence interview RAG mode, read `references/evidence-interview-rag.md`. For semantic mapping, assertion provenance, and shape rules, read `references/semantic-canon-model.md`. For question/answer loops, read `references/interactive-clarification-loop.md`. For regression goals and manual sample tests, read `references/v3.4-goals-and-manual-tests.md`, `references/v3.5-ux-manual-tests.md`, `references/v3.6-style-fidelity-tests.md`, and `references/v3.7-reference-preserve-tests.md`.

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

## User-Friendly Evidence Interview Mode

Run this before final canon lock. Treat the current conversation as the retrieval corpus: attached images, local image analyses, and user notes become temporary RAG sources. Do not create a vector DB, local UI, or persistent store.

Output `Evidence Cards`, `Retrieval Trace`, `Approval Review Pack`, `Approval Payload`, and `Lock Summary`. Every candidate assertion must include `evidence_refs`, `approval_status`, and `retrieval_scope: current_conversation_only`. Before approval, assertions stay `provisional` or `unresolved`; final `confirmed` requires `approval_status: approved`, evidence, matching version/hash, and `user_answers` provenance.

Default UX rule: do not make the user edit YAML unless they ask for strict/audit mode. Put `Guided Approval Interview`, `User Review`, `Quick Approval Table`, and `Next Reply Options` before technical details; put technical IDs and full YAML in a `Technical Appendix` when needed. Show at most 3 user-facing decision groups at the top.

`Guided Approval Interview` is the active approval process. Ask exactly one current approval question at the top of the response, label it `질문 1/N`, provide 2-4 numbered choices, include the recommended choice, and tell the user they can answer with the number or a short natural-language revision. Keep the provisional ontology and prompt pack available below, but make the current question impossible to miss. When the user answers, record a `user_answers` provenance item, update the affected assertions, then ask the next unresolved approval question until canon-critical decisions are resolved.

Accept plain Korean or English replies and convert them into `approval_payload` decisions internally:

- `추천대로 진행`, `apply recommendations` -> approve recommended identity/costume/proportion items and keep recommended optional props provisional.
- `전체 정본 승인`, `approve all as canon` -> approve all visible candidate assertions, including props and accessories.
- `정본은 승인, 소품은 임시` -> approve identity/costume/proportion candidates and keep prop candidates provisional.
- `수정: <label>=<new value>` -> create `user_answers`, mark the original assertion `revised`, and create a replacement assertion.
- `거절: <label>` or `reject: <label>` -> reject that candidate and keep it out of `Confirmed constraints`.

## Interactive Clarification Loop

When questions are needed, do not only list them and do not default to a ping-pong stop. Emit a `question_queue` with up to 5 stable IDs, `blocking_for_ready`, `blocking_for_provisional`, affected fields, and `default_if_unanswered`. Set `clarification_gate.status: proceeding_with_provisional` and produce the provisional ontology plus `$imagegen` Prompt Pack immediately when a safe provisional draft is possible.

Only set `clarification_gate.status: waiting_for_user` and stop when `hard_stop: true`, such as when there is no usable canon candidate, identity-critical sources conflict, required exact text cannot be safely omitted, or the user explicitly asks for confirmed-only output before any handoff.

When the user answers, create `user_answers` provenance records, link them to affected `canon_assertions`, recompute `canon_status`, `Handoff status`, `Confirmed constraints`, `Provisional constraints`, and `Unresolved questions`, then return the updated ontology and prompt pack.

## Confirmation And Handoff Gates

Treat `observed` and `confirmed canon` as different states:

```yaml
confirmation_gate:
  confirmed_when:
    - confidence: user_confirmed
      approval_status: approved
      user_answers_provenance: exists
      evidence_refs: min_count 1
  provisional_when:
    - confidence: observed
      source_role: reference image
    - confidence: observed
      source_role: canon candidate
      request_context: not_yet_approved
    - confidence: inferred
    - confidence: low_confidence
    - approval_status: pending_user_approval
    - approval_status: keep_provisional
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
    - all identity-critical assertions are confirmed through approval_status: approved
    - canon_lock_state is locked or no canon lock is required for the requested artifact
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

## Identity, Style, And Generation Contracts

When the user asks to preserve the original image, same character, same mascot, brand feeling, art direction, or visual vibe, treat the work as `identity_sensitive` or `style_sensitive`, not loose inspiration.

Separate the canon into operational layers:

- `identity_canon`: face geometry, silhouette, anatomy, proportions, unique marks, symbols, costume structure, and subject-left/right details.
- `style_canon`: line weight, line variation, shading model, rendering medium, texture density, palette temperature, value range, lighting mood, camera language, and composition rhythm.
- `variation_canon`: pose, expression, background, weather, action, minor wear, scene props, and other user-requested mutations.
- `generation_contract`: reference roles, change budget, allowed mutations, forbidden mutations, and invariant restatement.
- `evaluation_contract`: identity/style/proportion/semantic checks, drift taxonomy, pass/fix/reject rules, and next-prompt patch format.

For identity-sensitive tasks, prefer `edit`, `edit_target_preserve`, or reference-image handoff. Text-only generation is allowed only when no reference image exists, the user explicitly asks for loose inspiration, or identity/style preservation is not required. The prompt pack must say what changes and what stays unchanged; more descriptive adjectives are not a substitute for an explicit contract.

## Semantic Mapping And Provenance

Map the practical YAML output to ontology concepts:

```yaml
semantic_mapping:
  class: entity_type
  individual: id
  property: nested visual/proportion/style fields
  relation: subject-predicate-object records under relations
  constraint: validation_shapes
  provenance: canon_assertions source/confidence/evidence_refs/approval_status/user_answers/retrieval_scope fields
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
    confidence: user_confirmed
    canon_status: confirmed
    approval_status: approved
    evidence_refs:
      - EV_001
    retrieval_scope: current_conversation_only
    asserted_by: visual-canon-builder
    derived_from:
      - image_analysis_001
      - UA_001
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
    - style_canon
    - style_fidelity_model
    - generation_contract
    - evaluation_contract
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

style_fidelity_model:
  source_style_role: approved_reference_sheet_style
  rendering_mode:
    value: flat_2d_character_sheet_line_art
    immutable: true
  line_quality:
    outer_contour: clean_bold_black_line
    interior_lines: simple_thin_black_detail_lines
    sketch_or_hatching: only_if_visible_in_reference
  shading:
    allowed: minimal_flat_grayscale_or_subtle_reference_matching_shadow
    forbidden:
      - semi_realistic_soft_airbrush_shading
      - 3d_render_lighting
      - glossy_material_highlights
      - realistic_fur_or_skin_texture
  detail_density:
    value: match_reference_sheet_simplification
    forbidden:
      - realistic_product_rendering
      - extra_fashion_illustration_detail
  style_drift_forbidden:
    - semi_realistic_character_art
    - 3d_or_clay_render
    - adult_anatomical_proportions
    - painterly_gradient_background

# For full `style_canon`, `generation_contract`, and
# `evaluation_contract` shapes, use the dedicated reference files.

canon_assertions:
  - id: ASSERT_001
    subject: CHR_001
    predicate: hasEyeColor
    object: pale_gold
    assertion_version: 1
    value_hash: hash_of_subject_predicate_object_v1
    evidence_refs:
      - EV_001
    retrieval_scope: current_conversation_only
    source_image_id: Image_001
    source_role: approved canon source
    confidence: user_confirmed
    canon_status: confirmed
    approval_status: approved
    asserted_by: visual-canon-builder
    derived_from:
      - image_analysis_001
      - UA_001
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
Task sensitivity: <identity_sensitive | style_sensitive | loose_inspiration>
Primary request: <the user's requested image>
Handoff status: <ready | provisional | blocked>
Imagegen execution: mode=<edit | reference_generate | text_generate>; text_generate_allowed=<true | false>; reason=<why this mode is acceptable>; input_roles=<identity_anchor/style_anchor/edit_target/composition_reference/forbidden_example>; output_aspect=<ratio or size>; transparent_required=<true | false>; variants=<count>; postprocess=<none | chroma-key removal | native transparency fallback>
Reference preserve mode: <off | identity_preserve | edit_target_preserve>; source_cell=<front/full-body/expression/prop crop>; preserve=<silhouette, head/body ratio, limb length, line style, detail density>; allowed_change=<pose/expression/text only>
Source cell asset: <required | optional | not_needed>; crop_id=<source-cell crop or isolated edit target>; full_sheet_only=<allowed | blocked_for_exact_preservation>
Reference policy: <what each input image anchors; identity/style/composition/forbidden examples>
Change budget: <identity 0%; style 0-5%; pose/background/costume locked or allowed by request>
Input images: <Image 1: reference image; Image 2: edit target; Image 3: style reference> (optional)
Scene/backdrop: <environment or flat chroma-key background when needed>
Subject: <main subject and canon identity>
Style/medium: <illustration, concept art, anime, painterly, game sprite, etc.>
Style fidelity lock: <reference-sheet style, flatness, line weight, shading depth, detail density, and forbidden style drift>
Generation contract: <identity-preserving task, not redesign; preserve exact anchors; restate invariants>
Composition/framing: <front view, 3/4 view, full body, close-up, sheet layout, etc.>
View/proportion lock: <camera mode, yaw direction, visible side, pitch/roll, fixed height, per-landmark derived projected widths, distortion constraints>
Lighting/mood: <lighting and tone>
Color palette: <canon palette>
Materials/textures: <cloth, metal, skin, hair, prop materials>
Text (verbatim): "<exact text if needed>"
Confirmed constraints: <assertions with approval_status approved and user_answers provenance only>
Style constraints: <approved or explicitly user-confirmed style canon only>
Provisional constraints: <useful but unresolved details; label source role and do not present as hard canon>
Generation constraints: <request-local technical constraints that are not canon, such as chroma-key, padding, or no-shadow requirements>
Change only: <specific user-requested mutations>
Unresolved questions: <canon-critical blockers or needs_confirmation items>
Avoid: <confirmed forbidden rules, request-local prohibitions, drift risks, watermark, unwanted text>
Evaluation checklist: <identity_pass/style_pass/proportion_pass/semantic_pass/drift_notes/next_prompt_patch>
```

If canon-critical conflicts remain, set `Handoff status` to `blocked` or `provisional`. Never move unresolved details into `Confirmed constraints`; keep them in `Provisional constraints` or `Unresolved questions`.

Descriptive prompt fields such as `Subject`, `Style/medium`, `Color palette`, and `Materials/textures` may summarize provisional image evidence, but they must label it as provisional or reference-derived when it is not confirmed. Reserve `Text (verbatim)` for text attached to approved assertions; otherwise put visible but unconfirmed text in `Provisional constraints` and ask. Reserve `Avoid` for confirmed forbidden drift or request-local exclusions, not for locking unresolved canon.

For proportion-critical requests, compute `derived_projected_widths = abs(front_width * cos(yaw)) + abs(side_depth * sin(yaw))` separately for head, shoulder, torso, hip, and costume/accessory envelopes. Use `orthographic`, `neutral camera height`, and `no wide-angle distortion` for reference sheets; for dynamic scenes, phrase the lock as "maintain canon proportions with low-distortion perspective" rather than forcing exact sheet measurements.

For reference-sheet-derived mascot or cartoon characters, always add a strict style fidelity lock. Name the original visual treatment explicitly, such as "flat 2D black-and-white mascot line art from the reference sheet." Reject or avoid style drift into semi-realistic character art, 3D render shading, realistic fur, realistic sneaker/product rendering, adult anatomical proportions, fashion illustration, painterly gradients, glossy materials, or heavy volumetric lighting unless the user explicitly requests a style translation.

When the user expects a generated image to look like the same exact character sheet design, do not hand off a full multi-pose sheet as the only image. Require a `source_cell_asset`: a cropped or isolated cell that matches the requested output, such as the front full-body pose. Prefer `edit_target_preserve` when only expression, arm position, or shirt text should change; use `identity_preserve` only when a genuinely new pose is needed. If the source cell is not available, set `Handoff status: blocked` or `provisional` with `Unresolved questions: source_cell_asset required`, rather than pretending prompt text can guarantee exact preservation.

If a previous generation preserves identity but changes proportions/style, mark it `reject` and switch the next handoff to source-cell-based edit/preserve mode. More adjectives are not enough when the input image is a full sheet and the output must match one specific cell.

Use active `$imagegen` taxonomy slugs when they fit; if unavailable, use a plain use-case label and avoid claiming the slug is current.

## Chroma-Key Cutout Guidance

For sprite or transparent-background requests, prepare the prompt for `$imagegen`'s built-in-first chroma-key workflow:

```text
Scene/backdrop: flat solid #00ff00 background; perfectly uniform chroma-key field for background removal
Generation constraints: full subject visible, crisp separated edges, generous padding, no cast shadow, no contact shadow, no reflection, no background texture, do not use #00ff00 anywhere in the subject
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

Add these style-fidelity checks when a `style_fidelity_model` exists:
- 원본의 line weight, flat shading, and detail density가 유지되는가?
- 반실사화, 3D화, 과한 렌더링, 사실적인 제품 디테일이 생기지 않았는가?
- 마스코트의 나이감/귀여운 비율이 성숙하거나 패션 일러스트처럼 늘어나지 않았는가?
- reference-sheet character art가 scene illustration이나 product render 스타일로 바뀌지 않았는가?

Add these reference-preservation checks when `reference_preserve_mode` is active:
- 선택한 source cell의 머리:몸:다리 비율이 유지되는가?
- full multi-pose sheet가 아니라 실제 source_cell_asset 또는 isolated edit target을 입력으로 사용했는가?
- 신발, 손, 팔, 다리 디테일이 원본보다 현실적으로 복잡해지지 않았는가?
- 요청한 변경 외의 얼굴 구조, 몸통 길이, 다리 길이, 신발 크기가 재설계되지 않았는가?
- identity만 맞고 silhouette/proportion/style이 다른 경우 `fix`가 아니라 `reject`로 판정했는가?

Add these evaluation-loop outputs after reviewing a generated image:
- `evaluation_result`: generated image id, compared anchors, pass/fix/reject classification, and confidence.
- `drift_patterns`: identity, style, proportion, semantic, and composition drift labels.
- `prompt_patch`: short corrective instructions for the next generation or edit.
- `forbidden_example_candidate`: whether a rejected output should be stored as a useful forbidden example.

Use this canon status flow:

```text
generated -> reviewed -> corrected -> approved -> canon
```

Do not treat a generated image as canon just because it looks good. Only approved outputs can enter `canon_references`; rejected outputs can be kept as `forbidden examples` when useful.

## Output Contract
Return these sections unless the user asks for a narrower artifact:

1. User-facing approval first: `Guided Approval Interview`, `User Review`, `Quick Approval Table`, and `Next Reply Options`.
2. Source/evidence and analysis: `Image Inventory`, `Evidence Cards`, `Retrieval Trace`, `Approval Review Pack`, `Approval Payload`, `Lock Summary`, `Observed Visual Facts`, `Conflicts And Unknowns`, `Question Queue`, and `Clarification Gate`.
3. Approval/canon: `User Answer Provenance` when applying replies, `Visual Canon Ontology`, `Semantic Relations And Provenance`, and `Validation Shapes`.
4. Handoff: `$imagegen Prompt Pack`, `Validation Checklist`, and `Canon Promotion Notes`.

Keep the first screen concise and decision-oriented. Use Korean labels for user decisions, hide hashes from the top-level review, and include IDs/hashes only in technical sections. Keep outputs concise enough to be pasted into `$imagegen`, but include all immutable and forbidden rules needed to prevent visual drift.
