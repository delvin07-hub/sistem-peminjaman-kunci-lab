from django.db.models import Count, Q
from django.shortcuts import render
from django.utils import timezone

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

    today = timezone.localdate()

    aktivitas_hari_ini = Peminjaman.objects.filter(
        tanggal_pinjam=today
    ).select_related('mahasiswa', 'kunci', 'laboratorium').order_by(
        '-created_at'
    )

    context = {
        'total_kunci': stats['total'],
        'kunci_tersedia': stats['tersedia'],
        'kunci_dipinjam': stats['dipinjam'],
        'peminjaman_hari_ini': aktivitas_hari_ini.count(),
        'aktivitas_hari_ini': aktivitas_hari_ini,
        'tanggal_hari_ini': today.strftime('%d/%m/%Y'),
    }
    return render(request, 'dashboard/index.html', context)