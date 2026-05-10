# Style Canon Model

Use this reference when `$visual-canon-builder` must preserve the original visual feeling of a reference, not only the subject's named traits. Style canon is separate from identity canon: a generation can keep the same character species, costume, and marks while still failing because the line language, rendering, palette, or camera language drifted.

## When To Use

Create `style_canon` whenever:

- The user says same style, same feeling, original vibe, keep this look, preserve brand/mascot design, or do not redraw/reinterpret.
- The reference image has a distinctive line, shading, texture, palette, lighting, camera, or composition treatment.
- A previous generation matched identity but looked like a different illustrator, medium, render engine, or age/proportion system.

For loose inspiration, keep style observations provisional and do not turn them into hard constraints.

## Core Shape

```yaml
style_canon:
  id: STYLE_001
  source_images:
    - Image_001
  style_role: <identity_bound_style | style_reference | mood_reference | loose_inspiration>
  line_language:
    contour_weight: <thin | medium | bold | variable>
    contour_variation: <uniform | tapered_pressure | sketchy | none>
    interior_line_density: <sparse | medium | dense>
    edge_softness: <vector_sharp | clean_but_not_vector_sharp | painterly_soft>
    forbidden:
      - thick_comic_outline
      - sketchy_noise_lines
  rendering_language:
    medium: <flat_2d | cel_animation | painterly | 3d_render | photo | ink_sketch>
    shading_model: <none | flat_grayscale | cel_shadow | soft_cel | painterly_blend | volumetric>
    shadow_edge: <hard | soft_medium | diffuse>
    highlight_shape: <none | small_controlled | broad_glossy>
    detail_density: <low | medium_low | medium | high>
    surface_finish: <matte | satin | glossy>
    forbidden:
      - glossy_3d_render
      - hyperreal_skin_texture
      - oil_paint_impasto
  color_language:
    saturation: <muted | reference_matched | vivid | neon>
    value_range: <low_key | mid_to_high | broad>
    contrast: <low | moderate | high>
    temperature: <warm | neutral | cool | mixed>
    palette_drift_tolerance: <none | low | medium>
    forbidden:
      - neon_saturation
      - cold_blue_global_grade
  lighting_language:
    direction: <front | front_left | top | ambient | scene_specific>
    contrast: <gentle | moderate | harsh>
    ambient_fill: <low | medium | high>
    mood: <calm | playful | dramatic | eerie | etc>
    forbidden:
      - cinematic_rim_light
      - harsh_noir_shadow
  texture_language:
    material_detail: <simplified | stylized | realistic>
    surface_noise: <none | subtle | grainy | heavy>
    forbidden:
      - realistic_fur
      - product_render_sneaker_detail
  camera_language:
    camera_height: <neutral | low | high>
    lens_feel: <orthographic | low_distortion | portrait_lens | wide_angle>
    perspective_strength: <none | low | moderate | strong>
    forbidden:
      - extreme_low_angle
      - wide_angle_face_distortion
  composition_language:
    framing: <centered_character_first | sheet_cell | dynamic_scene | icon_silhouette>
    negative_space: <tight | balanced | generous>
    rhythm: <static | calm | playful | dynamic>
  identity_style_binding:
    style_is_part_of_identity: <true | false>
    must_preserve_across:
      - new_pose
      - new_scene
      - outfit_variant
```

## Style Assertions

Use `style_assertions` for style facts that need evidence, approval, or later correction.

```yaml
style_assertions:
  - id: SASSERT_001
    subject: STYLE_001
    predicate: hasLineLanguage
    object: clean bold black contour with sparse simple interior lines
    evidence_refs:
      - EV_Style_Line_001
    source_image_id: Image_001
    source_role: approved canon source
    confidence: observed
    approval_status: pending_user_approval
    canon_status: provisional
```

Promote style assertions to confirmed only when they are either user-approved or clearly included in a user-declared style reference. Style-reference-only observations remain provisional when the user is asking for identity canon, because style and identity anchors can differ.

## Extraction Checklist

- Describe the line language before naming a broad medium.
- Separate identity features from rendering features.
- Note what must not happen: 3D render, semi-realistic anatomy, glossy materials, realistic fur/skin, product-detail props, painterly gradients, or generic anime drift.
- If the style is part of the character identity, mark `style_is_part_of_identity: true`.
- If a style translation is requested, create a new style variant instead of editing the original style canon.

## `$imagegen` Handoff Add-On

```text
Style constraints:
- Preserve the reference line language: <line_language>.
- Preserve the rendering language: <rendering_language>.
- Preserve the color and lighting language: <color_language>; <lighting_language>.
- Do not restyle into: <negative_style_drift>.
```

If style is identity-bound, also include:

```text
This style is part of the character identity, not an optional aesthetic. Do not redesign, restyle, beautify, make more realistic, make more glossy, or make more generic.
```
