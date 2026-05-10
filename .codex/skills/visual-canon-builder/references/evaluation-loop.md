# Evaluation Loop

Use this reference after `$imagegen` creates an image from a visual canon pack. The goal is to turn review into a repeatable loop: compare the generated result against the canon and anchors, classify pass/fix/reject, record drift, and create a targeted prompt patch for the next generation or edit.

## Loop

```text
Generated image -> Evaluate against anchors/canon -> classify pass/fix/reject -> record drift -> produce prompt patch -> retry or approve -> promote only approved outputs to canon
```

Do not promote a generated image to canon because it looks good. It becomes canon only after review and explicit approval.

## Evaluation Result Shape

```yaml
evaluation_result:
  id: EVAL_001
  generated_image_id: GENIMG_001
  compared_against:
    identity_anchor: Image_001
    style_anchor: Image_001
    canon_version: CHR_001_v1.0.0
    generation_contract: GEN_001
  classification: <pass | fix | reject>
  confidence: <high | medium | low>
  summary: <short human-readable result>
  checks:
    identity_pass: <true | false | partial>
    style_pass: <true | false | partial>
    proportion_pass: <true | false | partial>
    semantic_pass: <true | false | partial>
    composition_pass: <true | false | partial>
  drift_patterns:
    - Drift_face_geometry_changed
  prompt_patch:
    id: PATCH_001
    apply_to_next_prompt: true
    instructions:
      - Restore the same face geometry and eye spacing from Image_001.
  forbidden_example_candidate:
    use_as_forbidden_example: <true | false>
    reason: <clear drift worth preserving as a negative reference>
```

## Drift Taxonomy

```yaml
drift_taxonomy:
  identity_drift:
    - face_geometry_changed
    - eye_shape_changed
    - head_body_ratio_changed
    - body_silhouette_changed
    - signature_mark_missing
    - costume_structure_changed
    - subject_left_right_swapped
  style_drift:
    - line_weight_changed
    - line_texture_changed
    - shading_model_changed
    - palette_temperature_changed
    - saturation_drift
    - texture_density_changed
    - glossy_or_3d_rendering_added
    - realism_level_changed
  proportion_drift:
    - limbs_elongated
    - torso_length_changed
    - shoe_or_hand_scale_changed
    - compact_mascot_ratio_lost
    - wide_angle_distortion_added
  semantic_drift:
    - required_symbol_missing
    - wrong_prop_added
    - forbidden_item_added
    - exact_text_wrong
  composition_drift:
    - wrong_framing
    - wrong_camera_height
    - excessive_perspective
    - source_cell_pose_not_preserved
```

## Classification Rules

```yaml
classification_rules:
  pass:
    - identity_pass: true
    - style_pass: true
    - proportion_pass: true
    - semantic_pass: true
    - no reject-severity validation shape failed
  fix:
    - identity mostly preserved
    - drift is local or correctable with targeted edit/prompt patch
    - no core identity redesign
  reject:
    - face geometry, head/body ratio, silhouette, or identity-bound style changed
    - source-cell preservation failed
    - forbidden prop, wrong left/right mark, or exact text error changes canon-critical meaning
    - output looks like a new drawing of a similar character rather than the same design
```

Identity-only similarity is not enough. If the generated image has the right species, colors, or symbols but changes proportions, silhouette, line language, rendering style, or source-cell design, classify it as `reject` for strict preservation tasks.

## Prompt Patch

The prompt patch should be short and corrective. It should name the drift and state the repair target.

```text
Prompt patch for next iteration:
- Face drift detected: restore the same facial proportions and eye spacing from Image_001.
- Style drift detected: remove glossy 3D lighting; return to matte flat 2D line art.
- Palette drift detected: remove neon saturation; use the muted warm palette from Image_001.
- Proportion drift detected: restore compact mascot head/body ratio and short simplified limbs.
- Composition drift detected: use neutral camera height and centered full-body framing.
```

When using a rejected image as a forbidden example, label exactly why it is forbidden:

```yaml
forbidden_examples:
  - id: Image_BAD_001
    reason:
      - elongated adult proportions
      - realistic product-detail shoes
      - glossy semi-3D shading
    use_for:
      - negative_style_drift
      - source_cell_preservation_failure
```

## Canon Promotion

```text
generated -> evaluated -> corrected -> user-approved -> canon_reference
```

Rules:

- `pass` can be shown for approval but is not automatically canon.
- `fix` requires a targeted edit or prompt patch before approval.
- `reject` stays out of canon; it may become a forbidden example if the failure is clear.
- If review reveals a new intended variant, create a new variant assertion with user approval rather than silently changing the original canon.
