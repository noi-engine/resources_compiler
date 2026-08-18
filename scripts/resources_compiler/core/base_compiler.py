from abc import ABC, abstractmethod
from pathlib import Path

class BaseResourceCompiler(ABC):
    """Abstract interface for all Resource compilers."""

    @abstractmethod
    def compile(self, src_path: Path, dst_dir: Path) -> Path:
        """
        Compiles or processes a source Resource file into the output directory.

        :param src_path: Path to the input source file.
        :param dst_dir: Target output directory.
        :return: Path to the generated output file.
        """
        pass