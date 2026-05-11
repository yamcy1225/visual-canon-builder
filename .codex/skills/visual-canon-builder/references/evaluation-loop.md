# Evaluation Loop

Use this reference after `$imagegen` creates an image from a visual canon pack. The goal is to turn review into a repeatable loop: compare the generated result against the canon and anchors, classify pass/fix/reject, record drift, and create a targeted prompt patch for the next generation or edit.

## Loop

```text
Generated image -> Evaluate against anchors/canon -> classify pass/fix/reject -> record drift -> produce prompt patch -> retry or approve -> promote only approved outputs to canon
```

Do not promote a generated image to canon because it looks good. It becomes canon only after review and explicit approval.

## Pass-Only Generation Gate

When the user asks for automatic verification or "only keep passing outputs", do not use a generation surface that immediately presents every candidate as final. Generate candidates into a temporary work directory, evaluate them, and copy only `classification: pass` candidates into `accepted/`.

Required loop:

```text
attempt prompt -> candidate image -> evaluation_result -> score gate
  pass: copy to accepted/ and show/use this image
  fix/reject: copy to rejected/, append prompt_patch to next attempt, regenerate
  max attempts exhausted: report no passing image instead of presenting the least-bad candidate
```

Use:

```bash
python .codex/skills/visual-canon-builder/scripts/score_generation_review.py \
  attempt_01.evaluation.json \
  --candidate-image attempt_01.png \
  --profile mascot_skateboard \
  --output-dir artifacts/sample_skate/skateboard-loop
```

For a complete command-driven loop, use `scripts/run_generation_loop.py` with a generator command that writes `{candidate}` and an evaluator command that writes `{evaluation}`. The evaluator may be a vision-model review, a human-authored JSON review, or another local QA script, but it must produce the `evaluation_result` shape below. Failed candidates must not be promoted or displayed as final.

## Visible Candidate Shortlist Gate

When the active generation surface exposes candidates immediately, do not treat that as a reason to skip verification. Use a visible-gated loop: show candidates as temporary outputs, evaluate each one immediately, then label it clearly.

```text
visible candidate -> evaluation_result -> score gate
  pass: copy to shortlist/ and label keep_candidate
  fix without strict failures: copy to repairable/ and label repair_candidate
  reject or required-check failure: copy to discarded/ or delete, label discard
  user chooses only from shortlist/ unless they explicitly ask to repair a repairable candidate
```

Use:

```bash
python .codex/skills/visual-canon-builder/scripts/score_generation_review.py \
  attempt_01.evaluation.json \
  --candidate-image attempt_01.png \
  --profile compact_mascot_identity \
  --review-mode visible_shortlist \
  --output-dir artifacts/sample_mascot/visible-shortlist
```

Visible shortlist mode is different from hidden pass-only delivery. It accepts that the user saw the raw outputs, but prevents canon contamination by not letting failed candidates become selectable finals, accepted references, or future style anchors.

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
    - arms_too_short
    - legs_too_long
    - limb_proportion_changed
    - wide_angle_distortion_added
  semantic_drift:
    - required_symbol_missing
    - wrong_prop_added
    - forbidden_item_added
    - exact_text_wrong
    - exact_text_wrong_case
    - exact_text_wrong_placement
  composition_drift:
    - wrong_framing
    - wrong_camera_height
    - excessive_perspective
    - source_cell_pose_not_preserved
  anatomy_prop_drift:
    - eye_construction_changed
    - star_pupil_missing_or_warped
    - eyelid_structure_changed
    - wrong_hand_digit_count
    - skateboard_proportion_invalid
    - board_length_invalid
    - oversized_longboard
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
    - eye construction, star-pupil shape, eyelid arcs, hand digit count, or source prop proportions fail strict task checks
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

## Exact Text And Mask Review

When `exact_text_policy.text_required: true`, text errors are semantic failures, not harmless style drift.

Reject when:

- required spelling is wrong
- case, punctuation, or line break changes meaning
- placement redesigns a logo, shirt print, poster, or faction mark
- a mask was required but the output changed the surrounding preserved source-cell region

Use `fix` only when the source-cell identity/style/proportion is intact and the text can be repaired with a localized edit or postprocess compositing.

## SampleSkate Skateboard Strict Checks

For SampleSkate skateboard images, the verifier must include these checks. Any `false` value requires `classification: reject`:

```yaml
checks:
  identity_pass: <true | false | partial>
  style_pass: <true | false | partial>
  proportion_pass: <true | false | partial>
  semantic_pass: <true | false | partial>
  eye_construction_pass: <true | false>
  star_pupil_pass: <true | false>
  hand_digit_count_pass: <true | false>
  skateboard_proportion_pass: <true | false>
```

Reject examples:

- star pupils missing, melted, off-model, or no longer crisp five-point highlights
- eyelid arcs simplified into unrelated eye shapes
- visible hand has four total digits instead of four rounded fingers plus one thumb
- skateboard becomes a longboard, surfboard, or stretched platform rather than the source prop proportions

## SampleMascot Strict Identity Checks

For SampleMascot images, the verifier must include these checks. Any `false` value requires `classification: reject` because SampleMascot's identity depends on compact source-sheet proportions as much as face and outfit details:

```yaml
checks:
  identity_pass: <true | false | partial>
  style_pass: <true | false | partial>
  proportion_pass: <true | false | partial>
  semantic_pass: <true | false | partial>
  character_identity_pass: <true | false>
  eye_construction_pass: <true | false>
  star_pupil_pass: <true | false>
  eyelash_pass: <true | false>
  hand_digit_count_pass: <true | false>
  ear_shape_pass: <true | false>
  compact_body_proportion_pass: <true | false>
  arm_length_pass: <true | false>
  leg_length_pass: <true | false>
  limb_proportion_pass: <true | false>
  exact_text_pass: <true | false>
  shoe_and_sock_design_pass: <true | false>
  source_sheet_style_pass: <true | false>
```

Reject examples:

- legs become long athletic legs instead of short rounded mascot legs
- arms shrink into tiny side nubs or lose the original rounded forearm-and-hand silhouette
- visible hands become ambiguous fists, four-finger hands, or unreadable blobs instead of one thumb plus four rounded fingers
- jump/run poses stretch the torso or limbs enough to lose SampleMascot's compact character-sheet ratio
