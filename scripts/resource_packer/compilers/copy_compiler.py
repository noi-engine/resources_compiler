import shutil
from pathlib import Path
from resource_packer.core.base_compiler import BaseResourceCompiler

class CopyResourceCompiler(BaseResourceCompiler):
    """Fallback compiler that copies raw Resource files without modification."""

    def compile(self, src_path: Path, dst_dir: Path) -> Path:
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst_path = dst_dir / src_path.name
        shutil.copy2(src_path, dst_path)
        return dst_path