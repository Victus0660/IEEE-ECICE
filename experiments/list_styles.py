import docx
import sys
sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document("c:/Users/Bill/Desktop/IEEE ECICE/Engineering_proceedings_Template_ecice2026.docx")
for s in doc.styles:
    print(f"Style: '{s.name}' (id: '{s.style_id}')")
