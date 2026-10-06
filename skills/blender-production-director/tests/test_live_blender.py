"""Tiny real-Blender smoke test. Explicitly skipped when Blender is absent."""
import os
from pathlib import Path
import tempfile
import unittest

from test_blender_task import runner

SCENE_SCRIPT = '''
import bpy
from mathutils import Vector
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0.7))
product = bpy.context.object
product.name = 'Product'
product.scale = (0.6, 0.4, 0.7)
bevel = product.modifiers.new('Edge finish', 'BEVEL')
bevel.width = 0.08
bevel.segments = 3
material = bpy.data.materials.new('Product finish')
material.use_nodes = True
material.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value = (0.03, 0.25, 0.6, 1)
product.data.materials.append(material)
product.keyframe_insert(data_path='location', frame=1)
product.location.z = 1.0
product.keyframe_insert(data_path='location', frame=3)
bpy.ops.mesh.primitive_plane_add(size=20)
bpy.context.object.name = 'Ground'
bpy.ops.object.light_add(type='AREA', location=(2, -3, 5))
light = bpy.context.object
light.data.energy = 500
light.data.shape = 'DISK'
light.data.size = 4
light.rotation_euler = (-light.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(3, -4, 2.5))
camera = bpy.context.object
camera.name = 'Hero camera'
camera.rotation_euler = (Vector((0,0,0.7))-camera.location).to_track_quat('-Z','Y').to_euler()
scene = bpy.context.scene
scene.camera = camera
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 1
scene.render.resolution_x = 64
scene.render.resolution_y = 48
scene.frame_start = 1
scene.frame_end = 3
scene.render.fps = 24
# Named parameterized procedural asset; node types shared across supported modern versions.
bpy.ops.mesh.primitive_cube_add(location=(1.5,0,0.4))
obj = bpy.context.object
obj.name = 'Procedural block'
group = bpy.data.node_groups.new('Block geometry', 'GeometryNodeTree')
if hasattr(group, 'interface'):
    group.interface.new_socket(name='Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
else:
    group.outputs.new('NodeSocketGeometry', 'Geometry')
cube = group.nodes.new('GeometryNodeMeshCube')
cube.inputs['Size'].default_value = (0.4,0.4,0.8)
out = group.nodes.new('NodeGroupOutput')
group.links.new(cube.outputs['Mesh'], out.inputs['Geometry'])
obj.modifiers.new('Procedural form','NODES').node_group = group
'''


class LiveBlenderTests(unittest.TestCase):
    def test_scene_render_resume_and_material_revision(self):
        environment = runner.doctor()
        if not environment["available"]:
            self.skipTest("Blender unavailable: real scene/render execution remains unverified")
        with tempfile.TemporaryDirectory(prefix="blender-live-test-") as directory:
            root = Path(directory)
            script = root / "scene.py"
            script.write_text(SCENE_SCRIPT, encoding="utf-8")
            source = root / "scene_v001.blend"
            build = runner.parser().parse_args(["build", "--project-root", str(root), "--script", str(script), "--output", str(source)])
            saved = runner.build(build, environment)
            self.assertTrue(saved["reopened"])
            self.assertIn("Procedural block", [o["name"] for o in saved["inspection"]["objects"]])
            before = runner.digest(source)
            render = runner.parser().parse_args(["render", "--project-root", str(root), "--blend", str(source), "--frames", "1,3", "--output-dir", str(root / "renders")])
            result = runner.render(render, environment)
            self.assertEqual(result["verified_frames"], [1, 3])
            manifest = runner.read_json(root / "renders" / "render-manifest.json")
            render.resume = True
            runner.render(render, environment)
            self.assertEqual(manifest["outputs"], runner.read_json(root / "renders" / "render-manifest.json")["outputs"])
            script.write_text("import bpy\nbpy.data.materials['Product finish'].node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value = 0.8\n", encoding="utf-8")
            build.blend = str(source)
            build.output = str(root / "scene_v002.blend")
            revised = runner.build(build, environment)
            self.assertEqual(revised["inspection"]["camera"], saved["inspection"]["camera"])
            self.assertEqual(revised["inspection"]["objects"], saved["inspection"]["objects"])
            self.assertEqual(runner.digest(source), before)


if __name__ == "__main__":
    unittest.main()
