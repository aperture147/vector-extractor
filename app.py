#!/usr/bin/env python3
from argparse import ArgumentParser
from extractor import Extractor


parser = ArgumentParser()

parser.add_argument("-a", "--artboard-only", 
                    default=False,
                    action="store_true",
                    help="Split artboards in Illustrator into separated SVG files")
parser.add_argument("--no-cleanup",
                    default=False,
                    action="store_true",
                    help="Don't cleanup temporary file")
parser.add_argument("-p", "--inkscape-path",
                    default=None,
                    help="Inkscape execution file path")
parser.add_argument("-l", "--log",
                    default=False,
                    action="store_true",
                    help="Write log to file")

args = parser.parse_args()

extractor = Extractor(inkscape_path=args.inkscape_path)

extraction_id = extractor.extract(
    'test.pdf',
    inkscape_log=args.log,
    artboard_only=args.artboard_only,
    cleanup=not args.no_cleanup)

print(f'extract ID: {extraction_id}')
