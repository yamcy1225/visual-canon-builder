# Visual Canon Templates

Use these templates when `$visual-canon-builder` needs a fuller reusable structure. Keep English keys for portability and Korean values/checklists when that matches the user's creative workflow.

## Contents

- Character Canon Ontology
- Faction Or World Canon Ontology
- Semantic Relations And Provenance
- Interactive Clarification Loop
- Projection Rules Template
- Validation Shapes
- Handoff Status Rules
- `$imagegen` Prompt Pack
- Cutout / Transparent-Background Prompt Add-On
- Validation Checklist
- Canon Promotion Flow

## Character Canon Ontology

```yaml
entity_type: Character
id: CHR_001
name: <character name>
version: 1.0.0

semantic_mapping:
  class: Character
  individual: CHR_001
  property_model: nested_yaml_fields
  relation_model: relations
  constraint_model: validation_shapes
  provenance_model: canon_assertions

identity:
  role: <playable_character | npc | boss | mascot | etc>
  faction: <faction id or name>
  visual_age_range: <visual age range>
  personality_keywords:
    - <keyword>

visual_core:
  silhouette:
    value: <slim_vertical | broad_armored | small_round | etc>
    immutable: true
  body:
    head_body_ratio: <ratio or descriptor>
    shoulder_width: <descriptor>
    leg_length: <descriptor>
    hand_size: <descriptor>
  face:
    eye_shape: <descriptor>
    eye_color: <canon color>
    unique_mark: <mark and location>
    jawline: <descriptor>
  hair:
    length: <descriptor>
    color: <canon color>
    bangs: <descriptor>
  costume:
    palette:
      primary: <canon color>
      secondary: <canon color>
      accent: <canon color>
    materials:
      - <material>
    must_have:
      - <required element>
    forbidden:
      - <forbidden element>

orientation_conventions:
  left_right_basis: subject_left_subject_right
  mirror_validation: required_for_asymmetric_details
  asymmetric_details:
    - <subject_left / subject_right detail>

relations:
  - subject: <entity id>
    predicate: <relation predicate>
    object: <entity id or value>

canon_assertions:
  - id: ASSERT_001
    subject: <entity id>
    predicate: <property or relation>
    object: <value>
    source_image_id: <Image id or user_answer id>
    source_role: <approved canon source | canon candidate | reference image | variant | style reference | user confirmation>
    confidence: <observed | inferred | low_confidence | needs_confirmation | user_confirmed>
    canon_status: <confirmed | provisional | unresolved | rejected>
    asserted_by: visual-canon-builder
    derived_from: <analysis id or question id>
    needs_confirmation: <true | false>

clarification_gate:
  status: <none | waiting_for_user | resolved>
  reason: <why answers are needed or none>

question_queue:
  - id: <Q_001>
    question: <canon-critical user question>
    type: <canon_source_approval | variant_or_drift | exact_text | prop_permanence | measurement_source | forbidden_rule>
    blocking: <true | false>
    affects:
      - <field or assertion id>
    required_for:
      - <ready_handoff | confirmed_constraints | proportion_lock>
    default_if_unanswered: <keep_provisional | keep_unresolved | block_ready_handoff>

user_answers:
  - id: <UA_001>
    answers_question: <Q_001>
    value: <user answer>
    asserted_by: user
    confidence: user_confirmed
    recorded_in_turn: current_conversation

proportion_model:
  units: height_units
  measurement_protocol:
    basis: <orthographic reference sheet | low-distortion image | user supplied>
    full_height_includes: <body_top_to_sole_without_hair_hat_or_weapon | specified otherwise>
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
    do_not_measure_from:
      - wide_angle_perspective
      - foreshortened_action_pose
      - cropped_body
      - heavy_cloak_or_flared_costume_only
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
  confidence:
    front_widths: <observed | inferred | needs_confirmation>
    side_depths: <observed | inferred | needs_confirmation>
    limb_lengths: <observed | inferred | needs_confirmation>

projection_rules:
  formula_type: orthographic_envelope_estimate
  width_formula_per_landmark: projected_width = abs(front_width * cos(yaw)) + abs(side_depth * sin(yaw))
  yaw_units: degrees
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
    - low-distortion perspective only for dynamic scenes

view_spec:
  view_type: <front | side | back | three_quarter | custom>
  yaw: <0 | 45 | 90 | custom degrees>
  yaw_direction: <positive_reveals_subject_right | positive_reveals_subject_left | none>
  visible_side: <subject_left | subject_right | centered | back>
  pitch: 0
  roll: 0
  camera_mode: <orthographic | low-distortion perspective>
  fixed_canvas_height: 1000
  derived_projected_widths:
    head: <calculated or needs_confirmation>
    shoulder: <calculated or needs_confirmation>
    torso: <calculated or needs_confirmation>
    hip: <calculated or needs_confirmation>
    costume_envelope: <calculated or needs_confirmation>
  numeric_width_check: <valid | invalid | low_confidence | needs_confirmation>
  asymmetry_validation_required: <true | false>

immutable:
  - <must-never-change visual rule>

allowed_variation:
  - <scene-dependent change allowed>

forbidden:
  - <visual drift or prohibited element>

canon_references:
  - front view sheet
  - side view sheet
  - back view sheet
  - face close-up
  - costume detail sheet
  - weapon or prop sheet
  - color palette
  - silhouette sheet
  - forbidden examples

validation_checks:
  identity:
    - <Korean checklist item>
  proportion:
    - 전체 키가 fixed_canvas_height 기준에 맞는가?
    - 머리:몸 비율이 유지되는가?
    - 시점별 폭이 projection_rules와 크게 어긋나지 않는가?
  costume:
    - <Korean checklist item>
  forbidden:
    - <Korean checklist item>

validation_shapes:
  - target: <entity id>
    path: <property path>
    constraint: <equals / min_count / max_count / must_not_be_confirmed_from_front_only_image / custom rule>
    severity: <pass | fix | reject | needs_confirmation | blocked>
    message: <Korean validation message>
```

