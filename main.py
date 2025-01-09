import os
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from app.api.routers.superbill import Pdf_router   
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
host = os.getenv('HOST')
port = int(os.getenv('PORT'))
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # This allows all HTTP methods
    allow_headers=["*"],  # This allows all headers
)

# Include your router with a prefix
app.include_router(Pdf_router)

if __name__ == "__main__":
    uvicorn.run("main:app",host= host,port = port, reload=True )
