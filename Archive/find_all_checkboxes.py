import fitz  # PyMuPDF

pdf_document = fitz.open('IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf')

# Check both pages for YES/NO text
for page_num in range(len(pdf_document)):
    page = pdf_document[page_num]
    text_dict = page.get_text("dict")

    print(f"\n{'='*80}")
    print(f"PAGE {page_num + 1} - Looking for YES/NO checkbox areas:")
    print('='*80)

    # Find all text with "Yes" or "No"
    yes_no_positions = []
    for block in text_dict["blocks"]:
        if "lines" in block:
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if text in ["Yes", "YES", "No", "NO", "Ja", "Nee"]:
                        bbox = span["bbox"]
                        yes_no_positions.append({
                            'text': text,
                            'x': bbox[0],
                            'y': bbox[1],
                            'bbox': bbox
                        })

    # Group by Y position (same line)
    lines = {}
    for item in yes_no_positions:
        y = item['y']
        found = False
        for line_y in lines.keys():
            if abs(y - line_y) < 5:
                lines[line_y].append(item)
                found = True
                break
        if not found:
            lines[y] = [item]

    # Sort and display
    sorted_lines = sorted(lines.items(), key=lambda x: x[0])

    for i, (y, items) in enumerate(sorted_lines):
        items.sort(key=lambda x: x['x'])
        print(f"\nCheckbox row {i+1} at Y={y:.1f}:")
        for item in items:
            print(f"  '{item['text']}' at X={item['x']:.1f}")

pdf_document.close()
