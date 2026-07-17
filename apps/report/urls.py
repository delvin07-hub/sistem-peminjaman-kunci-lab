from django.urls import path
from . import views

urlpatterns = [
    path('', views.laporan_view, name='report_index'),
    path('export/excel/', views.export_excel, name='report_export_excel'),
    path('export/csv/', views.export_csv, name='report_export_csv'),
]
