#!/usr/bin/env python3
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from resources_compiler.core.pipeline import ResourcePipeline

def main():
    parser = argparse.ArgumentParser(description="noi_engine Resource Packer Pipeline")
    parser.add_argument("-i", "--input", required=True, type=Path, help="Path to input resources directory")
    parser.add_argument("-o", "--output", required=True, type=Path, help="Path to output packed directory")

    args = parser.parse_args()
    pipeline = ResourcePipeline()
    pipeline.process_directory(args.input.resolve(), args.output.resolve())

if __name__ == "__main__":
    main()