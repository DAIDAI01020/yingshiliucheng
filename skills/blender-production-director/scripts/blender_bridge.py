"""Runs inside Blender only; request/report protocol for the host runner."""
import json
from pathlib import Path
import runpy
import sys

import bpy


def selected_scene(request):
    name = request.get("scene")
    if name and name not in bpy.data.scenes:
        raise ValueError("Requested scene does not exist.")
    scene = bpy.data.scenes[name] if name else bpy.context.scene
    bpy.context.window.scene = scene
    return scene


def inspect_scene(scene):
    dependencies, missing, unresolved = set(), [], []
    for collection in (bpy.data.images, bpy.data.fonts, bpy.data.libraries, bpy.data.movieclips, bpy.data.sounds):
        for item in collection:
            if getattr(item, "packed_file", None) or getattr(item, "packed_files", None):
                continue
            source = getattr(item, "source", "")
            if source in ("TILED", "SEQUENCE", "MOVIE"):
                unresolved.append(item.name)
                continue
            location = getattr(item, "filepath", "")
            if not location or location == "<builtin>" or source in ("GENERATED", "VIEWER"):
                continue
            target = str(Path(bpy.path.abspath(location, library=getattr(item, "library", None))).resolve())
            dependencies.add(target)
            if not Path(target).is_file():
                missing.append(target)
    output_nodes = []
    visited = set()
    def scan_tree(tree):
        if not tree or tree.as_pointer() in visited:
            return
        visited.add(tree.as_pointer())
        for node in tree.nodes:
            if node.bl_idname == "CompositorNodeOutputFile":
                output_nodes.append(node.name)
            scan_tree(getattr(node, "node_tree", None))
    for value in bpy.data.scenes:
        scan_tree(getattr(value, "node_tree", None))
        scan_tree(getattr(value, "compositing_node_group", None))
    return {"ok": True, "blender_version": bpy.app.version_string, "scene": scene.name,
            "engine": scene.render.engine, "camera": scene.camera.name if scene.camera else None,
            "frames": [scene.frame_start, scene.frame_end], "fps": scene.render.fps / scene.render.fps_base,
            "resolution": [scene.render.resolution_x, scene.render.resolution_y],
            "color_management": {"view_transform": scene.view_settings.view_transform, "look": scene.view_settings.look},
            "objects": [{"name": o.name, "type": o.type, "materials": [s.name for s in o.material_slots],
                         "vertices": len(o.data.vertices) if o.type == "MESH" else None} for o in scene.objects],
            "dependencies": sorted(dependencies), "missing_dependencies": sorted(missing),
            "unresolved_dependencies": unresolved, "file_output_nodes": output_nodes,
            "dependency_limit": "Caches, plugins and sequencer inputs require task-specific review.",
            "visual_qc_status": "not_reviewed"}


def execute(request):
    scene = selected_scene(request)
    if request["action"] == "inspect":
        return inspect_scene(scene)
    if request["action"] == "build":
        target = Path(request["output"])
        if target.exists():
            raise ValueError("Refusing existing scene output.")
        runpy.run_path(request["script"], init_globals={"OUTPUT_BLEND": str(target), "PROJECT_ROOT": request["project_root"]}, run_name="__blender_task__")
        if target.exists():
            raise ValueError("Task scripts must leave saving to the runner.")
        bpy.ops.wm.save_as_mainfile(filepath=str(target), check_existing=False)
        return {"ok": target.is_file(), "blend": str(target)}
    if request["action"] != "render":
        raise ValueError("Unknown action.")
    if not scene.camera:
        raise ValueError("Scene has no active camera.")
    if inspect_scene(scene)["file_output_nodes"]:
        raise ValueError("Compositor File Output nodes require separately scoped execution.")
    if request.get("engine"):
        scene.render.engine = request["engine"]
    scene.frame_set(request["frame"])
    scene.render.resolution_percentage = request["scale"]
    scene.render.image_settings.file_format = request["format"]
    scene.render.use_file_extension = True
    # Full frames only: cropped border output needs a dedicated task runner.
    if scene.render.use_border and scene.render.use_crop_to_border:
        raise ValueError("Cropped border renders need an explicit crop-aware workflow.")
    target = Path(request["output"])
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        raise ValueError("Refusing existing render output.")
    scene.render.filepath = str(target)
    bpy.ops.render.render(write_still=True, scene=scene.name)
    loaded = bpy.data.images.load(str(target), check_existing=False)
    size = list(loaded.size)
    expected = [max(1, scene.render.resolution_x * request["scale"] // 100),
                max(1, scene.render.resolution_y * request["scale"] // 100)]
    bpy.data.images.remove(loaded)
    if size != expected:
        raise ValueError(f"Rendered dimensions {size} differ from expected {expected}.")
    return {"ok": True, "decoded": True, "size": size, "engine": scene.render.engine, "frame": request["frame"]}


if __name__ == "__main__":
    request = json.loads(Path(sys.argv[sys.argv.index("--") + 1]).read_text(encoding="utf-8"))
    result = execute(request)
    Path(request["report"]).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
