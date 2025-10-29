from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, Header, HTTPException
from app.services.service import getServiceList, checkBankTransfer, payOrder
from app.models.model import PatientInfo, PatientInfoUpdate, OrderInfo
from app.core.config import settings
from fastapi.responses import JSONResponse

app = APIRouter()

@app.get("/api/services")
def get_service_list():
    return getServiceList()

@app.websocket("/checkTransfer")
async def check_bank_transfer(websocket: WebSocket):
    await checkBankTransfer(websocket)

@app.post("/api/payOrder")
async def pay_order(request: Request, authorization: str = Header(None)):
    auth = f"Apikey {settings.SEPAY_API_KEY}"
    if authorization != auth:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    results = await payOrder(payload)
    return JSONResponse(status_code=results["status"], content={"message": results["message"]})