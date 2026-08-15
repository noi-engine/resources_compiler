import shutil
from pathlib import Path
from asset_packer.core.base_compiler import BaseAssetCompiler

class CopyAssetCompiler(BaseAssetCompiler):
    """Fallback compiler that copies raw asset files without modification."""

    def compile(self, src_path: Path, dst_dir: Path) -> Path:
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst_path = dst_dir / src_path.name
        shutil.copy2(src_path, dst_path)
        return dst_path