from datetime import date, datetime, time
from unittest import mock
from zoneinfo import ZoneInfo

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.authentication.models import PenanggungJawab
from apps.master_data.models import Mahasiswa, Dosen, Laboratorium, Kunci
from apps.notifications.models import Notifikasi
from apps.transaction.models import Peminjaman

from .services import PeminjamanService


class HookNotifikasiTest(TestCase):
    def setUp(self):
        user = User.objects.create_user('pj', password='x')
        self.pj = PenanggungJawab.objects.create(
            user=user, nama_lengkap='PJ Lab'
        )
        self.lab = Laboratorium.objects.create(
            kode_lab='LK', nama_lab='Lab Kartu'
        )
        self.mahasiswa = Mahasiswa.objects.create(
            nim='2209000', nama='Rina Demo', program_studi='TI'
        )
        self.dosen = Dosen.objects.create(nidn='ND9', nama='Dosen D')
        self.kunci = Kunci.objects.create(
            laboratorium=self.lab, nomor_kunci='K1', status='Tersedia'
        )

    @mock.patch('apps.notifications.services._kirim_push_bg')
    def test_pinjam_kunci_membuat_notifikasi_dipinjam(self, _):
        peminjaman = PeminjamanService.pinjam_kunci({
            'mahasiswa': self.mahasiswa,
            'dosen': self.dosen,
            'laboratorium': self.lab,
            'kunci': self.kunci,
            'keperluan': 'Praktikum',
        })
        notif = Notifikasi.objects.get(tipe='Dipinjam')
        self.assertEqual(notif.peminjaman, peminjaman)
        self.assertEqual(notif.penanggung_jawab, self.pj)

    @mock.patch('apps.notifications.services._kirim_push_bg')
    def test_kembalikan_kunci_membuat_notifikasi_dikembalikan(self, _):
        peminjaman = PeminjamanService.pinjam_kunci({
            'mahasiswa': self.mahasiswa,
            'dosen': self.dosen,
            'laboratorium': self.lab,
            'kunci': self.kunci,
            'keperluan': 'Praktikum',
        })
        Notifikasi.objects.all().delete()
        PeminjamanService.kembalikan_kunci(peminjaman.id)
        notif = Notifikasi.objects.get(tipe='Dikembalikan')
        self.assertEqual(notif.peminjaman, peminjaman)


class RiwayatFilterTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('admin', 'a@x.com', 'pw')
        self.client.force_login(self.user)
        self.lab = Laboratorium.objects.create(kode_lab='LA', nama_lab='Lab A')
        self.m1 = Mahasiswa.objects.create(
            nim='2209001', nama='Andi', program_studi='TI'
        )
        self.m2 = Mahasiswa.objects.create(
            nim='2209002', nama='Budi', program_studi='SI'
        )
        self.d = Dosen.objects.create(nidn='ND1', nama='Dosen')
        self.k1 = Kunci.objects.create(
            laboratorium=self.lab, nomor_kunci='K1'
        )
        self.k2 = Kunci.objects.create(
            laboratorium=self.lab, nomor_kunci='K2'
        )
        self.p1 = Peminjaman.objects.create(
            mahasiswa=self.m1, dosen=self.d, laboratorium=self.lab,
            kunci=self.k1, tanggal_pinjam=date(2026, 1, 1),
            jam_pinjam=time(8, 0), keperluan='X', status='Dikembalikan',
        )
        self.p2 = Peminjaman.objects.create(
            mahasiswa=self.m2, dosen=self.d, laboratorium=self.lab,
            kunci=self.k2, tanggal_pinjam=date(2026, 6, 15),
            jam_pinjam=time(9, 0), keperluan='Y', status='Dipinjam',
        )

    def _riwayat(self, params):
        return self.client.get(reverse('riwayat_list'), params)

    def test_filter_nim(self):
        r = self._riwayat({'nim': '2209001'})
        self.assertContains(r, 'Andi')
        self.assertNotContains(r, 'Budi')

    def test_filter_nama(self):
        r = self._riwayat({'nama': 'Budi'})
        self.assertContains(r, 'Budi')
        self.assertNotContains(r, 'Andi')

    def test_filter_nomor_kunci(self):
        r = self._riwayat({'nomor_kunci': 'K2'})
        self.assertContains(r, 'K2')
        self.assertNotContains(r, 'K1')

    def test_filter_status(self):
        r = self._riwayat({'status': 'Dipinjam'})
        self.assertContains(r, 'Budi')
        self.assertNotContains(r, 'Andi')

    def test_filter_tanggal_range(self):
        r = self._riwayat({
            'tanggal_awal': '2026-06-01',
            'tanggal_akhir': '2026-06-30',
        })
        self.assertContains(r, 'Budi')
        self.assertNotContains(r, 'Andi')


