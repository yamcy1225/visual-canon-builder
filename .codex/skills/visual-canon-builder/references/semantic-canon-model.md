# Semantic Canon Model

Use this reference when `$visual-canon-builder` needs to make ontology concepts explicit without implementing full RDF, OWL, SHACL, or PROV-O.

## Purpose

The skill outputs practical YAML, but the model should behave like a small visual knowledge graph:

- `class`: the type of thing, usually `entity_type`.
- `individual`: the concrete entity id, usually `id`.
- `property`: a field that describes an individual.
- `relation`: a graph edge connecting subject, predicate, and object.
- `constraint`: a validation shape for checking canon.
- `provenance`: evidence showing where a canon assertion came from.
- `evidence_card`: a source-grounded observation node used by the evidence interview.
- `approval`: a user decision node that locks, revises, rejects, or keeps an assertion provisional.
- `style_canon`: identity-bound or reference-bound visual treatment, separate from character identity.
- `generation_contract`: operational handoff rules for image generation/editing.
- `evaluation_result`: generated-output review record that can create drift patterns and prompt patches.

## Semantic Mapping

```yaml
semantic_mapping:
  class: entity_type
  individual: id
  property: nested visual/proportion/style fields
  relation: relations subject-predicate-object records
  constraint: validation_shapes
  provenance: canon_assertions source/confidence/evidence_refs/approval_status/user_answers/retrieval_scope fields
```

## Relations / Triples

Use relation records whenever a fact connects two entities or should be queried later.

```yaml
relations:
  - subject: CHR_001
    predicate: hasFaction
    object: FCT_001
  - subject: Image_001
    predicate: depicts
    object: CHR_001
  - subject: CHR_001_Battle
    predicate: variantOf
    object: CHR_001
  - subject: ASSERT_001
    predicate: wasDerivedFrom
    object: Image_001
  - subject: ASSERT_001
    predicate: supportedBy
    object: EV_001
```

Good predicates for this skill:

```text
depicts
derivedFrom
wasDerivedFrom
hasFaction
hasCostume
hasProp
hasPalette
hasSymbol
variantOf
conflictsWith
approves
rejects
forbids
requiresConfirmation
answersQuestion
wasAnsweredBy
supportedBy
hasApprovalStatus
servesAs
hasStyleCanon
boundToIdentity
mustPreserve
allowsMutation
forbidsMutation
evaluates
detectsDrift
correctedBy
promptsNext
```

`evidence_refs` is the canonical evidence relation on an assertion. `supportedBy` triples are optional graph mirrors derived from `evidence_refs`; do not let them diverge.

## Canon Assertions

Use assertion records for any fact that may need evidence, review, or later correction.

```yaml
canon_assertions:
  - id: ASSERT_001
    subject: CHR_001
    predicate: hasEyeColor
    object: pale_gold
    assertion_version: 1
    value_hash: hash_of_subject_predicate_object_v1
    source_image_id: Image_001
    source_role: canon candidate
    confidence: observed
    canon_status: provisional
    approval_status: pending_user_approval
    evidence_refs:
      - EV_001
    retrieval_scope: current_conversation_only
    asserted_by: visual-canon-builder
    derived_from: image_analysis_001
    needs_confirmation: true
```

Before the evidence interview is answered, candidate assertions should remain `provisional` or `unresolved`. Promote to `confirmed` only after an approval decision matches the current `assertion_version` and `value_hash`, then creates user-answer provenance.

## User Answer Provenance

Treat user replies as provenance records, not loose notes:

```yaml
question_queue:
  - id: Q_001
    question: Which image is the approved canon source?
    type: canon_source_approval
    blocking_for_ready: true
    blocking_for_provisional: false
    affects:
      - canon_assertions.*.source_role
      - Confirmed constraints
    default_if_unanswered: keep_provisional

user_answers:
  - id: UA_001
    answers_question: Q_001
    applies_to_assertion: ASSERT_001
    review_pack_id: REVIEW_001
    expected_assertion_version: 1
    expected_value_hash: hash_of_subject_predicate_object_v1
    value: Image_001 is approved canon
    asserted_by: user
    confidence: user_confirmed
    recorded_in_turn: current_conversation
```

Link answers into the graph:

```yaml
relations:
  - subject: UA_001
    predicate: answersQuestion
    object: Q_001
  - subject: ASSERT_001
    predicate: wasDerivedFrom
    object: UA_001
```

Confidence values:

```text
observed
inferred
low_confidence
needs_confirmation
user_confirmed
rejected
```

Approval transition rules:
- `approve`: current assertion becomes `approval_status: approved`, `confidence: user_confirmed`, `canon_status: confirmed`.
- `reject`: current assertion becomes `approval_status: rejected`, `canon_status: rejected`.
- `revise`: original assertion becomes `approval_status: revised` and stays out of `Confirmed constraints`; create a replacement assertion with a new version/hash.
- `keep_provisional`: assertion remains prompt guidance only.

Rules:
- Put only assertions with `approval_status: approved` and linked `user_answers` provenance into `Confirmed constraints`.
- Keep `observed` assertions from a `canon candidate` provisional until the approval payload is applied.
- Keep `observed` facts from `reference image`, `variant`, or `style reference` roles in `Provisional constraints` unless the user confirms them.
- Keep `inferred`, `low_confidence`, and `needs_confirmation` out of hard `$imagegen` constraints.
- Never promote style-reference-only assertions to immutable canon unless the user confirms them.

