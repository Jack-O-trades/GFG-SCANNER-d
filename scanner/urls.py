from django.urls import path
from .views import scan_qr, scanner_page
from django import views
from . import views   

urlpatterns = [
    path("", scanner_page),      # opens scanner
    path("scan/", scan_qr),     # API endpoint
    path('api/stats/', views.stats_view, name='stats'),
    path('api/attendees/', views.attendees_view, name='attendees'), 
    path("admin/attendees/", views.admin_attendees_view, name="admin_attendees"),
]
