import pdfplumber
from typing import List, Dict


def parse_pdf(file_path: str) -> List[Dict]:
    data = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                headers = None
                for row in table:
                    # Skip empty or too short rows
                    if not row or len([cell for cell in row if cell and cell.strip()]) < 3:
                        continue

                    # Identify headers
                    if headers is None:
                        headers = [cell.strip() if cell else "" for cell in row]
                        continue

                    # Skip if row length doesn't match headers
                    if len(row) != len(headers):
                        continue

                    entry = dict(zip(headers, [cell.strip() if cell else "" for cell in row]))
                    data.append(entry)

    return data