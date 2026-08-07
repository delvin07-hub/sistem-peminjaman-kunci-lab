from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.shortcuts import render

from apps.authentication.mixins import admin_required
from apps.authentication.models import PenanggungJawab

from .models import Notifikasi


@admin_required
def log_notifikasi_view(request):
    qs = Notifikasi.objects.select_related(
        'penanggung_jawab', 'penanggung_jawab__user', 'peminjaman'
    )

    search = request.GET.get('search', '')
    jenjang = request.GET.get('tipe', '')
    status = request.GET.get('status', '')
    pj = request.GET.get('pj', '')

    if search:
        qs = qs.filter(
            Q(pesan__icontains=search) |
            Q(penanggung_jawab__nama_lengkap__icontains=search)
        )
    if jenjang:
        qs = qs.filter(tipe=jenjang)
    if status:
        qs = qs.filter(status=status)
    if pj:
        qs = qs.filter(penanggung_jawab_id=pj)

    return render(request, 'notifications/log.html', {
        'data': qs,
        'search': search,
        'tipe_filter': jenjang,
        'status_filter': status,
        'pj_filter': pj,
        'pj_list': PenanggungJawab.objects.all(),
    })