from django import forms
from .models import Mahasiswa, Dosen, Laboratorium, Kunci


class MahasiswaForm(forms.ModelForm):
    class Meta:
        model = Mahasiswa
        fields = ['nim', 'nama', 'program_studi']
        widgets = {
            'nim': forms.TextInput(attrs={'class': 'form-control'}),
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'program_studi': forms.TextInput(attrs={'class': 'form-control'}),
        }


class DosenForm(forms.ModelForm):
    class Meta:
        model = Dosen
        fields = ['nip', 'nama']
        widgets = {
            'nip': forms.TextInput(attrs={'class': 'form-control'}),
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
        }


class LaboratoriumForm(forms.ModelForm):
    class Meta:
        model = Laboratorium
        fields = ['kode_lab', 'nama_lab', 'gedung', 'lantai']
        widgets = {
            'kode_lab': forms.TextInput(attrs={'class': 'form-control'}),
            'nama_lab': forms.TextInput(attrs={'class': 'form-control'}),
            'gedung': forms.TextInput(attrs={'class': 'form-control'}),
            'lantai': forms.TextInput(attrs={'class': 'form-control'}),
        }


class KunciForm(forms.ModelForm):
    class Meta:
        model = Kunci
        fields = ['laboratorium', 'nomor_kunci']
        widgets = {
            'laboratorium': forms.Select(attrs={'class': 'form-select'}),
            'nomor_kunci': forms.TextInput(attrs={'class': 'form-control'}),
        }
