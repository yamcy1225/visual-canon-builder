# Generation Contract

Use this reference when `$visual-canon-builder` prepares an `$imagegen` handoff for a reference-preserving task. The contract turns visual canon into operational instructions: what input images anchor, what may change, what must not change, and how invariants are repeated in every prompt.

## Sensitivity Levels

```yaml
task_sensitivity:
  identity_sensitive:
    use_when:
      - same character, same mascot, same brand, same person-like identity
      - user says preserve original, do not redesign, same exact design
    default_mode: edit_or_reference_image
    text_generate_allowed: false
  style_sensitive:
    use_when:
      - same art direction, same illustration style, same line/rendering feel
    default_mode: reference_image_preferred
    text_generate_allowed: only_if_user_accepts_loose_style_match
  loose_inspiration:
    use_when:
      - user asks for inspired by, similar vibe, new design, exploration
    default_mode: text_generate_allowed
```

For identity-sensitive tasks, do not mark handoff `ready` when the only plan is text-only generation and a usable reference image exists.

## Contract Shape

```yaml
generation_contract:
  id: GEN_001
  task_type: identity_preserving_reference_generation
  task_sensitivity: identity_sensitive
  default_mode: edit_or_reference_image
  text_generate_allowed: false
  mode_reason: reference image is required to preserve identity and style
  reference_policy:
    primary_reference_required: true
    identity_anchor:
      source_id: Image_001
      must_preserve:
        - face_geometry
        - silhouette
        - proportions
        - unique_marks
        - costume_structure
    style_anchor:
      source_id: Image_001
      must_preserve:
        - line_language
        - rendering_language
        - palette
        - lighting_mood
        - texture_density
    composition_reference:
      source_id: Image_002
      role: optional_scene_layout
    forbidden_examples:
      - Image_BAD_001
  change_budget:
    identity: 0_percent
    style: 0_to_5_percent
    palette: 0_to_5_percent
    costume: locked_unless_requested
    pose: allowed_if_requested
    background: allowed_if_requested
    camera: limited_low_distortion
  mutation_policy:
    allowed_to_change:
      - pose
      - expression_intensity
      - scene_background
      - requested_prop
    must_not_change:
      - facial_identity
      - head_body_ratio
      - body_silhouette
      - eye_shape
      - canon_palette
      - line_weight
      - shading_language
      - signature_symbols
  invariant_restatement:
    required_every_prompt: true
    lines:
      - Preserve the exact same character identity from the reference image.
      - Do not redesign the face, body proportions, silhouette, costume canon, line style, rendering style, or palette.
      - Only change: <requested_change>.
```

## Mode Selection

Use this decision rule:

- `edit`: localized change, text swap, expression change, color correction, or when the target pose/cell should stay almost identical.
- `edit_target_preserve`: exact source-cell preservation with only small requested changes.
- `reference_generate`: new pose/scene, but identity/style must remain anchored to reference images.
- `text_generate`: no reference image exists, user explicitly wants loose inspiration, or identity/style preservation is not part of the request.

If the task expects exact character-sheet reuse, require a `source_cell_asset` rather than a full multi-pose sheet as the only input.

## Prompt Pack Fields

```text
Task sensitivity: identity_sensitive
Imagegen execution:
  mode: edit | reference_generate | text_generate
  text_generate_allowed: false
  reason: strict identity/style preservation requires reference input
  input_roles:
    identity_anchor: Image_001
    style_anchor: Image_001
    edit_target: CROP_001 optional
    composition_reference: Image_002 optional

Reference policy:
  preserve_from_identity_anchor:
    - face geometry
    - body proportions
    - silhouette
    - unique marks
    - costume structure
  preserve_from_style_anchor:
    - line language
    - shading model
    - color temperature
    - texture density
    - lighting mood
    - composition rhythm

Change budget:
  identity: 0%
  style: 0-5%
  pose: allowed only as requested
  background: allowed only as requested
  costume: locked unless requested

Change only:
  - <specific user-requested mutation>
```

## API Execution Profile

Add this block when the handoff is intended to be executable through an image API rather than only readable as art direction. Prefer the Responses API for multi-turn reference-preserving work and the Images API for a single direct edit/generation. For GPT Image reference preservation, use high input fidelity when identity, face, logo, or source-cell details matter.

