from app.repository.repo import Repository
from fastapi.responses import JSONResponse
from app.models.model import PatientInfo, PatientInfoUpdate, OrderInfo
from app.core.security import create_token, verify_token
from decimal import Decimal

def checkInsurance(citizen_id: str):
    try:
        repo = Repository()
        is_activate, message, insurance = repo.is_insurance(citizen_id)
        is_had, _ = repo.isHasPatientInfo(citizen_id)

        if insurance is None:
            return JSONResponse(
                status_code=404,
                content={"message": "Không tìm thấy thông tin bảo hiểm"},
            )
        
        if is_had:
            repo.updatePatientInsuranceState(citizen_id, is_activate)
        
        return {
            "citizen_id": insurance[0],
            "fullname": insurance[1],
            "gender": "Nam" if insurance[2] == 1 else "Nữ",
            "dob": insurance[3].isoformat() if insurance[3] else None,
            "phone_number": insurance[4],
            "registration_place": insurance[5],
            "valid_from": insurance[6].isoformat() if insurance[6] else None,
            "expired": insurance[7].isoformat() if insurance[7] else None,
            "is_activate": is_activate,
            "is_saved": is_had,
            "message": message,
            "token": create_token(insurance[0])
        }
    except Exception as e:
        print(f"Error in check insurance service: {e}")
        return JSONResponse(status_code=500, content={"message": "Lỗi hệ thống"})
    
def makePatientInfo(patient):
    repo = Repository()
    result, reason = repo.savePatientInfo(
        patient.patient_id,
        patient.full_name,
        patient.gender,
        patient.dob,
        patient.address,
        patient.phone_number,
        patient.ethnic,
        patient.job,
        patient.is_insur,
    )

    if not result:
        return JSONResponse(
            status_code=400, 
            content={"reason": reason}
        )
    else:
        return JSONResponse(
            status_code=201,
            content={"token": create_token(patient.patient_id)}
        )

def updatePatient(citizen_id: str, info):
    success = PatientInfoUpdate(citizen_id, info.address, info.ethnic, info.job)
    if not success:
        return JSONResponse(status_code=400, content={"message": "Error Update"})
    else:
        return JSONResponse(status_code=201, content={"Message": "Update Success"})
    
def checkPatient(citizen_id: str):
    repo = Repository()
    patient = repo.getPatient(citizen_id)
    if patient is None:
        return JSONResponse(
            status_code=404,
            content={"message": "Không tìm thấy thông tin bệnh nhân"}
        )
    return JSONResponse(
        status_code=200,
        content={
            "citizen_id": patient[0],
            "fullname": patient[1],
            "gender": "Nam" if patient[2] else "Nữ",
            "dob": str(patient[3]),
            "address": patient[4],
            "phone_number": patient[5],
            "ethnic": patient[6],
            "job": patient[7],
            "token": create_token(patient[0])
        }
    )

def getPatientHistoryAPI(citizen_id: str):
    repo = Repository()
    history = repo.getPatientHistory(citizen_id)
    if not history:
        return JSONResponse(
            status_code=404,
            content={"message": "Khong tim thay lich su kham benh"}
        )
    first = history[0]
    patient_info = {
        "citizen_id": first["citizen_id"],
        "fullname": first["fullname"],
        "gender": "Nam" if first["gender"]==1 else "Nữ",
        "dob": first["dob"].isoformat() if first["dob"] else None,
        "address": first["address"],
        "phone_number": first["phone_number"],
        "ethnic": first["ethnic"],
        "job": first["job"],
        "is_insurance": bool(first["is_insurance"])
    }

    results = []
    for row in history:
        results.append(
            {
                "order_id": row["order_id"],
                "time_order": (
                    row["time_order"].isoformat()
                    if hasattr(row["time_order"], "isoformat")
                    else str(row["time_order"])
                ),
                "queue_number": row["queue_number"],
                "service_name": row["service_name"],
                "clinic_name": row["clinic_name"],
                "address_room": row["address_room"],
                "doctor_name": row["doctor_name"],
                "payment_status": row["payment_status"],
                "payment_method": row["payment_method"],
                "price": (
                    float(row["price"])
                    if isinstance(row["price"], Decimal)
                    else row["price"]
                )
            }
        )
    return JSONResponse(
        status_code=200,
        content={"paient": patient_info, "history": results}
    )