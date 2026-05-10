# Visual Canon Templates

Use these templates when `$visual-canon-builder` needs a fuller reusable structure. Keep English keys for portability and Korean values/checklists when that matches the user's creative workflow.

## Contents

- Character Canon Ontology
- Faction Or World Canon Ontology
- Semantic Relations And Provenance
- Projection Rules Template
- Validation Shapes
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
    source_role: <canon candidate | variant | style reference | user confirmation>
    confidence: <observed | inferred | low_confidence | needs_confirmation>
    asserted_by: visual-canon-builder
    derived_from: <analysis id or question id>
    needs_confirmation: <true | false>

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
    do_not_measure_from:
      - wide_angle_perspective
      - foreshortened_action_pose
      - cropped_body
      - heavy_cloak_or_flared_costume_only
  anatomical_proportion:
    full_height: 1000
    head_height: <observed or needs_confirmation>
    arm_length: <observed or needs_confirmation>
    leg_length: <observed or needs_confirmation>
  costume_silhouette_envelope:
    shoulder_width_front: <observed or needs_confirmation>
    torso_width_front: <observed or needs_confirmation>
    hip_width_front: <observed or needs_confirmation>
    body_depth_side: <observed or needs_confirmation>
  full_height: 1000
  head_height: <observed or needs_confirmation>
  head_width_front: <observed or needs_confirmation>
  shoulder_width_front: <observed or needs_confirmation>
  torso_width_front: <observed or needs_confirmation>
  hip_width_front: <observed or needs_confirmation>
  body_depth_side: <observed or needs_confirmation>
  head_depth_side: <observed or needs_confirmation>
  arm_length: <observed or needs_confirmation>
  leg_length: <observed or needs_confirmation>
  confidence:
    front_widths: <observed | inferred | needs_confirmation>
    side_depths: <observed | inferred | needs_confirmation>
    limb_lengths: <observed | inferred | needs_confirmation>

projection_rules:
  formula_type: orthographic_envelope_estimate
  width_formula: projected_width = abs(front_width * cos(yaw)) + abs(side_depth * sin(yaw))
  yaw_units: degrees
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
  pitch: 0
  roll: 0
  camera_mode: <orthographic | low-distortion perspective>
  fixed_canvas_height: 1000
  derived_projected_width: <calculated or needs_confirmation>
  numeric_width_check: <valid | invalid | low_confidence | needs_confirmation>

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
    severity: <pass | fix | reject | needs_confirmation>
    message: <Korean validation message>
```

## Faction Or World Canon Ontology

```yaml
entity_type: Faction
id: FCT_001
name: <faction name>
version: 1.0.0

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
    source_role: canon candidate
    confidence: observed
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
    body_depth_side: <number or needs_confirmation>
  projection_formula: projected_width = abs(front_width * cos(yaw)) + abs(side_depth * sin(yaw))
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
    front_yaw_0: projected_width = front_width
    side_yaw_90: projected_width = side_depth
    three_quarter_yaw_45: projected_width = 0.707 * front_width + 0.707 * side_depth
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
View/proportion lock: <camera mode, yaw/pitch/roll, fixed height, derived projected width, distortion constraints>
Lighting/mood: <lighting and emotion>
Color palette: <canon palette>
Materials/textures: <canon materials>
Text (verbatim): "<exact text, if any>"
Confirmed constraints: <confirmed immutable rules, canon lock, must keep>
Provisional constraints: <useful but unresolved details; do not present as hard canon>
Unresolved questions: <canon-critical blockers or needs_confirmation items>
Avoid: <forbidden rules, drift risks, watermark, unwanted text>
```

## Cutout / Transparent-Background Prompt Add-On

Use this add-on when the intended result is a sprite, sticker, item cutout, transparent asset, or background-extraction task.

```text
Scene/backdrop: flat solid #00ff00 background; perfectly uniform chroma-key field for background removal
Constraints: full subject visible, crisp separated edges, generous padding, no cast shadow, no contact shadow, no reflection, no background texture, do not use #00ff00 anywhere in the subject
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
