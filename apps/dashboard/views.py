from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from datetime import date
from apps.master_data.models import Kunci
from apps.transaction.models import Peminjaman


@login_required
def index(request):
    total_kunci = Kunci.objects.count()
    kunci_tersedia = Kunci.objects.filter(status='Tersedia').count()
    kunci_dipinjam = Kunci.objects.filter(status='Dipinjam').count()
    peminjaman_hari_ini = Peminjaman.objects.filter(tanggal_pinjam=date.today()).count()
    peminjaman_terbaru = Peminjaman.objects.select_related(
        'mahasiswa', 'kunci', 'laboratorium'
    ).order_by('-created_at')[:10]

    context = {
        'total_kunci': total_kunci,
        'kunci_tersedia': kunci_tersedia,
        'kunci_dipinjam': kunci_dipinjam,
        'peminjaman_hari_ini': peminjaman_hari_ini,
        'peminjaman_terbaru': peminjaman_terbaru,
    }
    return render(request, 'dashboard/index.html', context)
