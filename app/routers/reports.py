from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.appointment import Appointment
from app.models.billing import Bill
from app.models.medical_record import MedicalRecord
from app.models.prescription import Prescription

router = APIRouter()

def get_date_range(period: str) -> tuple[datetime, datetime]:
    """Get start and end dates for the specified period"""
    now = datetime.now()
    
    if period == "week":
        # This week (Monday to Sunday)
        start = now - timedelta(days=now.weekday())
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=6, hours=23, minutes=59, seconds=59)
    elif period == "last_week":
        # Last week (Monday to Sunday)
        start = now - timedelta(days=now.weekday() + 7)
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=6, hours=23, minutes=59, seconds=59)
    elif period == "month":
        # This month
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if now.month == 12:
            end = now.replace(year=now.year + 1, month=1, day=1) - timedelta(microseconds=1)
        else:
            end = now.replace(month=now.month + 1, day=1) - timedelta(microseconds=1)
    elif period == "last_month":
        # Last month
        if now.month == 1:
            start = now.replace(year=now.year - 1, month=12, day=1, hour=0, minute=0, second=0, microsecond=0)
            end = now.replace(day=1) - timedelta(microseconds=1)
        else:
            start = now.replace(month=now.month - 1, day=1, hour=0, minute=0, second=0, microsecond=0)
            end = now.replace(day=1) - timedelta(microseconds=1)
    elif period == "quarter":
        # This quarter
        quarter_start_month = ((now.month - 1) // 3) * 3 + 1
        start = now.replace(month=quarter_start_month, day=1, hour=0, minute=0, second=0, microsecond=0)
        if quarter_start_month == 10:
            end = now.replace(year=now.year + 1, month=1, day=1) - timedelta(microseconds=1)
        else:
            end = now.replace(month=quarter_start_month + 3, day=1) - timedelta(microseconds=1)
    elif period == "last_quarter":
        # Last quarter
        quarter_start_month = ((now.month - 1) // 3) * 3 + 1
        if quarter_start_month == 1:
            start = now.replace(year=now.year - 1, month=10, day=1, hour=0, minute=0, second=0, microsecond=0)
            end = now.replace(month=1, day=1) - timedelta(microseconds=1)
        else:
            start = now.replace(month=quarter_start_month - 3, day=1, hour=0, minute=0, second=0, microsecond=0)
            end = now.replace(month=quarter_start_month, day=1) - timedelta(microseconds=1)
    elif period == "year":
        # This year
        start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end = now.replace(year=now.year + 1, month=1, day=1) - timedelta(microseconds=1)
    elif period == "last_year":
        # Last year
        start = now.replace(year=now.year - 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end = now.replace(month=1, day=1) - timedelta(microseconds=1)
    else:
        # Default to all time
        start = datetime(2020, 1, 1)
        end = now
    
    return start, end

@router.get("/overview")
async def get_reports_overview(
    period: str = Query("month", description="Time period: week, month, quarter, year"),
    db: Session = Depends(get_db)
):
    """Get comprehensive overview statistics for the specified period"""
    try:
        start_date, end_date = get_date_range(period)
        
        # Count totals for the period
        total_patients = db.query(func.count(Patient.id)).filter(
            Patient.created_at >= start_date,
            Patient.created_at <= end_date
        ).scalar()
        
        total_doctors = db.query(func.count(Doctor.id)).filter(
            Doctor.created_at >= start_date,
            Doctor.created_at <= end_date
        ).scalar()
        
        total_appointments = db.query(func.count(Appointment.id)).filter(
            Appointment.created_at >= start_date,
            Appointment.created_at <= end_date
        ).scalar()
        
        total_bills = db.query(func.count(Bill.id)).filter(
            Bill.created_at >= start_date,
            Bill.created_at <= end_date
        ).scalar()
        
        # Calculate revenue for the period
        total_revenue = db.query(func.sum(Bill.total_amount)).filter(
            Bill.created_at >= start_date,
            Bill.created_at <= end_date
        ).scalar() or 0
        
        paid_revenue = db.query(func.sum(Bill.paid_amount)).filter(
            Bill.created_at >= start_date,
            Bill.created_at <= end_date
        ).scalar() or 0
        
        pending_bills = db.query(func.count(Bill.id)).filter(
            Bill.status == "pending",
            Bill.created_at >= start_date,
            Bill.created_at <= end_date
        ).scalar()
        
        # Appointment statistics for the period
        completed_appointments = db.query(func.count(Appointment.id)).filter(
            Appointment.status == "completed",
            Appointment.created_at >= start_date,
            Appointment.created_at <= end_date
        ).scalar()
        
        cancelled_appointments = db.query(func.count(Appointment.id)).filter(
            Appointment.status == "cancelled",
            Appointment.created_at >= start_date,
            Appointment.created_at <= end_date
        ).scalar()
        
        # Medical records and prescriptions for the period
        total_medical_records = db.query(func.count(MedicalRecord.id)).filter(
            MedicalRecord.created_at >= start_date,
            MedicalRecord.created_at <= end_date
        ).scalar()
        
        total_prescriptions = db.query(func.count(Prescription.id)).filter(
            Prescription.created_at >= start_date,
            Prescription.created_at <= end_date
        ).scalar()
        
        return {
            "totalPatients": total_patients,
            "totalDoctors": total_doctors,
            "totalAppointments": total_appointments,
            "totalBills": total_bills,
            "totalRevenue": float(total_revenue),
            "paidRevenue": float(paid_revenue),
            "pendingBills": pending_bills,
            "completedAppointments": completed_appointments,
            "cancelledAppointments": cancelled_appointments,
            "totalMedicalRecords": total_medical_records,
            "totalPrescriptions": total_prescriptions,
            "period": period,
            "startDate": start_date.isoformat(),
            "endDate": end_date.isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating overview: {str(e)}"
        )

@router.get("/monthly-revenue")
async def get_monthly_revenue(
    period: str = Query("month", description="Time period: week, month, quarter, year"),
    db: Session = Depends(get_db)
):
    """Get revenue data for the specified period"""
    try:
        start_date, end_date = get_date_range(period)
        
        if period == "week":
            # For week, show daily revenue
            revenue_data = db.query(
                extract('day', Bill.created_at).label('day'),
                func.sum(Bill.total_amount).label('amount')
            ).filter(
                Bill.created_at >= start_date,
                Bill.created_at <= end_date
            ).group_by(
                extract('day', Bill.created_at)
            ).order_by(
                extract('day', Bill.created_at)
            ).all()
            
            # Format as daily data
            formatted_data = []
            for data in revenue_data:
                formatted_data.append({
                    "period": f"Day {data.day}",
                    "amount": float(data.amount) if data.amount else 0
                })
            
        elif period == "month":
            # For month, show weekly revenue
            revenue_data = db.query(
                extract('week', Bill.created_at).label('week'),
                func.sum(Bill.total_amount).label('amount')
            ).filter(
                Bill.created_at >= start_date,
                Bill.created_at <= end_date
            ).group_by(
                extract('week', Bill.created_at)
            ).order_by(
                extract('week', Bill.created_at)
            ).all()
            
            formatted_data = []
            for data in revenue_data:
                formatted_data.append({
                    "period": f"Week {data.week}",
                    "amount": float(data.amount) if data.amount else 0
                })
                
        elif period == "quarter":
            # For quarter, show monthly revenue
            revenue_data = db.query(
                extract('month', Bill.created_at).label('month'),
                func.sum(Bill.total_amount).label('amount')
            ).filter(
                Bill.created_at >= start_date,
                Bill.created_at <= end_date
            ).group_by(
                extract('month', Bill.created_at)
            ).order_by(
                extract('month', Bill.created_at)
            ).all()
            
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            formatted_data = []
            for data in revenue_data:
                month_name = months[data.month - 1]
                formatted_data.append({
                    "period": month_name,
                    "amount": float(data.amount) if data.amount else 0
                })
                
        elif period == "year":
            # For year, show monthly revenue
            revenue_data = db.query(
                extract('month', Bill.created_at).label('month'),
                func.sum(Bill.total_amount).label('amount')
            ).filter(
                Bill.created_at >= start_date,
                Bill.created_at <= end_date
            ).group_by(
                extract('month', Bill.created_at)
            ).order_by(
                extract('month', Bill.created_at)
            ).all()
            
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            formatted_data = []
            for data in revenue_data:
                month_name = months[data.month - 1]
                formatted_data.append({
                    "period": month_name,
                    "amount": float(data.amount) if data.amount else 0
                })
        else:
            # Default to monthly for last 6 months
            current_date = datetime.now()
            six_months_ago = current_date - timedelta(days=180)
            
            revenue_data = db.query(
                extract('month', Bill.created_at).label('month'),
                extract('year', Bill.created_at).label('year'),
                func.sum(Bill.total_amount).label('amount')
            ).filter(
                Bill.created_at >= six_months_ago
            ).group_by(
                extract('month', Bill.created_at),
                extract('year', Bill.created_at)
            ).order_by(
                extract('year', Bill.created_at),
                extract('month', Bill.created_at)
            ).all()
            
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            formatted_data = []
            for data in revenue_data:
                month_name = months[data.month - 1]
                formatted_data.append({
                    "period": month_name,
                    "amount": float(data.amount) if data.amount else 0
                })
        
        return formatted_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating revenue data: {str(e)}"
        )

@router.get("/appointment-stats")
async def get_appointment_statistics(
    period: str = Query("month", description="Time period: week, month, quarter, year"),
    db: Session = Depends(get_db)
):
    """Get appointment statistics by status for the specified period"""
    try:
        start_date, end_date = get_date_range(period)
        
        stats = db.query(
            Appointment.status,
            func.count(Appointment.id).label('count')
        ).filter(
            Appointment.created_at >= start_date,
            Appointment.created_at <= end_date
        ).group_by(Appointment.status).all()
        
        return [
            {"status": stat.status, "count": stat.count}
            for stat in stats
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating appointment statistics: {str(e)}"
        )

@router.get("/department-stats")
async def get_department_statistics(db: Session = Depends(get_db)):
    """Get patient count by department"""
    try:
        # Since we don't have a department field in the doctor model yet,
        # return empty data structure for now
        return []
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating department statistics: {str(e)}"
        )

@router.get("/recent-activity")
async def get_recent_activity(
    period: str = Query("month", description="Time period: week, month, quarter, year"),
    db: Session = Depends(get_db)
):
    """Get recent system activity for the specified period"""
    try:
        start_date, end_date = get_date_range(period)
        recent_activities = []
        
        # Recent appointments for the period
        recent_appointments = db.query(Appointment).filter(
            Appointment.created_at >= start_date,
            Appointment.created_at <= end_date
        ).order_by(Appointment.created_at.desc()).limit(3).all()
        
        for appointment in recent_appointments:
            recent_activities.append({
                "type": "appointment",
                "description": f"New appointment scheduled for Patient #{appointment.patient_id}",
                "date": appointment.created_at.strftime("%Y-%m-%d %H:%M")
            })
        
        # Recent bills for the period
        recent_bills = db.query(Bill).filter(
            Bill.created_at >= start_date,
            Bill.created_at <= end_date
        ).order_by(Bill.created_at.desc()).limit(2).all()
        
        for bill in recent_bills:
            recent_activities.append({
                "type": "billing",
                "description": f"Payment received for Bill #{bill.bill_number}",
                "date": bill.created_at.strftime("%Y-%m-%d %H:%M")
            })
        
        # Recent patients for the period
        recent_patients = db.query(Patient).filter(
            Patient.created_at >= start_date,
            Patient.created_at <= end_date
        ).order_by(Patient.created_at.desc()).limit(2).all()
        
        for patient in recent_patients:
            recent_activities.append({
                "type": "patient",
                "description": f"New patient registered: {patient.first_name} {patient.last_name}",
                "date": patient.created_at.strftime("%Y-%m-%d %H:%M")
            })
        
        # Sort by date and return top 5
        recent_activities.sort(key=lambda x: x["date"], reverse=True)
        return recent_activities[:5]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating recent activity: {str(e)}"
        )

