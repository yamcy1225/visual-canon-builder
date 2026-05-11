# Visual Canon Builder

`visual-canon-builder` is a Codex skill for turning character notes, worldbuilding notes, and reference images into an imagegen-ready visual canon kit with evidence-backed, user-friendly approval before final canon lock.

It does not generate images directly. It prepares:

- visual canon ontology
- image inventory and observed visual facts
- evidence cards, retrieval traces, guided approval questions, quick approval reviews, and batch approval payloads
- semantic relations and provenance-backed assertions
- identity canon, style canon, generation contracts, reference preservation, proportion, and view-projection rules
- API execution profiles, source-cell manifests, and exact text/mask policies
- evaluation loops, drift taxonomy, and targeted next-prompt patches
- validation shapes and checklists
- safe two-layer `$imagegen` edit/reference prompt packs
- no-dependency operational scripts and contract fixtures

## Repository Layout

```text
.codex/skills/visual-canon-builder/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   ├── approval_payload.schema.json
│   ├── evaluation_result.schema.json
│   ├── prompt_pack.schema.json
│   └── visual_canon.schema.json
├── scripts/
│   ├── apply_approval_payload.py
│   ├── build_prompt_pack.py
│   ├── create_source_cell_manifest.py
│   ├── run_generation_loop.py
│   ├── score_generation_review.py
│   └── validate_canon.py
└── references/
    ├── image-analysis-to-canon.md
    ├── evidence-interview-rag.md
    ├── evaluation-loop.md
    ├── generation-contract.md
    ├── interactive-clarification-loop.md
    ├── semantic-canon-model.md
    ├── style-canon-model.md
    ├── v3.4-goals-and-manual-tests.md
    ├── v3.5-ux-manual-tests.md
    ├── v3.6-style-fidelity-tests.md
    ├── v3.7-reference-preserve-tests.md
    └── visual-canon-template.md

tests/
├── fixtures/
│   ├── sample_approval.input.json
│   ├── sample_approval.payload.json
│   ├── sample_reference_preserve.input.json
│   └── sample_style_drift.evaluation.json
└── run_contract_tests.py
```

The installable skill directory is:

```text
.codex/skills/visual-canon-builder
```

## Install

### Global Codex Skill

Use this when you want the skill available across projects.

```bash
git clone https://github.com/yamcy1225/visual-canon-builder.git
SKILLS_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$SKILLS_DIR"
if [ -d "$SKILLS_DIR/visual-canon-builder" ]; then
  mv "$SKILLS_DIR/visual-canon-builder" "$SKILLS_DIR/visual-canon-builder.backup.$(date +%Y%m%d%H%M%S)"
fi
cp -R visual-canon-builder/.codex/skills/visual-canon-builder "$SKILLS_DIR/"
```

### Project-Local Skill

Use this when you want the skill available only in one workspace.

```bash
git clone https://github.com/yamcy1225/visual-canon-builder.git
PROJECT_SKILLS_DIR="/path/to/project/.codex/skills"
mkdir -p "$PROJECT_SKILLS_DIR"
if [ -d "$PROJECT_SKILLS_DIR/visual-canon-builder" ]; then
  mv "$PROJECT_SKILLS_DIR/visual-canon-builder" "$PROJECT_SKILLS_DIR/visual-canon-builder.backup.$(date +%Y%m%d%H%M%S)"
fi
cp -R visual-canon-builder/.codex/skills/visual-canon-builder "$PROJECT_SKILLS_DIR/"
```

## Validate

Run the built-in operational contract tests:

```bash
python tests/run_contract_tests.py
```

Validate a canon artifact:

```bash
python .codex/skills/visual-canon-builder/scripts/validate_canon.py \
  tests/fixtures/sample_reference_preserve.input.json
```

Build a two-layer prompt pack:

```bash
python .codex/skills/visual-canon-builder/scripts/build_prompt_pack.py \
  tests/fixtures/sample_reference_preserve.input.json
```

Gate a generated candidate so only pass-classified images are promoted:

```bash
python .codex/skills/visual-canon-builder/scripts/score_generation_review.py \
  tests/fixtures/sample_skateboard_fail.evaluation.json \
  --profile mascot_skateboard \
  --output-dir artifacts/sample_skate/skateboard-loop
```

If the image tool already exposed the candidates, use visible shortlist mode and offer only `shortlist/` candidates for user selection:

```bash
python .codex/skills/visual-canon-builder/scripts/score_generation_review.py \
  tests/fixtures/sample_compact_jump_pass.evaluation.json \
  --profile compact_mascot_identity \
  --review-mode visible_shortlist \
  --output-dir artifacts/sample_mascot/visible-shortlist
```

SampleMascot's strict profile also gates compact mascot proportions:

```bash
python .codex/skills/visual-canon-builder/scripts/score_generation_review.py \
  tests/fixtures/sample_compact_jump_limb_fail.evaluation.json \
  --profile compact_mascot_identity \
  --output-dir artifacts/sample_mascot/jump-loop
```

For automatic regenerate-until-pass workflows, use `run_generation_loop.py` with a generator command that writes `{candidate}` and an evaluator command that writes `{evaluation}`. Failed candidates are copied to `rejected/`; only pass candidates are copied to `accepted/`.