```yaml
api_execution_profile:
  preferred_api: responses_api
  reason: multi_turn_reference_preserving_workflow
  model_family: gpt_image
  action: edit
  input_fidelity: high
  reference_ordering:
    first_image: identity_anchor_or_source_cell_asset
    second_image: style_anchor_if_separate
    later_images:
      - composition_reference
      - prop_reference
      - forbidden_example
  mask:
    required: false
    use_when:
      - localized_edit
      - exact_text_change
      - expression_or_arm_position_change
    rule: mask_targets_change_area_only_keep_rest_preserved
  output:
    size: auto_or_requested
    format: png
    background: transparent_or_opaque_or_auto
```

Reference ordering matters. Put the source cell or strongest identity anchor first. Put a separate style anchor second only when it is not the same image. Put composition, prop, and forbidden examples later so they do not outrank identity preservation.

## Source Cell Asset Manifest

For exact character-sheet reuse, the prompt pack should include a manifest for the cropped or isolated source cell. A full multi-pose sheet can be useful context, but it should not make an exact-preservation handoff `ready` by itself.

```yaml
source_cell_asset_manifest:
  id: CROP_SampleMascot_FrontFullBody_001
  crop_id: CROP_SampleMascot_FrontFullBody_001
  source_image_id: Image_SampleMascot_001
  source_region:
    label: front_full_body
    bbox:
      x: needs_user_or_script
      y: needs_user_or_script
      width: needs_user_or_script
      height: needs_user_or_script
  asset_path: attached_or_local_crop_path
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
    - shoe_simplification
  ready_state: ready | coordinates_ready_crop_not_verified | blocked_until_crop_exists
```

Use `scripts/create_source_cell_manifest.py` to create this manifest when coordinates or a crop path are available.

## Technical Contract And Final Prompt Split

Keep the full ontology and handoff metadata in `technical_contract`, then produce a shorter final prompt that image generation can execute. The final prompt should normally prioritize:

1. task type
2. reference roles
3. change-only instructions
4. preserve rules
5. style fidelity lock
6. avoid list

```yaml
prompt_pack:
  technical_contract:
    generation_contract: GEN_001
    reference_preserve_model: active
    source_cell_asset_manifest: CROP_SampleMascot_FrontFullBody_001
    exact_text_policy: optional
    evaluation_contract: EVAL_CONTRACT_001
  final_imagegen_prompt:
    max_length_target: 1200_to_2500_chars
    content: |
      This is an identity-preserving edit/reference task, not a redesign.
      Use CROP_SampleMascot_FrontFullBody_001 as the first input image.
      Change only: angry expression, crossed arms, shirt text "MAD".
      Preserve: exact source-cell silhouette, head/body ratio, compact torso, short limbs, simplified shoes, flat 2D line art.
      Avoid: taller body, realistic shoes, glossy 3D shading, semi-realistic redraw.
```

The full technical contract can be long; the final prompt should stay short, explicit, and repetition-safe.

## Exact Text And Mask Policy

When exact text matters, add a policy instead of hoping the model spells and places it correctly.

```yaml
exact_text_policy:
  text_required: true
  text_source:
    assertion_id: ASSERT_ShirtText_001
    approval_status: approved
  rendering_strategy:
    primary: image_edit_with_mask
    fallback: generate_without_text_then_add_text_in_postprocess
  validation:
    reject_when:
      - misspelled_text
      - wrong_case
      - wrong_placement_changes_design
```

Use a mask for localized shirt text, logo, arm-position, or expression edits when the surrounding source cell should stay preserved.

## Invariant Restatement

Include an invariant block in every final prompt or edit prompt. Do not rely on prior turns.

```text
This is an identity-preserving reference-image task, not a redesign.
Use Image_001 as the identity and style anchor.
Only change: <requested_change>.
Preserve the original character identity, proportions, silhouette, line language, rendering style, color palette, and emotional tone.
Do not redesign, restyle, beautify, make more generic, make more realistic, make glossier, change the face, change proportions, change the palette, or change the line style.
```

## Handoff Status

```yaml
handoff_status_rules:
  ready:
    - identity-sensitive task has a usable identity anchor
    - style-sensitive task has a usable style anchor or user accepted loose style matching
    - confirmed constraints include all identity-critical assertions
    - change budget and change-only field are explicit
  provisional:
    - one usable reference exists but source roles or style assertions are not approved
    - only non-critical style or scene details remain unresolved
  blocked:
    - exact preservation is requested but no source cell or edit target is available
    - identity anchors conflict on face/proportions/symbols
    - user requires confirmed-only handoff before approving canon
```
