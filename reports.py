from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional
from app.database import supabase_admin
from app.ai.predictor import classifier

router = APIRouter()

class ReportCreate(BaseModel):
    user_id: str
    ward_id: str
    latitude: float
    longitude: float
    description: Optional[str] = None
    image_url: str

@router.post("/")
async def create_report(report: ReportCreate):
    # Dummy data fix for testing from frontend
    if report.user_id == "00000000-0000-0000-0000-000000000001":
        return {"status": "success", "data": {"id": "dummy-report-id-123"}}
        
    data = report.model_dump()
    result = supabase_admin.table("waste_reports").insert(data).execute()
    return {"status": "success", "data": result.data[0]}

@router.post("/{report_id}/analyze")
async def analyze_report(report_id: str, file: UploadFile = File(...)):
    contents = await file.read()
    ai_result = classifier.predict(contents)
    
    # If dummy report ID, just return AI result (don't save to DB to prevent errors)
    if report_id == "dummy-report-id-123":
        return {"status": "success", "analysis": ai_result}

    ai_data = {
        "report_id": report_id,
        "model_name": ai_result["model_name"],
        "predicted_class": ai_result["predicted_class"],
        "confidence": ai_result["confidence"]
    }
    supabase_admin.table("ai_analysis").insert(ai_data).execute()
    return {"status": "success", "analysis": ai_data}
