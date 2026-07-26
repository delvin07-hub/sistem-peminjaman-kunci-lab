from django.db import models


class Mahasiswa(models.Model):
    nim = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=100)
    program_studi = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Mahasiswa"
        ordering = ['nama']

    def __str__(self):
        return f"{self.nama} ({self.nim})"


class Dosen(models.Model):
    nidn = models.CharField(max_length=30, unique=True, verbose_name='NIDN')
    nama = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Dosen"
        ordering = ['nama']

    def __str__(self):
        return f"{self.nama} ({self.nidn})"


class Laboratorium(models.Model):
    kode_lab = models.CharField(max_length=20, unique=True)
    nama_lab = models.CharField(max_length=100)
    gedung = models.CharField(max_length=50, blank=True)
    lantai = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Laboratorium"
        ordering = ['kode_lab']

    def __str__(self):
        return f"{self.kode_lab} - {self.nama_lab}"


class Kunci(models.Model):
    STATUS_CHOICES = [
        ('Tersedia', 'Tersedia'),
        ('Dipinjam', 'Dipinjam'),
    ]

    laboratorium = models.ForeignKey(
        Laboratorium, on_delete=models.CASCADE, related_name='kunci'
    )
    nomor_kunci = models.CharField(max_length=20)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Tersedia'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Kunci"
        unique_together = ['laboratorium', 'nomor_kunci']
        ordering = ['laboratorium', 'nomor_kunci']

    def __str__(self):
        return f"Kunci {self.nomor_kunci} - {self.laboratorium.kode_lab}"
