from fastapi import FastAPI, UploadFile, File, HTTPException, Header, Depends
from fastapi.responses import JSONResponse
from app.data_loader import load_data, save_data, get_status
from app.parser import parse_pdf
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()
API_KEY = os.getenv("API_KEY")

app = FastAPI()

@app.get("/location")
def get_by_location(state: str, district: str):
    result = load_data({"State Name": state, "District Name": district})
    return JSONResponse(content={"results": result})

@app.get("/pincode/{pincode}")
def get_by_pincode(pincode: str):
    result = load_data({"Pin Code": pincode})
    return JSONResponse(content={"results": result})

@app.get("/kendra/{kendra_code}")
def get_by_kendra_code(kendra_code: str):
    result = load_data({"Kendra Code": kendra_code})
    return JSONResponse(content={"results": result})

@app.get("/status")
def status():
    return get_status()

@app.post("/upload")
async def upload(file: UploadFile = File(...), authorization: Optional[str] = Header(None)):
    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Invalid API Key")
    try:
        contents = await file.read()
        entries, updated_at = parse_pdf(contents)
        save_data(entries, updated_at)
        return {"message": "Data updated successfully", "entries": len(entries)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process PDF: {e}")
