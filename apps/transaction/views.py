import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone

from .models import Peminjaman
from .forms import PeminjamanForm
from .services import PeminjamanService
from apps.master_data.models import Mahasiswa, Kunci


@login_required
def peminjaman_create(request):
    if request.method == 'POST':
        form = PeminjamanForm(request.POST)
        if form.is_valid():
            try:
                data = {
                    'mahasiswa': form.cleaned_data['mahasiswa'],
                    'dosen': form.cleaned_data['dosen'],
                    'laboratorium': form.cleaned_data['laboratorium'],
                    'kunci': form.cleaned_data['kunci'],
                    'jam_pinjam': form.cleaned_data['jam_pinjam'],
                    'keperluan': form.cleaned_data['keperluan'],
                }
                PeminjamanService.pinjam_kunci(data)
                messages.success(request, 'Peminjaman berhasil dicatat!')
                return redirect('peminjaman_create')
            except ValueError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, 'Periksa kembali form peminjaman.')
    else:
        form = PeminjamanForm()

    context = {
        'form': form,
    }
    return render(request, 'transaction/peminjaman_form.html', context)


@login_required
def get_mahasiswa(request):
    term = request.GET.get('term', '')
    mahasiswa = Mahasiswa.objects.filter(
        Q(nim__icontains=term) | Q(nama__icontains=term)
    )[:10]
    data = [{'id': m.id, 'text': f"{m.nama} ({m.nim})"} for m in mahasiswa]
    return JsonResponse({'results': data})


@login_required
def get_kunci(request):
    lab_id = request.GET.get('lab_id')
    if lab_id:
        kunci = Kunci.objects.filter(
            laboratorium_id=lab_id, status='Tersedia'
        )
    else:
        kunci = Kunci.objects.filter(status='Tersedia')
    data = [{'id': k.id, 'text': k.nomor_kunci} for k in kunci]
    return JsonResponse({'results': data})


@login_required
def pengembalian_list(request):
    peminjaman = Peminjaman.objects.filter(status='Dipinjam').select_related(
        'mahasiswa', 'kunci', 'laboratorium'
    )
    search = request.GET.get('search')
    if search:
        peminjaman = peminjaman.filter(
            Q(mahasiswa__nim__icontains=search) |
            Q(mahasiswa__nama__icontains=search) |
            Q(kunci__nomor_kunci__icontains=search)
        )
    context = {'data': peminjaman}
    return render(request, 'transaction/pengembalian_list.html', context)


@login_required
def pengembalian_process(request, pk):
    peminjaman = get_object_or_404(
        Peminjaman.objects.select_related('kunci', 'mahasiswa', 'laboratorium', 'dosen'),
        id=pk, status='Dipinjam'
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
    context = {
        'p': peminjaman,
        'now': timezone.now(),
    }
    return render(request, 'transaction/pengembalian_confirm.html', context)


@login_required
def riwayat_list(request):
    peminjaman = Peminjaman.objects.select_related(
        'mahasiswa', 'kunci', 'laboratorium', 'dosen'
    ).all()

    search = request.GET.get('search')
    status = request.GET.get('status')

    if search:
        peminjaman = peminjaman.filter(
            Q(mahasiswa__nim__icontains=search) |
            Q(mahasiswa__nama__icontains=search) |
            Q(kunci__nomor_kunci__icontains=search)
        )
    if status:
        peminjaman = peminjaman.filter(status=status)

    paginator = Paginator(peminjaman, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search': search,
        'status_filter': status,
    }
    return render(request, 'transaction/riwayat_list.html', context)


@login_required
def search(request):
    query = request.GET.get('q', '')
    peminjaman = Peminjaman.objects.select_related(
        'mahasiswa', 'kunci', 'laboratorium'
    ).filter(
        Q(mahasiswa__nim__icontains=query) |
        Q(mahasiswa__nama__icontains=query) |
        Q(kunci__nomor_kunci__icontains=query)
    )[:20]
    data = [
        {
            'id': p.id,
            'mahasiswa': p.mahasiswa.nama,
            'nim': p.mahasiswa.nim,
            'kunci': p.kunci.nomor_kunci,
            'lab': p.laboratorium.nama_lab,
            'tgl': str(p.tanggal_pinjam),
            'status': p.status,
        }
        for p in peminjaman
    ]
    return JsonResponse({'data': data})
