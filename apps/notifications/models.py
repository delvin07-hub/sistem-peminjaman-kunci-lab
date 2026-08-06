from django.db import models


class Notifikasi(models.Model):
    JENIS = [
        ('Dipinjam', 'Dipinjam'),
        ('Dikembalikan', 'Dikembalikan'),
    ]

    penanggung_jawab = models.ForeignKey(
        'authentication.PenanggungJawab',
        on_delete=models.CASCADE,
        related_name='notifikasi',
    )
    peminjaman = models.ForeignKey(
        'transaction.Peminjaman',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifikasi',
    )
    tipe = models.CharField(max_length=20, choices=JENIS)
    pesan = models.CharField(max_length=255)
    dibaca = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Notifikasi'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.tipe}: {self.pesan[:40]}'


class DeviceToken(models.Model):
    penanggung_jawab = models.ForeignKey(
        'authentication.PenanggungJawab',
        on_delete=models.CASCADE,
        related_name='device_tokens',
    )
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Device Tokens'

    def __str__(self):
        return f'{self.penanggung_jawab} ({self.token[:20]}...)'