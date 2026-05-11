# Visual Canon Templates

Use these templates when `$visual-canon-builder` needs a fuller reusable structure. Keep English keys for portability and Korean values/checklists when that matches the user's creative workflow.

## Contents

- Character Canon Ontology
- Faction Or World Canon Ontology
- Semantic Relations And Provenance
- Style Canon Model
- Generation Contract
- Evaluation Loop
- Guided Approval Interview
- User Review First
- Evidence Interview RAG Mode
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

style_fidelity_model:
  source_style_role: <approved_reference_sheet_style | style_reference | user_declared_style>
  rendering_mode:
    value: <flat_2d_character_sheet_line_art | sketch_line_art | cel_animation | etc>
    immutable: <true | false>
  line_quality:
    outer_contour: <clean_bold_black_line | rough_sketch_line | etc>
    interior_lines: <simple_thin_black_detail_lines | hatching | etc>
  shading:
    allowed: <minimal_flat_grayscale | none | cel_shadow_only>
    forbidden:
      - <semi_realistic_soft_airbrush_shading>
      - <3d_render_lighting>
      - <glossy_material_highlights>
  detail_density:
    value: <match_reference_sheet_simplification>
    forbidden:
      - <realistic_product_rendering>
      - <extra_fashion_illustration_detail>
  style_drift_forbidden:
    - <semi_realistic_character_art>
    - <3d_or_clay_render>
    - <adult_anatomical_proportions>

reference_preserve_model:
  mode: <off | identity_preserve | edit_target_preserve>
  source_cell_asset:
    required: <true | false>
    crop_id: <CROP_001 or null>
    asset_path: <path or attached image id or null>
    full_sheet_only: <allowed | blocked_for_exact_preservation>
  source_cell:
    source_id: <SRC_Image_001>
    region: <front_full_body | side_full_body | expression_head | prop_crop>
    role: <proportion_and_style_anchor | edit_target | identity_reference>
  preserve:
    - silhouette
    - head_body_ratio
    - limb_length
    - shoe_simplification
    - line_style
    - detail_density
  allowed_change:
    - <pose | expression | shirt_text | minor_hand_position>
  forbidden_change:
    - body_redesign
    - elongated_adult_proportions
    - realistic_product_detail

style_canon:
  id: <STYLE_001>
  source_images:
    - <SRC_Image_001>
  style_role: <identity_bound_style | style_reference | mood_reference | loose_inspiration>
  line_language:
    contour_weight: <thin | medium | bold | variable>
    contour_variation: <uniform | tapered_pressure | sketchy | none>
    interior_line_density: <sparse | medium | dense>
    edge_softness: <vector_sharp | clean_but_not_vector_sharp | painterly_soft>
    forbidden:
      - <thick_comic_outline>
      - <sketchy_noise_lines>
  rendering_language:
    medium: <flat_2d | cel_animation | painterly | 3d_render | photo | ink_sketch>
    shading_model: <none | flat_grayscale | cel_shadow | soft_cel | painterly_blend | volumetric>
    detail_density: <low | medium_low | medium | high>
    surface_finish: <matte | satin | glossy>
    forbidden:
      - <glossy_3d_render>
      - <hyperreal_skin_texture>
  color_language:
    saturation: <muted | reference_matched | vivid | neon>
    value_range: <low_key | mid_to_high | broad>
    temperature: <warm | neutral | cool | mixed>
    palette_drift_tolerance: <none | low | medium>
  lighting_language:
    direction: <front | front_left | top | ambient | scene_specific>
    contrast: <gentle | moderate | harsh>
    mood: <calm | playful | dramatic | eerie | etc>
  camera_language:
    camera_height: <neutral | low | high>
    lens_feel: <orthographic | low_distortion | portrait_lens | wide_angle>
    perspective_strength: <none | low | moderate | strong>
  identity_style_binding:
    style_is_part_of_identity: <true | false>
    must_preserve_across:
      - <new_pose | new_scene | outfit_variant>

