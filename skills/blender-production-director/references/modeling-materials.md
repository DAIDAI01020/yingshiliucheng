# Modeling And Materials

## Construction

Inspect references for silhouette, dimensions, assembly, material zones and manufacturing cues. Separate measured facts from inferred hidden surfaces.

- Product/hard surface: block proportions first; choose bevels, subdivision, booleans or explicit topology for reflection quality and editability. Check bevel width against real scale.
- Environments/stages: establish floor, camera and screen/performer proportions before detail. Use modular assets and instances where appropriate.
- Organic/character assets: choose authorized assets, sculpting or retopology according to deformation/close-up needs. State remaining manual sculpt/weight refinement.
- Lettering: lock exact glyphs, font source, spacing, depth and edges. Preserve text sources when useful and create mesh copies when needed. Font substitution is a visible change.
- Single images supply shape/style evidence, not precise unseen geometry. Imported CAD/scans/game assets need scale, axis, normals and dependencies checked.

## Geometry Validation

For rendered props inspect silhouette, shading, highlights, intersections, normals and excessive geometry. For deformation inspect joint/facial topology. For fabrication/export check manifoldness, thickness and destination constraints only when needed.

Preserve hidden parts needed by later angles/animation. Keep source collections separate from export subsets; do not flatten the editable master by default.

## UV And Shaders

- Use UVs where logo placement, baking or controlled texture mapping requires them; procedural coordinates may suit other surfaces.
- Set color space according to texture meaning: color versus normal/roughness/displacement data. Verify normal orientation on the object.
- Match roughness, material scale, metal/anisotropic response and glass thickness under representative light.
- Name slots/parameters by function. Check shared materials before target-only changes.
- Bake only required maps, with appropriate resolution and margins; validate on an export copy and preserve the original network.
- Pack distributable textures or preserve relative paths. Linked assets, fonts, sequences and caches may need separate packaging. Record source/license of external assets.

## Revision

Identify target objects/materials by stable name. Compare before/after inventories; preserve camera, animation and unaffected assignments. Geometry changes that invalidate UVs, rigs or caches must update those dependencies explicitly.