class JamPinjamOtomatisTest(TestCase):
    def setUp(self):
        PenanggungJawab.objects.create(
            user=User.objects.create_user('pj', password='x'),
            nama_lengkap='PJ Lab',
        )
        self.lab = Laboratorium.objects.create(
            kode_lab='LK', nama_lab='Lab Kartu'
        )
        self.mahasiswa = Mahasiswa.objects.create(
            nim='2209000', nama='Rina', program_studi='TI'
        )
        self.dosen = Dosen.objects.create(nidn='ND9', nama='Dosen D')
        self.kunci = Kunci.objects.create(
            laboratorium=self.lab, nomor_kunci='K1', status='Tersedia'
        )

    def _pinjam(self):
        return PeminjamanService.pinjam_kunci({
            'mahasiswa': self.mahasiswa,
            'dosen': self.dosen,
            'laboratorium': self.lab,
            'kunci': self.kunci,
            'keperluan': 'Praktikum',
        })

    @mock.patch('apps.notifications.services._kirim_push_bg')
    def test_pinjam_mencatat_jam_dan_tanggal_server(self, _):
        fixed = datetime(2026, 8, 6, 14, 32, 5, tzinfo=ZoneInfo('Asia/Jakarta'))
        with mock.patch(
            'apps.transaction.services.timezone.now', return_value=fixed
        ):
            p = self._pinjam()
        self.assertEqual(p.tanggal_pinjam, date(2026, 8, 6))
        self.assertEqual(p.jam_pinjam, time(14, 32, 5))


class KunciRuanganValidasiTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('root', 'r@x.com', 'pw')
        self.client.force_login(self.admin)
        self.lab_a = Laboratorium.objects.create(
            kode_lab='LA', nama_lab='Ruang A'
        )
        self.lab_b = Laboratorium.objects.create(
            kode_lab='LB', nama_lab='Ruang B'
        )
        self.kunci_a = Kunci.objects.create(
            laboratorium=self.lab_a, nomor_kunci='KA', status='Tersedia'
        )
        self.kunci_b = Kunci.objects.create(
            laboratorium=self.lab_b, nomor_kunci='KB', status='Tersedia'
        )
        self.mahasiswa = Mahasiswa.objects.create(
            nim='2209005', nama='Sari', program_studi='TI'
        )
        self.dosen = Dosen.objects.create(nidn='ND5', nama='Dosen S')

    def _post_form(self, lab, kunci):
        return self.client.post(reverse('peminjaman_create'), {
            'mahasiswa': self.mahasiswa.id,
            'dosen': self.dosen.id,
            'laboratorium': lab.id,
            'kunci': kunci.id,
            'keperluan': 'Praktikum',
        })

    def test_service_tolak_kunci_beda_ruangan(self):
        with self.assertRaises(ValueError):
            PeminjamanService.pinjam_kunci({
                'mahasiswa': self.mahasiswa,
                'dosen': self.dosen,
                'laboratorium': self.lab_a,
                'kunci': self.kunci_b,
                'keperluan': 'Praktikum',
            })

    def test_form_tolak_kunci_beda_ruangan(self):
        response = self._post_form(self.lab_a, self.kunci_b)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'Kunci tidak sesuai dengan ruangan yang dipilih.'
        )
        self.assertFalse(Peminjaman.objects.filter(mahasiswa=self.mahasiswa).exists())

    @mock.patch('apps.notifications.services._kirim_push_bg')
    def test_form_terima_kunci_seruangan(self, _):
        response = self._post_form(self.lab_a, self.kunci_a)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Peminjaman.objects.filter(mahasiswa=self.mahasiswa).exists())