generation_contract:
  id: <GEN_001>
  task_sensitivity: <identity_sensitive | style_sensitive | loose_inspiration>
  default_mode: <edit_or_reference_image | reference_image_preferred | text_generate_allowed>
  text_generate_allowed: <true | false>
  reference_policy:
    identity_anchor: <SRC_Image_001 or null>
    style_anchor: <SRC_Image_001 or null>
    composition_reference: <SRC_Image_002 or null>
    forbidden_examples:
      - <SRC_Bad_001>
  change_budget:
    identity: <0_percent | low | open>
    style: <0_to_5_percent | low | open>
    pose: <locked | allowed_if_requested | open>
    background: <locked | allowed_if_requested | open>
    costume: <locked | requested_change_only | open>
  mutation_policy:
    allowed_to_change:
      - <user_requested_change>
    must_not_change:
      - <face_geometry>
      - <head_body_ratio>
      - <line_language>
      - <palette>
  invariant_restatement:
    required_every_prompt: true
    lines:
      - <Preserve the exact same character identity from the reference image.>
      - <Only change: requested_change.>

api_execution_profile:
  preferred_api: <responses_api | image_api>
  reason: <multi_turn_reference_preserving_workflow | single_prompt_generation>
  model_family: gpt_image
  action: <auto | generate | edit>
  input_fidelity: <high | low>
  reference_ordering:
    first_image: <identity_anchor_or_source_cell_asset>
    second_image: <style_anchor_if_separate_or_null>
    later_images:
      - <composition_reference>
      - <prop_reference>
      - <forbidden_example>
  mask:
    required: <true | false>
    use_when:
      - localized_edit
      - exact_text_change
      - expression_or_arm_position_change
    rule: mask_targets_change_area_only_keep_rest_preserved
  output:
    size: <auto_or_requested>
    format: <png | webp | jpeg>
    background: <transparent | opaque | auto>

source_cell_asset_manifest:
  id: <CROP_001>
  crop_id: <CROP_001>
  source_image_id: <SRC_Image_001>
  source_region:
    label: <front_full_body | side_full_body | expression_head | prop_crop>
    bbox:
      x: <number or needs_user_or_script>
      y: <number or needs_user_or_script>
      width: <number or needs_user_or_script>
      height: <number or needs_user_or_script>
  asset_path: <path | attached image id | null>
  role:
    - identity_anchor
    - style_anchor
    - proportion_anchor
  preservation_priority:
    - silhouette
    - head_body_ratio
    - limb_length
    - line_weight
    - detail_density
  ready_state: <ready | coordinates_ready_crop_not_verified | blocked_until_crop_exists>

exact_text_policy:
  text_required: <true | false>
  text_source:
    assertion_id: <ASSERT_Text_001>
    approval_status: <approved | pending_user_approval>
  rendering_strategy:
    primary: <image_edit_with_mask | postprocess_compositing | no_exact_text_needed>
    fallback: <generate_without_text_then_add_text_in_postprocess>
  validation:
    reject_when:
      - misspelled_text
      - wrong_case
      - wrong_placement_changes_design

evaluation_contract:
  after_each_generation:
    - assign_generated_image_id
    - compare_against_identity_anchor
    - compare_against_style_anchor
    - classify_result
    - record_drift_patterns
    - produce_prompt_patch
  drift_taxonomy:
    identity_drift:
      - face_geometry_changed
      - head_body_ratio_changed
      - silhouette_changed
    style_drift:
      - line_weight_changed
      - shading_model_changed
      - palette_temperature_changed
    semantic_drift:
      - missing_symbol
      - wrong_left_right
      - added_forbidden_prop
  retry_rules:
    pass: ask_user_for_approval_before_canon_promotion
    fix: generate_targeted_edit_prompt_or_prompt_patch
    reject: keep_out_of_canon_and_consider_forbidden_example

orientation_conventions:
  left_right_basis: subject_left_subject_right
  mirror_validation: required_for_asymmetric_details
  asymmetric_details:
    - <subject_left / subject_right detail>

