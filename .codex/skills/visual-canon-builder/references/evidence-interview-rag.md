# Evidence Interview RAG Mode

Use this reference when `$visual-canon-builder` must lock canon together with the user before finalizing a visual ontology. This is current-conversation evidence retrieval, not vector-database RAG. Do not create a vector database, local HTML UI, persistent index, or external RAG service.

## Workflow

```text
Source Inventory -> Evidence Cards -> Candidate Assertions -> Approval Review Pack -> User Answer Provenance -> Locked Canon Ontology
```

Rules:
- `retrieval_scope` defaults to `current_conversation_only`.
- Every candidate assertion must point to one or more `evidence_refs`.
- Approval can be batched, but the default surface is guided: show one active approval question first, then a compact `user_review` and plain-language reply shortcuts before any YAML payload.
- Keep one editable `approval_payload` for auditability so strict users can approve, revise, reject, or keep items provisional in one reply.
- Before approval, candidate assertions are `canon_status: provisional` or `unresolved`, never `confirmed`.
- Final `confirmed` status requires `approval_status: approved`, at least one `evidence_refs` item, matching `assertion_version`/`value_hash`, and a linked `user_answers` record.
- `evidence_refs` is the canonical support link. `relations: supportedBy` may mirror it for graph traversal, but must be derived from `evidence_refs`, not maintained separately.

## Guided Approval Interview

Use this as the first visible section whenever canon candidates need approval. It creates the missing "question -> user answer -> next question" feeling while preserving the batch payload for audit.

```yaml
guided_approval_interview:
  status: awaiting_user_decision
  current_question_index: 1
  total_questions: 3
  current_question:
    id: QAPP_SampleMascot_Identity
    label: "캐릭터 정체성"
    asks: "흰 샘플 마스코트 마스코트 정체성, 다이아몬드형 눈, 검은 줄무늬를 정본으로 승인할까요?"
    recommendation: "1"
    choices:
      - key: "1"
        label: "승인"
        effect: "관련 identity assertions -> approved/confirmed"
      - key: "2"
        label: "수정해서 승인"
        effect: "사용자 수정값으로 replacement assertion 생성"
      - key: "3"
        label: "임시 유지"
        effect: "keep_provisional"
      - key: "4"
        label: "거절"
        effect: "rejected"
    reply_hint: "숫자만 답해도 되고, `수정: 눈은 원형이 아니라 다이아몬드형`처럼 답해도 됩니다."
```

Rules:
- Ask exactly one active approval question at a time unless the user explicitly asks for batch approval.
- Put this section before `User Review`, tables, ontology, and prompt packs.
- The question must name the visual decision in natural language, not only an assertion ID.
- The response may still include provisional ontology and `$imagegen` prompt pack below, but it should end with the same current question reminder.
- When the user answers, create `user_answers`, update assertion approval state, recompute `lock_summary`, and ask the next unresolved approval question.
- If the user says `추천대로 진행`, apply all recommended actions and skip remaining low-risk interview questions.

## User Review First

Always put this compact layer before technical ontology details. It answers "what did you find, what do I need to decide, and what can I reply?"

```yaml
user_review:
  status: "초안 준비됨; 아직 정본 잠금 전"
  evidence_scope: current_conversation_only
  found:
    - "흰 샘플 마스코트 마스코트: 둥근 귀, 다이아몬드 눈, 검은 줄무늬"
    - "기본 의상: 하와이안 셔츠, 어두운 반바지, 흰 클로그"
    - "소품 후보: 긴 보드"
  needs_decision:
    - label: "캐릭터 정체성"
      covers:
        - ASSERT_SampleMascot_FaceIdentity
        - ASSERT_SampleMascot_TigerMarkings
      recommendation: approve
      reason: "정면/측면/후면/표정 컷에서 반복됩니다."
    - label: "긴 보드"
      covers:
        - ASSERT_SampleMascot_LongboardProp
      recommendation: keep_provisional
      reason: "액션 컷과 소품 컷에는 보이지만 항상 착용하는 물건인지는 미확정입니다."
  fast_reply:
    - "추천대로 진행"
    - "전체 정본 승인"
    - "정체성과 의상은 승인, 소품은 임시"
    - "수정: 긴 보드는 장면 소품"
```

Do not show `value_hash` or long assertion IDs in the top-level prose unless the user asks for strict/audit mode. Use readable labels first; keep IDs in `covers` for traceability.

## Quick Approval Table

Use a short table when the user is likely reviewing several candidates:

| 결정 항목 | 추천 | 이유 | 빠른 답변 |
| --- | --- | --- | --- |
| 캐릭터 정체성 | 승인 | 여러 뷰에서 반복 | `캐릭터 정체성 승인` |
| 기본 의상 | 승인 | 턴어라운드와 소품 컷 일치 | `기본 의상 승인` |
| 긴 보드 | 임시 | 고정 소품인지 미확정 | `긴 보드는 임시` |

