from django.db import models
from django.utils import timezone
from apps.master_data.models import Mahasiswa, Dosen, Laboratorium, Kunci


class Peminjaman(models.Model):
    STATUS_CHOICES = [
        ('Dipinjam', 'Dipinjam'),
        ('Dikembalikan', 'Dikembalikan'),
    ]

    mahasiswa = models.ForeignKey(
        Mahasiswa, on_delete=models.SET_NULL, related_name='peminjaman',
        null=True
    )
    dosen = models.ForeignKey(
        Dosen, on_delete=models.SET_NULL, related_name='peminjaman', null=True
    )
    laboratorium = models.ForeignKey(
        Laboratorium, on_delete=models.SET_NULL, related_name='peminjaman',
        null=True, verbose_name='Ruangan'
    )
    kunci = models.ForeignKey(
        Kunci, on_delete=models.SET_NULL, related_name='peminjaman',
        null=True, verbose_name='Kunci'
    )
    tanggal_pinjam = models.DateField(default=timezone.localdate)
    jam_pinjam = models.TimeField()
    tanggal_kembali = models.DateField(null=True, blank=True)
    jam_kembali = models.TimeField(null=True, blank=True)
    keperluan = models.TextField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Dipinjam'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Peminjaman"
        ordering = ['-created_at']

    def __str__(self):
        mhs = self.mahasiswa.nama if self.mahasiswa else '-'
        kunci = str(self.kunci) if self.kunci else '-'
        return f"{mhs} - {kunci} ({self.tanggal_pinjam})"
