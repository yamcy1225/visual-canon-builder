# Image Analysis To Canon

Use this reference when `$visual-canon-builder` receives one or more images and needs to turn visual evidence into canon documentation, style fidelity rules, proportion rules, and `$imagegen` prompt packs.

## Contents

- Input Handling
- Image Inventory
- Observation Rules
- Evidence Interview RAG Mode
- Canon Confirmation Gate
- Single Image Analysis
- Multiple Image Comparison
- Style Fidelity Extraction
- Reference Preserve Planning
- Proportion Extraction
- View Projection
- Clarifying Questions
- User Answer Application
- `$imagegen` Handoff
- Canon Assertion Provenance

## Input Handling

- If images are attached in the conversation, analyze them directly.
- If the user provides local file paths, inspect each image before analysis.
- Label every image by index and role:
  - `canon candidate`: possible source of truth
  - `reference image`: useful but not automatically canon
  - `variant`: intentional alternate outfit, pose, lighting, damage, or season
  - `edit target`: image to preserve while editing later through `$imagegen`
  - `style reference`: rendering or mood reference, not identity canon
  - `forbidden example`: visual drift to avoid
- Do not promote any image to canon unless the user confirms it or the request clearly says it is canon.
- Image roles gate canon promotion. Repeated details in `style reference` images stay style guidance, not immutable identity canon.

## Image Inventory

```yaml
image_inventory:
  - id: Image 1
    role: canon candidate
    view: front
    camera: orthographic_or_low_distortion
    visible_regions:
      - full body
      - face
      - costume front
    hidden_regions:
      - back
      - side depth
    measurement_reliability: high
  - id: Image 2
    role: variant
    view: three_quarter
    camera: scene-specific perspective
    visible_regions:
      - face
      - torso
      - weapon
    hidden_regions:
      - back
      - exact side depth
    measurement_reliability: medium
```

## Observation Rules

Separate evidence from inference:

```yaml
observed_visual_facts:
  silhouette:
    - slim vertical body shape
  palette:
    - deep indigo clothing
    - pale gold accent
  markings:
    - crescent emblem on collar
  style_fidelity:
    rendering_mode: flat_2d_character_sheet_line_art
    line_quality: clean_black_outline_with_simple_inner_lines
    shading: minimal_flat_grayscale
    detail_density: simplified_reference_sheet_detail

inferred_or_uncertain:
  body_depth_side: needs_confirmation
  back_design: needs_confirmation
  exact_material: inferred_matte_silk_low_confidence
```

## Style Fidelity Extraction

When the reference image has a distinctive visual treatment, extract it as `style_fidelity_model` before handoff. This is separate from identity canon: the character can keep the same identity but still fail if the rendering style drifts.

Track:
- rendering mode: flat 2D, ink sketch, cel animation, painterly, 3D, photo, etc.
- line quality: bold outline, thin interior detail, hatching, sketch roughness.
- shading depth: none, flat grayscale, cel shadow, soft airbrush, volumetric.
- detail density: simplified mascot sheet, realistic product detail, dense fashion illustration, etc.
- forbidden drift: semi-realistic anatomy, 3D render, realistic fur/skin, product-render shoes, glossy lighting.

For mascot/reference-sheet art, default to strict style preservation unless the user asks for a style translation.

## Reference Preserve Planning

If the user expects an output to look like the same exact character design, choose a source cell before `$imagegen` handoff. A full character sheet is useful evidence, but it is not a sufficient edit/preserve target. A single closest source cell crop or isolated image is required for exact preservation.

Record:

```yaml
reference_preserve_model:
  mode: identity_preserve
  source_cell_asset:
    required: true
    crop_id: CROP_SampleMascot_FrontFullBody_001
    asset_path: needs_crop_or_attached_cell
    full_sheet_only: blocked_for_exact_preservation
  source_cell:
    source_id: SRC_Image_001
    region: front_full_body
    role: proportion_and_style_anchor
  preserve:
    - silhouette
    - head_body_ratio
    - limb_length
    - shoe_simplification
    - line_style
    - detail_density
  allowed_change:
    - expression
    - shirt_text
    - arm_pose
  forbidden_change:
    - body_redesign
    - elongated_adult_proportions
    - realistic_shoe_redesign
```

Use `edit_target_preserve` when the task is closer to editing one reference pose than generating a new pose. Use `identity_preserve` when a new pose is needed but the character's source-cell proportions and style must remain locked.

