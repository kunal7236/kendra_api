from fastapi import FastAPI, UploadFile, File, HTTPException, Header, Query
from fastapi.responses import JSONResponse
from app.data_loader import load_data, save_data, client
from app.parser import parse_pdf
from datetime import datetime
from dotenv import load_dotenv
import os

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
    data = load_data({
        "State Name": {"$regex": f"^{state}$", "$options": "i"},
        "District Name": {"$regex": f"^{district}$", "$options": "i"}
    })
    return JSONResponse(content=data)

@app.get("/pincode/{pincode}")
def get_by_pincode(pincode: str):
    data = load_data({"Pin Code": pincode})
    return JSONResponse(content=data)

@app.get("/kendra/{kendra_code}")
def get_by_kendra_code(kendra_code: str):
    data = load_data({"Kendra Code": {"$regex": f"^{kendra_code}$", "$options": "i"}})
    return JSONResponse(content=data)

@app.get("/status")
def get_status():
    data = load_data()
    return {"message": "Service is live", "updated_at": data["updated_at"]}
    

@app.post("/upload")
async def upload(
    file: UploadFile = File(...),
    x_api_key: str = Header(...),
    reset: bool = Query(False, description="Set true on first chunk to reset DB")
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    temp_pdf_path = f"/tmp/{datetime.now().timestamp()}_{file.filename}"
    with open(temp_pdf_path, "wb") as f:
        while chunk := await file.read(1024 * 1024):  # 1MB chunks
            f.write(chunk)

    try:
        if reset:
            save_data(parse_pdf(temp_pdf_path),
                      updated_at=datetime.now().isoformat(),
                      reset=True)
        else:
            save_data(parse_pdf(temp_pdf_path),
                      reset=False,
                      batch_size=750)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

    return {"message": "Chunk uploaded successfully", "reset": reset}

@app.on_event("shutdown")
def shutdown_db_client():
    client.close() 