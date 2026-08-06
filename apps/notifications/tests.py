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

    def test_peminjaman_detail_di_serializer_notifikasi(self):
        mhs = Mahasiswa.objects.create(
            nim='2200001', nama='Budi Lab', program_studi='SI'
        )
        dosen = Dosen.objects.create(nidn='NX002', nama='Dosen Y')
        lab = Laboratorium.objects.create(kode_lab='LY', nama_lab='Lab Y')
        kunci = Kunci.objects.create(laboratorium=lab, nomor_kunci='K2')
        peminjaman = Peminjaman.objects.create(
            mahasiswa=mhs,
            dosen=dosen,
            laboratorium=lab,
            kunci=kunci,
            jam_pinjam=time(9, 30),
            keperluan='TA',
            status='Dipinjam',
        )
        Notifikasi.objects.create(
            penanggung_jawab=self.pj,
            peminjaman=peminjaman,
            tipe='Dipinjam',
            pesan='pesan',
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/api/notifikasi/')
        results = response.data.get('results', response.data)
        detail = results[0]['peminjaman_detail']
        self.assertEqual(detail['mahasiswa']['nim'], '2200001')
        self.assertEqual(detail['mahasiswa']['nama'], 'Budi Lab')
        self.assertEqual(detail['dosen']['nama'], 'Dosen Y')
        self.assertEqual(detail['laboratorium']['kode_lab'], 'LY')
        self.assertEqual(detail['kunci']['nomor_kunci'], 'K2')
        self.assertEqual(detail['keperluan'], 'TA')

    def test_peminjaman_aktif_di_status_kunci(self):
        mhs = Mahasiswa.objects.create(
            nim='2200002', nama='Citra', program_studi='IF'
        )
        dosen = Dosen.objects.create(nidn='NX003', nama='Dosen Z')
        lab = Laboratorium.objects.create(kode_lab='LZ', nama_lab='Lab Z')
        kunci = Kunci.objects.create(
            laboratorium=lab, nomor_kunci='K3', status='Dipinjam'
        )
        Peminjaman.objects.create(
            mahasiswa=mhs,
            dosen=dosen,
            laboratorium=lab,
            kunci=kunci,
            jam_pinjam=time(10, 0),
            keperluan='Praktikum',
            status='Dipinjam',
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/api/status-kunci/')
        results = response.data.get('results', response.data)
        aktif = next(r for r in results if r['id'] == kunci.id)
        self.assertEqual(aktif['status'], 'Dipinjam')
        self.assertEqual(aktif['peminjaman_aktif']['mahasiswa']['nama'], 'Citra')
        self.assertEqual(aktif['peminjaman_aktif']['dosen']['nama'], 'Dosen Z')

    def test_detail_kunci_dengan_riwayat(self):
        mhs = Mahasiswa.objects.create(
            nim='2200003', nama='Dedi', program_studi='TI'
        )
        dosen = Dosen.objects.create(nidn='NX004', nama='Dosen W')
        lab = Laboratorium.objects.create(kode_lab='LW', nama_lab='Lab W')
        kunci = Kunci.objects.create(
            laboratorium=lab, nomor_kunci='K4', status='Dipinjam'
        )
        Peminjaman.objects.create(
            mahasiswa=mhs,
            dosen=dosen,
            laboratorium=lab,
            kunci=kunci,
            jam_pinjam=time(11, 0),
            keperluan='Riset',
            status='Dipinjam',
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(f'/api/status-kunci/{kunci.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['nomor_kunci'], 'K4')
        self.assertEqual(response.data['riwayat'][0]['mahasiswa']['nama'], 'Dedi')
        self.assertEqual(
            response.data['riwayat'][0]['mahasiswa']['nim'], '2200003'
        )

    def test_device_token_register_dan_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(
            '/api/device-token/',
            {'token': 'fcm-token-abc'},
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        from .models import DeviceToken

        dt = DeviceToken.objects.get(token='fcm-token-abc')
        self.assertEqual(dt.penanggung_jawab, self.pj)

        response = self.client.delete(
            '/api/device-token/', {'token': 'fcm-token-abc'}, format='json'
        )
        self.assertEqual(response.status_code, 204)
        self.assertFalse(DeviceToken.objects.filter(pk=dt.pk).exists())

    def test_device_token_milik_orang_lain_tidak_bisa_dihapus(self):
        from .models import DeviceToken

        other_user = User.objects.create_user('pj_lain', password='x')
        other_pj = PenanggungJawab.objects.create(
            user=other_user, nama_lengkap='PJ Lain'
        )
        DeviceToken.objects.create(
            penanggung_jawab=other_pj, token='fcm-token-lain'
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete(
            '/api/device-token/', {'token': 'fcm-token-lain'}, format='json'
        )
        self.assertEqual(response.status_code, 404)


class PushNotifikasiServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('pjs', password='x')
        self.pj = PenanggungJawab.objects.create(
            user=self.user, nama_lengkap='PJ Push', aktif=True
        )

    def test_push_tanpa_key_file_tidak_error(self):
        from .models import DeviceToken, Notifikasi
        from .services import PushNotifikasiService

        DeviceToken.objects.create(
            penanggung_jawab=self.pj, token='fcm-token-1'
        )
        notif = Notifikasi.objects.create(
            penanggung_jawab=self.pj, tipe='Dipinjam', pesan='pesan'
        )
        try:
            PushNotifikasiService.kirim(notif)
        except Exception as exc:  # pragma: no cover
            self.fail(f'kirim melempar exception: {exc}')

    def test_hook_buat_tidak_error_tanpa_key(self):
        mhs = Mahasiswa.objects.create(
            nim='2200004', nama='Eka', program_studi='TI'
        )
        dosen = Dosen.objects.create(nidn='NX005', nama='Dosen V')
        lab = Laboratorium.objects.create(kode_lab='LV', nama_lab='Lab V')
        kunci = Kunci.objects.create(laboratorium=lab, nomor_kunci='K5')
        peminjaman = Peminjaman.objects.create(
            mahasiswa=mhs,
            dosen=dosen,
            laboratorium=lab,
            kunci=kunci,
            jam_pinjam=time(7, 0),
            keperluan='Praktikum',
        )
        try:
            NotifikasiService.buat(peminjaman, 'Dipinjam')
        except Exception as exc:  # pragma: no cover
            self.fail(f'buat melempar exception: {exc}')