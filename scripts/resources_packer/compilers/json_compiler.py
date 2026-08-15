import json
import sys
import msgpack
from pathlib import Path
from resources_packer.core.base_compiler import BaseResourceCompiler

class JsonResourceCompiler(BaseResourceCompiler):
    """Compiles JSON text files into binary MessagePack (.msgpack)."""

    def compile(self, src_path: Path, dst_dir: Path) -> Path:
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst_path = dst_dir / f"{src_path.stem}.msgpack"

        try:
            with open(src_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            packed_bytes = msgpack.packb(data, use_bin_type=True)

            with open(dst_path, "wb") as f:
                f.write(packed_bytes)

            return dst_path

        except json.JSONDecodeError as err:
            print(f"\n[Resource PACKER ERROR] Syntax error in JSON file: {src_path}", file=sys.stderr)
            print(f"  --> Line {err.lineno}, Column {err.colno}: {err.msg}\n", file=sys.stderr)
            raise RuntimeError(f"Failed to compile JSON Resource: {src_path.name}") from err

        except Exception as err:
            print(f"\n[Resource PACKER ERROR] Unexpected error while processing {src_path}: {err}\n", file=sys.stderr)
            raise