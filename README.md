# Visual Canon Builder

`visual-canon-builder` is a Codex skill for turning character notes, worldbuilding notes, and reference images into an imagegen-ready visual canon kit.

It does not generate images directly. It prepares:

- visual canon ontology
- image inventory and observed visual facts
- semantic relations and provenance-backed assertions
- proportion and view-projection rules
- validation shapes and checklists
- safe `$imagegen` prompt packs

## Repository Layout

```text
.codex/skills/visual-canon-builder/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── image-analysis-to-canon.md
    ├── interactive-clarification-loop.md
    ├── semantic-canon-model.md
    ├── v3.2-goals-and-manual-tests.md
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
Use $visual-canon-builder to create a faction visual canon ontology and a safe $imagegen prompt pack.
```

```text
Use $visual-canon-builder to prepare a sprite cutout prompt pack with proportion lock and transparent-background constraints.
```

## Output Contract

The skill is designed to produce:

- `Image Inventory`
- `Observed Visual Facts`
- `Conflicts And Unknowns`
- `Question Queue`
- `Clarification Gate`
- `User Answer Provenance`
- `Visual Canon Ontology`
- `Semantic Relations And Provenance`
- `Validation Shapes`
- `$imagegen Prompt Pack`
- `Validation Checklist`
- `Canon Promotion Notes`

Unconfirmed image-derived facts stay in `needs_confirmation`, `Provisional constraints`, or `Unresolved questions`. They should not be promoted into hard `$imagegen` constraints.

## Notes

- This is a lightweight ontology-inspired skill, not a full RDF/OWL/SHACL engine.
- The skill delegates actual image generation to `$imagegen`.
- The proportion projection model is an approximate orthographic envelope estimate, not a full 3D reconstruction.
- Blocking canon questions are handled through `question_queue` and `user_answers` before ready handoff.
- `references/v3.2-goals-and-manual-tests.md` records the current hardening goals and a Byuli character-sheet manual golden test.
