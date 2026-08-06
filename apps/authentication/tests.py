from django.contrib.auth.models import User
from django.test import TestCase

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


class PenanggungJawabAdminCreateTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('root', 'r@x.com', 'pw')
        self.client.force_login(self.admin)

    def test_tambah_membuat_user_dan_password(self):
        response = self.client.post(
            '/admin/authentication/penanggungjawab/add/',
            {
                'username': 'pj_baru',
                'password': 'pass1234',
                'nama_lengkap': 'Sari',
                'telepon': '0812',
                'aktif': 'on',
            },
        )
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='pj_baru')
        self.assertTrue(user.check_password('pass1234'))
        self.assertTrue(PenanggungJawab.objects.filter(user=user).exists())