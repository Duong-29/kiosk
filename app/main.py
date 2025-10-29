from fastapi import FastAPI
from app.api.patient_router import app as patient_router
from app.api.service_router import app as service_router
from app.api.order_router import app as order_router
from fastapi.middleware.cors import CORSMiddleware
from app.db.createdb import create_table
from app.core.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=settings.BACKEND_CORS_ORIGINS
)

app.include_router(patient_router)
app.include_router(service_router)
app.include_router(order_router)

create_table()