@router.get("/performance-metrics")
async def get_performance_metrics(db: Session = Depends(get_db)):
    """Get performance indicators"""
    try:
        total_appointments = db.query(func.count(Appointment.id)).scalar()
        completed_appointments = db.query(func.count(Appointment.id)).filter(Appointment.status == "completed").scalar()
        
        # Calculate success rate
        success_rate = (completed_appointments / total_appointments * 100) if total_appointments > 0 else 0
        
        # For a new system, we don't have historical data for these metrics
        # Return appropriate defaults
        return {
            "patientSatisfaction": 0.0,  # No data yet
            "appointmentSuccessRate": round(success_rate, 1),
            "averageWaitTime": 0,  # No data yet
            "revenueGrowth": 0.0  # No historical data yet
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating performance metrics: {str(e)}"
        )

@router.get("/export")
async def export_reports(
    report_type: str = "overview",
    format: str = "json",
    period: str = Query("month", description="Time period: week, month, quarter, year"),
    db: Session = Depends(get_db)
):
    """Export reports in various formats"""
    try:
        if report_type == "overview":
            data = await get_reports_overview(period, db)
        elif report_type == "revenue":
            data = await get_monthly_revenue(period, db)
        elif report_type == "appointments":
            data = await get_appointment_statistics(period, db)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid report type"
            )
        
        return {
            "report_type": report_type,
            "format": format,
            "period": period,
            "data": data,
            "exported_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error exporting report: {str(e)}"
        )

