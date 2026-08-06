from django import forms
from django.contrib import admin
from django.contrib.auth.models import User

from .models import PenanggungJawab


class PenanggungJawabAdminForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label='Username')
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label='Password',
        help_text='Password awal akun penanggung jawab.',
    )

    class Meta:
        model = PenanggungJawab
        fields = ['username', 'password', 'nama_lengkap', 'telepon', 'aktif']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['username'].initial = self.instance.user.username
            self.fields['password'].required = False
            self.fields['password'].help_text = (
                'Kosongkan bila tidak ingin mengubah password.'
            )

    def save(self, commit=True):
        pj = super().save(commit=False)
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if self.instance.pk:
            user = self.instance.user
        else:
            user = None

        if user is None:
            user = User(username=username)

        user.username = username
        if password:
            user.set_password(password)
        user.save()

        pj.user = user
        pj.save()
        if commit:
            pj.save_m2m()
        return pj


@admin.register(PenanggungJawab)
class PenanggungJawabAdmin(admin.ModelAdmin):
    form = PenanggungJawabAdminForm
    list_display = ['nama_lengkap', 'telepon', 'aktif', 'user']
    list_filter = ['aktif']
    search_fields = ['nama_lengkap', 'telepon', 'user__username']