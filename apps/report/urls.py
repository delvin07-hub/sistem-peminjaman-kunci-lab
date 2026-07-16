from django.urls import path
from . import views

urlpatterns = [
    path('', views.laporan_view, name='report_index'),
]
