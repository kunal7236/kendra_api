import pdfplumber
from typing import List, Dict

def parse_pdf(pdf_path) -> List[Dict]:
    """
    Parse Jan Aushadhi Kendra PDF into structured records.
    Expected columns:
    Sr.No | Kendra Code | Name | Contact | State Name | District Name | Pin Code | Address
    """
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if not table:
                continue
            for row in table:
                if not row or not row[0] or not row[0].strip().isdigit():
                    continue
                # Ensure row has at least 8 columns
                while len(row) < 8:
                    row.append("")
                entry = {
                    "Sr.No": row[0].strip(),
                    "Kendra Code": row[1].strip(),
                    "Name": row[2].strip(),
                    "Contact": row[3].strip(),
                    "State Name": row[4].strip(),
                    "District Name": row[5].strip(),
                    "Pin Code": row[6].strip(),
                    "Address": row[7].strip()
                }
                data.append(entry)
    return data
