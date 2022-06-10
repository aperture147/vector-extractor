#!/usr/bin/env python3
from argparse import ArgumentParser
from extractor import Extractor


parser = ArgumentParser()

parser.add_argument("-a", "--artboard-only", 
                    default=False,
                    action="store_true",
                    help="Split artboards in Illustrator into separated SVG files")
parser.add_argument("-c", "--no-cleanup",
                    default=False,
                    action="store_true",
                    help="Don't cleanup temporary file")
parser.add_argument("-p", "--inkscape-path",
                    default='inkscape',
                    help="Inkscape execution file path")
args = parser.parse_args()

DEFAULT_WINDOWS_INKSCAPE_PATH = "C:/Program Files/Inkscape/bin/inkscape.com"

extractor = Extractor(inkscape_path=DEFAULT_WINDOWS_INKSCAPE_PATH)

extraction_id = extractor.extract(
    'test.pdf',
    artboard_only=args.artboard_only,
    cleanup=not args.no_cleanup)

print(f'extract ID: {extraction_id}')
