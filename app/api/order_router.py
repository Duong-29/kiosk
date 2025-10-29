from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from app.core.security import oAuthBearer
from app.services.order import makeOrder, showPDF, downloadPDF, cancelOrderAPI
from fastapi.responses import JSONResponse
from app.models.model import PatientInfo, PatientInfoUpdate, OrderInfo

app = APIRouter()

@app.get("/test")
def test():
    return JSONResponse(status_code=200, content={"data": "Hello world"})

@app.post("/orders/create/{citizen_id}")
def make_order(citizen_id: str, orderInfo: OrderInfo, token: str = Depends(oAuthBearer)):
    result, status_code = makeOrder(citizen_id, orderInfo, token)
    return JSONResponse(
        status_code= status_code,
        content= result
    )

@app.get("/showPDF/{order_id}")
def show_pdf(order_id: str):
    return showPDF(order_id)

@app.get("/downloadPDF/{order_id}")
def download_pdf(order_id: str):
    return downloadPDF(order_id)

@app.put("/cancel/{order_id}")
def cancel_order_api(order_id: str):
    return cancelOrderAPI(order_id)
