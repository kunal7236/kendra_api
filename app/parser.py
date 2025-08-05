import pdfplumber
from typing import Dict, Iterator

def parse_pdf(pdf_path: str) -> Iterator[Dict]:
    """
    Parse Jan Aushadhi Kendra PDF into structured records.
    Streams entries instead of building a huge list.
    Expected columns:
    Sr.No | Kendra Code | Name | Contact | State Name | District Name | Pin Code | Address
    """
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if not table:
                continue

            for row in table:
                # Skip empty rows
                if not row or not row[0]:
                    continue

                # First column must be a number (Sr.No)
                if not row[0].strip().isdigit():
                    continue

                # Ensure row has at least 8 columns
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
