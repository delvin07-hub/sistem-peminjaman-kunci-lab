from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.authentication.mixins import admin_required
from .forms import PeminjamanForm
from .filters import PeminjamanFilter
from .models import Peminjaman
from .services import PeminjamanService
from apps.master_data.models import Kunci, Mahasiswa, Dosen, Laboratorium


def _search_peminjaman_q(term):
    """Q object untuk pencarian peminjaman by NIM/Nama/NoKunci."""
    return (
        Q(mahasiswa__nim__icontains=term) |
        Q(mahasiswa__nama__icontains=term) |
        Q(kunci__nomor_kunci__icontains=term)
    )


@admin_required
def peminjaman_create(request):
    if request.method == 'POST':
        form = PeminjamanForm(request.POST)
        if form.is_valid():
            try:
                PeminjamanService.pinjam_kunci(form.cleaned_data)
                mhs = form.cleaned_data['mahasiswa']
                kunci = form.cleaned_data['kunci']
                jam = timezone.localtime().strftime('%H:%M')
                messages.success(
                    request,
                    f'Peminjaman berhasil dicatat! {mhs.nama} meminjam kunci '
                    f'{kunci.nomor_kunci} pukul {jam}.',
                )
                return redirect('peminjaman_create')
            except ValueError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, 'Periksa kembali form peminjaman.')
    else:
        form = PeminjamanForm()

    return render(request, 'transaction/peminjaman_form.html', {'form': form})


@admin_required
def get_mahasiswa(request):
    term = request.GET.get('term', '')
    data = [
        {'id': m.id, 'text': f"{m.nama} ({m.nim})"}
        for m in Mahasiswa.objects.filter(
            Q(nim__icontains=term) | Q(nama__icontains=term)
        )[:10]
    ]
    return JsonResponse({'results': data})


@admin_required
def get_kunci(request):
    lab_id = request.GET.get('lab_id')
    qs = Kunci.objects.filter(status='Tersedia')
    if lab_id:
        qs = qs.filter(laboratorium_id=lab_id)
    data = [{'id': k.id, 'text': k.nomor_kunci} for k in qs]
    return JsonResponse({'results': data})


@admin_required
def pengembalian_list(request):
    qs = Peminjaman.objects.filter(status='Dipinjam').select_related(
        'mahasiswa', 'kunci', 'laboratorium'
    )
    search = request.GET.get('search')
    if search:
        qs = qs.filter(_search_peminjaman_q(search))
    return render(request, 'transaction/pengembalian_list.html', {'data': qs})


@admin_required
def pengembalian_process(request, pk):
    peminjaman = get_object_or_404(
        Peminjaman.objects.select_related('kunci', 'mahasiswa', 'laboratorium', 'dosen'),
        id=pk, status='Dipinjam',
    )
    if request.method == 'POST':
        jam_kembali = request.POST.get('jam_kembali')
        try:
            jam = timezone.datetime.strptime(jam_kembali, '%H:%M').time() if jam_kembali else None
            PeminjamanService.kembalikan_kunci(pk, jam)
            messages.success(request, 'Kunci berhasil dikembalikan!')
            return redirect('pengembalian_list')
        except ValueError as e:
            messages.error(request, str(e))

    return render(request, 'transaction/pengembalian_confirm.html', {
        'p': peminjaman,
        'now': timezone.now(),
    })


@admin_required
def riwayat_list(request):
    qs = Peminjaman.objects.select_related(
        'mahasiswa', 'kunci', 'laboratorium', 'dosen'
    )

    search = request.GET.get('search')
    if search:
        qs = qs.filter(_search_peminjaman_q(search))

    filter_set = PeminjamanFilter(request.GET, queryset=qs)
    qs = filter_set.qs

    return render(request, 'transaction/riwayat_list.html', {
        'data': qs,
        'filter_set': filter_set,
        'search': search,
        'status_filter': request.GET.get('status', ''),
        'lab_list': Laboratorium.objects.all(),
        'dosen_list': Dosen.objects.all(),
        'prodi_list': list(
            Mahasiswa.objects.exclude(program_studi='')
            .values_list('program_studi', flat=True)
            .distinct().order_by('program_studi')
        ),
    })


@admin_required
def search(request):
    query = request.GET.get('q', '')
    data = [
        {
            'id': p.id,
            'mahasiswa': p.mahasiswa.nama if p.mahasiswa else '-',
            'nim': p.mahasiswa.nim if p.mahasiswa else '-',
            'kunci': p.kunci.nomor_kunci if p.kunci else '-',
            'lab': p.laboratorium.nama_lab if p.laboratorium else '-',
            'tgl': str(p.tanggal_pinjam),
            'status': p.status,
        }
        for p in Peminjaman.objects.select_related(
            'mahasiswa', 'kunci', 'laboratorium'
        ).filter(_search_peminjaman_q(query))[:20]
    ]
    return JsonResponse({'data': data})
