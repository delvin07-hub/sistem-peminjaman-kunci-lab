from django import forms
import django_filters
from .models import Peminjaman


class PeminjamanFilter(django_filters.FilterSet):
    nim = django_filters.CharFilter(
        field_name='mahasiswa__nim', lookup_expr='icontains',
        label='NIM'
    )
    nama = django_filters.CharFilter(
        field_name='mahasiswa__nama', lookup_expr='icontains',
        label='Nama Mahasiswa'
    )
    nomor_kunci = django_filters.CharFilter(
        field_name='kunci__nomor_kunci', lookup_expr='icontains',
        label='Nomor Kunci'
    )
    tanggal_awal = django_filters.DateFilter(
        field_name='tanggal_pinjam', lookup_expr='gte',
        label='Tanggal Awal',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    tanggal_akhir = django_filters.DateFilter(
        field_name='tanggal_pinjam', lookup_expr='lte',
        label='Tanggal Akhir',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Peminjaman
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
