from django.urls import path

from . import web_views

urlpatterns = [
    path('', web_views.log_notifikasi_view, name='notifikasi_log'),
]