# Evidence Interview RAG Mode

Use this reference when `$visual-canon-builder` must lock canon together with the user before finalizing a visual ontology. v3.4 is current-conversation evidence retrieval, not vector-database RAG. Do not create a vector database, local HTML UI, persistent index, or external RAG service.

## Workflow

```text
Source Inventory -> Evidence Cards -> Candidate Assertions -> Approval Review Pack -> User Answer Provenance -> Locked Canon Ontology
```

Rules:
- `retrieval_scope` defaults to `current_conversation_only`.
- Every candidate assertion must point to one or more `evidence_refs`.
- Approval is batched: output one editable `approval_payload` so the user can approve, revise, reject, or keep items provisional in one reply.
- Before approval, candidate assertions are `canon_status: provisional` or `unresolved`, never `confirmed`.
- Final `confirmed` status requires `approval_status: approved`, at least one `evidence_refs` item, matching `assertion_version`/`value_hash`, and a linked `user_answers` record.
- `evidence_refs` is the canonical support link. `relations: supportedBy` may mirror it for graph traversal, but must be derived from `evidence_refs`, not maintained separately.

## Source Inventory

```yaml
source_inventory:
  retrieval_scope: current_conversation_only
  sources:
    - id: SRC_Image_001
      type: attached_image
      role: canon candidate
      description: character sheet with front, side, back, expressions, and props
    - id: SRC_UserNote_001
      type: user_note
      role: instruction
      description: user asks to build a canon candidate and imagegen prompt pack
```

## Evidence Cards

```yaml
evidence_cards:
  - id: EV_Dallae_Face_001
    source_id: SRC_Image_001
    modality: image
    region_or_note: front and expression heads
    source_anchor: Image 1 / upper character sheet / face views
    view_label: front_and_expression_heads
    bbox_or_region: descriptive_region_no_pixel_bbox
    source_text_span: null
    observation: white rabbit mascot face, long upright ears, star pupils, small black nose
    confidence: observed
    usable_for:
      - identity
      - face
    limitations:
      - exact fur material is not proven
```

Good evidence cards are small enough to review but specific enough to audit. Prefer several targeted cards over one huge card.

## Candidate Assertions

```yaml
canon_assertions:
  - id: ASSERT_Dallae_StarPupils
    subject: CHR_Dallae
    predicate: hasEyeMotif
    object: black eyes with white star-shaped pupils
    assertion_version: 1
    value_hash: hash_of_subject_predicate_object_v1
    evidence_refs:
      - EV_Dallae_Face_001
    retrieval_scope: current_conversation_only
    source_image_id: SRC_Image_001
    source_role: canon candidate
    confidence: observed
    canon_status: provisional
    approval_status: pending_user_approval
    asserted_by: visual-canon-builder
    derived_from: image_analysis_dallae_001
    needs_confirmation: true
```

`approval_status` values:
- `pending_user_approval`: should be reviewed before canon lock.
- `approved`: user accepted the assertion as canon.
- `rejected`: user rejected the assertion.
- `revised`: original assertion was superseded by a user replacement; it is not itself confirmed.
- `keep_provisional`: useful prompt guidance but not canon.

## Approval Review Pack

```yaml
approval_review_pack:
  review_pack_id: REVIEW_Dallae_001
  entity_id: CHR_Dallae
  canon_lock_state: unlocked
  derived_lock_state: true
  instructions: "각 항목을 approve, reject, revise, keep_provisional 중 하나로 표시하세요."
  bulk_actions:
    - approve_all_low_risk
    - keep_all_optional_provisional
  items:
    - assertion_id: ASSERT_Dallae_StarPupils
      assertion_version: 1
      value_hash: hash_of_subject_predicate_object_v1
      evidence_refs:
        - EV_Dallae_Face_001
      current_value: black eyes with white star-shaped pupils
      recommended_action: approve
      risk_tier: identity_critical
      risk_if_wrong: face identity drift
```

Use clickable choice UI when available. If not available, show the payload below and ask the user to return it with edits.

## Approval Payload

```yaml
approval_payload:
  review_pack_id: REVIEW_Dallae_001
  applies_to: CHR_Dallae
  answer_mode: batch
  decisions:
    - assertion_id: ASSERT_Dallae_StarPupils
      expected_assertion_version: 1
      expected_value_hash: hash_of_subject_predicate_object_v1
      action: approve
      revised_value: null
      note: null
    - assertion_id: ASSERT_Dallae_ShirtText
      expected_assertion_version: 1
      expected_value_hash: hash_of_subject_predicate_object_v1
      action: keep_provisional
      revised_value: null
      note: exact text not yet locked
```

Allowed `action` values are `approve`, `reject`, `revise`, and `keep_provisional`.

Reject stale payloads: if `review_pack_id`, `expected_assertion_version`, or `expected_value_hash` does not match the current assertion, keep the assertion pending and ask for a refreshed approval payload.

## Applying Answers

Convert each decision into provenance before changing canon:

```yaml
user_answers:
  - id: UA_Dallae_Approval_001
    answers_question: approval_payload
    applies_to_assertion: ASSERT_Dallae_StarPupils
    review_pack_id: REVIEW_Dallae_001
    expected_assertion_version: 1
    expected_value_hash: hash_of_subject_predicate_object_v1
    value: approve
    asserted_by: user
    confidence: user_confirmed
    recorded_in_turn: current_conversation

relations:
  - subject: ASSERT_Dallae_StarPupils
    predicate: wasDerivedFrom
    object: UA_Dallae_Approval_001
```

Recompute rules:
- `approve` -> `approval_status: approved`, `confidence: user_confirmed`, `canon_status: confirmed`.
- `reject` -> `approval_status: rejected`, `canon_status: rejected`; move harmful drift to `forbidden` when useful.
- `revise` -> mark the original `approval_status: revised`, keep it out of `Confirmed constraints`, and create a replacement assertion with a new ID/version/value_hash. If the revised value is explicit in the same user answer, the replacement assertion may be `approval_status: approved`, `confidence: user_confirmed`, and `canon_status: confirmed`.
- `keep_provisional` -> keep the assertion out of `Confirmed constraints`.

## Lock Summary

```yaml
lock_summary:
  canon_lock_state: partially_locked
  derived_from_assertion_status: true
  pending: 2
  approved: 8
  rejected: 1
  revised: 1
  keep_provisional: 3
  ready_for_final_canon: false
```

Set `canon_lock_state: locked` only when all canon-critical assertions are approved, rejected, or revised into approved replacement assertions and no pending user approval remains. This summary is derived from assertion states; do not hand-edit it as independent truth.
