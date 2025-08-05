import pdfplumber
from typing import Dict, Iterator

def parse_pdf(pdf_path: str) -> Iterator[Dict]:
    """
    Parse Jan Aushadhi Kendra PDF into structured records.
    Streams entries one page at a time without loading the entire PDF into memory.
    Expected columns:
    Sr.No | Kendra Code | Name | Contact | State Name | District Name | Pin Code | Address
    """
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = pdf.page_count

    for i in range(total_pages):
        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[i]
            table = page.extract_table()
            if not table:
                continue

            for row in table:
                if not row or not row[0]:
                    continue
                if not row[0].strip().isdigit():
                    continue

                while len(row) < 8:
                    row.append("")

                yield {
                    "Sr.No": row[0].strip(),
                    "Kendra Code": row[1].strip() if row[1] else "",
                    "Name": row[2].strip() if row[2] else "",
                    "Contact": row[3].strip() if row[3] else "",
                    "State Name": row[4].strip() if row[4] else "",
                    "District Name": row[5].strip() if row[5] else "",
                    "Pin Code": row[6].strip() if row[6] else "",
                    "Address": row[7].strip() if row[7] else ""
                }
