# 🔑 Rancang Bangun Sistem Peminjaman Kunci Laboratorium Berbasis Python Menggunakan Metode Prototype

[![Python](https://img.shields.io/badge/Python-3.14-blue)](https://python.org)
[![Django](https://img.shields.io/badge/Django-6.0-green)](https://djangoproject.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)](https://getbootstrap.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 📋 Deskripsi Proyek

Sistem informasi berbasis web yang dikembangkan untuk mengelola peminjaman dan pengembalian kunci laboratorium di lingkungan perguruan tinggi. Sistem ini menggantikan pencatatan manual berbasis buku dengan sistem digital yang terkomputerisasi, sehingga memudahkan laboran/admin dalam mengelola data peminjaman kunci laboratorium secara efisien dan akurat.

Proyek ini dikembangkan menggunakan metode **Prototype** dengan tahapan:
1. Analisis kebutuhan pengguna
2. Pembuatan prototype awal
3. Pengujian prototype oleh pengguna (laboran/dosen)
4. Revisi berdasarkan masukan
5. Sistem final

---

## ✨ Fitur Utama

### 🔐 Autentikasi
- Login dan logout admin/laboran
- Session-based authentication

### 📊 Dashboard
- Total kunci tersedia
- Jumlah kunci sedang dipinjam
- Jumlah peminjaman hari ini
- Aktivitas peminjaman terbaru

### 👥 Manajemen Data Master
- **Mahasiswa** — CRUD data mahasiswa (NIM, Nama, Program Studi)
- **Dosen** — CRUD data dosen (NIP, Nama)
- **Laboratorium** — CRUD data laboratorium (Kode, Nama, Gedung, Lantai)
- **Kunci** — CRUD data kunci dengan relasi ke laboratorium dan status otomatis (Tersedia/Dipinjam)

### 📝 Transaksi Peminjaman
- Form peminjaman lengkap (Mahasiswa, Dosen, Lab, Kunci, Jam Pinjam, Keperluan)
- Validasi ketersediaan kunci otomatis
- Dropdown kunci dinamis berdasarkan laboratorium (AJAX)
- Transaction atomic untuk menjaga konsistensi data
- Kunci yang sedang dipinjam tidak dapat dipinjam oleh orang lain

### ↩️ Transaksi Pengembalian
- Daftar peminjaman aktif
- Pencarian peminjaman berdasarkan NIM/Nama/No Kunci
- Konfirmasi pengembalian dengan pencatatan jam kembali
- Status kunci otomatis berubah menjadi **Tersedia** setelah dikembalikan

### 📜 Riwayat & Pencarian
- Riwayat seluruh peminjaman
- Pencarian multi-kriteria (NIM, Nama Mahasiswa, Nomor Kunci)
- Filter berdasarkan status (Dipinjam/Dikembalikan)
- Pagination data

### 📈 Laporan
- Filter laporan berdasarkan rentang tanggal
- Filter berdasarkan status peminjaman
- Ringkasan statistik (Total, Dipinjam, Dikembalikan)
- **Export ke Excel (.xlsx)**
- **Export ke CSV**

### 🧑🔧 Penanggung Jawab
- Role penanggung jawab kunci laboratorium (1–2 orang)
- Dikelola dari Django Admin (`/admin/`), satu form membuat akun + profil sekaligus
- Notifikasi otomatis dikirim saat kunci **dipinjam** dan **dikembalikan**

### 📱 Mobile App (API JSON)
- **REST API** dengan Django REST Framework + Token Authentication
- Login token, daftar notifikasi, tandai notifikasi dibaca, dan status kunci
- Siap dikonsumsi aplikasi mobile (Flutter) — lihat `docs/ROADMAP_MOBILE.md`

---

## 🛠️ Teknologi

| Teknologi | Versi | Kegunaan |
|-----------|-------|----------|
| Python | 3.14 | Bahasa pemrograman utama |
| Django | 6.0 | Framework web MVC |
| SQLite / MySQL | - | Database |
| Bootstrap | 5.3 | Framework CSS frontend |
| jQuery | 3.7 | JavaScript library untuk AJAX |
| Bootstrap Icons | 1.11 | Ikon antarmuka |
| openpyxl | - | Export laporan ke Excel |
| Django REST Framework | 3.17 | REST API untuk aplikasi mobile |

---

## 📁 Struktur Folder

```
sistem-peminjaman-kunci-lab/
├── apps/
│   ├── authentication/     # Login & logout, Penanggung Jawab
│   ├── dashboard/          # Dashboard & statistik
│   ├── master_data/        # CRUD Mahasiswa, Dosen, Lab, Kunci
│   ├── transaction/        # Peminjaman, Pengembalian, Riwayat
│   ├── notifications/      # Notifikasi + REST API mobile
│   └── report/             # Laporan & export
├── config/                 # Konfigurasi Django (settings, urls)
├── static/                 # File statis (CSS, JS)
├── templates/              # Template HTML (Bootstrap 5)
├── manage.py               # Entry point Django
├── requirements.txt        # Dependensi Python
└── .env                    # Konfigurasi environment
```

---

## 🚀 Cara Instalasi & Menjalankan

### Prasyarat
- Python 3.11 atau lebih baru
- Git (opsional, untuk cloning)

### Langkah-langkah

**1. Clone atau download repositori**
```bash
git clone https://github.com/delvin07-hub/sistem-peminjaman-kunci-lab.git
cd sistem-peminjaman-kunci-lab
```

**2. Buat dan aktifkan virtual environment**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install dependensi**
```bash
pip install -r requirements.txt
```

**4. Konfigurasi environment (opsional)**
```bash
# Edit file .env sesuai kebutuhan
# Untuk MySQL, set USE_MYSQL=True dan isi kredensial database
```

**5. Jalankan migrasi database**
```bash
python manage.py migrate
```

**6. Buat superuser (admin)**
```bash
python manage.py createsuperuser
```
Isi username, email, dan password saat diminta.

**7. (Opsional) Isi data awal untuk demo**
```bash
python manage.py seed_data
```

**8. Jalankan server**
```bash
python manage.py runserver
```

**9. Buka di browser**
- Aplikasi: http://127.0.0.1:8000/
- Admin Django: http://127.0.0.1:8000/admin/

---

## 🔑 Akun Default

Setelah menjalankan `python manage.py seed_data`, akun berikut tersedia:

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Superuser (full akses) |
| pj1 | pj12345 | Penanggung jawab (login mobile/API) |

> **Peringatan:** Ganti password default pada lingkungan produksi!

---

## 🗄️ Menggunakan MySQL

1. Buat database MySQL:
```sql
CREATE DATABASE kunci_lab CHARACTER SET utf8mb4;
```

2. Edit `.env`:
```env
USE_MYSQL=True
DB_NAME=kunci_lab
DB_USER=root
DB_PASSWORD=password_anda
DB_HOST=localhost
DB_PORT=3306
```

3. Jalankan migrasi:
```bash
python manage.py migrate
```

---

## 📖 Panduan Penggunaan

### Alur Kerja Sistem

```
Login → Dashboard → Kelola Data Master → Peminjaman → Pengembalian → Riwayat/Laporan
```

### 1. Login
- Buka aplikasi di browser
- Masukkan username dan password
- Klik **Masuk**

### 2. Dashboard
- Setelah login, halaman dashboard menampilkan:
  - Total kunci, kunci tersedia, kunci dipinjam
  - Jumlah peminjaman hari ini
  - 10 aktivitas peminjaman terbaru

### 3. Kelola Data Master
- **Mahasiswa**: Tambah, edit, hapus, dan cari data mahasiswa
- **Dosen**: Tambah, edit, hapus, dan cari data dosen
- **Laboratorium**: Tambah, edit, hapus laboratorium
- **Kunci**: Tambah, edit, hapus kunci (terkait dengan laboratorium tertentu)

### 4. Peminjaman Kunci
1. Pilih mahasiswa
2. Pilih dosen pengampu
3. Pilih laboratorium
4. Pilih kunci (hanya kunci **Tersedia** yang muncul)
5. Isi jam pinjam dan keperluan
6. Klik **PINJAM KUNCI**

### 5. Pengembalian Kunci
1. Buka menu **Pengembalian**
2. Cari data peminjaman aktif
3. Klik **Kembalikan**
4. Konfirmasi jam kembali
5. Klik **KONFIRMASI PENGEMBALIAN**
6. Status kunci otomatis menjadi **Tersedia**

### 6. Riwayat & Laporan
- **Riwayat**: Lihat seluruh transaksi, cari berdasarkan NIM/Nama/No Kunci
- **Laporan**: Filter berdasarkan tanggal, export ke Excel atau CSV

---

## 📱 Aplikasi Mobile (Penanggung Jawab)

Aplikasi mobile untuk penanggung jawab (1–2 orang) membaca notifikasi dan status kunci melalui REST API.

| Fitur | Endpoint |
|-------|----------|
| Login (ambil token) | `POST /api/token/` |
| Daftar notifikasi | `GET /api/notifikasi/` |
| Tandai dibaca | `PATCH /api/notifikasi/<id>/baca/` |
| Status kunci | `GET /api/status-kunci/` |

Semua endpoint (kecuali login) memerlukan header `Authorization: Token <token>`.
Panduan lengkap & contoh respons: **`docs/ROADMAP_MOBILE.md`**.

```bash
# Contoh login untuk mengambil token
curl -X POST http://localhost:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username":"pj1","password":"pj12345"}'
```

---

## 🧪 Metode Pengembangan (Prototype)

Proyek ini dikembangkan menggunakan metode **Prototype** yang terdiri dari 5 tahap:

| Tahap | Aktivitas | Output |
|-------|-----------|--------|
| **1. Analisis Kebutuhan** | Wawancara dengan laboran, identifikasi masalah | Dokumen kebutuhan fungsional & non-fungsional |
| **2. Prototype Awal** | Pembuatan aplikasi dengan fitur inti | Aplikasi versi alpha |
| **3. Uji Coba** | Pengujian oleh laboran/dosen | Feedback dan masukan |
| **4. Revisi** | Perbaikan berdasarkan feedback | Aplikasi versi beta |
| **5. Final** | Penyempurnaan dan dokumentasi | Aplikasi versi 1.0 |

---

## 📊 Entity Relationship Diagram (ERD)

```
┌─────────────┐     ┌─────────────┐     ┌──────────────┐
│  Mahasiswa  │     │    Kunci    │     │  Peminjaman  │
├─────────────┤     ├─────────────┤     ├──────────────┤
│ PK id       │     │ PK id       │     │ PK id        │
│ nim (uniq)  │────▶│ nomor_kunci │◄────│ FK mahasiswa │
│ nama        │     │ status      │     │ FK dosen     │
│ prodi       │     │ FK lab      │     │ FK kunci     │
└─────────────┘     └──────┬──────┘     │ FK lab       │
                          │            │ jam_pinjam   │
┌─────────────┐            │            │ jam_kembali  │
│   Dosen     │            │            │ keperluan    │
├─────────────┤            │            │ status       │
│ PK id       │            │            └──────────────┘
│ nip (uniq)  │            │
│ nama        │            │
└──────┬──────┘            │
       │                   │
       │  ┌────────────────┘
       │  │
       │  ▼
       │  ┌──────────────┐
       │  │ Laboratorium │
       │  ├──────────────┤
       └──│ PK id        │
          │ kode_lab     │
          │ nama_lab     │
          └──────────────┘
```

### Relasi Antar Tabel

| Tabel 1 | Tabel 2 | Relasi | Keterangan |
|---------|---------|--------|------------|
| Laboratorium | Kunci | One to Many | 1 lab punya banyak kunci |
| Kunci | Peminjaman | One to Many | 1 kunci bisa dipinjam berkali-kali |
| Mahasiswa | Peminjaman | One to Many | 1 mahasiswa bisa pinjam berkali-kali |
| Dosen | Peminjaman | One to Many | 1 dosen terkait banyak peminjaman |

---

## 🔌 API Endpoints

| Method | URL | Deskripsi | Login |
|--------|-----|-----------|-------|
| GET | `/` | Halaman login | ✗ |
| GET | `/logout/` | Logout | ✓ |
| GET | `/dashboard/` | Dashboard | ✓ |
| GET | `/master/mahasiswa/` | List mahasiswa | ✓ |
| GET/POST | `/master/mahasiswa/tambah/` | Tambah mahasiswa | ✓ |
| GET/POST | `/master/mahasiswa/edit/<id>/` | Edit mahasiswa | ✓ |
| POST | `/master/mahasiswa/hapus/<id>/` | Hapus mahasiswa | ✓ |
| GET | `/master/dosen/` | List dosen | ✓ |
| GET/POST | `/master/dosen/tambah/` | Tambah dosen | ✓ |
| GET | `/master/laboratorium/` | List lab | ✓ |
| GET/POST | `/master/laboratorium/tambah/` | Tambah lab | ✓ |
| GET | `/master/kunci/` | List kunci | ✓ |
| GET/POST | `/master/kunci/tambah/` | Tambah kunci | ✓ |
| GET/POST | `/transaksi/peminjaman/` | Form peminjaman | ✓ |
| GET | `/transaksi/pengembalian/` | Daftar pengembalian | ✓ |
| POST | `/transaksi/pengembalian/<id>/` | Proses pengembalian | ✓ |
| GET | `/transaksi/riwayat/` | Riwayat peminjaman | ✓ |
| GET | `/laporan/` | Laporan & export | ✓ |
| GET | `/transaksi/api/get-mahasiswa/` | API cari mahasiswa (AJAX) | ✓ |
| GET | `/transaksi/api/get-kunci/` | API filter kunci (AJAX) | ✓ |
| POST | `/api/token/` | Login API, dapatkan token | ✗ |
| GET | `/api/notifikasi/` | Daftar notifikasi penanggung jawab | Token |
| PATCH | `/api/notifikasi/<id>/baca/` | Tandai notifikasi dibaca | Token |
| GET | `/api/status-kunci/` | Status kunci untuk mobile | Token |
| GET | `/admin/` | Django Admin | ✓ |

---

## 👨‍💻 Pengembang

**Delvin**  
Proyek Tugas Akhir / Capstone  
Program Studi Informatika / Sistem Informasi / Teknik Komputer

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah **MIT License** — lihat file [LICENSE](LICENSE) untuk detail.

---

*© 2026 Sistem Peminjaman Kunci Laboratorium*
