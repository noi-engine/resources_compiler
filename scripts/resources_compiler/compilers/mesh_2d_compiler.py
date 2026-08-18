import subprocess
from pathlib import Path

from resources_compiler.core.base_compiler import BaseResourceCompiler


class Mesh2DResourceCompiler(BaseResourceCompiler):
    def compile(self, src_path: Path, dst_dir: Path) -> Path:
        dst_dir.mkdir(parents=True, exist_ok=True)

        schema_path = Path(__file__).parent / "fbs" / "mesh_2d.fbs"

        subprocess.run(
            [
                "flatc",
                "--binary",
                "-o",
                str(dst_dir),
                str(schema_path),
                str(src_path),
            ],
            check=True,
        )

        output_path = dst_dir / f"{src_path.stem}.mesh"
        generated_path = dst_dir / f"{src_path.stem}.bin"

        generated_path.rename(output_path)

        return output_path