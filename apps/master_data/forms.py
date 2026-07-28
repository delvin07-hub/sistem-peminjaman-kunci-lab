from django import forms
from .models import Mahasiswa, Dosen, Laboratorium, Kunci


class _BootstrapFormMixin:
    """Auto-apply Bootstrap classes to all form fields."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            css = 'form-select' if isinstance(widget, forms.Select) else 'form-control'
            widget.attrs.setdefault('class', css)


class MahasiswaForm(_BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Mahasiswa
        fields = ['nim', 'nama', 'program_studi']


class DosenForm(_BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Dosen
        fields = ['nidn', 'nama']


class LaboratoriumForm(_BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Laboratorium
        fields = ['kode_lab', 'nama_lab', 'gedung', 'lantai']


class KunciForm(_BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Kunci
        fields = ['laboratorium', 'nomor_kunci']
