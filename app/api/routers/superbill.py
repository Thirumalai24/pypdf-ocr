import os
from dotenv import load_dotenv
from fastapi import APIRouter, UploadFile, File, HTTPException,Header, Depends
from fastapi.responses import JSONResponse
from app.api.controllers.superbill import PdfExtraction  

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

Pdf_router = APIRouter()

# Validate api_key
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")

@Pdf_router.get("/ping")
async def ping():
    return {"ping": "pong"}

@Pdf_router.post("/extract-pdf")
async def extract_pdf(
    file: UploadFile = File(...),
    x_api_key: str = Depends(verify_api_key)
):
    try:
        #check uploaded file is pdf or not
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are supported.")

        # Read file content
        pdf_content = await file.read()
        
        # Initialize PdfExtraction with file content
        extraction = PdfExtraction(pdf_content)
        
        if extraction.json_output is None:
            raise HTTPException(status_code=500, detail="Error processing PDF file")

        return JSONResponse(content=extraction.json_output)

    except HTTPException as he:
        raise he
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
