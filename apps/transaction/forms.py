from django import forms
from .models import Peminjaman
from apps.master_data.models import Kunci, Mahasiswa, Dosen, Laboratorium


class PeminjamanForm(forms.ModelForm):
    class Meta:
        model = Peminjaman
        fields = ['mahasiswa', 'dosen', 'laboratorium', 'kunci', 'jam_pinjam', 'keperluan']
        widgets = {
            'mahasiswa': forms.Select(attrs={'class': 'form-select', 'id': 'id_mahasiswa'}),
            'dosen': forms.Select(attrs={'class': 'form-select'}),
            'laboratorium': forms.Select(attrs={'class': 'form-select', 'id': 'id_laboratorium'}),
            'kunci': forms.Select(attrs={'class': 'form-select'}),
            'jam_pinjam': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'keperluan': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kunci'].queryset = Kunci.objects.filter(status='Tersedia')

    def clean_kunci(self):
        kunci = self.cleaned_data['kunci']
        if kunci.status != 'Tersedia':
            raise forms.ValidationError(f"Kunci {kunci.nomor_kunci} sedang tidak tersedia!")
        return kunci
