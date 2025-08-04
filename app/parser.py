from typing import Tuple, List, Dict
import fitz  # PyMuPDF
from datetime import datetime

def parse_pdf(pdf_bytes: bytes) -> Tuple[List[Dict], str]:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    entries = []
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            for l in b.get("lines", []):
                text_line = " ".join([s["text"].strip() for s in l["spans"]])
                if text_line.strip() and text_line[0].isdigit():
                    parts = text_line.split()
                    try:
                        entry = {
                            "Kendra Code": parts[0],
                            "Name": " ".join(parts[1:-5]),
                            "Contact": parts[-5],
                            "State Name": parts[-4],
                            "District Name": parts[-3],
                            "Pin Code": parts[-2],
                            "Address": parts[-1]
                        }
                        entries.append(entry)
                    except:
                        continue
    updated_at = datetime.now().isoformat()
    return entries, updated_at
