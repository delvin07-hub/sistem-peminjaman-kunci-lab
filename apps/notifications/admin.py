from django.contrib import admin

from .models import DeviceToken, Notifikasi


@admin.register(Notifikasi)
class NotifikasiAdmin(admin.ModelAdmin):
    list_display = ['tipe', 'pesan', 'penanggung_jawab', 'dibaca', 'created_at']
    list_filter = ['tipe', 'dibaca', 'created_at']
    search_fields = ['pesan']


@admin.register(DeviceToken)
class DeviceTokenAdmin(admin.ModelAdmin):
    list_display = ['penanggung_jawab', 'token', 'created_at']
    search_fields = ['penanggung_jawab__user__username', 'token']
