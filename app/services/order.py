from app.repository.repo import Repository
from fastapi.responses import JSONResponse, StreamingResponse
from app.models.model import PatientInfo, PatientInfoUpdate, OrderInfo
from app.core.security import verify_token, create_token
from app.utils.makeqr import make_qrcode
from app.utils.makepdf import makePDF
from fastapi import WebSocket, WebSocketDisconnect

def makeOrder(citizen_id: str, orderInfo, token: str):
    repo = Repository()
    patient = repo.getPatient(citizen_id)
    if patient is None:
        return JSONResponse(
            status_code=400, 
            content={"detail": "Patient khong ton tai"}
        )
    
    access, detail = verify_token(token, citizen_id)
    if not access:
        return {"detail": detail}, 401
    
    order_id = repo.createOrder(citizen_id, orderInfo.service_name, orderInfo.type)
    if order_id is None:
        return JSONResponse(
            status_code=400,
            content={"detail": "Loi tao order"}
        )
    else:
        order = repo.getOrder(order_id)
        return JSONResponse(
            status_code=200,
            content={
                "citizen_id": order[0],
                "fullname": order[1],
                "gender": "Nam" if order[2]==1 else "Nữ",
                "dob": order[3].isoformat() if order[3] else None,
                "queue_number": order[4],
                "time_order": order[5].isoformat() if order[5] else None,
                "is_insurance": order[7],
                "use insurance": order[13],
                "service_name": order[9],
                "clinic_name": order[10],
                "address_room": order[11],
                "doctor_name": order[12],
                "price": float(order[6]),
                "order_id": order_id,
                "QRCode": make_qrcode(
                    f"http://healthcare-kiosk.onrender.com/downloadPDF/{order_id}"
                )
            }
        )
    
def showPDF(order_id: str):
    repo = Repository()
    order = repo.getOrder(order_id)
    if order is not None:
        pdf_buffer = makePDF(order)
        return StreamingResponse(
            content= pdf_buffer,
            media_type= "application/pdf",
            headers={"Content-Disposition": 'inline; filename="phieu-kham-benh.pdf"'},
        )
    
def downloadPDF(order_id: str):
    repo = Repository()
    order = repo.getOrder(order_id)
    if order is not None:
        pdf_buffer = makePDF(order)
        return StreamingResponse(
            content=pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename-phieu-kham-benh.pdf"},
        )
    
def cancelOrderAPI(order_id: str):
    repo = Repository()
    order = repo.getOrderInfo(order_id)
    if order is None:
        return JSONResponse(
            status_code=404,
            content={"message": "Khong tim thay don hang"}
        )
    
    if order["payment_status"] == "PAID":
        return JSONResponse(
            status_code=400,
            content={"message": "Don hang da thanh toan, khong the huy"},
        )
    if order["payment_status"] == "CANCELLED":
        return JSONResponse(
            status_code=400,
            content={"message": "Don hang da huy truoc do"}
        )
    if repo.cancelOrder(order_id):
        return JSONResponse(
            status_code=200,
            content={"message": f"Don {order_id} da duoc huy thanh cong"},
        )
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "Loi khi huy don"}
        )