from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.master_data.models import Mahasiswa, Dosen, Laboratorium, Kunci
from apps.transaction.models import Peminjaman


class DashboardTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('root', 'r@x.com', 'pw')
        self.client.force_login(self.admin)
        self.peminjaman = Peminjaman.objects.create(
            mahasiswa=Mahasiswa.objects.create(
                nim='1001', nama='Ani', program_studi='Informatika'
            ),
            dosen=Dosen.objects.create(nidn='9001', nama='Pak Budi'),
            laboratorium=Laboratorium.objects.create(
                kode_lab='R1', nama_lab='Lab A'
            ),
            kunci=Kunci.objects.create(
                laboratorium=Laboratorium.objects.get(kode_lab='R1'),
                nomor_kunci='K1',
            ),
            jam_pinjam='08:00:00',
            keperluan='Praktikum',
        )

    def test_dashboard_aktivitas_hari_ini(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Aktivitas Hari Ini')
        self.assertContains(response, 'Ani')

    def test_dashboard_chart_data_hadir(self):
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, 'chart-7hari')
        self.assertContains(response, 'chart-ruangan')

    def test_aktivitas_lama_tidak_tampil(self):
        lama = timezone.localdate() - timezone.timedelta(days=5)
        Peminjaman.objects.filter(id=self.peminjaman.id).update(
            tanggal_pinjam=lama
        )
        response = self.client.get(reverse('dashboard'))
        self.assertNotContains(response, 'Ani')