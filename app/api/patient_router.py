from fastapi import APIRouter
from app.services.patient import checkInsurance, makePatientInfo, updatePatient, checkPatient, getPatientHistoryAPI
from app.models.model import PatientInfo, PatientInfoUpdate, OrderInfo

app = APIRouter()

@app.get("/health-insurance/{citizen_id}", status_code=200)
def check_insurance(citizen_id: str):
    return checkInsurance(citizen_id)

@app.post("/patient/register")
def make_patient_info(patient: PatientInfo):
    return makePatientInfo(patient)

@app.put("/patient/insurance-info/{citizen_id}")
def update_patient(citizen_id: str, info: PatientInfoUpdate):
    return updatePatient(citizen_id, info)

@app.get("/patient/check/{citizen_id}")
def check_patient(citizen_id):
    return checkPatient(citizen_id)

@app.get("/patient/history/{sitizen_id}")
def get_patient_history(citizen_id: str):
    return getPatientHistoryAPI(citizen_id)
