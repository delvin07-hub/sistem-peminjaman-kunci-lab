import csv
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from apps.transaction.models import Peminjaman


def _get_filtered_data(request):
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

    return peminjaman, tgl_awal, tgl_akhir, status


@login_required
def laporan_view(request):
    peminjaman, tgl_awal, tgl_akhir, status = _get_filtered_data(request)

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


@login_required
def export_excel(request):
    peminjaman, _, _, _ = _get_filtered_data(request)

    import openpyxl
    from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Laporan Peminjaman'

    header_font = Font(bold=True, color='FFFFFF', size=11)
    header_fill = PatternFill(start_color='0D6EFD', end_color='0D6EFD', fill_type='solid')
    header_align = Alignment(horizontal='center', vertical='center', wrap_text=True)
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin'),
    )

    headers = [
        'No', 'Tanggal Pinjam', 'NIM', 'Nama Mahasiswa',
        'Program Studi', 'Dosen', 'Lab', 'Nomor Kunci',
        'Jam Pinjam', 'Tanggal Kembali', 'Jam Kembali', 'Keperluan', 'Status',
    ]

    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_align
        cell.border = thin_border

    for i, p in enumerate(peminjaman, 1):
        row_data = [
            i,
            p.tanggal_pinjam.strftime('%d/%m/%Y') if p.tanggal_pinjam else '-',
            p.mahasiswa.nim,
            p.mahasiswa.nama,
            p.mahasiswa.program_studi,
            p.dosen.nama,
            f'{p.laboratorium.kode_lab} - {p.laboratorium.nama_lab}',
            p.kunci.nomor_kunci,
            str(p.jam_pinjam)[:5],
            p.tanggal_kembali.strftime('%d/%m/%Y') if p.tanggal_kembali else '-',
            str(p.jam_kembali)[:5] if p.jam_kembali else '-',
            p.keperluan,
            p.status,
        ]
        for col, value in enumerate(row_data, 1):
            cell = ws.cell(row=i + 1, column=col, value=value)
            cell.border = thin_border
            cell.alignment = Alignment(vertical='center')

    ws.column_dimensions['A'].width = 5
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 25
    ws.column_dimensions['E'].width = 20
    ws.column_dimensions['F'].width = 25
    ws.column_dimensions['G'].width = 20
    ws.column_dimensions['H'].width = 15
    ws.column_dimensions['I'].width = 12
    ws.column_dimensions['J'].width = 15
    ws.column_dimensions['K'].width = 12
    ws.column_dimensions['L'].width = 30
    ws.column_dimensions['M'].width = 15

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="laporan_peminjaman_{__import__("datetime").date.today()}.xlsx"'
    wb.save(response)
    return response


@login_required
def export_csv(request):
    peminjaman, _, _, _ = _get_filtered_data(request)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="laporan_peminjaman_{__import__("datetime").date.today()}.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'No', 'Tanggal Pinjam', 'NIM', 'Nama Mahasiswa',
        'Program Studi', 'Dosen', 'Lab', 'Nomor Kunci',
        'Jam Pinjam', 'Tanggal Kembali', 'Jam Kembali', 'Keperluan', 'Status',
    ])

    for i, p in enumerate(peminjaman, 1):
        writer.writerow([
            i,
            p.tanggal_pinjam.strftime('%d/%m/%Y') if p.tanggal_pinjam else '-',
            p.mahasiswa.nim,
            p.mahasiswa.nama,
            p.mahasiswa.program_studi,
            p.dosen.nama,
            f'{p.laboratorium.kode_lab} - {p.laboratorium.nama_lab}',
            p.kunci.nomor_kunci,
            str(p.jam_pinjam)[:5],
            p.tanggal_kembali.strftime('%d/%m/%Y') if p.tanggal_kembali else '-',
            str(p.jam_kembali)[:5] if p.jam_kembali else '-',
            p.keperluan,
            p.status,
        ])

    return response
