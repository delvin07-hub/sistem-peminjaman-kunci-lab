from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password/', views.ubah_password_view, name='ubah_password'),
    path('penanggung-jawab/', views.PenanggungJawabListView.as_view(), name='penanggung_jawab_list'),
    path('penanggung-jawab/tambah/', views.PenanggungJawabCreateView.as_view(), name='penanggung_jawab_create'),
    path('penanggung-jawab/edit/<int:pk>/', views.PenanggungJawabUpdateView.as_view(), name='penanggung_jawab_update'),
    path('penanggung-jawab/hapus/<int:pk>/', views.PenanggungJawabDeleteView.as_view(), name='penanggung_jawab_delete'),
]
