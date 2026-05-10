# Interactive Clarification Loop

Use this reference when `$visual-canon-builder` needs user input before promoting visual facts, resolving conflicts, or preparing a ready `$imagegen` handoff. The default behavior is immediate provisional progression: ask the questions as a structured queue, but still produce a provisional ontology and `$imagegen` prompt pack in the same response when that is safe.

## Purpose

The skill should not merely list questions and continue as if they were answered. It should also avoid ping-pong blocking when a useful provisional result is possible. It should:

1. Create a stable `question_queue`.
2. Ask the user only ready-blocking or high-value questions.
3. Mark each question separately for `ready` handoff and `provisional` handoff.
4. Convert user replies into `user_answers` provenance records.
5. Recompute canon assertions, handoff status, prompt constraints, and unresolved questions.

## Question Queue Schema

```yaml
clarification_gate:
  status: proceeding_with_provisional
  reason: unresolved_questions_do_not_block_provisional_handoff
  mode: immediate_provisional_progression
  hard_stop: false
  max_questions_this_turn: 5

question_queue:
  - id: Q_Byuli_001
    question: Image_Byuli_001을 approved canon source로 승격할까요?
    type: canon_source_approval
    blocking_for_ready: true
    blocking_for_provisional: false
    affects:
      - canon_assertions.*.source_role
      - canon_assertions.*.canon_status
      - Confirmed constraints
      - Handoff status
    required_for:
      - ready_handoff
      - confirmed_constraints
    options:
      - approve_as_canon
      - keep_as_candidate
      - use_as_reference_only
    default_if_unanswered: keep_provisional
```

Question fields:
- `id`: stable ID that can be answered later.
- `question`: user-facing question, concise and specific.
- `type`: reason category such as `canon_source_approval`, `variant_or_drift`, `exact_text`, `prop_permanence`, `left_right_asymmetry`, `measurement_source`, or `forbidden_rule`.
- `blocking_for_ready`: `true` when the answer changes whether handoff can be `ready`.
- `blocking_for_provisional`: `true` only when the answer is required before even a provisional handoff can be safe.
- `affects`: ontology fields, assertions, or prompt fields changed by the answer.
- `required_for`: what cannot be safely finalized without the answer.
- `default_if_unanswered`: usually `keep_provisional`, `keep_unresolved`, or `block_ready_handoff`.

## When To Proceed Or Stop

Proceed immediately with `Handoff status: provisional` when:
- One usable canon candidate exists.
- Unanswered questions can be kept out of `Confirmed constraints`.
- The prompt pack can put uncertain facts in `Provisional constraints` or `Unresolved questions`.
- The requested image can be drafted without pretending unconfirmed facts are canon.

Stop and wait only when `hard_stop: true`, such as:
- There is no usable canon candidate.
- Identity-critical canon candidates conflict and no safe provisional identity can be selected.
- Required exact text, face identity, left/right asymmetry, or proportion lock would have to be guessed.
- The user explicitly asks for confirmed-only output, ready-only output, or approval before `$imagegen`.

When proceeding, include the queue and a short status line such as:

```text
Clarification Gate: proceeding_with_provisional
아래 질문은 ready 승격을 위한 큐입니다. 현재 산출물은 provisional로 즉시 생성했고, 답변을 주면 user_answers provenance로 반영해 다시 계산합니다.
```

## User Answer Provenance

When answers arrive, record them before updating assertions:

```yaml
user_answers:
  - id: UA_Byuli_001
    answers_question: Q_Byuli_001
    value: approve_as_canon
    asserted_by: user
    confidence: user_confirmed
    recorded_in_turn: current_conversation
    applies_to:
      - Image_Byuli_001
      - CHR_Byuli
```

Then update linked assertions:

```yaml
canon_assertions:
  - id: ASSERT_Byuli_StarEyes
    subject: CHR_Byuli
    predicate: hasEyeMotif
    object: black_eyes_with_white_star_pupils
    source_image_id: Image_Byuli_001
    source_role: approved canon source
    confidence: user_confirmed
    canon_status: confirmed
    approval_status: approved
    evidence_refs:
      - EV_Byuli_Face_001
    retrieval_scope: current_conversation_only
    asserted_by: user
    derived_from:
      - image_analysis_byuli_001
      - UA_Byuli_001
    needs_confirmation: false
```

Also add graph relations when useful:

```yaml
relations:
  - subject: UA_Byuli_001
    predicate: answersQuestion
    object: Q_Byuli_001
  - subject: ASSERT_Byuli_StarEyes
    predicate: wasDerivedFrom
    object: UA_Byuli_001
```

## Recompute Rules

After applying answers:

1. Move answered questions from `question_queue` to `answered_questions`.
2. Update affected `canon_assertions`:
   - `approve_as_canon` -> `source_role: approved canon source`, `approval_status: approved`, `confidence: user_confirmed`, `canon_status: confirmed`.
   - `keep_as_candidate` -> keep observed facts `canon_status: provisional`.
   - `reference_only` -> `source_role: reference image`, keep out of hard canon.
   - `not_permanent_prop` -> move prop facts to `allowed_variation` or scene-specific notes.
   - `exact_text_required` -> put text in `Text (verbatim)`; move it into `Confirmed constraints` only after the linked assertion is approved.
3. Recompute `Handoff status`:
   - `ready` only when all `blocking_for_ready: true` questions are answered and no reject validation shape remains.
   - `provisional` when remaining uncertainty is explicit and no `blocking_for_provisional: true` question remains unanswered.
   - `blocked` only when a `blocking_for_provisional: true` question remains unanswered or a hard-stop condition applies.
4. Rebuild `$imagegen Prompt Pack` from the recomputed assertion states.

## Output Pattern

When questions are pending but a provisional result is safe:

```text
Clarification Gate: proceeding_with_provisional

Question Queue:
Q_Byuli_001 [ready-blocking]: Image_Byuli_001을 approved canon source로 승격할까요?
Q_Byuli_002 [ready-blocking]: 티셔츠 문구를 항상 정확히 유지해야 하나요?
Q_Byuli_003 [optional]: 말차 라떼와 스케이트보드는 고정 소품인가요?

Current Handoff status: provisional
Provisional output generated now: ontology + $imagegen prompt pack.
Next action after answers: update user_answers provenance, recompute canon_status, regenerate prompt pack.
```

When answers have been applied:

```text
Clarification Gate: resolved
Applied user_answers:
- UA_Byuli_001 answered Q_Byuli_001: approve_as_canon

Recomputed Handoff status: ready
```
