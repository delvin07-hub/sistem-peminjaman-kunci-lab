from datetime import date

from django.db.models import Count, Q
from django.shortcuts import render

from apps.authentication.mixins import admin_required
from apps.master_data.models import Kunci
from apps.transaction.models import Peminjaman


@admin_required
def index(request):
    stats = Kunci.objects.aggregate(
        total=Count('id'),
        tersedia=Count('id', filter=Q(status='Tersedia')),
        dipinjam=Count('id', filter=Q(status='Dipinjam')),
    )

    context = {
        'total_kunci': stats['total'],
        'kunci_tersedia': stats['tersedia'],
        'kunci_dipinjam': stats['dipinjam'],
        'peminjaman_hari_ini': Peminjaman.objects.filter(
            tanggal_pinjam=date.today()
        ).count(),
        'peminjaman_terbaru': Peminjaman.objects.select_related(
            'mahasiswa', 'kunci', 'laboratorium'
        ).order_by('-created_at')[:10],
    }
    return render(request, 'dashboard/index.html', context)
