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
