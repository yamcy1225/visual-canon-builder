---
name: visual-canon-builder
description: Build user-friendly, imagegen-ready visual canon kits from character, faction, worldbuilding, costume, item, environment, game-asset notes, or one or more reference images, especially when preserving identity, original style, proportions, palette, line language, and preventing visual drift matters. Use when Codex needs to analyze visual references, run a compact evidence interview before canon lock, let the user approve/revise/reject canon candidates in plain language, document observed visual facts, create a lightweight visual knowledge graph with provenance, validation shapes, proportion/view-projection rules, generation contracts, evaluation loops, API execution profiles, source-cell manifests, and safe `$imagegen` edit/reference prompt packs without directly generating images.
---

# Visual Canon Builder

## Purpose

Use this skill to turn creative notes and visual references into a practical visual canon system. The output should help `$imagegen` preserve the same character, mascot, prop, faction mark, sprite, illustration style, or product-like asset across generations by making canon, uncertainty, handoff rules, and review criteria explicit before image generation.

This skill does not generate images, call image APIs, train adapters, or operate ControlNet/IP-Adapter. It prepares an evidence-backed canon kit and an `$imagegen`-ready prompt pack. If the user also wants images, produce the prompt pack first, then hand off to `$imagegen`.

This is a lightweight ontology-inspired workflow, not a full RDF/OWL/SHACL implementation. Still, treat entities as classes/individuals, fields as properties, relationships as triples, assertions as provenance-backed claims, and validation rules as SHACL-like shapes.

## Core Workflow

1. Identify the target asset: character, faction, costume, item, environment, UI icon set, skill effect, sprite, source-cell edit, or scene.
2. If images are provided, start with an `Image Inventory`. Inspect local image paths before analysis; analyze attached images directly.
3. Split evidence into small `Evidence Cards`, map them to `Candidate Assertions`, and keep all image-derived claims provisional until the approval gate says otherwise.
4. Run the user-friendly evidence interview before final canon lock:
   - Ask exactly one current approval question at the top when approval is needed.
   - Show a compact `User Review`, `Quick Approval Table`, and `Next Reply Options`.
   - Keep IDs, hashes, and full YAML in technical sections unless the user asks for strict/audit mode.
5. Build canon layers:
   - `identity_canon`: face geometry, silhouette, anatomy, proportions, unique marks, symbols, costume structure, subject-left/right details.
   - `style_canon`: line, rendering, color, lighting, texture, camera, and composition language.
   - `variation_canon`: pose, expression, weathering, background, minor wear, scene props, and requested mutations.
   - `generation_contract`: reference roles, change budget, allowed mutations, forbidden mutations, invariant restatement.
   - `evaluation_contract`: identity/style/proportion/semantic checks, drift taxonomy, pass/fix/reject rules, prompt-patch format.
6. Separate observed facts from inference. Mark hidden, ambiguous, unapproved, or conflicting details as `needs_confirmation`, `pending_user_approval`, `keep_provisional`, or `unresolved`.
7. Ask only canon-critical clarification questions. Use a `question_queue` with stable IDs, `blocking_for_ready`, `blocking_for_provisional`, affected fields, and defaults. Continue with a provisional ontology and prompt pack unless a hard-stop condition applies.
8. Compile one or more `$imagegen` prompt packs. Put only user-approved assertions in `Confirmed constraints`; keep pending, inferred, role-ambiguous, or source-ambiguous facts in `Provisional constraints` or `Unresolved questions`.
9. Add a validation checklist, drift taxonomy, prompt-patch loop, and canon promotion rule. Generated outputs never become canon automatically.

## v3.8 Operational Mode

Use the operational pipeline when the user needs production-like repeatability, exact source-cell preservation, or repeated prompt-pack generation:

1. Build or update the canon ontology.
2. Apply approval decisions with `scripts/apply_approval_payload.py` when the user gives batch approval.
3. Validate invariants with `scripts/validate_canon.py`.
4. Build a two-layer prompt pack with `scripts/build_prompt_pack.py`:
   - `technical_contract`: full ontology, contracts, assertions, source-cell manifest, API profile, and evaluation rules.
   - `final_imagegen_prompt`: short executable prompt focused on task, references, change-only rules, preserve rules, style lock, and avoid list.
5. For exact character-sheet reuse, create a `source_cell_asset_manifest` with `scripts/create_source_cell_manifest.py` or equivalent manual coordinates before marking handoff `ready`.
6. For pass-only delivery, generate candidates into a temporary directory, evaluate each candidate, and gate it with `scripts/score_generation_review.py`; use `scripts/run_generation_loop.py` when a command-driven generator/evaluator is available.
   - If the generation surface exposes candidates immediately, use `--review-mode visible_shortlist` instead of pretending they were hidden: label each exposed output as `keep_candidate`, `repair_candidate`, or `discard`, and offer only `shortlist/` candidates for user selection.
7. Run `tests/run_contract_tests.py` after changing schemas, scripts, or handoff rules.

No new dependency is required for these scripts when inputs are JSON. YAML is accepted only when PyYAML is already installed.

Do not present failed candidates as final. If the user asks for automatic verification, failed candidates go to `rejected/`, the prompt patch is appended to the next attempt, and only `pass` candidates are copied to `accepted/`. If candidates are already visible because of the active image tool, keep the visible review honest: immediately score them, mark failures as `discard`, keep only passing outputs in `shortlist/`, and make it clear that discarded images are not canon or selectable finals.

## Reference Navigation

