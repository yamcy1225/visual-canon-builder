# Interactive Clarification Loop

Use this reference when `$visual-canon-builder` needs user input before promoting visual facts, resolving conflicts, or preparing a ready `$imagegen` handoff.

## Purpose

The skill should not merely list questions and continue as if they were answered. It should:

1. Create a stable `question_queue`.
2. Ask the user only the blocking or high-value questions.
3. Stop when blocking answers are required for a ready handoff.
4. Convert user replies into `user_answers` provenance records.
5. Recompute canon assertions, handoff status, prompt constraints, and unresolved questions.

## Question Queue Schema

```yaml
clarification_gate:
  status: waiting_for_user
  reason: blocking_questions_prevent_ready_handoff
  max_questions_this_turn: 5

question_queue:
  - id: Q_Byuli_001
    question: Image_Byuli_001을 approved canon source로 승격할까요?
    type: canon_source_approval
    blocking: true
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
- `blocking`: `true` only when the answer changes whether handoff can be `ready`.
- `affects`: ontology fields, assertions, or prompt fields changed by the answer.
- `required_for`: what cannot be safely finalized without the answer.
- `default_if_unanswered`: usually `keep_provisional`, `keep_unresolved`, or `block_ready_handoff`.

## When To Stop And Wait

Stop and wait for user input when:
- A `blocking: true` question prevents `Handoff status: ready`.
- The user explicitly asks to confirm before `$imagegen`.
- A canon-critical conflict would otherwise be guessed.

Do not stop when:
- Only minor atmosphere, optional props, non-critical texture, or mood remains uncertain.
- A provisional prompt pack is acceptable and every uncertainty is clearly labeled.

When stopping, end the response with the queue and a short instruction such as:

```text
Clarification Gate: waiting_for_user
아래 질문에 답하면 user_answers provenance로 반영해서 온톨로지와 $imagegen prompt pack을 다시 계산하겠습니다.
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
   - `approve_as_canon` -> `source_role: approved canon source`, `confidence: user_confirmed`, `canon_status: confirmed`.
   - `keep_as_candidate` -> keep observed facts `canon_status: provisional`.
   - `reference_only` -> `source_role: reference image`, keep out of hard canon.
   - `not_permanent_prop` -> move prop facts to `allowed_variation` or scene-specific notes.
   - `exact_text_required` -> put text in `Text (verbatim)` and `Confirmed constraints`.
3. Recompute `Handoff status`:
   - `ready` only when all blocking questions are answered and no blocking validation shape remains.
   - `provisional` when remaining uncertainty is explicit and non-blocking.
   - `blocked` when a blocking question remains unanswered.
4. Rebuild `$imagegen Prompt Pack` from the recomputed assertion states.

## Output Pattern

When questions are pending:

```text
Clarification Gate: waiting_for_user

Question Queue:
Q_Byuli_001 [blocking]: Image_Byuli_001을 approved canon source로 승격할까요?
Q_Byuli_002 [blocking]: 티셔츠 문구를 항상 정확히 유지해야 하나요?
Q_Byuli_003 [non_blocking]: 말차 라떼와 스케이트보드는 고정 소품인가요?

Current Handoff status: provisional
Next action after answers: update user_answers provenance, recompute canon_status, regenerate prompt pack.
```

When answers have been applied:

```text
Clarification Gate: resolved
Applied user_answers:
- UA_Byuli_001 answered Q_Byuli_001: approve_as_canon

Recomputed Handoff status: ready
```