## Faction Or World Canon Ontology

```yaml
entity_type: Faction
id: FCT_001
name: <faction name>
version: 1.0.0

semantic_mapping:
  class: Faction
  individual: FCT_001
  property_model: visual_language
  relation_model: relations
  constraint_model: validation_shapes
  provenance_model: canon_assertions

identity:
  role_in_world: <kingdom | guild | cult | company | school | etc>
  tone_keywords:
    - <keyword>

visual_language:
  palette:
    primary: <canon color>
    secondary: <canon color>
    accent: <canon color>
  symbols:
    - <symbol>
  shapes:
    - <shape language>
  materials:
    - <material>
  architecture:
    - <architectural motif>
  costume_rules:
    - <dress rule>
  ui_or_icon_rules:
    - <icon or interface motif>

relations:
  - subject: <character or asset id>
    predicate: hasFaction
    object: FCT_001
  - subject: <Image id>
    predicate: depictsFactionVisualLanguage
    object: FCT_001

canon_assertions:
  - id: ASSERT_FCT_001
    subject: FCT_001
    predicate: hasPalette
    object: <palette token or value>
    source_image_id: <Image id or user_answer id>
    source_role: <approved canon source | canon candidate | reference image | variant | style reference | user confirmation>
    confidence: <observed | inferred | low_confidence | needs_confirmation | user_confirmed>
    canon_status: <confirmed | provisional | unresolved | rejected>
    asserted_by: visual-canon-builder
    derived_from: <analysis id or question id>
    needs_confirmation: <true | false>

immutable:
  - <must-keep faction/world rule>

allowed_variation:
  - <regional, rank, class, or asset-type variation>

forbidden:
  - <color, symbol, style, or material that breaks canon>

canon_references:
  - faction emblem sheet
  - palette sheet
  - architecture sheet
  - costume rank sheet
  - forbidden examples

validation_checks:
  faction_identity:
    - 세력 색상과 문양이 유지되는가?
  world_consistency:
    - 지역/시대/재질 규칙이 깨지지 않았는가?
  forbidden:
    - 금지 색상, 금지 문양, 금지 실루엣이 생기지 않았는가?

validation_shapes:
  - target: FCT_001
    path: visual_language.palette.primary
    constraint: equals <canon color>
    severity: <pass | fix | reject | needs_confirmation | blocked>
    message: 세력 대표 색상이 정본과 다르면 시각 언어가 흔들린다.
  - target: FCT_001
    path: visual_language.symbols
    constraint: min_count 1
    severity: needs_confirmation
    message: 세력 문양이 정본으로 확정되지 않았다.
```

