from django.urls import path
from . import views

urlpatterns = [
    path('peminjaman/', views.peminjaman_create, name='peminjaman_create'),
    path('api/get-mahasiswa/', views.get_mahasiswa, name='get_mahasiswa'),
    path('api/get-kunci/', views.get_kunci, name='get_kunci'),
    path('pengembalian/', views.pengembalian_list, name='pengembalian_list'),
    path('pengembalian/<int:pk>/', views.pengembalian_process, name='pengembalian_process'),
    path('riwayat/', views.riwayat_list, name='riwayat_list'),
    path('cari/', views.search, name='search'),
]
