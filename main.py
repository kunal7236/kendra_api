from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from fastapi.responses import JSONResponse
from app.data_loader import load_data, save_data
from app.parser import parse_pdf
import os
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()
API_KEY = os.getenv("API_KEY")

app = FastAPI(title="Jan Aushadhi Kendra API", version="1.0")
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/location")
def get_by_location(state: str, district: str):
    data = load_data({"State Name": state, "District Name": district})
    return JSONResponse(content=data)

@app.get("/pincode/{pincode}")
def get_by_pincode(pincode: str):
    data = load_data({"Pin Code": pincode})
    return JSONResponse(content=data)

@app.get("/kendra/{kendra_code}")
def get_by_kendra_code(kendra_code: str):
    data = load_data({"Kendra Code": kendra_code})
    return JSONResponse(content=data)

@app.get("/status")
def get_status():
    data = load_data()
    return {"message": "Service is live", "updated_at": data["updated_at"]}

@app.post("/upload")
async def upload(file: UploadFile = File(...), x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    try:
        contents = await file.read()
        file_like = BytesIO(contents)
        entries = parse_pdf(file_like)

        save_data(entries)
        return {"message": "Data updated successfully", "entries": len(entries)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process PDF: {e}")