Canon status values:

```text
confirmed
provisional
unresolved
rejected
```

## Expanded Classes For Image Generation Control

Use these classes when the task needs original-feeling preservation or retry loops:

```yaml
classes:
  - VisualAsset
  - Character
  - Costume
  - Prop
  - Environment
  - ReferenceImage
  - IdentityAnchor
  - StyleAnchor
  - CompositionAnchor
  - PaletteAnchor
  - ProportionModel
  - ViewProjection
  - CanonAssertion
  - StyleCanon
  - StyleAssertion
  - GenerationContract
  - EvaluationResult
  - DriftPattern
  - PromptPatch
  - ForbiddenExample
```

Example control triples:

```yaml
relations:
  - subject: Image_001
    predicate: servesAs
    object: IdentityAnchor
  - subject: Image_001
    predicate: servesAs
    object: StyleAnchor
  - subject: CHR_001
    predicate: hasStyleCanon
    object: STYLE_001
  - subject: STYLE_001
    predicate: boundToIdentity
    object: CHR_001
  - subject: GEN_001
    predicate: mustPreserve
    object: STYLE_001
  - subject: EVAL_001
    predicate: detectsDrift
    object: Drift_face_geometry
  - subject: Drift_face_geometry
    predicate: correctedBy
    object: PATCH_001
```

## Style Canon And Generation Contract Records

```yaml
style_canon:
  id: STYLE_001
  style_role: identity_bound_style
  source_images:
    - Image_001
  line_language:
    contour_weight: clean_bold_black
    interior_line_density: sparse
  rendering_language:
    shading_model: minimal_flat_grayscale
    surface_finish: matte
  color_language:
    palette_drift_tolerance: low
  identity_style_binding:
    style_is_part_of_identity: true

generation_contract:
  id: GEN_001
  task_sensitivity: identity_sensitive
  default_mode: edit_or_reference_image
  text_generate_allowed: false
  reference_policy:
    identity_anchor: Image_001
    style_anchor: Image_001
  change_budget:
    identity: 0_percent
    style: 0_to_5_percent
  mutation_policy:
    allowed_to_change:
      - user_requested_pose
    must_not_change:
      - face_geometry
      - head_body_ratio
      - line_language
      - palette
```

## Evaluation, Drift, And Prompt Patch Records

```yaml
evaluation_result:
  id: EVAL_001
  generated_image_id: GENIMG_001
  compared_against:
    identity_anchor: Image_001
    style_anchor: Image_001
    generation_contract: GEN_001
  classification: fix
  drift_patterns:
    - Drift_line_weight_changed
    - Drift_limbs_elongated
  prompt_patch: PATCH_001

drift_patterns:
  - id: Drift_line_weight_changed
    category: style_drift
    message: output uses thicker comic outline than reference
    severity: fix

prompt_patches:
  - id: PATCH_001
    target: next_imagegen_prompt
    instructions:
      - Restore the source-cell line weight and sparse interior detail from Image_001.
      - Keep compact mascot limb proportions; do not elongate legs.
```

## Validation Shapes

Use shape records when a rule needs target, path, severity, and a repeatable message.

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
  - target: canon_assertions[*]
    path: canon_status
    constraint: if equals confirmed then approval_status equals approved and user_answers provenance exists
    severity: reject
    message: approved decision provenance 없이 confirmed assertion을 만들 수 없다.
  - target: canon_assertions[*]
    path: evidence_refs
    constraint: min_count 1
    severity: reject
    message: assertion은 최소 하나의 evidence card를 참조해야 한다.
  - target: approval_payload.decisions[*]
    path: expected_value_hash
    constraint: equals current assertion value_hash
    severity: blocked
    message: stale approval payload는 적용하지 않는다.
```

Severity values:

```text
pass
fix
reject
needs_confirmation
blocked
```

## Handoff Safety

Set `$imagegen` handoff status from assertion state:

```yaml
imagegen_handoff:
  status: ready
  ready_when:
    - all identity-critical assertions have canon_status: confirmed and approval_status: approved
    - canon_lock_state is locked or no canon lock is required for the requested artifact
    - no reject-severity validation shape is unresolved
  provisional_when:
    - one usable canon candidate exists but is not yet approved
    - non-critical style or measurement assertions remain inferred
  blocked_when:
    - no usable canon candidate exists
    - identity, faction, left/right, or proportion canon conflicts remain unresolved
```

Use this stricter status matrix when preparing prompt packs:

```yaml
ready:
  - all identity-critical assertions have canon_status: confirmed and approval_status: approved
  - canon_lock_state is locked or no canon lock is required for the requested artifact
  - required text, palette, left/right details, and required proportions are resolved
  - no reject or blocked validation shape is unresolved
provisional:
  - one usable canon candidate exists but is not yet approved
  - only non-critical style, material, accessory, atmosphere, or minor prop details remain inferred
  - requested output can proceed while uncertainty is explicit
  - every uncertain detail is listed under Provisional constraints or Unresolved questions
blocked:
  - no usable canon candidate exists
  - canon candidates conflict on identity-critical facts
  - face identity, faction mark, required text, subject-left/right detail, or core proportions are unresolved
  - any reject or blocked validation shape remains unresolved
```

Prompt pack fields:

```text
Confirmed constraints: assertions with approval_status approved and user_answers provenance only
Provisional constraints: inferred or low-confidence facts that may help but must not be treated as canon
Unresolved questions: canon-critical blockers and needs_confirmation fields
```
