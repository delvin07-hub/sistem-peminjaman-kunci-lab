from django.db import models


class PenanggungJawab(models.Model):
    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='penanggung_jawab',
    )
    nama_lengkap = models.CharField(max_length=100)
    telepon = models.CharField(max_length=30, blank=True)
    aktif = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Penanggung Jawab'
        ordering = ['nama_lengkap']

    def __str__(self):
        return self.nama_lengkap

    def delete(self, *args, **kwargs):
        user = self.user
        super().delete(*args, **kwargs)
        user.delete()