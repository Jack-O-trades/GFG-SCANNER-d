from django.utils import timezone  # ✅ CORRECT import
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Attendee
from django.db.models import Q
import json

def index(request):
    """Render the QR scanner page."""
    return render(request, 'scanner/index.html')

@require_http_methods(["POST"])
@csrf_exempt
def scan_qr(request):
    """
    Handle QR scan and mark attendance.
    Expects: POST data with registration_number field
    """
    try:
        # Get registration number from POST data
        reg_no = request.POST.get("registration_number", "").strip()
        
        if not reg_no:
            return JsonResponse({
                "status": "invalid_qr",
                "message": "QR code could not be read"
            }, status=400)
        
        print(f"[DEBUG] Scanning registration: {reg_no}")  # Debug log
        
        # Check if attendee exists (case-insensitive search)
        try:
            # Try exact match first
            attendee = Attendee.objects.get(registration_number=reg_no)
        except Attendee.DoesNotExist:
            # Try case-insensitive match if exact fails
            try:
                attendee = Attendee.objects.get(registration_number__iexact=reg_no)
            except Attendee.DoesNotExist:
                print(f"[DEBUG] Not found in database")
                return JsonResponse({
                    "status": "not_registered",
                    "message": f"Registration #{reg_no} not found"
                }, status=404)
        
        print(f"[DEBUG] Found: {attendee.name}, Attended: {attendee.attended}")
        
        # Check if already marked
        if attendee.attended:
            print(f"[DEBUG] Already marked")
            return JsonResponse({
                "status": "already_marked",
                "name": attendee.name,
                "registration_number": attendee.registration_number,
                "message": f"{attendee.registration_number} - {attendee.name} - Already marked"
            }, status=200)
        
        # Mark attendance
        attendee.attended = True
        attendee.checked_in_at = timezone.now()
        attendee.save()
        
        print(f"[DEBUG] Attendance marked for {attendee.name}")
        return JsonResponse({
            "status": "success",
            "name": attendee.name,
            "registration_number": attendee.registration_number,
            "message": f"{attendee.registration_number} - {attendee.name} - Attendance marked"
        }, status=200)
    
    except Exception as e:
        print(f"[DEBUG] Error: {str(e)}")
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)

def scanner_page(request):
    """Render scanner page."""
    return render(request, "scanner/index.html")

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Attendee

@require_http_methods(["GET"])
def stats_view(request):
    total_registered = Attendee.objects.count()
    present_count = Attendee.objects.filter(attended=True).count()
    absent_count = Attendee.objects.filter(attended=False).count()
    
    return JsonResponse({
        'total_registered': total_registered,
        'present': present_count,
        'absent': absent_count
    })

@require_http_methods(["GET"])
def attendees_view(request):
    attendees = Attendee.objects.filter(attended=True).order_by('-checked_in_at')  # Most recent first
    
    attendees_data = [
        {
            'id': attendee.id,
            'registration_number': attendee.registration_number,
            'name': attendee.name,
            'attended': attendee.attended,
            'checked_in_at': attendee.checked_in_at.isoformat() if attendee.checked_in_at else None
        }
        for attendee in attendees
    ]
    
    return JsonResponse({
        'attendees': attendees_data
    })