relations:
  - subject: <entity id>
    predicate: <relation predicate>
    object: <entity id or value>

guided_approval_interview:
  status: <awaiting_user_decision | applying_answer | complete>
  current_question_index: <1-based index>
  total_questions: <count>
  current_question:
    id: <QAPP_001>
    label: <사용자용 결정 항목>
    asks: <자연어 승인 질문>
    recommendation: <choice key>
    choices:
      - key: "1"
        label: <승인 | 수정해서 승인 | 임시 유지 | 거절>
        effect: <affected assertions and status change>
    reply_hint: <숫자 또는 짧은 수정 답변 안내>
  answered:
    - question_id: <QAPP_000>
      answer: <user answer or null>
      user_answer_id: <UA_000 or null>

user_review:
  status: <초안 준비됨; 아직 정본 잠금 전 | 일부 승인됨 | 정본 잠금 완료>
  evidence_scope: current_conversation_only
  found:
    - <사용자가 바로 이해할 수 있는 관찰 요약>
  needs_decision:
    - label: <캐릭터 정체성 | 기본 의상 | 고정 소품 | 정확한 문구 등>
      covers:
        - <ASSERT_001>
      recommendation: <approve | reject | revise | keep_provisional>
      reason: <추천 이유>
  fast_reply:
    - "추천대로 진행"
    - "전체 정본 승인"
    - "정체성과 의상은 승인, 소품은 임시"
    - "수정: <항목>=<새 값>"

quick_approval_table:
  - label: <사용자용 결정 항목>
    recommendation: <승인 | 수정 | 거절 | 임시>
    reason: <짧은 이유>
    reply_example: <짧은 자연어 답변>

source_inventory:
  retrieval_scope: current_conversation_only
  sources:
    - id: <SRC_001>
      type: <attached_image | local_image | user_note>
      role: <canon candidate | reference image | instruction>
      description: <short source description>

evidence_cards:
  - id: <EV_001>
    source_id: <SRC_001>
    modality: <image | text | mixed>
    region_or_note: <visible region, crop description, or note span>
    source_anchor: <image label, page, message id, or note id>
    view_label: <front | side | back | expression | prop | text_note | mixed>
    bbox_or_region: <pixel bbox, crop id, or descriptive_region_no_pixel_bbox>
    source_text_span: <quoted note span or null>
    observation: <directly observed fact>
    confidence: <observed | inferred | low_confidence | needs_confirmation>
    usable_for:
      - <identity | proportion | costume | prop | style | text>
    limitations:
      - <what this evidence cannot prove>

canon_assertions:
  - id: ASSERT_001
    subject: <entity id>
    predicate: <property or relation>
    object: <value>
    assertion_version: <integer>
    value_hash: <stable hash or short fingerprint of subject/predicate/object>
    evidence_refs:
      - <EV_001>
    retrieval_scope: current_conversation_only
    source_image_id: <Image id or user_answer id>
    source_role: <approved canon source | canon candidate | reference image | variant | style reference | user confirmation>
    confidence: <observed | inferred | low_confidence | needs_confirmation | user_confirmed>
    canon_status: <confirmed | provisional | unresolved | rejected>
    approval_status: <pending_user_approval | approved | rejected | revised | keep_provisional>
    asserted_by: visual-canon-builder
    derived_from: <analysis id or question id>
    needs_confirmation: <true | false>

retrieval_trace:
  - assertion_id: <ASSERT_001>
    evidence_refs:
      - <EV_001>
    rationale: <why the evidence supports this assertion>

approval_review_pack:
  review_pack_id: <REVIEW_001>
  entity_id: <entity id>
  canon_lock_state: <unlocked | partially_locked | locked>
  derived_lock_state: true
  bulk_actions:
    - <approve_all_low_risk | keep_all_optional_provisional>
  items:
    - assertion_id: <ASSERT_001>
      assertion_version: <integer>
      value_hash: <stable hash or short fingerprint>
      evidence_refs:
        - <EV_001>
      current_value: <value to approve>
      recommended_action: <approve | reject | revise | keep_provisional>
      risk_tier: <identity_critical | canon_critical | optional | style_only>
      risk_if_wrong: <identity drift, text drift, proportion drift, etc>

