from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import pytesseract
import io
import re

app = FastAPI()

def extract_receipt_data(text):
    store = "Unknown"
    date = "Unknown"
    total = "Unknown"

    lines = text.strip().splitlines()
    for line in lines:
        if any(keyword in line.lower() for keyword in ['biltema', 'coop', 'obs', 'byggmax', 'jysk', 'extra', 'kiwi']):
            store = line.strip()
            break
    if store == "Unknown" and lines:
        store = lines[0].strip()

    date_match = re.search(r'(\d{2}[./-]\d{2}[./-]\d{2,4})', text)
    if date_match:
        date = date_match.group(1)

    total_match = re.search(r'(total(?:t)?|sum|beløp)\s*[:\-]?\s*([\d\s,.]+)', text, re.IGNORECASE)
    if total_match:
        raw_total = total_match.group(2)
        total = raw_total.replace(" ", "").replace(",", ".").strip()

    return {
        "store": store,
        "date": date,
        "total": total
    }

@app.post("/parse")
async def parse_receipt(file: UploadFile = File(...)):
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))
    text = pytesseract.image_to_string(image, lang='nor+eng')
    data = extract_receipt_data(text)
    return JSONResponse(content=data)
