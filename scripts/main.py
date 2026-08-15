#!/usr/bin/env python3
import sys
import argparse
from pathlib import Path

# Add script directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from asset_packer.core.pipeline import AssetPipeline

def main():
    parser = argparse.ArgumentParser(description="noi_engine Asset Packer Pipeline")
    parser.add_argument("-i", "--input", required=True, type=Path, help="Path to input resources directory")
    parser.add_argument("-o", "--output", required=True, type=Path, help="Path to output packed directory")
    parser.add_argument("-f", "--file", type=Path, help="Process a single file instead of full directory")

    args = parser.parse_args()
    pipeline = AssetPipeline()

    if args.file:
        pipeline.process_file(args.file.resolve(), args.input.resolve(), args.output.resolve())
    else:
        pipeline.process_directory(args.input.resolve(), args.output.resolve())

if __name__ == "__main__":
    main()