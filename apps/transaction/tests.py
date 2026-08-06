from datetime import time

from django.contrib.auth.models import User
from django.test import TestCase

from apps.authentication.models import PenanggungJawab
from apps.master_data.models import Mahasiswa, Dosen, Laboratorium, Kunci
from apps.notifications.models import Notifikasi

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

    def test_pinjam_kunci_membuat_notifikasi_dipinjam(self):
        peminjaman = PeminjamanService.pinjam_kunci({
            'mahasiswa': self.mahasiswa,
            'dosen': self.dosen,
            'laboratorium': self.lab,
            'kunci': self.kunci,
            'jam_pinjam': time(9, 0),
            'keperluan': 'Praktikum',
        })
        notif = Notifikasi.objects.get(tipe='Dipinjam')
        self.assertEqual(notif.peminjaman, peminjaman)
        self.assertEqual(notif.penanggung_jawab, self.pj)

    def test_kembalikan_kunci_membuat_notifikasi_dikembalikan(self):
        peminjaman = PeminjamanService.pinjam_kunci({
            'mahasiswa': self.mahasiswa,
            'dosen': self.dosen,
            'laboratorium': self.lab,
            'kunci': self.kunci,
            'jam_pinjam': time(9, 0),
            'keperluan': 'Praktikum',
        })
        Notifikasi.objects.all().delete()
        PeminjamanService.kembalikan_kunci(peminjaman.id)
        notif = Notifikasi.objects.get(tipe='Dikembalikan')
        self.assertEqual(notif.peminjaman, peminjaman)