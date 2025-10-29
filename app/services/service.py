from app.repository.repo import Repository
from fastapi.responses import JSONResponse
from app.models.model import PatientInfo, PatientInfoUpdate, OrderInfo
from fastapi import WebSocket, WebSocketDisconnect, Header
from app.core.config import Settings
from app.utils.makepdf import round_like_js 
import asyncio

def getServiceList():
    repo = Repository()
    clinics = []
    listService = repo.getService()
    clinic_name = sorted(set([clinic[0] for clinic in listService]))
    for name in clinic_name:
        services = []
        for service in listService:
            if service[0] == name:
                services.append({
                    "service_name": service[1],
                    "service_description": service[2],
                    "price": float(service[3])
                })
        clinics.append({
            "clinic_name": name,
            "clinic_services": services
        })
    return JSONResponse(
        status_code=200,
        content={"clinics": clinics}
    )

async def checkBankTransfer(websocket: WebSocket):
    await websocket.accept()

    repo = Repository()
    data = await websocket.receive_json()
    order_id = data["order_id"]

    repo.setPaymentMethod(order_id, "BANKING")

    while True:
        try:
            state, detail = repo.getTransferState(order_id)
            await websocket.send_json({"result": state, "detail": detail})
            if state and detail == "":
                break
            await asyncio.sleep(5)
        except WebSocketDisconnect:
            break

async def payOrder(payload: dict)->dict:
    try:
        repo = Repository()
        code = payload.get("code", "")
        money = payload.get("transferSmount", 0)
        order_id = code.replace("ORDER", "")

        order = repo.getOrderInfo(order_id)
        if order is None:
            return {"status": 404, "message": "Khong tim thay don hang"}
        
        if round_like_js(order[8] * 26181) == int(money):
            repo.updateTransferState(order_id)
            return {"status": 200, "message": "Thanh toan thanh cong"}
        else:
            return {"status": 400, "message": "Sai so tien chuyen khoan"}
    except Exception as e:
        return {"status": 500, "message": "Loi thanh toan"}