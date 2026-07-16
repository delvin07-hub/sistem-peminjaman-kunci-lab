from django.contrib import admin
from .models import Peminjaman


@admin.register(Peminjaman)
class PeminjamanAdmin(admin.ModelAdmin):
    list_display = ['mahasiswa', 'kunci', 'laboratorium', 'jam_pinjam', 'status']
    list_filter = ['status', 'tanggal_pinjam']
    search_fields = ['mahasiswa__nim', 'mahasiswa__nama', 'kunci__nomor_kunci']
