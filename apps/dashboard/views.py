import json
from datetime import timedelta

from django.db.models import Count, Q
from django.shortcuts import render
from django.utils import timezone

from apps.authentication.mixins import admin_required
from apps.master_data.models import Kunci, Laboratorium
from apps.transaction.models import Peminjaman


@admin_required
def index(request):
    stats = Kunci.objects.aggregate(
        total=Count('id'),
        tersedia=Count('id', filter=Q(status='Tersedia')),
        dipinjam=Count('id', filter=Q(status='Dipinjam')),
    )

    today = timezone.localdate()
    start_7 = today - timedelta(days=6)

    harian = dict(
        Peminjaman.objects.filter(tanggal_pinjam__gte=start_7)
        .values('tanggal_pinjam')
        .annotate(total=Count('id'))
        .values_list('tanggal_pinjam', 'total')
    )
    labels_7 = [
        (start_7 + timedelta(days=i)).strftime('%d/%m') for i in range(7)
    ]
    seri_7 = [
        harian.get(start_7 + timedelta(days=i), 0) for i in range(7)
    ]

    per_ruangan = list(
        Peminjaman.objects.exclude(laboratorium__isnull=True)
        .values('laboratorium__nama_lab')
        .annotate(total=Count('id'))
        .order_by('-total')[:8]
    )
    kontainer = Laboratorium.objects.count()

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
        'chart_labels': json.dumps(labels_7),
        'chart_seri': json.dumps(seri_7),
        'chart_lab_labels': json.dumps(
            [r['laboratorium__nama_lab'] for r in per_ruangan]
        ),
        'chart_lab_seri': json.dumps([r['total'] for r in per_ruangan]),
        'chart_lab_list': Laboratorium.objects.all(),
    }
    return render(request, 'dashboard/index.html', context)