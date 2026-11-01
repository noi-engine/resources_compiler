from pathlib import Path

from resources_compiler.core.base_compiler import BaseResourceCompiler
from resources_compiler.core.flatc import compile_flatbuffer


class ShaderResourceCompiler(BaseResourceCompiler):
    def compile(self, src_path: Path, dst_dir: Path) -> Path:
        dst_dir.mkdir(parents=True, exist_ok=True)
        return compile_flatbuffer("shader.fbs", src_path, dst_dir, src_path.stem, ".shader")
