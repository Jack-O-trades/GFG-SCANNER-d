from django.urls import path
from .views import scan_qr, scanner_page

urlpatterns = [
    path("", scanner_page),      # opens scanner
    path("scan/", scan_qr),     # API endpoint
    path('api/stats/', views.stats_view, name='stats'),
    path('api/attendees/', views.attendees_view, name='attendees'), 
]
