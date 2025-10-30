from fastapi import FastAPI
from app.api.patient_router import app as patient_router
from app.api.service_router import app as service_router
from app.api.order_router import app as order_router
from fastapi.middleware.cors import CORSMiddleware
from app.db.createdb import create_table
from app.core.config import settings
import os
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=settings.BACKEND_CORS_ORIGINS
)

app.include_router(patient_router)
app.include_router(service_router)
app.include_router(order_router)

@app.on_event("startup")
def startup_event():
    create_table()  # tạo bảng nếu chưa có
    print("✅ All tables checked/created successfully.")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)