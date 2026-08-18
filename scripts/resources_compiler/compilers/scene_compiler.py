import json
import subprocess
import tempfile
from pathlib import Path

from resources_compiler.core.base_compiler import BaseResourceCompiler

class SceneResourceCompiler(BaseResourceCompiler):
    _component_types = {
        "transform": "TransformComponent",
        "render_layer": "RenderLayerComponent",
        "mesh_renderer": "MeshRendererComponent",
        "scripts": "ScriptsComponent",
        "camera_2d": "Camera2DComponent",
    }

    def compile(self, src_path: Path, dst_dir: Path) -> Path:
        dst_dir.mkdir(parents=True, exist_ok=True)

        schema_path = Path(__file__).parent / "fbs" / "scene.fbs"

        with src_path.open("r", encoding="utf-8") as file:
            scene = json.load(file)

        self._preprocess_components(scene)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_scene_path = Path(temp_dir) / src_path.name

            with temp_scene_path.open("w", encoding="utf-8") as file:
                json.dump(scene, file, indent=2)

            subprocess.run(
                [
                    "flatc",
                    "--binary",
                    "-o",
                    str(dst_dir),
                    str(schema_path),
                    str(temp_scene_path),
                ],
                check=True,
            )

        generated_path = dst_dir / f"{src_path.stem}.bin"
        output_path = dst_dir / f"{src_path.stem}.scene"

        generated_path.rename(output_path)

        return output_path

    def _preprocess_components(self, scene: dict) -> None:
        for entity in scene.get("entities", []):
            for component in entity.get("components", []):
                if "properties" not in component:
                    continue

                component_type = component.get("type")

                if component_type not in self._component_types:
                    raise ValueError(
                        f"Unknown component type: '{component_type}'"
                    )

                component["properties_type"] = (
                    self._component_types[component_type]
                )
                