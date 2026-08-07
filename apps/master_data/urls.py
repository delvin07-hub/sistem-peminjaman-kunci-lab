from django.urls import path
from . import views

urlpatterns = [
    path('mahasiswa/', views.MahasiswaListView.as_view(), name='mahasiswa_list'),
    path('mahasiswa/tambah/', views.MahasiswaCreateView.as_view(), name='mahasiswa_create'),
    path('mahasiswa/edit/<int:pk>/', views.MahasiswaUpdateView.as_view(), name='mahasiswa_update'),
    path('mahasiswa/hapus/<int:pk>/', views.MahasiswaDeleteView.as_view(), name='mahasiswa_delete'),
    path('mahasiswa/impor/', views.impor_mahasiswa_view, name='mahasiswa_import'),
    path('mahasiswa/impor/template/', views.template_mahasiswa_view, name='mahasiswa_import_template'),

    path('dosen/', views.DosenListView.as_view(), name='dosen_list'),
    path('dosen/tambah/', views.DosenCreateView.as_view(), name='dosen_create'),
    path('dosen/edit/<int:pk>/', views.DosenUpdateView.as_view(), name='dosen_update'),
    path('dosen/hapus/<int:pk>/', views.DosenDeleteView.as_view(), name='dosen_delete'),
    path('dosen/impor/', views.impor_dosen_view, name='dosen_import'),
    path('dosen/impor/template/', views.template_dosen_view, name='dosen_import_template'),

    path('laboratorium/', views.LaboratoriumListView.as_view(), name='laboratorium_list'),
    path('laboratorium/tambah/', views.LaboratoriumCreateView.as_view(), name='laboratorium_create'),
    path('laboratorium/edit/<int:pk>/', views.LaboratoriumUpdateView.as_view(), name='laboratorium_update'),
    path('laboratorium/hapus/<int:pk>/', views.LaboratoriumDeleteView.as_view(), name='laboratorium_delete'),

    path('kunci/', views.KunciListView.as_view(), name='kunci_list'),
    path('kunci/tambah/', views.KunciCreateView.as_view(), name='kunci_create'),
    path('kunci/edit/<int:pk>/', views.KunciUpdateView.as_view(), name='kunci_update'),
    path('kunci/hapus/<int:pk>/', views.KunciDeleteView.as_view(), name='kunci_delete'),
]