approval_payload:
  review_pack_id: <REVIEW_001>
  applies_to: <entity id>
  answer_mode: <natural_language_first | batch_yaml>
  decisions:
    - assertion_id: <ASSERT_001>
      expected_assertion_version: <integer>
      expected_value_hash: <stable hash or short fingerprint>
      action: <approve | reject | revise | keep_provisional>
      revised_value: <new value or null>
      replacement_assertion_id: <ASSERT_002 or null>
      note: <optional note>

lock_summary:
  canon_lock_state: <unlocked | partially_locked | locked>
  derived_from_assertion_status: true
  pending: <count>
  approved: <count>
  rejected: <count>
  revised: <count>
  keep_provisional: <count>
  ready_for_final_canon: <true | false>

clarification_gate:
  status: <none | proceeding_with_provisional | waiting_for_user | resolved>
  reason: <why answers are needed or none>
  mode: <immediate_provisional_progression | hard_stop_wait | resolved>
  hard_stop: <true | false>

question_queue:
  - id: <Q_001>
    question: <canon-critical user question>
    type: <canon_source_approval | variant_or_drift | exact_text | prop_permanence | measurement_source | forbidden_rule>
    blocking_for_ready: <true | false>
    blocking_for_provisional: <true | false>
    affects:
      - <field or assertion id>
    required_for:
      - <ready_handoff | confirmed_constraints | proportion_lock>
    default_if_unanswered: <keep_provisional | keep_unresolved | block_ready_handoff>

user_answers:
  - id: <UA_001>
    answers_question: <Q_001>
    applies_to_assertion: <ASSERT_001>
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
  - subject: UA_Approval_001
    predicate: approves
    object: ASSERT_001

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
      - UA_Approval_001
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
  provenance: canon_assertions source/confidence/evidence_refs/approval_status fields
```

## Interactive Clarification Loop

Use this when canon-critical decisions require user input before a ready handoff. By default, continue with a provisional ontology and prompt pack unless `hard_stop: true`.

```yaml
clarification_gate:
  status: proceeding_with_provisional
  reason: blocking_questions_prevent_ready_but_not_provisional_handoff
  mode: immediate_provisional_progression
  hard_stop: false

question_queue:
  - id: Q_001
    question: Which image is the approved canon source?
    type: canon_source_approval
    blocking_for_ready: true
    blocking_for_provisional: false
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
  - target: canon_assertions[*]
    path: canon_status
    constraint: if equals confirmed then approval_status equals approved and user_answers provenance exists
    severity: reject
    message: confirmed assertion은 approved 상태와 사용자 승인 provenance 없이는 허용되지 않는다.
  - target: canon_assertions[*]
    path: evidence_refs
    constraint: min_count 1
    severity: reject
    message: 모든 candidate assertion은 최소 하나의 evidence card를 참조해야 한다.
  - target: approval_payload.decisions[*]
    path: expected_value_hash
    constraint: equals current assertion value_hash
    severity: blocked
    message: 오래된 approval payload로 정본을 잠그지 않는다.
