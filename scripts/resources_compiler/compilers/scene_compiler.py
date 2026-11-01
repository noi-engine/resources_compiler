import json
import tempfile
from pathlib import Path

from resources_compiler.core.base_compiler import BaseResourceCompiler
from resources_compiler.core.flatc import compile_flatbuffer

class SceneResourceCompiler(BaseResourceCompiler):
    # Entity fields only the editor uses (e.g. its Hierarchy folders). The game never sees them,
    # and flatc would reject them since scene.fbs doesn't declare them.
    _editor_only_entity_keys = ("folder",)

    _component_types = {
        "transform": "TransformComponent",
        "render_layer": "RenderLayerComponent",
        "mesh_renderer": "MeshRendererComponent",
        "scripts": "ScriptsComponent",
        "camera_2d": "Camera2DComponent",
        "box_collider": "BoxColliderComponent",
    }

    def compile(self, src_path: Path, dst_dir: Path) -> Path:
        dst_dir.mkdir(parents=True, exist_ok=True)

        with src_path.open("r", encoding="utf-8") as file:
            scene = json.load(file)

        self._preprocess_components(scene)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_scene_path = Path(temp_dir) / src_path.name

            with temp_scene_path.open("w", encoding="utf-8") as file:
                json.dump(scene, file, indent=2)

            return compile_flatbuffer("scene.fbs", temp_scene_path, dst_dir, src_path.stem, ".scene")

    def _preprocess_components(self, scene: dict) -> None:
        for entity in scene.get("entities", []):
            for key in self._editor_only_entity_keys:
                entity.pop(key, None)
            entity["components"] = [
                self._add_properties_type(component)
                for component in entity.get("components", [])
            ]

    def _add_properties_type(self, component: dict) -> dict:
        if "properties" not in component:
            return component

        component_type = component.get("type")

        if component_type not in self._component_types:
            raise ValueError(f"Unknown component type: '{component_type}'")

        # flatc's JSON parser resolves a union's value using its "<field>_type"
        # sibling, and only if that sibling has already been seen by the time
        # it reaches the value - so properties_type must be inserted right
        # before properties, regardless of the source JSON's own key order
        # (e.g. editor-saved scenes serialize properties before type).
        result = {}
        for key, value in component.items():
            if key == "properties":
                result["properties_type"] = self._component_types[component_type]
            result[key] = value
        return result
                