from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.master_data.models import Kunci, Laboratorium


class KodeOtomatisTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('root', 'r@x.com', 'pw')
        self.client.force_login(self.admin)

    def test_tambah_ruangan_kode_otomatis(self):
        response = self.client.post(
            reverse('laboratorium_create'),
            {'nama_lab': 'Aula', 'gedung': 'G1', 'lantai': '1'},
        )
        self.assertEqual(response.status_code, 302)
        lab = Laboratorium.objects.get(nama_lab='Aula')
        self.assertEqual(lab.kode_lab, 'R1')

    def test_kode_ruangan_unik_berurutan(self):
        self.client.post(
            reverse('laboratorium_create'),
            {'nama_lab': 'Aula', 'gedung': 'G1', 'lantai': '1'},
        )
        self.client.post(
            reverse('laboratorium_create'),
            {'nama_lab': 'Auditorium', 'gedung': 'G1', 'lantai': '2'},
        )
        kode = list(
            Laboratorium.objects.values_list('kode_lab', flat=True)
        )
        self.assertIn('R1', kode)
        self.assertIn('R2', kode)
        self.assertEqual(len(kode), len(set(kode)))

    def test_tambah_kunci_nomor_otomatis_per_ruangan(self):
        lab1 = Laboratorium.objects.create(
            kode_lab='R1', nama_lab='Aula'
        )
        lab2 = Laboratorium.objects.create(
            kode_lab='R2', nama_lab='Auditorium'
        )
        self.client.post(
            reverse('kunci_create'), {'laboratorium': lab1.id}
        )
        self.client.post(
            reverse('kunci_create'), {'laboratorium': lab1.id}
        )
        self.client.post(
            reverse('kunci_create'), {'laboratorium': lab2.id}
        )
        nomor_lab1 = list(
            Kunci.objects.filter(laboratorium=lab1)
            .values_list('nomor_kunci', flat=True)
        )
        nomor_lab2 = list(
            Kunci.objects.filter(laboratorium=lab2)
            .values_list('nomor_kunci', flat=True)
        )
        self.assertEqual(sorted(nomor_lab1), ['K1', 'K2'])
        self.assertEqual(nomor_lab2, ['K1'])