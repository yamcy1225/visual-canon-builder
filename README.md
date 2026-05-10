# Visual Canon Builder

`visual-canon-builder` is a Codex skill for turning character notes, worldbuilding notes, and reference images into an imagegen-ready visual canon kit with evidence-backed, user-friendly approval before final canon lock.

It does not generate images directly. It prepares:

- visual canon ontology
- image inventory and observed visual facts
- evidence cards, retrieval traces, guided approval questions, quick approval reviews, and batch approval payloads
- semantic relations and provenance-backed assertions
- identity canon, style canon, generation contracts, reference preservation, proportion, and view-projection rules
- evaluation loops, drift taxonomy, and targeted next-prompt patches
- validation shapes and checklists
- safe `$imagegen` edit/reference prompt packs

## Repository Layout

```text
.codex/skills/visual-canon-builder/
├── SKILL.md
├── agents/
│   └── openai.yaml
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
- `Evaluation Result`
- `Drift Patterns`
- `Prompt Patch`
- `$imagegen Prompt Pack`
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
- When exact preservation is required, a cropped or isolated `source_cell_asset` should be used; a full multi-pose sheet alone should not be marked ready.
- Generated outputs are reviewed through `evaluation_result`, `drift_patterns`, and `prompt_patch`; `pass` still requires user approval before canon promotion.
- Canon questions are handled through `question_queue` and `user_answers`; unanswered ready-blocking questions no longer stop provisional output.
- Evidence Interview RAG Mode uses only current conversation inputs by default; it does not create a vector DB or separate click UI.
- The first-screen UX should be decision-oriented; strict IDs, hashes, and full YAML remain available in technical sections.
- `references/v3.4-goals-and-manual-tests.md` records the hardening goals, and `references/v3.5-ux-manual-tests.md` records the user-friendly approval tests.
