import subprocess
from pathlib import Path

_SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "compilers" / "fbs"


def compile_flatbuffer(schema_name: str, json_path: Path, dst_dir: Path, stem: str, extension: str) -> Path:
    """
    Runs `flatc --binary` on a JSON file against one of the bundled schemas
    and renames flatc's `<stem>.bin` output to `<stem><extension>`.
    """
    schema_path = _SCHEMAS_DIR / schema_name

    subprocess.run(
        [
            "flatc",
            "--binary",
            "-o",
            str(dst_dir),
            str(schema_path),
            str(json_path),
        ],
        check=True,
    )

    generated_path = dst_dir / f"{stem}.bin"
    output_path = dst_dir / f"{stem}{extension}"

    generated_path.rename(output_path)

    return output_path
