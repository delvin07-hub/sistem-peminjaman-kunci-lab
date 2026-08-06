import csv

import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

from apps.authentication.mixins import admin_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from apps.transaction.models import Peminjaman

EXPORT_HEADERS = [
    'No', 'Tanggal Pinjam', 'NIM', 'Nama Mahasiswa',
    'Program Studi', 'Dosen', 'Lab', 'Nomor Kunci',
    'Jam Pinjam', 'Tanggal Kembali', 'Jam Kembali', 'Keperluan', 'Status',
]

COLUMN_WIDTHS = {
    'A': 5, 'B': 15, 'C': 15, 'D': 25, 'E': 20, 'F': 25, 'G': 20,
    'H': 15, 'I': 12, 'J': 15, 'K': 12, 'L': 30, 'M': 15,
}


def _get_filtered_data(request):
    """Return filtered queryset dan parameter filter aktif."""
    qs = Peminjaman.objects.select_related(
        'mahasiswa', 'kunci', 'laboratorium', 'dosen'
    )

    tgl_awal = request.GET.get('tgl_awal')
    tgl_akhir = request.GET.get('tgl_akhir')
    status = request.GET.get('status')

    if tgl_awal:
        qs = qs.filter(tanggal_pinjam__gte=tgl_awal)
    if tgl_akhir:
        qs = qs.filter(tanggal_pinjam__lte=tgl_akhir)
    if status:
        qs = qs.filter(status=status)

    return qs, tgl_awal, tgl_akhir, status


def _fmt_date(d):
    return d.strftime('%d/%m/%Y') if d else '-'


def _fmt_time(t):
    return str(t)[:5] if t else '-'


def _peminjaman_to_row(i, p):
    """Konversi satu record Peminjaman jadi list untuk export."""
    return [
        i,
        _fmt_date(p.tanggal_pinjam),
        p.mahasiswa.nim,
        p.mahasiswa.nama,
        p.mahasiswa.program_studi,
        p.dosen.nama,
        f'{p.laboratorium.kode_lab} - {p.laboratorium.nama_lab}',
        p.kunci.nomor_kunci,
        _fmt_time(p.jam_pinjam),
        _fmt_date(p.tanggal_kembali),
        _fmt_time(p.jam_kembali),
        p.keperluan,
        p.status,
    ]


@admin_required
def laporan_view(request):
    peminjaman, tgl_awal, tgl_akhir, status = _get_filtered_data(request)

    total = peminjaman.count()
    dipinjam = peminjaman.filter(status='Dipinjam').count()

    paginator = Paginator(peminjaman, 50)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'total': total,
        'dipinjam': dipinjam,
        'dikembalikan': total - dipinjam,
        'tgl_awal': tgl_awal,
        'tgl_akhir': tgl_akhir,
        'status_filter': status,
    }
    return render(request, 'report/laporan.html', context)


@admin_required
def export_excel(request):
    peminjaman, _, _, _ = _get_filtered_data(request)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Laporan Peminjaman'

    header_font = Font(bold=True, color='FFFFFF', size=11)
    header_fill = PatternFill(start_color='0D6EFD', end_color='0D6EFD', fill_type='solid')
    header_align = Alignment(horizontal='center', vertical='center', wrap_text=True)
    thin_border = Border(
        left=Side(style='thin'), right=Side(style='thin'),
        top=Side(style='thin'), bottom=Side(style='thin'),
    )

    for col, header in enumerate(EXPORT_HEADERS, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_align
        cell.border = thin_border

    for i, p in enumerate(peminjaman, 1):
        for col, value in enumerate(_peminjaman_to_row(i, p), 1):
            cell = ws.cell(row=i + 1, column=col, value=value)
            cell.border = thin_border
            cell.alignment = Alignment(vertical='center')

    for letter, width in COLUMN_WIDTHS.items():
        ws.column_dimensions[letter].width = width

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="laporan_peminjaman_{timezone.now().date()}.xlsx"'
    wb.save(response)
    return response


@admin_required
def export_csv(request):
    peminjaman, _, _, _ = _get_filtered_data(request)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="laporan_peminjaman_{timezone.now().date()}.csv"'

    writer = csv.writer(response)
    writer.writerow(EXPORT_HEADERS)

    for i, p in enumerate(peminjaman, 1):
        writer.writerow(_peminjaman_to_row(i, p))

    return response