Limit the table to the few decisions the user can realistically act on. Put lower-risk details into the technical payload with safe defaults.

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
  - id: EV_SampleMascot_Face_001
    source_id: SRC_Image_001
    modality: image
    region_or_note: front and expression heads
    source_anchor: Image 1 / upper character sheet / face views
    view_label: front_and_expression_heads
    bbox_or_region: descriptive_region_no_pixel_bbox
    source_text_span: null
    observation: white animal mascot face, long upright ears, star pupils, small black nose
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
  - id: ASSERT_SampleMascot_StarPupils
    subject: CHR_SampleMascot
    predicate: hasEyeMotif
    object: black eyes with white star-shaped pupils
    assertion_version: 1
    value_hash: hash_of_subject_predicate_object_v1
    evidence_refs:
      - EV_SampleMascot_Face_001
    retrieval_scope: current_conversation_only
    source_image_id: SRC_Image_001
    source_role: canon candidate
    confidence: observed
    canon_status: provisional
    approval_status: pending_user_approval
    asserted_by: visual-canon-builder
    derived_from: image_analysis_sample_mascot_001
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
  review_pack_id: REVIEW_SampleMascot_001
  entity_id: CHR_SampleMascot
  canon_lock_state: unlocked
  derived_lock_state: true
  instructions: "각 항목을 approve, reject, revise, keep_provisional 중 하나로 표시하세요."
  bulk_actions:
    - approve_all_low_risk
    - keep_all_optional_provisional
  items:
    - assertion_id: ASSERT_SampleMascot_StarPupils
      assertion_version: 1
      value_hash: hash_of_subject_predicate_object_v1
      evidence_refs:
        - EV_SampleMascot_Face_001
      current_value: black eyes with white star-shaped pupils
      recommended_action: approve
      risk_tier: identity_critical
      risk_if_wrong: face identity drift
```

Use clickable choice UI when available. If not available, show the human-friendly `fast_reply` options first. Show the payload below as an audit fallback, not as the primary thing the user must edit.

## Approval Payload

```yaml
approval_payload:
  review_pack_id: REVIEW_SampleMascot_001
  applies_to: CHR_SampleMascot
  answer_mode: batch
  decisions:
    - assertion_id: ASSERT_SampleMascot_StarPupils
      expected_assertion_version: 1
      expected_value_hash: hash_of_subject_predicate_object_v1
      action: approve
      revised_value: null
      note: null
    - assertion_id: ASSERT_SampleMascot_ShirtText
      expected_assertion_version: 1
      expected_value_hash: hash_of_subject_predicate_object_v1
      action: keep_provisional
      revised_value: null
      note: exact text not yet locked
```

Allowed `action` values are `approve`, `reject`, `revise`, and `keep_provisional`.

Reject stale payloads: if `review_pack_id`, `expected_assertion_version`, or `expected_value_hash` does not match the current assertion, keep the assertion pending and ask for a refreshed approval payload.

## Natural-Language Approval

Accept short plain-language replies and convert them to the same internal provenance as YAML decisions:

```yaml
natural_language_approval_map:
  - user_says:
      - "추천대로 진행"
      - "apply recommendations"
    action:
      approve:
        risk_tiers:
          - identity_critical
          - canon_critical
      keep_provisional:
        risk_tiers:
          - optional
          - style_only
        unless_user_explicitly_promotes: true
  - user_says:
      - "전체 승인"
      - "전체 정본 승인"
      - "approve all as canon"
    action:
      approve:
        risk_tiers:
          - identity_critical
          - canon_critical
          - optional
          - style_only
  - user_says:
      - "정체성과 의상은 승인, 소품은 임시"
    action:
      approve_labels:
        - "캐릭터 정체성"
        - "기본 의상"
      keep_provisional_labels:
        - "소품"
  - user_says_pattern: "수정: <label>=<new value>"
    action: revise
  - user_says_pattern: "거절: <label>"
    action: reject
```

When interpreting natural language, create `user_answers` that preserve the original user phrase and the normalized action. If a phrase is ambiguous, apply only the unambiguous parts and keep the rest pending or provisional.

## Applying Answers

Convert each decision into provenance before changing canon:

```yaml
user_answers:
  - id: UA_SampleMascot_Approval_001
    answers_question: approval_payload
    applies_to_assertion: ASSERT_SampleMascot_StarPupils
    review_pack_id: REVIEW_SampleMascot_001
    expected_assertion_version: 1
    expected_value_hash: hash_of_subject_predicate_object_v1
    value: approve
    asserted_by: user
    confidence: user_confirmed
    recorded_in_turn: current_conversation

relations:
  - subject: ASSERT_SampleMascot_StarPupils
    predicate: wasDerivedFrom
    object: UA_SampleMascot_Approval_001
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
