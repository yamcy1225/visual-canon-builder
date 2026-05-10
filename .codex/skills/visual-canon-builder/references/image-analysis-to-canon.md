# Image Analysis To Canon

Use this reference when `$visual-canon-builder` receives one or more images and needs to turn visual evidence into canon documentation, proportion rules, and `$imagegen` prompt packs.

## Contents

- Input Handling
- Image Inventory
- Observation Rules
- Canon Confirmation Gate
- Single Image Analysis
- Multiple Image Comparison
- Proportion Extraction
- View Projection
- Clarifying Questions
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

inferred_or_uncertain:
  body_depth_side: needs_confirmation
  back_design: needs_confirmation
  exact_material: inferred_matte_silk_low_confidence
```

Use confidence labels:
- `observed`: directly visible and reliable.
- `inferred`: likely, but not directly confirmed.
- `low_confidence`: distorted, obscured, or stylized enough to be risky.
- `needs_confirmation`: canon decision requires the user.
- `user_confirmed`: the user explicitly approved the assertion as canon.

## Canon Confirmation Gate

Do not treat every observed detail as confirmed canon. A fact can enter `Confirmed constraints` only when the assertion has both reliable confidence and an approved source role.

```yaml
confirmation_gate:
  confirmed_constraints_allowed_when:
    - confidence: user_confirmed
    - confidence: observed
      source_role: approved canon source
    - confidence: observed
      source_role: canon candidate
      request_context: clearly_declared_as_canon
  provisional_constraints_when:
    - confidence: observed
      source_role: reference image
    - confidence: observed
      source_role: canon candidate
      request_context: not_yet_approved
    - confidence: inferred
    - confidence: low_confidence
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

If the user does not answer and work must continue, mark the field as `needs_confirmation` and keep it out of `immutable`.

## `$imagegen` Handoff

Include this line in proportion-critical prompt packs:

```text
View/proportion lock: orthographic or low-distortion camera; yaw <degrees>, yaw direction <subject-left/right convention>, visible side <subject_left/subject_right/centered/back>, pitch <degrees>, roll <degrees>; fixed canvas height <height_units>; per-landmark derived projected widths <calculated values or needs_confirmation>; maintain canon head-to-body ratio and limb lengths; no wide-angle distortion or oversized foreground body parts.
```

Also include execution and certainty fields:

```text
Handoff status: <ready | provisional | blocked>
Imagegen execution: mode=<generate | edit>; input_roles=<reference image/edit target/style reference>; output_aspect=<ratio or size>; transparent_required=<true | false>; variants=<count>; postprocess=<none | chroma-key removal | native transparency fallback>
Confirmed constraints: <user-confirmed canon, observed facts from approved canon sources, or observed canon-candidate facts when the request clearly declares the source as canon>
Provisional constraints: <inferred or low-confidence guidance>
Unresolved questions: <needs_confirmation items and canon blockers>
```

If canon-critical conflicts remain, set `Handoff status` to `blocked` or `provisional`. Do not put unresolved details in `Confirmed constraints`.

Use this handoff status matrix:

```yaml
ready:
  - all identity-critical assertions are confirmed
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
```
