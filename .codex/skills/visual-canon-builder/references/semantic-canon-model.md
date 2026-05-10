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

## Semantic Mapping

```yaml
semantic_mapping:
  class: entity_type
  individual: id
  property: nested visual/proportion/style fields
  relation: relations subject-predicate-object records
  constraint: validation_shapes
  provenance: canon_assertions source/confidence fields
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
```

## Canon Assertions

Use assertion records for any fact that may need evidence, review, or later correction.

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
```

## User Answer Provenance

Treat user replies as provenance records, not loose notes:

```yaml
question_queue:
  - id: Q_001
    question: Which image is the approved canon source?
    type: canon_source_approval
    blocking: true
    affects:
      - canon_assertions.*.source_role
      - Confirmed constraints
    default_if_unanswered: keep_provisional

user_answers:
  - id: UA_001
    answers_question: Q_001
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

Rules:
- Put only `user_confirmed` assertions or `observed` assertions from an `approved canon source` into `Confirmed constraints`.
- Put `observed` assertions from a `canon candidate` into `Confirmed constraints` only when the user request clearly declares that source as canon.
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
    - all identity-critical assertions have canon_status: confirmed
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
  - all identity-critical assertions have canon_status: confirmed
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
Confirmed constraints: user-confirmed canon, observed facts from approved canon sources, or observed canon-candidate facts when the request clearly declares the source as canon
Provisional constraints: inferred or low-confidence facts that may help but must not be treated as canon
Unresolved questions: canon-critical blockers and needs_confirmation fields
```