If only the full sheet is available, tell the user that exact preservation needs a crop/isolated source-cell asset. The skill may still produce a provisional prompt, but the handoff should not be marked `ready` for exact preservation until the crop is available.

## Evidence Interview RAG Mode

When the user wants canon built from conversation images or notes, create evidence cards before writing final canon. The retrieval corpus is only the current conversation unless the user explicitly provides more sources.

```yaml
source_inventory:
  retrieval_scope: current_conversation_only
  sources:
    - id: SRC_Image_001
      type: attached_image
      role: canon candidate
      description: character sheet reference

evidence_cards:
  - id: EV_Character_Face_001
    source_id: SRC_Image_001
    modality: image
    region_or_note: face views
    source_anchor: Image 1 / face views
    view_label: front_and_expression_heads
    bbox_or_region: descriptive_region_no_pixel_bbox
    source_text_span: null
    observation: directly visible face identity details
    confidence: observed
    usable_for:
      - identity
      - face
    limitations:
      - hidden side details cannot be proven

retrieval_trace:
  - assertion_id: ASSERT_Character_Face_001
    evidence_refs:
      - EV_Character_Face_001
    rationale: face assertion is visible in the front and expression views
```

Every image-derived assertion must include `evidence_refs`, `approval_status`, and `retrieval_scope`. Before the user returns an approval payload, keep the assertion out of `Confirmed constraints`.

Use confidence labels:
- `observed`: directly visible and reliable.
- `inferred`: likely, but not directly confirmed.
- `low_confidence`: distorted, obscured, or stylized enough to be risky.
- `needs_confirmation`: canon decision requires the user.
- `user_confirmed`: the user explicitly approved the assertion as canon.

## Canon Confirmation Gate

Do not treat every observed detail as confirmed canon. A fact can enter `Confirmed constraints` only when the assertion has `approval_status: approved`, linked `user_answers` provenance, and at least one `evidence_refs` item.

```yaml
confirmation_gate:
  confirmed_constraints_allowed_when:
    - confidence: user_confirmed
      approval_status: approved
      user_answers_provenance: exists
      evidence_refs: min_count 1
  provisional_constraints_when:
    - confidence: observed
      source_role: reference image
    - confidence: observed
      source_role: canon candidate
      request_context: not_yet_approved
    - confidence: inferred
    - confidence: low_confidence
    - approval_status: pending_user_approval
    - approval_status: keep_provisional
  unresolved_questions_when:
    - confidence: needs_confirmation
    - source_role_conflict: true
    - canon_critical_conflict: true
```

Use `canon_status` on assertions:

```text
confirmed
provisional
unresolved
rejected
```

Use `approval_status` separately from `canon_status`:

```text
pending_user_approval
approved
rejected
revised
keep_provisional
```

Use left/right labels from the subject's body, not the viewer's screen:

```yaml
orientation_conventions:
  left_right_basis: subject_left_subject_right
  mirror_validation: required_for_asymmetric_details
```

## Single Image Analysis

For one image:

1. Record visible visual facts.
2. Extract only visible proportion candidates.
3. Mark hidden back/side/depth measurements as `needs_confirmation`.
4. Ask for missing canon-critical dimensions only if the requested output depends on them.

```yaml
single_image_result:
  immutable_candidates:
    - eye color
    - face mark
    - emblem location
  allowed_variation_candidates:
    - lighting
    - pose
    - sleeve wrinkles
  needs_confirmation:
    - body_depth_side
    - back costume design
    - whether current weapon is permanent canon
```

## Multiple Image Comparison

For multiple images:

1. Resolve image roles before promoting repeated features.
2. Treat pose, camera, expression, weathering, and scene light changes as `allowed_variation` candidates.
3. Treat contradictions as `conflicts`, not automatic decisions.
4. Ask which image is canon if two images disagree on identity, palette, major costume structure, or proportions.

```yaml
multi_image_comparison:
  consistent_elements:
    - pale gold eyes across Image 1, Image 2, Image 3
    - crescent collar emblem across Image 1 and Image 3
  variant_elements:
    - battle dust only in Image 2
    - cloak damage only in Image 2
  conflicts_and_unknowns:
    - Image 1 has narrow shoulders; Image 3 has broad shoulders
    - Image 2 hides the left collar emblem
```

## Proportion Extraction

Use a practical 2.5D model, not full 3D reconstruction.

Normalize measurements with either:
- `height_units: 1000` for imagegen prompt and validation work.
- `head_units` when the user prefers classic character-sheet ratios.

Required fields:

```yaml
proportion_model:
  units: height_units
  measurement_protocol:
    basis: <orthographic reference sheet | low-distortion image | user supplied>
    full_height_includes: body_top_to_sole_without_hair_hat_or_weapon
    landmarks:
      head_height: chin_to_skull_top_excluding_hair_volume
      shoulder_width_front: subject_left_shoulder_outer_to_subject_right_shoulder_outer
      arm_length: shoulder_joint_to_wrist
      leg_length: hip_joint_to_ankle
    tolerance:
      strict_identity_sheet: 3_percent
      dynamic_scene: 8_percent
    calibration_status: <uncalibrated | calibrated>
    tolerance_applies: <true | false>
    calibration_evidence:
      pixel_crop: <none | crop coordinates or description>
      normalized_landmarks: <none | landmark list>
      measured_by: <agent | user | script | unknown>
    tolerance_valid_when:
      - calibrated_reference_sheet
      - pixel_normalized_landmarks
      - full_body_uncropped
      - camera_low_distortion_or_orthographic
    fallback_when_uncalibrated: use_descriptive_or_low_confidence_proportions
  anatomical_proportion:
    full_height: 1000
    head_height: <observed or needs_confirmation>
    head_width_front: <observed or needs_confirmation>
    head_depth_side: <observed or needs_confirmation>
    arm_length: <observed or needs_confirmation>
    leg_length: <observed or needs_confirmation>
  costume_silhouette_envelope:
    shoulder_width_front: <observed or needs_confirmation>
    shoulder_depth_side: <observed or needs_confirmation>
    torso_width_front: <observed or needs_confirmation>
    torso_depth_side: <observed or needs_confirmation>
    hip_width_front: <observed or needs_confirmation>
    hip_depth_side: <observed or needs_confirmation>
    body_depth_side: <observed or needs_confirmation>
    costume_or_shell_depth_side: <observed or needs_confirmation>
  accessory_envelope:
    weapon_width_or_reach: <observed or not_applicable>
    prop_extension: <observed or not_applicable>
```

Measurement rules:
- Use front/reference-sheet images for front widths.
- Use side/reference-sheet images for side depths.
- Use dynamic action scenes only as low-confidence hints.
- Do not use wide-angle or foreshortened body parts as canon dimensions.
- Separate anatomical proportions from costume or silhouette envelope.
- State whether full height excludes or includes hair, hats, heels, and weapons.
- Mark any missing or hidden measurement as `needs_confirmation`.
- Use numeric tolerance bands only after calibrated reference-sheet measurements. Without calibration, describe proportions or mark them `low_confidence`.
- Normalize pixel measurements by cropping to the declared full-height landmarks, scaling to `full_height: 1000`, and rounding to the nearest practical unit such as 5 height units.
- Set `calibration_status: uncalibrated` and `tolerance_applies: false` unless pixel crop, normalized landmarks, and measurement method are recorded.

## View Projection

Store front width and side depth separately per landmark or envelope. Calculate an approximate orthographic envelope for angled views:

```text
projected_width = abs(front_width * cos(yaw)) + abs(side_depth * sin(yaw))
```

Use degrees for yaw:

```yaml
projection_examples:
  front:
    yaw: 0
    projected_width: front_width
  side:
    yaw: 90
    projected_width: side_depth
  three_quarter:
    yaw: 45
    projected_width: 0.707 * front_width + 0.707 * side_depth
```

Example calculation:

```yaml
input:
  shoulder_width_front: 260
  shoulder_depth_side: 150
  yaw: 45
calculation:
  derived_projected_shoulder_width: 0.707 * 260 + 0.707 * 150
  result: 290
```

Compute the formula separately for `head`, `shoulder`, `torso`, `hip`, and `costume_envelope` when those dimensions matter. Do not collapse the entire character into one `derived_projected_width`. Use each result as a prompt/validation constraint, not as a pixel-perfect guarantee.

Record yaw direction:

```yaml
view_spec:
  yaw: 45
  yaw_direction: positive_reveals_subject_right
  visible_side: subject_right
  asymmetry_validation_required: true
```

Invalidation rules:
- If `pitch` or `roll` is not zero, do not apply numeric yaw-only width checks.
- If the image uses strong perspective, mark projection reliability as `low_confidence`.
- If arms, weapons, cloak, skirt, wings, or props extend the silhouette, separate body envelope from accessory envelope.
- If the pose is foreshortened, do not extract canon limb length from it.

## Clarifying Questions

Ask only questions that change the canon:

