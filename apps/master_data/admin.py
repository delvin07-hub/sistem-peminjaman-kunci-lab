from django.contrib import admin
from .models import Mahasiswa, Dosen, Laboratorium, Kunci


@admin.register(Mahasiswa)
class MahasiswaAdmin(admin.ModelAdmin):
    list_display = ['nim', 'nama', 'program_studi']
    search_fields = ['nim', 'nama']


@admin.register(Dosen)
class DosenAdmin(admin.ModelAdmin):
    list_display = ['nidn', 'nama']
    search_fields = ['nidn', 'nama']


@admin.register(Laboratorium)
class LaboratoriumAdmin(admin.ModelAdmin):
    list_display = ['kode_lab', 'nama_lab', 'gedung', 'lantai']


@admin.register(Kunci)
class KunciAdmin(admin.ModelAdmin):
    list_display = ['nomor_kunci', 'laboratorium', 'status']
    list_filter = ['status', 'laboratorium']
    search_fields = ['nomor_kunci']
