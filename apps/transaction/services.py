from django.db import transaction
from django.utils import timezone
from .models import Peminjaman


class PeminjamanService:

    @staticmethod
    @transaction.atomic
    def pinjam_kunci(data: dict) -> Peminjaman:
        kunci = data['kunci']
        if kunci.status != 'Tersedia':
            raise ValueError(f"Kunci {kunci.nomor_kunci} sedang dipinjam")
        peminjaman = Peminjaman.objects.create(**data)
        kunci.status = 'Dipinjam'
        kunci.save()
        return peminjaman

    @staticmethod
    @transaction.atomic
    def kembalikan_kunci(peminjaman_id: int, jam_kembali=None) -> Peminjaman:
        peminjaman = Peminjaman.objects.select_related('kunci').get(id=peminjaman_id)
        if peminjaman.status != 'Dipinjam':
            raise ValueError("Peminjaman ini sudah dikembalikan")
        now = timezone.now()
        peminjaman.jam_kembali = jam_kembali or now.time()
        peminjaman.tanggal_kembali = now.date()
        peminjaman.status = 'Dikembalikan'
        peminjaman.save()
        peminjaman.kunci.status = 'Tersedia'
        peminjaman.kunci.save()
        return peminjaman
