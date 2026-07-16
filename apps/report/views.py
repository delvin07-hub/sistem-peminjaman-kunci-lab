from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from apps.transaction.models import Peminjaman


@login_required
def laporan_view(request):
    peminjaman = Peminjaman.objects.select_related(
        'mahasiswa', 'kunci', 'laboratorium', 'dosen'
    ).all()

    tgl_awal = request.GET.get('tgl_awal')
    tgl_akhir = request.GET.get('tgl_akhir')
    status = request.GET.get('status')

    if tgl_awal:
        peminjaman = peminjaman.filter(tanggal_pinjam__gte=tgl_awal)
    if tgl_akhir:
        peminjaman = peminjaman.filter(tanggal_pinjam__lte=tgl_akhir)
    if status:
        peminjaman = peminjaman.filter(status=status)

    total = peminjaman.count()
    dipinjam = peminjaman.filter(status='Dipinjam').count()
    dikembalikan = peminjaman.filter(status='Dikembalikan').count()

    context = {
        'data': peminjaman[:100],
        'total': total,
        'dipinjam': dipinjam,
        'dikembalikan': dikembalikan,
        'tgl_awal': tgl_awal,
        'tgl_akhir': tgl_akhir,
        'status_filter': status,
    }
    return render(request, 'report/laporan.html', context)