```

## Handoff Status Rules

```yaml
handoff_status_rules:
  ready:
    - all identity-critical assertions are confirmed through approval_status: approved
    - canon_lock_state is locked or no canon lock is required for the requested artifact
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
Task sensitivity: <identity_sensitive | style_sensitive | loose_inspiration>
Primary request: <requested image>
Handoff status: <ready | provisional | blocked>
API execution profile: <preferred_api/action/input_fidelity/reference_ordering/mask/output>
Imagegen execution: mode=<edit | reference_generate | text_generate>; text_generate_allowed=<true | false>; reason=<why this mode is acceptable>; input_roles=<identity_anchor/style_anchor/edit_target/composition_reference/forbidden_example>; output_aspect=<ratio or size>; transparent_required=<true | false>; variants=<count>; postprocess=<none | chroma-key removal | native transparency fallback>
Reference preserve mode: <off | identity_preserve | edit_target_preserve>; source_cell=<front/full-body/expression/prop crop>; preserve=<silhouette, head/body ratio, limb length, line style, detail density>; allowed_change=<pose/expression/text only>
Source cell asset: <required | optional | not_needed>; crop_id=<source-cell crop or isolated edit target>; full_sheet_only=<allowed | blocked_for_exact_preservation>
Reference policy: <identity/style/composition/forbidden role for each input>
Change budget: <identity/style/palette/costume/pose/background limits>
Input images: <Image 1: reference image; Image 2: edit target; Image 3: style reference> (optional)
Scene/backdrop: <environment or chroma-key background>
Subject: <main subject and canon identity>
Style/medium: <photo, illustration, concept art, sprite, icon, etc>
Style fidelity lock: <reference-sheet style, flatness, line weight, shading depth, detail density, and forbidden style drift>
Generation contract: <identity-preserving task, not redesign; preserve exact anchors; restate invariants>
Composition/framing: <view, crop, layout, camera>
View/proportion lock: <camera mode, yaw direction, visible side, pitch/roll, fixed height, per-landmark derived projected widths, distortion constraints>
Lighting/mood: <lighting and emotion>
Color palette: <canon palette>
Materials/textures: <canon materials>
Text (verbatim): "<exact text, if any>"
Confirmed constraints: <assertions with approval_status approved and user_answers provenance only>
Style constraints: <approved or user-confirmed style canon only>
Provisional constraints: <useful but unresolved details; label source role and do not present as hard canon>
Generation constraints: <request-local technical constraints that are not canon, such as chroma-key, padding, or no-shadow requirements>
Change only: <specific user-requested mutations>
Unresolved questions: <canon-critical blockers or needs_confirmation items>
Avoid: <confirmed forbidden rules, request-local prohibitions, drift risks, watermark, unwanted text>
Evaluation checklist: <identity_pass/style_pass/proportion_pass/semantic_pass/drift_notes/next_prompt_patch>
```

For API-ready output, split the prompt pack into:

```yaml
prompt_pack:
  technical_contract:
    # full canon, assertions, source-cell manifest, API profile, and review rules
  final_imagegen_prompt:
    max_length_target: 1200_to_2500_chars
    priority_order:
      - task_type
      - reference_roles
      - change_only
      - preserve
      - style_fidelity_lock
      - avoid
```

## Cutout / Transparent-Background Prompt Add-On

Use this add-on when the intended result is a sprite, sticker, item cutout, transparent asset, or background-extraction task.

```text
Scene/backdrop: flat solid #00ff00 background; perfectly uniform chroma-key field for background removal
Generation constraints: full subject visible, crisp separated edges, generous padding, no cast shadow, no contact shadow, no reflection, no background texture, do not use #00ff00 anywhere in the subject
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

[Style Fidelity Check]
- 원본 레퍼런스의 line weight, flatness, shading depth, detail density가 유지되는가?
- 반실사화, 3D 렌더, 과한 부드러운 명암, 사실적인 털/피부/신발 디테일이 생기지 않았는가?
- 마스코트의 귀여운 나이감과 단순화된 비율이 성숙하거나 패션 일러스트처럼 늘어나지 않았는가?

[Reference Preservation Check]
- 선택한 source cell의 silhouette, head/body ratio, limb length가 유지되는가?
- full multi-pose sheet가 아니라 실제 source_cell_asset 또는 isolated edit target을 입력으로 사용했는가?
- 요청한 변경 외의 얼굴 구조, 몸통 길이, 다리 길이, 신발 크기가 재설계되지 않았는가?
- identity만 맞고 원본 비율/스타일이 다르면 `reject`로 판정했는가?

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
- `Confirmed constraints`에는 approved assertion과 user_answers provenance가 있는 정본 규칙만 들어갔는가?
- `Generation constraints`에는 chroma-key, padding, no-shadow 같은 요청-local 기술 조건만 들어갔는가?
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
