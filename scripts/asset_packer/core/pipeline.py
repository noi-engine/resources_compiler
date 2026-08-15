import sys
import shutil
import zipfile
from pathlib import Path
from typing import Dict
from asset_packer.core.base_compiler import BaseAssetCompiler
from asset_packer.compilers.json_compiler import JsonAssetCompiler
from asset_packer.compilers.copy_compiler import CopyAssetCompiler

class AssetPipeline:
    def __init__(self):
        self._fallback_compiler = CopyAssetCompiler()
        self._compilers: Dict[str, BaseAssetCompiler] = {
            ".json": JsonAssetCompiler(),
        }

    def process_file(self, src_file: Path, input_root: Path, temp_staging_root: Path) -> Path:
        rel_path = src_file.relative_to(input_root)
        dst_dir = (temp_staging_root / rel_path).parent

        extension = src_file.suffix.lower()
        compiler = self._compilers.get(extension, self._fallback_compiler)

        return compiler.compile(src_file, dst_dir)

    def process_directory(self, input_root: Path, output_pack_file: Path) -> None:
        if not input_root.exists():
            print(f"[ASSET PACKER ERROR] Source directory does not exist: '{input_root}'", file=sys.stderr)
            sys.exit(1)

        temp_staging_dir = output_pack_file.parent / f".tmp_{output_pack_file.stem}"
        if temp_staging_dir.exists():
            shutil.rmtree(temp_staging_dir)
        temp_staging_dir.mkdir(parents=True, exist_ok=True)

        success_count = 0
        error_count = 0

        for src_file in input_root.rglob("*"):
            if src_file.is_file():
                try:
                    out_path = self.process_file(src_file, input_root, temp_staging_dir)
                    print(f"[COMPILED] {src_file.relative_to(input_root)} -> {out_path.relative_to(temp_staging_dir)}")
                    success_count += 1
                except Exception:
                    error_count += 1

        if error_count > 0:
            shutil.rmtree(temp_staging_dir, ignore_errors=True)
            print(f"\n[ASSET PACKER BUILD FAILED] {error_count} file(s) failed to compile.", file=sys.stderr)
            sys.exit(1)

        output_pack_file.parent.mkdir(parents=True, exist_ok=True)

        final_pack_path = output_pack_file.with_suffix(".pack")

        print(f"\n[PACKING] Archiving into binary package: {final_pack_path}")
        with zipfile.ZipFile(final_pack_path, "w", zipfile.ZIP_DEFLATED) as pack:
            for compiled_file in temp_staging_dir.rglob("*"):
                if compiled_file.is_file():
                    arcname = compiled_file.relative_to(temp_staging_dir)
                    pack.write(compiled_file, arcname)

        shutil.rmtree(temp_staging_dir, ignore_errors=True)

        print(f"[ASSET PACKER SUCCESS] Successfully packed {success_count} asset(s) into '{final_pack_path.name}'.")