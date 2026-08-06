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