## Semantic Relations And Provenance

Use graph-style relations when nested YAML would hide important links between characters, images, factions, variants, and approvals.

```yaml
relations:
  - subject: CHR_001
    predicate: hasFaction
    object: FCT_001
  - subject: Image_001
    predicate: depicts
    object: CHR_001
  - subject: CHR_001_Winter
    predicate: variantOf
    object: CHR_001
  - subject: Approval_001
    predicate: approves
    object: ASSERT_001

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

Use this semantic mapping:

```yaml
semantic_mapping:
  class: entity_type
  individual: id
  property: nested visual/proportion/style fields
  relation: relations subject-predicate-object records
  constraint: validation_shapes
  provenance: canon_assertions source/confidence fields
```

## Interactive Clarification Loop

Use this when canon-critical decisions require user input before a ready handoff.

```yaml
clarification_gate:
  status: waiting_for_user
  reason: blocking_questions_prevent_ready_handoff

question_queue:
  - id: Q_001
    question: Which image is the approved canon source?
    type: canon_source_approval
    blocking: true
    affects:
      - canon_assertions.*.source_role
      - Confirmed constraints
    required_for:
      - ready_handoff
    default_if_unanswered: keep_provisional

user_answers:
  - id: UA_001
    answers_question: Q_001
    value: Image_001 is approved canon
    asserted_by: user
    confidence: user_confirmed
    recorded_in_turn: current_conversation

relations:
  - subject: UA_001
    predicate: answersQuestion
    object: Q_001
  - subject: ASSERT_001
    predicate: wasDerivedFrom
    object: UA_001
```

## Projection Rules Template

Use this when a character, prop, vehicle, monster, or icon must preserve natural proportions across front, side, back, and angled views.

```yaml
proportion_lock:
  measurement_basis: orthographic reference sheet
  units: height_units
  fixed_canvas_height: 1000
  formula_type: orthographic_envelope_estimate
  front_widths:
    head_width_front: <number>
    shoulder_width_front: <number>
    torso_width_front: <number>
    hip_width_front: <number>
  side_depths:
    head_depth_side: <number or needs_confirmation>
    shoulder_depth_side: <number or needs_confirmation>
    torso_depth_side: <number or needs_confirmation>
    hip_depth_side: <number or needs_confirmation>
    body_depth_side: <number or needs_confirmation>
    costume_or_shell_depth_side: <number or needs_confirmation>
  projection_formula_per_landmark: projected_width = abs(front_width * cos(yaw)) + abs(side_depth * sin(yaw))
  yaw_direction_convention:
    positive_yaw_reveals: subject_right
    negative_yaw_reveals: subject_left
  valid_when:
    - yaw_only_turnaround
    - pitch_is_0
    - roll_is_0
  invalid_or_low_confidence_when:
    - pitch_or_roll_present
    - strong_perspective
    - foreshortened_pose
    - arms_or_weapon_extend_silhouette
    - cloak_or_skirt_flare_changes_envelope
  examples:
    front_yaw_0: each_projected_width = matching_front_width
    side_yaw_90: each_projected_width = matching_side_depth
    three_quarter_yaw_45: each_projected_width = 0.707 * matching_front_width + 0.707 * matching_side_depth
  camera_rules:
    reference_sheets:
      - orthographic
      - neutral camera height
      - no wide-angle distortion
    dynamic_scenes:
      - maintain canon proportions
      - use low-distortion perspective
      - avoid oversized hands, face, weapon, or foreground limbs unless explicitly requested
```

## Validation Shapes

Use these alongside human-readable checklists when a rule needs a target, severity, and repeatable path.

```yaml
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
    message: 좌우 비대칭 표식은 subject_left/subject_right 기준으로 기록한다.
```

## Handoff Status Rules

```yaml
handoff_status_rules:
  ready:
    - all identity-critical assertions are confirmed
    - canon source, required text, palette, left/right details, and required proportions are resolved
    - no reject or blocked validation shape is unresolved
  provisional:
    - one usable canon candidate exists but is not yet approved
    - only non-critical style, material, accessory, or atmosphere details remain inferred
    - requested output can proceed while uncertainty is explicit
    - unresolved details are listed in Provisional constraints or Unresolved questions
  blocked:
    - no usable canon candidate exists
    - canon candidates conflict on face identity, faction mark, required text, subject-left/right detail, or core proportions
    - required dimensions or identity-critical facts are missing for the requested output
