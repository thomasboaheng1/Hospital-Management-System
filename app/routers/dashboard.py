from fastapi import APIRouter

router = APIRouter()

@router.get("/overview")
async def get_dashboard_overview():
    return {"message": "Dashboard overview endpoint - to be implemented"}

@router.get("/appointments/chart")
async def get_appointments_chart():
    return {"message": "Appointments chart endpoint - to be implemented"}

@router.get("/revenue/chart")
async def get_revenue_chart():
    return {"message": "Revenue chart endpoint - to be implemented"} 