If Codex's `skill-creator` validator is available:

```bash
uv run --with pyyaml python "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" \
  "${CODEX_HOME:-$HOME/.codex}/skills/visual-canon-builder"
```

For project-local installs, replace the final path with:

```text
/path/to/project/.codex/skills/visual-canon-builder
```

## Use

Invoke the skill explicitly:

```text
Use $visual-canon-builder to turn these character reference images into an imagegen-ready visual canon kit.
```

Useful request shapes:

```text
Use $visual-canon-builder to analyze these three character references and identify immutable, variant, and unresolved canon details.
```

```text
Use $visual-canon-builder to run an evidence interview on this character sheet before locking the final canon.
```

For the friendlier review flow:

```text
$visual-canon-builder
이 이미지를 canon candidate로 보고 Evidence Interview Mode로 정본 후보를 정리해줘.
먼저 User Review와 Quick Approval Table로 승인할 항목을 쉽게 보여주고,
질문 1/N 방식으로 하나씩 승인할 수 있게 해주고,
그 다음 Visual Canon Ontology와 $imagegen prompt pack을 만들어줘.
```

Typical short replies after the first pass:

```text
1
```

```text
수정: 긴 보드는 장면 소품
```

```text
추천대로 진행
```

```text
전체 정본 승인
```

```text
정체성과 의상은 승인, 소품은 임시
```

```text
수정: 긴 보드는 장면 소품, 반바지 로고는 제거
```

```text
Use $visual-canon-builder to create a faction visual canon ontology and a safe $imagegen prompt pack.
```

```text
Use $visual-canon-builder to prepare a sprite cutout prompt pack with proportion lock and transparent-background constraints.
```

For strict identity/style preservation:

```text
Use $visual-canon-builder to build an identity-preserving edit/reference prompt pack from this character sheet.
Treat Image_001 as the identity anchor and style anchor.
Build identity_canon, style_canon, generation_contract, evaluation_loop, and a next_prompt_patch template.
Only change the requested pose; do not redesign the face, proportions, palette, line language, or rendering style.
```

## Output Contract

The skill is designed to produce:

- `User Review`
- `Guided Approval Interview`
- `Quick Approval Table`
- `Next Reply Options`
- `Image Inventory`
- `Evidence Cards`
- `Retrieval Trace`
- `Approval Review Pack`
- `Approval Payload`
- `Lock Summary`
- `Observed Visual Facts`
- `Conflicts And Unknowns`
- `Question Queue`
- `Clarification Gate`
- `User Answer Provenance`
- `Visual Canon Ontology`
- `Semantic Relations And Provenance`
- `Validation Shapes`
- `Style Canon`
- `Generation Contract`
- `API Execution Profile`
- `Source Cell Asset Manifest`
- `Exact Text Policy`
- `Evaluation Result`
- `Drift Patterns`
- `Prompt Patch`
- `$imagegen Prompt Pack` with `technical_contract` and `final_imagegen_prompt`
- `Validation Checklist`
- `Canon Promotion Notes`

Unconfirmed image-derived facts stay in `needs_confirmation`, `pending_user_approval`, `Provisional constraints`, or `Unresolved questions`. They should not be promoted into hard `$imagegen` constraints.

## Notes

- This is a lightweight ontology-inspired skill, not a full RDF/OWL/SHACL engine.
- The skill delegates actual image generation to `$imagegen`.
- The proportion projection model is an approximate orthographic envelope estimate, not a full 3D reconstruction.
- Reference-sheet-derived mascot/cartoon assets should include a strict `Style fidelity lock` so `$imagegen` does not drift into semi-realistic or 3D-rendered output.
- Identity-sensitive work should default to edit/reference-image handoff; text-only generation is for loose inspiration or no-reference cases.
- Exact character-sheet reuse should include `Reference preserve mode` with a chosen source cell; identity-only similarity is not enough when proportions or style are redesigned.
- When exact preservation is required, a cropped or isolated `source_cell_asset` should be used and listed first in reference ordering; a full multi-pose sheet alone should not be marked ready.
- API-ready prompt packs should specify `preferred_api`, `action`, `input_fidelity`, input ordering, mask policy, output format, and exact text fallback strategy.
- `final_imagegen_prompt` should stay short and executable; keep the full ontology and provenance in `technical_contract`.
- Generated outputs are reviewed through `evaluation_result`, `drift_patterns`, and `prompt_patch`; `pass` still requires user approval before canon promotion.
- Pass-only workflows must not present every generated candidate as final. Generate to a work directory, evaluate, reject/regenerate on failure, and expose only `accepted/` candidates.
- Character-specific strict profiles should include failure checks for known drift modes, such as star pupils and skateboard scale for SampleSkate, or arm/leg length and compact mascot ratio for SampleMascot.
- Canon questions are handled through `question_queue` and `user_answers`; unanswered ready-blocking questions no longer stop provisional output.
- Evidence Interview RAG Mode uses only current conversation inputs by default; it does not create a vector DB or separate click UI.
- The first-screen UX should be decision-oriented; strict IDs, hashes, and full YAML remain available in technical sections.
- `tests/run_contract_tests.py` turns the v3.4-v3.7 manual expectations into a small no-dependency regression surface.
