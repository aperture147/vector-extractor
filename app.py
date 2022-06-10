#!/usr/bin/env python3
from argparse import ArgumentParser
from extractor import Extractor


parser = ArgumentParser()

parser.add_argument("-a", "--artboard-only", default=False, action="store_true")
parser.add_argument("-c", "--not-cleanup", default=False, action="store_true")
parser.add_argument("-p", "--inkscape-path", default='inkscape')
args = parser.parse_args()

extractor = Extractor("C:/Program Files/Inkscape/bin/inkscape")

extraction_id = extractor.extract(
    'test.pdf',
    artboard_only=args.artboard_only,
    cleanup=not args.not_cleanup)
    
print(f'extract ID: {extraction_id}')
