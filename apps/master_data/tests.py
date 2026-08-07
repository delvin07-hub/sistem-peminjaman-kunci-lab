from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.master_data.models import Kunci, Laboratorium, Mahasiswa, Dosen

from apps.transaction.models import Peminjaman


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

    def test_hapus_kunci_renumber_otomatis(self):
        lab = Laboratorium.objects.create(
            kode_lab='R1', nama_lab='Aula'
        )
        for n in ['K1', 'K2', 'K3']:
            Kunci.objects.create(laboratorium=lab, nomor_kunci=n)
        k2 = Kunci.objects.get(nomor_kunci='K2')
        response = self.client.post(reverse('kunci_delete', args=[k2.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Kunci.objects.filter(id=k2.id).exists())
        sisa = sorted(
            Kunci.objects.filter(laboratorium=lab)
            .values_list('nomor_kunci', flat=True)
        )
        self.assertEqual(sisa, ['K1', 'K2'])

    def test_hapus_kunci_dipinjam_ditolak(self):
        lab = Laboratorium.objects.create(
            kode_lab='R1', nama_lab='Aula'
        )
        k = Kunci.objects.create(
            laboratorium=lab, nomor_kunci='K1', status='Dipinjam'
        )
        response = self.client.post(reverse('kunci_delete', args=[k.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Kunci.objects.filter(id=k.id).exists())


class HapusEntitasDipinjamTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('root', 'r@x.com', 'pw')
        self.client.force_login(self.admin)
        self.mahasiswa = Mahasiswa.objects.create(
            nim='1001', nama='Ani', program_studi='Informatika'
        )
        self.dosen = Dosen.objects.create(nidn='9001', nama='Pak Budi')
        self.lab = Laboratorium.objects.create(
            kode_lab='R1', nama_lab='Lab A'
        )
        self.kunci = Kunci.objects.create(
            laboratorium=self.lab, nomor_kunci='K1'
        )

    def _pinjam(self):
        Peminjaman.objects.create(
            mahasiswa=self.mahasiswa,
            dosen=self.dosen,
            laboratorium=self.lab,
            kunci=self.kunci,
            jam_pinjam='08:00:00',
            keperluan='Praktikum',
            status='Dipinjam',
        )

    def test_hapus_mahasiswa_dipinjam_ditolak(self):
        self._pinjam()
        resp = self.client.post(
            reverse('mahasiswa_delete', args=[self.mahasiswa.id])
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Mahasiswa.objects.filter(id=self.mahasiswa.id).exists())

    def test_hapus_dosen_dipinjam_ditolak(self):
        self._pinjam()
        resp = self.client.post(
            reverse('dosen_delete', args=[self.dosen.id])
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Dosen.objects.filter(id=self.dosen.id).exists())

    def test_hapus_ruangan_punya_kunci_ditolak(self):
        resp = self.client.post(
            reverse('laboratorium_delete', args=[self.lab.id])
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(
            Laboratorium.objects.filter(id=self.lab.id).exists()
        )

    def test_hapus_ruangan_dipinjam_ditolak(self):
        self._pinjam()
        resp = self.client.post(
            reverse('laboratorium_delete', args=[self.lab.id])
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(
            Laboratorium.objects.filter(id=self.lab.id).exists()
        )

    def test_hapus_entitas_tanpa_pinjaman_berhasil(self):
        resp = self.client.post(
            reverse('mahasiswa_delete', args=[self.mahasiswa.id])
        )
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(
            Mahasiswa.objects.filter(id=self.mahasiswa.id).exists()
        )

    def test_riwayat_set_null_setelah_hapus(self):
        self.kunci.status = 'Dikembalikan'
        self.kunci.save()
        self._pinjam()
        p = Peminjaman.objects.get(mahasiswa=self.mahasiswa)
        p.status = 'Dikembalikan'
        p.save()

        self.client.post(reverse('mahasiswa_delete', args=[self.mahasiswa.id]))
        resp = self.client.get(reverse('riwayat_list'))

        self.assertContains(resp, '-')
        p.refresh_from_db()
        self.assertIsNone(p.mahasiswa)


class ImportExcelTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('root', 'r@x.com', 'pw')
        self.client.force_login(self.admin)

    def _buat_xlsx(self, headers, rows):
        import io

        import openpyxl

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(headers)
        for r in rows:
            ws.append(r)
        buf = io.BytesIO()
        wb.save(buf)
        buf.seek(0)
        return buf

    def test_impor_mahasiswa_membuat_dan_update(self):
        file = self._buat_xlsx(
            ['NIM', 'Nama', 'Program Studi'],
            [['1001', 'Ani', 'Informatika'], ['1002', 'Budi', 'Sistem Informasi']],
        )
        resp = self.client.post(
            reverse('mahasiswa_import'), {'file': file}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Mahasiswa.objects.count(), 2)

        file2 = self._buat_xlsx(
            ['NIM', 'Nama', 'Program Studi'],
            [['1001', 'Ani Updated', 'Informatika']],
        )
        self.client.post(reverse('mahasiswa_import'), {'file': file2})
        self.assertEqual(Mahasiswa.objects.count(), 2)
        self.assertEqual(
            Mahasiswa.objects.get(nim='1001').nama, 'Ani Updated'
        )

    def test_impor_dosen_membuat_dan_update(self):
        file = self._buat_xlsx(
            ['NIDN', 'Nama'], [['9001', 'Pak Budi']]
        )
        resp = self.client.post(reverse('dosen_import'), {'file': file})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Dosen.objects.count(), 1)
        self.assertEqual(Dosen.objects.get(nidn='9001').nama, 'Pak Budi')

    def test_template_tersedia(self):
        resp = self.client.get(reverse('mahasiswa_import_template'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(
            'application/vnd.openxmlformats', resp['Content-Type']
        )