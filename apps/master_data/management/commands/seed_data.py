from datetime import time, date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from apps.authentication.models import PenanggungJawab
from apps.master_data.models import Mahasiswa, Dosen, Laboratorium, Kunci
from apps.transaction.models import Peminjaman


class Command(BaseCommand):
    help = 'Mengisi data awal untuk demo aplikasi'

    def handle(self, *args, **kwargs):
        self.stdout.write('Mengisi data awal...')

        self._create_superuser()
        self._create_penanggung_jawab()
        self._create_mahasiswa()
        self._create_dosen()
        self._create_laboratorium()
        self._create_kunci()
        self._create_peminjaman()

        self.stdout.write(self.style.SUCCESS('Data awal berhasil diisi!'))

    def _create_superuser(self):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@lab.com', 'admin123')
            self.stdout.write('  [OK] Superuser admin/admin123')

    def _create_penanggung_jawab(self):
        if not User.objects.filter(username='pj1').exists():
            user = User.objects.create_user('pj1', password='pj12345')
            PenanggungJawab.objects.create(
                user=user,
                nama_lengkap='Penanggung Jawab Lab',
                telepon='081234567890',
            )
            self.stdout.write('  [OK] Penanggung jawab pj1/pj12345')

    def _create_mahasiswa(self):
        data = [
            ('2201001', 'Andi Pratama', 'Informatika'),
            ('2201002', 'Budi Santoso', 'Sistem Informasi'),
            ('2201003', 'Cici Dewi Lestari', 'Teknik Komputer'),
            ('2201004', 'Dadang Hermawan', 'Informatika'),
            ('2201005', 'Eka Putri Rahayu', 'Sistem Informasi'),
            ('2201006', 'Fajar Ramadhan', 'Teknik Komputer'),
            ('2201007', 'Gita Ayu Kusuma', 'Informatika'),
            ('2201008', 'Hendra Gunawan', 'Sistem Informasi'),
            ('2201009', 'Intan Permatasari', 'Teknik Komputer'),
            ('2201010', 'Joko Susilo', 'Informatika'),
            ('2201011', 'Kartika Dewi', 'Sistem Informasi'),
            ('2201012', 'Leo Saputra', 'Teknik Komputer'),
        ]
        for nim, nama, prodi in data:
            Mahasiswa.objects.get_or_create(nim=nim, defaults={'nama': nama, 'program_studi': prodi})
        self.stdout.write(f'  [OK] {len(data)} mahasiswa')

    def _create_dosen(self):
        data = [
            ('198001012010011001', 'Dr. Ahmad Fauzi, M.Kom.'),
            ('198002022010021002', 'Dr. Siti Rahmah, M.T.'),
            ('198003032010031003', 'Bambang Wijaya, S.Kom., M.Kom.'),
            ('198004042010041004', 'Dewi Sartika, S.T., M.T.'),
            ('198005052010051005', 'Prof. Dr. Hendra Gunawan, M.Sc.'),
        ]
        for nidn, nama in data:
            Dosen.objects.get_or_create(nidn=nidn, defaults={'nama': nama})
        self.stdout.write(f'  [OK] {len(data)} dosen')

    def _create_laboratorium(self):
        data = [
            ('LAB-01', 'Lab Komputer 1', 'Gedung A', 'Lantai 2'),
            ('LAB-02', 'Lab Jaringan', 'Gedung A', 'Lantai 3'),
            ('LAB-03', 'Lab Multimedia', 'Gedung B', 'Lantai 1'),
            ('LAB-04', 'Lab Hardware', 'Gedung B', 'Lantai 2'),
            ('LAB-05', 'Lab RPL', 'Gedung C', 'Lantai 1'),
        ]
        for kode, nama, gedung, lantai in data:
            Laboratorium.objects.get_or_create(
                kode_lab=kode,
                defaults={'nama_lab': nama, 'gedung': gedung, 'lantai': lantai},
            )
        self.stdout.write(f'  [OK] {len(data)} laboratorium')

    def _create_kunci(self):
        lab_list = list(Laboratorium.objects.all())
        created_count = 0
        for lab in lab_list:
            for i in range(1, 5):
                nomor = f'{lab.kode_lab}-K{i:02d}'
                _, created = Kunci.objects.get_or_create(
                    laboratorium=lab, nomor_kunci=nomor,
                    defaults={'status': 'Tersedia'},
                )
                if created:
                    created_count += 1
        self.stdout.write(f'  [OK] {created_count} kunci')

    def _create_peminjaman(self):
        mahasiswa = list(Mahasiswa.objects.all())
        dosen = list(Dosen.objects.all())
        kunci_list = list(Kunci.objects.all())

        if not kunci_list:
            self.stdout.write('  [SKIP] Tidak ada kunci untuk membuat peminjaman')
            return

        now = timezone.now()
        today = now.date()
        count = 0

        for i in range(min(8, len(mahasiswa))):
            m = mahasiswa[i]
            d = dosen[i % len(dosen)]
            k = kunci_list[i % len(kunci_list)]

            if Peminjaman.objects.filter(
                mahasiswa=m, kunci=k,
                tanggal_pinjam=today - timedelta(days=i % 3),
            ).exists():
                continue

            jam_pinjam = time(8 + i, 0)
            is_returned = i % 2 == 0

            if is_returned:
                jam_kembali = time(jam_pinjam.hour + 1 + (i % 2), 30)
                Peminjaman.objects.create(
                    mahasiswa=m,
                    dosen=d,
                    laboratorium=k.laboratorium,
                    kunci=k,
                    tanggal_pinjam=today - timedelta(days=i % 3),
                    jam_pinjam=jam_pinjam,
                    tanggal_kembali=today - timedelta(days=i % 3),
                    jam_kembali=jam_kembali,
                    keperluan=f'Praktikum {["Basis Data", "Jaringan", "Multimedia", "Pemrograman"][i % 4]}',
                    status='Dikembalikan',
                )
            else:
                Peminjaman.objects.create(
                    mahasiswa=m,
                    dosen=d,
                    laboratorium=k.laboratorium,
                    kunci=k,
                    tanggal_pinjam=today,
                    jam_pinjam=jam_pinjam,
                    keperluan=f'Praktikum {["Basis Data", "Jaringan", "Multimedia", "Pemrograman"][i % 4]}',
                    status='Dipinjam',
                )
                k.status = 'Dipinjam'
                k.save()

            count += 1

        self.stdout.write(f'  [OK] {count} peminjaman contoh')
