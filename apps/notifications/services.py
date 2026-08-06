from apps.authentication.models import PenanggungJawab

from .models import Notifikasi


class NotifikasiService:
    @staticmethod
    def buat(peminjaman, tipe):
        pesan = NotifikasiService._bentuk_pesan(peminjaman, tipe)
        for pj in PenanggungJawab.objects.filter(aktif=True):
            Notifikasi.objects.create(
                penanggung_jawab=pj,
                peminjaman=peminjaman,
                tipe=tipe,
                pesan=pesan,
            )

    @staticmethod
    def _bentuk_pesan(peminjaman, tipe):
        kunci = peminjaman.kunci
        lab = peminjaman.laboratorium
        mhs = peminjaman.mahasiswa
        if tipe == 'Dipinjam':
            return (
                f'{mhs.nama} meminjam kunci {kunci.nomor_kunci}'
                f' ({lab.kode_lab}) jam {peminjaman.jam_pinjam}'
            )
        return (
            f'{mhs.nama} mengembalikan kunci {kunci.nomor_kunci}'
            f' ({lab.kode_lab})'
        )