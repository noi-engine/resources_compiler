import sys
from pathlib import Path
from typing import Dict

from resources_compiler.core.base_compiler import BaseResourceCompiler
from resources_compiler.compilers.copy_compiler import CopyResourceCompiler
from resources_compiler.compilers.scene_compiler import SceneResourceCompiler
from resources_compiler.compilers.mesh_2d_compiler import Mesh2DResourceCompiler
from resources_compiler.compilers.shader_compiler import ShaderResourceCompiler

class ResourcePipeline:
    def __init__(self):
        self._fallback_compiler = CopyResourceCompiler()

        self._compilers: Dict[str, BaseResourceCompiler] = {
            ".scene": SceneResourceCompiler(),
            ".mesh": Mesh2DResourceCompiler(),
            ".shader": ShaderResourceCompiler(),
        }

    def process_file(
        self,
        src_file: Path,
        input_root: Path,
        output_root: Path
    ) -> Path:
        rel_path = src_file.relative_to(input_root)
        dst_dir = (output_root / rel_path).parent

        filename = src_file.name.lower()

        compiler = self._fallback_compiler

        for extension, candidate in self._compilers.items():
            if filename.endswith(extension):
                compiler = candidate
                break

        return compiler.compile(src_file, dst_dir)

    def process_directory(
        self,
        input_root: Path,
        output_root: Path
    ) -> None:
        if not input_root.exists():
            print(
                f"[Resource COMPILER ERROR] "
                f"Source directory does not exist: '{input_root}'",
                file=sys.stderr
            )
            sys.exit(1)

        output_root.mkdir(
            parents=True,
            exist_ok=True
        )

        success_count = 0
        error_count = 0

        for src_file in input_root.rglob("*"):
            if not src_file.is_file():
                continue

            try:
                out_path = self.process_file(
                    src_file,
                    input_root,
                    output_root
                )

                print(
                    f"[COMPILED] "
                    f"{src_file.relative_to(input_root)} "
                    f"-> "
                    f"{out_path.relative_to(output_root)}"
                )

                success_count += 1

            except Exception as exception:
                error_count += 1

                print(
                    f"[COMPILE ERROR] "
                    f"{src_file.relative_to(input_root)}: "
                    f"{exception}",
                    file=sys.stderr
                )

        if error_count > 0:
            print(
                f"\n[Resource COMPILER FAILED] "
                f"{error_count} file(s) failed to compile.",
                file=sys.stderr
            )

            sys.exit(1)

        print(
            f"\n[Resource COMPILER SUCCESS] "
            f"Successfully compiled {success_count} Resource(s)."
        )