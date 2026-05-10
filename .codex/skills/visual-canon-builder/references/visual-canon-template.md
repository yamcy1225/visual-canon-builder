# Visual Canon Templates

Use these templates when `$visual-canon-builder` needs a fuller reusable structure. Keep English keys for portability and Korean values/checklists when that matches the user's creative workflow.

## Character Canon Ontology

```yaml
entity_type: Character
id: CHR_001
name: <character name>
version: 1.0.0

identity:
  role: <playable_character | npc | boss | mascot | etc>
  faction: <faction id or name>
  visual_age_range: <visual age range>
  personality_keywords:
    - <keyword>

visual_core:
  silhouette:
    value: <slim_vertical | broad_armored | small_round | etc>
    immutable: true
  body:
    head_body_ratio: <ratio or descriptor>
    shoulder_width: <descriptor>
    leg_length: <descriptor>
    hand_size: <descriptor>
  face:
    eye_shape: <descriptor>
    eye_color: <canon color>
    unique_mark: <mark and location>
    jawline: <descriptor>
  hair:
    length: <descriptor>
    color: <canon color>
    bangs: <descriptor>
  costume:
    palette:
      primary: <canon color>
      secondary: <canon color>
      accent: <canon color>
    materials:
      - <material>
    must_have:
      - <required element>
    forbidden:
      - <forbidden element>

immutable:
  - <must-never-change visual rule>

allowed_variation:
  - <scene-dependent change allowed>

forbidden:
  - <visual drift or prohibited element>

canon_references:
  - front view sheet
  - side view sheet
  - back view sheet
  - face close-up
  - costume detail sheet
  - weapon or prop sheet
  - color palette
  - silhouette sheet
  - forbidden examples

validation_checks:
  identity:
    - <Korean checklist item>
  proportion:
    - <Korean checklist item>
  costume:
    - <Korean checklist item>
  forbidden:
    - <Korean checklist item>
```

## Faction Or World Canon Ontology

```yaml
entity_type: Faction
id: FCT_001
name: <faction name>
version: 1.0.0

identity:
  role_in_world: <kingdom | guild | cult | company | school | etc>
  tone_keywords:
    - <keyword>

visual_language:
  palette:
    primary: <canon color>
    secondary: <canon color>
    accent: <canon color>
  symbols:
    - <symbol>
  shapes:
    - <shape language>
  materials:
    - <material>
  architecture:
    - <architectural motif>
  costume_rules:
    - <dress rule>
  ui_or_icon_rules:
    - <icon or interface motif>

immutable:
  - <must-keep faction/world rule>

allowed_variation:
  - <regional, rank, class, or asset-type variation>

forbidden:
  - <color, symbol, style, or material that breaks canon>

canon_references:
  - faction emblem sheet
  - palette sheet
  - architecture sheet
  - costume rank sheet
  - forbidden examples

validation_checks:
  faction_identity:
    - 세력 색상과 문양이 유지되는가?
  world_consistency:
    - 지역/시대/재질 규칙이 깨지지 않았는가?
  forbidden:
    - 금지 색상, 금지 문양, 금지 실루엣이 생기지 않았는가?
```

## `$imagegen` Prompt Pack

```text
Use case: <imagegen taxonomy slug>
Asset type: <where this asset will be used>
Primary request: <requested image>
Input images: <Image 1: reference image; Image 2: edit target; Image 3: style reference> (optional)
Scene/backdrop: <environment or chroma-key background>
Subject: <main subject and canon identity>
Style/medium: <photo, illustration, concept art, sprite, icon, etc>
Composition/framing: <view, crop, layout, camera>
Lighting/mood: <lighting and emotion>
Color palette: <canon palette>
Materials/textures: <canon materials>
Text (verbatim): "<exact text, if any>"
Constraints: <immutable rules, canon lock, must keep>
Avoid: <forbidden rules, drift risks, watermark, unwanted text>
```

## Cutout / Transparent-Background Prompt Add-On

Use this add-on when the intended result is a sprite, sticker, item cutout, transparent asset, or background-extraction task.

```text
Scene/backdrop: flat solid #00ff00 background; perfectly uniform chroma-key field for background removal
Constraints: full subject visible, crisp separated edges, generous padding, no cast shadow, no contact shadow, no reflection, no background texture, do not use #00ff00 anywhere in the subject
Avoid: shadows, floor plane, gradients, key-color clothing or effects, watermark, extra text
```

## Validation Checklist

```text
[Identity Check]
- 핵심 얼굴, 실루엣, 색상, 문양이 정본과 일치하는가?
- 캐릭터/세력/아이템의 고유 표식이 올바른 위치에 있는가?

[Variation Check]
- 이번 장면에서 허용된 변주만 적용되었는가?
- 포즈, 날씨, 손상, 표정 변화가 정체성을 침범하지 않는가?

[Forbidden Check]
- 금지 색상, 금지 장식, 금지 의상, 금지 스타일이 생기지 않았는가?
- 다른 캐릭터나 세력의 시각 언어가 섞이지 않았는가?

[Imagegen Prompt Check]
- `Constraints`에 모든 immutable 규칙이 들어갔는가?
- `Avoid`에 모든 forbidden 규칙이 들어갔는가?
- 레퍼런스 이미지 역할이 `reference image`, `edit target`, `style reference`처럼 명확한가?
```

## Canon Promotion Flow

```text
generated -> reviewed -> corrected -> approved -> canon
```

- `generated`: 생성 직후. 아직 정본이 아니다.
- `reviewed`: 체크리스트로 검수된 상태.
- `corrected`: 수정 또는 재생성 지시가 반영된 상태.
- `approved`: 사람이 정본 후보로 승인한 상태.
- `canon`: 이후 프롬프트와 레퍼런스의 기준으로 사용할 수 있는 상태.

Rejected images can become `forbidden examples` if they clearly show a drift pattern to avoid.
