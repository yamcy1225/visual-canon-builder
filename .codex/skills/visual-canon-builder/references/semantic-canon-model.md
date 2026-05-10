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
    source_role: canon candidate
    confidence: observed
    asserted_by: visual-canon-builder
    derived_from: image_analysis_001
    needs_confirmation: false
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
- Put only `observed` or `user_confirmed` assertions into `confirmed_constraints`.
- Keep `inferred`, `low_confidence`, and `needs_confirmation` out of hard `$imagegen` constraints.
- Never promote style-reference-only assertions to immutable canon unless the user confirms them.

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
    - all identity-critical assertions are observed or user_confirmed
    - no reject-severity validation shape is unresolved
  provisional_when:
    - non-critical style or measurement assertions remain inferred
  blocked_when:
    - identity, faction, left/right, or proportion canon conflicts remain unresolved
```

Prompt pack fields:

```text
Confirmed constraints: observed or user_confirmed facts only
Provisional constraints: inferred or low-confidence facts that may help but must not be treated as canon
Unresolved questions: canon-critical blockers and needs_confirmation fields
```