@router.get("/comparison")
async def get_period_comparison(
    current_period: str = Query("month", description="Current period: week, month, quarter, year"),
    db: Session = Depends(get_db)
):
    """Get comparison data between current period and previous equivalent period"""
    try:
        # Map current periods to their previous equivalents
        period_mapping = {
            "week": "last_week",
            "month": "last_month", 
            "quarter": "last_quarter",
            "year": "last_year"
        }
        
        previous_period = period_mapping.get(current_period, "last_month")
        
        # Get current period data
        current_start, current_end = get_date_range(current_period)
        previous_start, previous_end = get_date_range(previous_period)
        
        # Current period statistics
        current_patients = db.query(func.count(Patient.id)).filter(
            Patient.created_at >= current_start,
            Patient.created_at <= current_end
        ).scalar()
        
        current_appointments = db.query(func.count(Appointment.id)).filter(
            Appointment.created_at >= current_start,
            Appointment.created_at <= current_end
        ).scalar()
        
        current_revenue = db.query(func.sum(Bill.total_amount)).filter(
            Bill.created_at >= current_start,
            Bill.created_at <= current_end
        ).scalar() or 0
        
        current_bills = db.query(func.count(Bill.id)).filter(
            Bill.created_at >= current_start,
            Bill.created_at <= current_end
        ).scalar()
        
        # Previous period statistics
        previous_patients = db.query(func.count(Patient.id)).filter(
            Patient.created_at >= previous_start,
            Patient.created_at <= previous_end
        ).scalar()
        
        previous_appointments = db.query(func.count(Appointment.id)).filter(
            Appointment.created_at >= previous_start,
            Appointment.created_at <= previous_end
        ).scalar()
        
        previous_revenue = db.query(func.sum(Bill.total_amount)).filter(
            Bill.created_at >= previous_start,
            Bill.created_at <= previous_end
        ).scalar() or 0
        
        previous_bills = db.query(func.count(Bill.id)).filter(
            Bill.created_at >= previous_start,
            Bill.created_at <= previous_end
        ).scalar()
        
        # Calculate percentage changes
        def calculate_change(current, previous):
            if previous == 0:
                return 100 if current > 0 else 0
            return round(((current - previous) / previous) * 100, 1)
        
        return {
            "currentPeriod": {
                "period": current_period,
                "startDate": current_start.isoformat(),
                "endDate": current_end.isoformat(),
                "patients": current_patients,
                "appointments": current_appointments,
                "revenue": float(current_revenue),
                "bills": current_bills
            },
            "previousPeriod": {
                "period": previous_period,
                "startDate": previous_start.isoformat(),
                "endDate": previous_end.isoformat(),
                "patients": previous_patients,
                "appointments": previous_appointments,
                "revenue": float(previous_revenue),
                "bills": previous_bills
            },
            "changes": {
                "patients": calculate_change(current_patients, previous_patients),
                "appointments": calculate_change(current_appointments, previous_appointments),
                "revenue": calculate_change(current_revenue, previous_revenue),
                "bills": calculate_change(current_bills, previous_bills)
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating comparison data: {str(e)}"
        ) 