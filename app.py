from extractor import extract

extraction_id = extract('test.pdf', artboard_only=True)
print(f'extract ID: {extraction_id}')