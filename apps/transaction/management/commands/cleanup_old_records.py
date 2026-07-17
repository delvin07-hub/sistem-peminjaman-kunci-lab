from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.transaction.models import Peminjaman


class Command(BaseCommand):
    help = 'Menghapus record peminjaman yang sudah dikembalikan dan berusia lebih dari 30 hari'

    def handle(self, *args, **kwargs):
        cutoff = timezone.now().date() - timedelta(days=30)
        records = Peminjaman.objects.filter(
            tanggal_pinjam__lt=cutoff, status='Dikembalikan'
        )
        count = records.count()
        if count > 0:
            records.delete()
            self.stdout.write(self.style.SUCCESS(
                f'Berhasil menghapus {count} record lama (> 30 hari)'
            ))
        else:
            self.stdout.write('Tidak ada record yang perlu dihapus')
