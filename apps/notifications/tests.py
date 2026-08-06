from datetime import time

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.authentication.models import PenanggungJawab
from apps.master_data.models import Mahasiswa, Dosen, Laboratorium, Kunci
from apps.transaction.models import Peminjaman

from .models import Notifikasi
from .services import NotifikasiService


class NotifikasiServiceTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('u1', password='x')
        self.user2 = User.objects.create_user('u2', password='x')
        self.pj1 = PenanggungJawab.objects.create(
            user=self.user1, nama_lengkap='PJ Satu', aktif=True
        )
        self.pj2 = PenanggungJawab.objects.create(
            user=self.user2, nama_lengkap='PJ Dua', aktif=True
        )

        self.mahasiswa = Mahasiswa.objects.create(
            nim='2209999', nama='Andi Demo', program_studi='TI'
        )
        self.dosen = Dosen.objects.create(nidn='NX001', nama='Dosen X')
        self.lab = Laboratorium.objects.create(
            kode_lab='L99', nama_lab='Lab Uji'
        )
        self.kunci = Kunci.objects.create(
            laboratorium=self.lab, nomor_kunci='K1', status='Tersedia'
        )
        self.peminjaman = Peminjaman.objects.create(
            mahasiswa=self.mahasiswa,
            dosen=self.dosen,
            laboratorium=self.lab,
            kunci=self.kunci,
            jam_pinjam=time(8, 0),
            keperluan='Praktikum',
        )

    def test_buat_dipinjam_ke_semua_pj_aktif(self):
        NotifikasiService.buat(self.peminjaman, 'Dipinjam')
        self.assertEqual(Notifikasi.objects.filter(tipe='Dipinjam').count(), 2)

    def test_buat_mengabaikan_pj_nonaktif(self):
        self.pj2.aktif = False
        self.pj2.save()
        NotifikasiService.buat(self.peminjaman, 'Dipinjam')
        self.assertEqual(Notifikasi.objects.filter(tipe='Dipinjam').count(), 1)

    def test_pesan_berisi_nama_mahasiswa_dan_nomor_kunci(self):
        NotifikasiService.buat(self.peminjaman, 'Dipinjam')
        notif = Notifikasi.objects.first()
        self.assertIn('Andi Demo', notif.pesan)
        self.assertIn('K1', notif.pesan)


class NotifikasiModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('p3', password='x')
        self.pj = PenanggungJawab.objects.create(
            user=self.user, nama_lengkap='PJ Tiga'
        )

    def test_dibaca_default_false(self):
        notif = Notifikasi.objects.create(
            penanggung_jawab=self.pj, tipe='Dipinjam', pesan='x'
        )
        self.assertFalse(notif.dibaca)


class NotifikasiAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('pj_api', password='pw')
        self.pj = PenanggungJawab.objects.create(
            user=self.user, nama_lengkap='PJ API'
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()

    def test_login_token(self):
        response = self.client.post(
            '/api/token/', {'username': 'pj_api', 'password': 'pw'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

    def test_list_notifikasi_hanya_milik_sendiri(self):
        Notifikasi.objects.create(
            penanggung_jawab=self.pj, tipe='Dipinjam', pesan='x'
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/api/notifikasi/')
        self.assertEqual(response.status_code, 200)
        results = response.data.get('results', response.data)
        self.assertEqual(len(results), 1)

    def test_tandai_baca(self):
        notif = Notifikasi.objects.create(
            penanggung_jawab=self.pj, tipe='Dipinjam', pesan='x'
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.patch(
            f'/api/notifikasi/{notif.id}/baca/', {}, format='json'
        )
        self.assertEqual(response.status_code, 200)
        notif.refresh_from_db()
        self.assertTrue(notif.dibaca)

    def test_status_kunci(self):
        lab = Laboratorium.objects.create(kode_lab='LX', nama_lab='Lab X')
        Kunci.objects.create(laboratorium=lab, nomor_kunci='K9')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/api/status-kunci/')
        self.assertEqual(response.status_code, 200)
        results = response.data.get('results', response.data)
        self.assertEqual(len(results), 1)

    def test_akses_ditolak_tanpa_token(self):
        response = self.client.get('/api/notifikasi/')
        self.assertEqual(response.status_code, 401)