```

## `$imagegen` Prompt Pack

```text
Use case: <imagegen taxonomy slug>
Asset type: <where this asset will be used>
Primary request: <requested image>
Handoff status: <ready | provisional | blocked>
Imagegen execution: mode=<generate | edit>; input_roles=<reference image/edit target/style reference>; output_aspect=<ratio or size>; transparent_required=<true | false>; variants=<count>; postprocess=<none | chroma-key removal | native transparency fallback>
Input images: <Image 1: reference image; Image 2: edit target; Image 3: style reference> (optional)
Scene/backdrop: <environment or chroma-key background>
Subject: <main subject and canon identity>
Style/medium: <photo, illustration, concept art, sprite, icon, etc>
Composition/framing: <view, crop, layout, camera>
View/proportion lock: <camera mode, yaw direction, visible side, pitch/roll, fixed height, per-landmark derived projected widths, distortion constraints>
Lighting/mood: <lighting and emotion>
Color palette: <canon palette>
Materials/textures: <canon materials>
Text (verbatim): "<exact text, if any>"
Confirmed constraints: <user-confirmed canon, approved-canon-source facts, or clearly declared canon-candidate facts only>
Provisional constraints: <useful but unresolved details; label source role and do not present as hard canon>
Unresolved questions: <canon-critical blockers or needs_confirmation items>
Avoid: <confirmed forbidden rules, request-local prohibitions, drift risks, watermark, unwanted text>
```

## Cutout / Transparent-Background Prompt Add-On

Use this add-on when the intended result is a sprite, sticker, item cutout, transparent asset, or background-extraction task.

```text
Scene/backdrop: flat solid #00ff00 background; perfectly uniform chroma-key field for background removal
Confirmed constraints: full subject visible, crisp separated edges, generous padding, no cast shadow, no contact shadow, no reflection, no background texture, do not use #00ff00 anywhere in the subject
Avoid: shadows, floor plane, gradients, key-color clothing or effects, watermark, extra text
```

## Validation Checklist

```text
[Identity Check]
- 핵심 얼굴, 실루엣, 색상, 문양이 정본과 일치하는가?
- 캐릭터/세력/아이템의 고유 표식이 올바른 위치에 있는가?

[Variation Check]
- 이번 장면에서 허용된 변주만 적용되었는가?
- 포즈, 날씨, 손상, 표정 변화가 정체성을 침범하지 않는가?

[Proportion Check]
- 전체 키가 기준 캔버스 높이에 맞는가?
- 머리:몸 비율이 유지되는가?
- 측면/3/4뷰 폭이 투영 규칙과 크게 어긋나지 않는가?
- 어깨/골반/머리 폭이 시점 변화에 맞게 자연스럽게 줄거나 넓어졌는가?
- 원근 때문에 손, 얼굴, 무기만 과도하게 커지지 않았는가?

[Forbidden Check]
- 금지 색상, 금지 장식, 금지 의상, 금지 스타일이 생기지 않았는가?
- 다른 캐릭터나 세력의 시각 언어가 섞이지 않았는가?

[Imagegen Prompt Check]
- `Confirmed constraints`에는 확인된 immutable 규칙만 들어갔는가?
- 미확정 요소가 `Provisional constraints` 또는 `Unresolved questions`에 남아 있는가?
- `Avoid`에 모든 forbidden 규칙이 들어갔는가?
- 레퍼런스 이미지 역할이 `reference image`, `edit target`, `style reference`처럼 명확한가?
```

## Canon Promotion Flow

```text
generated -> reviewed -> corrected -> approved -> canon
```

- `generated`: 생성 직후. 아직 정본이 아니다.
- `reviewed`: 체크리스트로 검수된 상태.
- `corrected`: 수정 또는 재생성 지시가 반영된 상태.
- `approved`: 사람이 정본 후보로 승인한 상태.
- `canon`: 이후 프롬프트와 레퍼런스의 기준으로 사용할 수 있는 상태.

Rejected images can become `forbidden examples` if they clearly show a drift pattern to avoid.
