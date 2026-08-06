from django import forms
from .models import Peminjaman
from apps.master_data.models import Kunci


class PeminjamanForm(forms.ModelForm):
    class Meta:
        model = Peminjaman
        fields = ['mahasiswa', 'dosen', 'laboratorium', 'kunci', 'keperluan']
        widgets = {
            'keperluan': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kunci'].queryset = Kunci.objects.filter(status='Tersedia')
        # Auto-apply Bootstrap classes
        for name, field in self.fields.items():
            widget = field.widget
            css = 'form-select' if isinstance(widget, forms.Select) else 'form-control'
            widget.attrs.setdefault('class', css)

    def clean_kunci(self):
        kunci = self.cleaned_data['kunci']
        if kunci.status != 'Tersedia':
            raise forms.ValidationError(f"Kunci {kunci.nomor_kunci} sedang tidak tersedia!")
        return kunci

    def clean(self):
        cleaned = super().clean()
        lab = cleaned.get('laboratorium')
        kunci = cleaned.get('kunci')
        if lab and kunci and kunci.laboratorium_id != lab.id:
            self.add_error(
                'kunci', 'Kunci tidak sesuai dengan ruangan yang dipilih.'
            )
        return cleaned
