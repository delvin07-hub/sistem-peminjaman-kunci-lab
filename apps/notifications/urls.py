from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    KunciStatusDetailView,
    KunciStatusListView,
    NotifikasiBacaView,
    NotifikasiListView,
)

urlpatterns = [
    path('token/', obtain_auth_token, name='api-token'),
    path('notifikasi/', NotifikasiListView.as_view(), name='api-notifikasi-list'),
    path('notifikasi/<int:pk>/baca/', NotifikasiBacaView.as_view(), name='api-notifikasi-baca'),
    path('status-kunci/', KunciStatusListView.as_view(), name='api-status-kunci'),
    path('status-kunci/<int:pk>/', KunciStatusDetailView.as_view(), name='api-status-kunci-detail'),
]
