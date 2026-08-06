from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.authentication.models import PenanggungJawab


class PenanggungJawabModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('pj1', password='secret123')
        self.pj = PenanggungJawab.objects.create(
            user=self.user,
            nama_lengkap='Budi Penanggung',
            telepon='0812',
            aktif=True,
        )

    def test_str_menampilkan_nama_lengkap(self):
        self.assertIn('Budi', str(self.pj))

    def test_reverse_relation_dari_user(self):
        self.assertEqual(self.pj, self.user.penanggung_jawab)

    def test_aktif_default_true(self):
        u2 = User.objects.create_user('pj2', password='x')
        pj = PenanggungJawab.objects.create(user=u2, nama_lengkap='C')
        self.assertTrue(pj.aktif)


class PenanggungJawabWebTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('root', 'r@x.com', 'pw')
        self.pj_user = User.objects.create_user('pj1', password='secret123')
        self.pj = PenanggungJawab.objects.create(
            user=self.pj_user,
            nama_lengkap='Budi Penanggung',
            telepon='0812',
            aktif=True,
        )

    def _post_create(self, **overrides):
        data = {
            'username': 'pj_baru',
            'password': 'pass1234',
            'nama_lengkap': 'Sari',
            'telepon': '0812',
            'aktif': 'on',
        }
        data.update(overrides)
        return self.client.post(reverse('penanggung_jawab_create'), data)

    def test_tambah_membuat_user_dan_password(self):
        self.client.force_login(self.admin)
        response = self._post_create()
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='pj_baru')
        self.assertTrue(user.check_password('pass1234'))
        self.assertTrue(PenanggungJawab.objects.filter(user=user).exists())

    def test_tambah_username_duplikat_ditolak(self):
        self.client.force_login(self.admin)
        response = self._post_create(username='pj1')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Username sudah dipakai.')

    def test_edit_pj_password_kosong_tidak_mengubah_password(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse('penanggung_jawab_update', args=[self.pj.id]),
            {
                'username': 'pj1',
                'password': '',
                'nama_lengkap': 'Budi Baru',
                'telepon': '0812',
                'aktif': 'on',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.pj.refresh_from_db()
        self.assertEqual(self.pj.nama_lengkap, 'Budi Baru')
        self.assertTrue(self.pj_user.check_password('secret123'))

    def test_edit_pj_password_diisi_akan_berubah(self):
        self.client.force_login(self.admin)
        self.client.post(
            reverse('penanggung_jawab_update', args=[self.pj.id]),
            {
                'username': 'pj1',
                'password': 'baru123',
                'nama_lengkap': 'Budi Baru',
                'telepon': '0812',
                'aktif': 'on',
            },
        )
        self.pj_user.refresh_from_db()
        self.assertTrue(self.pj_user.check_password('baru123'))

    def test_hapus_pj_menghapus_user(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse('penanggung_jawab_delete', args=[self.pj.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(PenanggungJawab.objects.filter(id=self.pj.id).exists())
        self.assertFalse(User.objects.filter(id=self.pj_user.id).exists())

    def test_non_superuser_mendapat_403(self):
        self.client.force_login(self.pj_user)
        response = self.client.get(reverse('penanggung_jawab_list'))
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse('mahasiswa_list'))
        self.assertEqual(response.status_code, 403)

    def test_login_web_non_superuser_ditolak(self):
        response = self.client.post(reverse('login'), {
            'username': 'pj1',
            'password': 'secret123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hanya admin')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_superuser_akses_list(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse('penanggung_jawab_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Budi Penanggung')