Load only the reference needed for the current turn:

- `references/image-analysis-to-canon.md`: image inventory, observed facts, image role gates, proportion/view extraction.
- `references/evidence-interview-rag.md`: evidence cards, guided approval interview, approval payloads, user-answer provenance.
- `references/interactive-clarification-loop.md`: question queues, provisional progression, answer application.
- `references/style-canon-model.md`: identity-bound style extraction and style drift prevention.
- `references/generation-contract.md`: edit/reference handoff, API execution profile, final prompt split, exact text/mask policy.
- `references/evaluation-loop.md`: pass/fix/reject review, drift taxonomy, prompt patches, canon promotion.
- `references/semantic-canon-model.md`: ontology mapping, relations, assertions, validation shapes, JSON-LD export profile.
- `references/visual-canon-template.md`: copy/paste templates for full canon kits.
- `references/v3.4-goals-and-manual-tests.md`, `references/v3.5-ux-manual-tests.md`, `references/v3.6-style-fidelity-tests.md`, `references/v3.7-reference-preserve-tests.md`: regression goals and manual sample checks.

Use bundled schemas when checking or producing machine-readable artifacts:

- `assets/visual_canon.schema.json`
- `assets/approval_payload.schema.json`
- `assets/prompt_pack.schema.json`
- `assets/evaluation_result.schema.json`

## Confirmation And Handoff Gates

Treat `observed` and `confirmed canon` as different states:

```yaml
confirmation_gate:
  confirmed_when:
    - confidence: user_confirmed
      approval_status: approved
      user_answers_provenance: exists
      evidence_refs: min_count 1
  provisional_when:
    - confidence: observed
    - confidence: inferred
    - confidence: low_confidence
    - approval_status: pending_user_approval
    - approval_status: keep_provisional
  blocked_when:
    - identity_critical_conflict_unresolved
    - left_right_asymmetry_conflict_unresolved
    - canon_source_conflict_unresolved
    - proportion_required_but_missing_reference_dimension
```

Set `$imagegen` handoff status from canon risk:

```yaml
handoff_status_rules:
  ready:
    - all identity-critical assertions are approved or no canon lock is required
    - required source-cell, text, palette, left/right, and proportion locks are resolved
    - no reject or blocked validation shape remains unresolved
  provisional:
    - one usable canon candidate exists but is not yet approved
    - uncertainty is explicit in Provisional constraints or Unresolved questions
    - the requested draft can proceed without pretending provisional facts are canon
  blocked:
    - no usable canon candidate exists
    - identity-critical sources conflict
    - exact preservation is requested but no source-cell crop or isolated edit target exists
    - required text or left/right identity detail would have to be guessed
```

For identity-sensitive or style-sensitive requests, prefer `edit`, `edit_target_preserve`, or reference-image handoff. Text-only generation is allowed only when no reference exists, the user explicitly asks for loose inspiration, or identity/style preservation is not required.

## Reference Preserve Rules

When the user expects the output to look like the same exact character-sheet cell, a full multi-pose sheet alone is not enough. Require a `source_cell_asset` or isolated edit target and state which input image must be first.

```yaml
source_cell_asset_manifest:
  id: CROP_001
  source_image_id: Image_001
  source_region:
    label: front_full_body
    bbox: {x: needs_user_or_script, y: needs_user_or_script, width: needs_user_or_script, height: needs_user_or_script}
  role:
    - identity_anchor
    - style_anchor
    - proportion_anchor
  preservation_priority:
    - silhouette
    - head_body_ratio
    - limb_length
    - line_weight
    - detail_density
  ready_state: blocked_until_crop_exists
```

If a generated image keeps the broad identity but changes source-cell silhouette, proportions, line language, rendering style, or detail density, classify it as `reject` for strict preservation tasks, not `fix`.

## API Execution Profile

When preparing an API-ready handoff, include an `api_execution_profile` in the prompt pack:

```yaml
api_execution_profile:
  preferred_api: responses_api
  model_family: gpt_image
  action: edit
  input_fidelity: high
  reference_ordering:
    first_image: identity_anchor_or_source_cell_asset
    second_image: style_anchor_if_separate
    later_images:
      - composition_reference
      - prop_reference
      - forbidden_example
  mask:
    required: false
    use_when:
      - localized_edit
      - exact_text_change
      - expression_or_arm_position_change
  output:
    size: auto_or_requested
    format: png
    background: transparent_or_opaque_or_auto
```

For exact text such as shirt lettering, logos, poster text, or brand names, add `exact_text_policy`. Prefer image edit with a mask or postprocess text compositing when spelling, placement, and case must be exact.

## Output Contract

Return these sections unless the user asks for a narrower artifact:

1. User-facing approval first: `Guided Approval Interview`, `User Review`, `Quick Approval Table`, `Next Reply Options`.
2. Source and evidence: `Image Inventory`, `Evidence Cards`, `Retrieval Trace`, `Approval Review Pack`, `Approval Payload`, `Lock Summary`.
3. Canon and safety: `Visual Canon Ontology`, `Semantic Relations And Provenance`, `Validation Shapes`, `Question Queue`, `Clarification Gate`, `User Answer Provenance` when applicable.
4. Handoff: `$imagegen Prompt Pack`, `api_execution_profile`, `source_cell_asset_manifest` when needed, `Validation Checklist`, `Canon Promotion Notes`.

Keep the first screen concise and decision-oriented. Keep the final image prompt short enough to execute; keep the full technical contract available for audit and later regeneration.
