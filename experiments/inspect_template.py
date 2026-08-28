import docx
import sys

# Set stdout encoding
sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document("c:/Users/Bill/Desktop/IEEE ECICE/Engineering_proceedings_Template_ecice2026.docx")

paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]

print(f"Total non-empty paragraphs: {len(paragraphs)}")
for i, p in enumerate(paragraphs[:35]):
    print(f"[{i}] {p[:120]}")