```text
1. Which image should be treated as the primary canon source?
2. Are the shoulder-width differences intentional variants or drift?
3. Should the side depth be inferred from Image 2, or do you have a true side-view reference?
4. Is this weapon permanent canon or scene-specific?
5. Should the distorted action pose be excluded from proportion measurements?
```

If the user does not answer, mark the field as `needs_confirmation`, keep it out of `immutable`, and continue with a provisional ontology plus `$imagegen` prompt pack when safe.

Use `question_queue` instead of bare questions when answers affect canon state:

```yaml
clarification_gate:
  status: proceeding_with_provisional
  reason: canon_candidate_not_yet_approved_but_safe_for_provisional_handoff
  mode: immediate_provisional_progression
  hard_stop: false

question_queue:
  - id: Q_SampleSkate_001
    question: Image_SampleSkate_001을 approved canon source로 승격할까요?
    type: canon_source_approval
    blocking_for_ready: true
    blocking_for_provisional: false
    affects:
      - canon_assertions.*.source_role
      - canon_assertions.*.canon_status
      - Confirmed constraints
      - Handoff status
    default_if_unanswered: keep_provisional
```

If a question prevents only a ready handoff, ask the queue in chat and continue with `Handoff status: provisional`. Stop only when `hard_stop: true`, such as no usable canon candidate, conflicting identity-critical sources, or a user request for confirmed-only output.

## User Answer Application

When the user replies, convert the answer into provenance before recomputing the prompt pack:

```yaml
user_answers:
  - id: UA_SampleSkate_001
    answers_question: Q_SampleSkate_001
    applies_to_assertion: ASSERT_SampleSkate_001
    value: keep_as_candidate
    asserted_by: user
    confidence: user_confirmed
    recorded_in_turn: current_conversation
```

Then update affected assertions and handoff fields:
- `approve_as_canon` or approval-payload `approve` promotes matching observed assertions to `approval_status: approved`, `confidence: user_confirmed`, and `canon_status: confirmed`.
- `keep_as_candidate` leaves matching observed assertions in `Provisional constraints`.
- `reference_only` keeps the image out of `immutable` and hard `$imagegen` constraints.
- `exact_text_required` may populate `Text (verbatim)`; it enters `Confirmed constraints` only after the linked assertion is approved.

## `$imagegen` Handoff

Include this line in proportion-critical prompt packs:

```text
View/proportion lock: orthographic or low-distortion camera; yaw <degrees>, yaw direction <subject-left/right convention>, visible side <subject_left/subject_right/centered/back>, pitch <degrees>, roll <degrees>; fixed canvas height <height_units>; per-landmark derived projected widths <calculated values or needs_confirmation>; maintain canon head-to-body ratio and limb lengths; no wide-angle distortion or oversized foreground body parts.
```

Also include execution and certainty fields:

```text
Handoff status: <ready | provisional | blocked>
Imagegen execution: mode=<generate | edit>; input_roles=<reference image/edit target/style reference>; output_aspect=<ratio or size>; transparent_required=<true | false>; variants=<count>; postprocess=<none | chroma-key removal | native transparency fallback>
Confirmed constraints: <assertions with approval_status approved and user_answers provenance only>
Provisional constraints: <inferred or low-confidence guidance>
Generation constraints: <request-local technical constraints, not canon>
Unresolved questions: <needs_confirmation items and canon blockers>
```

If canon-critical conflicts remain, set `Handoff status` to `blocked` or `provisional`. Do not put unresolved details in `Confirmed constraints`.

Use this handoff status matrix:

```yaml
ready:
  - all identity-critical assertions are confirmed through approval_status: approved
  - canon_lock_state is locked or no canon lock is required for the requested artifact
  - no required view/proportion dimensions are missing
provisional:
  - one usable canon candidate exists but is not yet approved
  - only non-critical style, material, accessory, or atmosphere details remain inferred
  - requested output can proceed while uncertainty is explicit
blocked:
  - no usable canon candidate exists
  - canon candidates conflict on face identity, required text, subject-left/right detail, faction mark, or core proportions
  - required dimensions or identity-critical facts are missing for the requested output
```

For reference sheets:

```text
View/proportion lock: orthographic turnaround sheet, neutral camera height, fixed canvas height 1000 units, preserve canon head-to-body ratio, use calculated projected widths for each view, no wide-angle distortion.
```

For dynamic scenes:

```text
View/proportion lock: low-distortion perspective, maintain canon proportions and natural view-based width change, avoid exaggerated foreshortening unless explicitly requested.
```

## Canon Assertion Provenance

Create provenance records for important facts:

```yaml
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
```
