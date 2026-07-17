# RANCANG BANGUN SISTEM PEMINJAMAN KUNCI LABORATORIUM BERBASIS PYTHON MENGGUNAKAN METODE PROTOTYPE

**Dokumen Perencanaan Proyek — Tugas Akhir / Capstone**

---

## DAFTAR ISI

1. [Analisis Kebutuhan Sistem](#1-analisis-kebutuhan-sistem)
2. [Flowchart](#2-flowchart)
3. [Use Case Diagram](#3-use-case-diagram)
4. [Activity Diagram](#4-activity-diagram)
5. [Sequence Diagram](#5-sequence-diagram)
6. [ERD Database](#6-erd-database)
7. [Relasi Tabel](#7-relasi-tabel)
8. [Struktur Folder Project](#8-struktur-folder-project)
9. [Daftar Model Django](#9-daftar-model-django)
10. [Daftar URL / Route](#10-daftar-url--route)
11. [Daftar View](#11-daftar-view)
12. [Rancangan Dashboard](#12-rancangan-dashboard)
13. [Rancangan Halaman Login](#13-rancangan-halaman-login)
14. [Rancangan Halaman Data Mahasiswa](#14-rancangan-halaman-data-mahasiswa)
15. [Rancangan Halaman Data Laboratorium](#15-rancangan-halaman-data-laboratorium)
16. [Rancangan Halaman Data Kunci](#16-rancangan-halaman-data-kunci)
17. [Rancangan Halaman Peminjaman](#17-rancangan-halaman-peminjaman)
18. [Rancangan Halaman Pengembalian](#18-rancangan-halaman-pengembalian)
19. [Rancangan Halaman Riwayat](#19-rancangan-halaman-riwayat)
20. [Best Practice Implementasi Django](#20-best-practice-implementasi-django)

---

## 1. ANALISIS KEBUTUHAN SISTEM

### 1.1 Analisis Sistem Berjalan (Manual)

| No | Aktivitas | Media | Masalah |
|----|-----------|-------|---------|
| 1 | Pencatatan peminjaman kunci | Buku catatan manual | Mudah rusak, hilang, sulit dicari |
| 2 | Pengecekan ketersediaan kunci | Cek fisik lemari kunci | Tidak efisien, memakan waktu |
| 3 | Pencarian riwayat peminjaman | Membuka halaman buku satu per satu | Lambat, tidak praktis |
| 4 | Pembuatan laporan bulanan | Rekap manual dari buku catatan | Rentan kesalahan, tidak akurat |

### 1.2 Analisis Kebutuhan Fungsional

| Kode | Kebutuhan | Modul |
|------|-----------|-------|
| F-01 | Sistem dapat melakukan autentikasi admin/laboran | Authentication |
| F-02 | Sistem menampilkan dashboard dengan statistik kunci | Dashboard |
| F-03 | Sistem dapat mengelola data mahasiswa (CRUD) | Master Data |
| F-04 | Sistem dapat mengelola data laboratorium (CRUD) | Master Data |
| F-05 | Sistem dapat mengelola data kunci (CRUD) | Master Data |
| F-06 | Sistem dapat mengelola data dosen (CRUD) | Master Data |
| F-07 | Sistem mencatat peminjaman kunci dengan validasi | Transaction |
| F-08 | Sistem memvalidasi ketersediaan kunci secara otomatis | Transaction |
| F-09 | Sistem mencatat pengembalian kunci | Transaction |
| F-10 | Sistem mengubah status kunci otomatis saat dikembalikan | Transaction |
| F-11 | Sistem menyimpan dan menampilkan riwayat peminjaman | Transaction |
| F-12 | Sistem menyediakan pencarian multi-kriteria (NIM/Nama/No Kunci) | Transaction |
| F-13 | Sistem menghasilkan laporan peminjaman dengan export | Report |

### 1.3 Analisis Kebutuhan Non-Fungsional

| Kode | Kebutuhan |
|------|-----------|
| NF-01 | Framework Django 6.0 (Python 3.14) |
| NF-02 | Database SQLite (development) / MySQL (production) |
| NF-03 | Tampilan responsif menggunakan Bootstrap 5.3 |
| NF-04 | Keamanan password menggunakan PBKDF2 (default Django) |
| NF-05 | Sistem dapat diakses melalui web browser |
| NF-06 | Waktu respon halaman < 3 detik |

### 1.4 Aktor Sistem

| Aktor | Deskripsi | Hak Akses |
|-------|-----------|-----------|
| Admin/Laboran | Pengelola sistem yang bertugas mencatat peminjaman dan pengembalian kunci laboratorium | Full akses (login, CRUD, transaksi, laporan) |

---

## 2. FLOWCHART

### 2.1 Flowchart Utama

```
                    ┌─────────────────────┐
                    │       START         │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │   Halaman Login     │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │   Validasi Login    │
                    └──────────┬──────────┘
                    ┌──────────┴──────────┐
                    │        VALID?        │
                    └──────────┬──────────┘
                    ┌──────────┴──────────┐
                    │        YA           │          TIDAK
                    ▼                     ▼
           ┌────────────────┐   ┌────────────────┐
           │   Dashboard    │   │ Tampilkan Error│
           └───────┬────────┘   └──────┬─────────┘
                   ▼                   │
        ┌──────────────────────┐       │
        │   Menu Utama:        │◄──────┘
        │ 1. Data Mahasiswa    │
        │ 2. Data Lab          │
        │ 3. Data Kunci        │
        │ 4. Data Dosen        │
        │ 5. Peminjaman        │
        │ 6. Pengembalian      │
        │ 7. Riwayat           │
        │ 8. Laporan           │
        └──────────────────────┘
                   ▼
        ┌──────────────────────┐
        │   Pilih Menu         │
        └──────────────────────┘
                   ▼
        ┌──────────────────────┐
        │   Proses CRUD /      │
        │   Transaksi          │
        └──────────────────────┘
                   ▼
        ┌──────────────────────┐
        │   Simpan ke DB       │
        └──────────────────────┘
                   ▼
        ┌──────────────────────┐
        │  Kembali ke Menu?    │
        └──────┬───────┬───────┘
               │ YA    │ TIDAK
               ▼       ▼
         ┌────────┐ ┌──────────┐
         │  Menu  │ │  STOP    │
         └────────┘ └──────────┘
```

### 2.2 Flowchart Detail Peminjaman

```
                    ┌──────────────────────┐
                    │   Form Peminjaman    │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Input Data:          │
                    │ - Mahasiswa          │
                    │ - Dosen              │
                    │ - Laboratorium       │
                    │ - Kunci             │
                    │ - Jam Pinjam         │
                    │ - Keperluan          │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Cek Ketersediaan     │
                    │ Status Kunci         │
                    └──────────┬───────────┘
                    ┌──────────┴───────────┐
                    │   TERSEDIA?          │
                    └──────────┬───────────┘
                    ┌──────────┴───────────┐
                    │ YA                   │ TIDAK
                    ▼                      ▼
          ┌──────────────────┐  ┌──────────────────┐
          │ Status → Dipinjam│  │Tampilkan Pesan   │
          │ Simpan ke TB     │  │Kunci Tidak       │
          │Peminjaman        │  │Tersedia          │
          │ Tampilkan Sukses │  │                  │
          └──────────────────┘  └──────────────────┘
```

### 2.3 Flowchart Detail Pengembalian

```
                    ┌──────────────────────┐
                    │   Menu Pengembalian  │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Tampilkan Daftar     │
                    │ Peminjaman Aktif     │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Cari/Pilih Data      │
                    │ Peminjaman           │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Tampilkan Detail     │
                    │ & Konfirmasi         │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Input Jam Kembali    │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Status Kunci →       │
                    │ Tersedia             │
                    │ Status Peminjaman →  │
                    │ Dikembalikan         │
                    │ Update Tgl Kembali   │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Tampilkan Notifikasi │
                    │ Sukses               │
                    └──────────────────────┘
```

---

## 3. USE CASE DIAGRAM

### 3.1 Diagram Use Case

```
                      ┌─────────────────────────────────────┐
                      │  SISTEM PEMINJAMAN KUNCI LAB        │
                      └─────────────────────────────────────┘
                                      │
       ┌──────────────────────────────┼──────────────────────────────┐
       │                              │                              │
       │  ┌─────────────────────┐     │                              │
       │  │ UC-01: Login        │     │                              │
       │  ├─────────────────────┤     │                              │
       │  │ UC-02: Dashboard    │     │                              │
       │  ├─────────────────────┤     │                              │
       │  │ UC-03: Kelola Mhs   │     │                              │
       │  ├─────────────────────┤     │                              │
       │  │ UC-04: Kelola Lab   │     │                              │
       │  ├─────────────────────┤     │                              │
       │  │ UC-05: Kelola Kunci │     │                              │
       │  ├─────────────────────┤     │                              │
       │  │ UC-06: Kelola Dosen │     │                              │
       │  ├─────────────────────┤     │                              │
       │  │ UC-07: Peminjaman   ├─────┼──────► «include» UC-07a      │
       │  ├─────────────────────┤     │         Validasi Ketersediaan│
       │  │ UC-08: Pengembalian ├─────┼──────► «include» UC-08a      │
       │  ├─────────────────────┤     │         Update Status Kunci  │
       │  │ UC-09: Riwayat      │     │                              │
       │  ├─────────────────────┤     │                              │
       │  │ UC-10: Cari Data    ├─────┼──────► «extend» By NIM/Nama  │
       │  ├─────────────────────┤     │                  /No. Kunci  │
       │  │ UC-11: Laporan      │     │                              │
       │  ├─────────────────────┤     │                              │
       │  │ UC-12: Logout       │     │                              │
       │  └─────────────────────┘     │                              │
       │                              │                              │
       └──────────────────────────────┘
                                      │
                              ┌───────┴───────┐
                              │ Admin/Laboran │
                              └───────────────┘
```

### 3.2 Deskripsi Use Case

| Kode | Use Case | Aktor | Deskripsi |
|------|----------|-------|-----------|
| UC-01 | Login | Admin/Laboran | Autentikasi pengguna dengan username dan password |
| UC-02 | Dashboard | Admin/Laboran | Melihat statistik kunci dan aktivitas terbaru |
| UC-03 | Kelola Mahasiswa | Admin/Laboran | CRUD data mahasiswa (tambah, lihat, edit, hapus) |
| UC-04 | Kelola Lab | Admin/Laboran | CRUD data laboratorium |
| UC-05 | Kelola Kunci | Admin/Laboran | CRUD data kunci dengan relasi laboratorium |
| UC-06 | Kelola Dosen | Admin/Laboran | CRUD data dosen |
| UC-07 | Peminjaman Kunci | Admin/Laboran | Mencatat peminjaman dengan validasi ketersediaan otomatis |
| UC-07a | Validasi Ketersediaan | Sistem | Mengecek status kunci sebelum peminjaman |
| UC-08 | Pengembalian Kunci | Admin/Laboran | Mencatat pengembalian dan update status kunci |
| UC-08a | Update Status Kunci | Sistem | Mengubah status kunci menjadi Tersedia |
| UC-09 | Riwayat | Admin/Laboran | Melihat seluruh riwayat peminjaman |
| UC-10 | Cari Data | Admin/Laboran | Mencari data peminjaman berdasarkan NIM/Nama/No Kunci |
| UC-11 | Laporan | Admin/Laboran | Membuat laporan peminjaman dengan filter dan export |
| UC-12 | Logout | Admin/Laboran | Keluar dari sistem |

---

## 4. ACTIVITY DIAGRAM

### 4.1 Activity Diagram Login

```
┌──────────┐          ┌──────────────────┐          ┌─────────────┐
│  Admin/  │          │   Sistem         │          │  Database   │
│  Laboran │          │                  │          │             │
└─────┬────┘          └────────┬─────────┘          └──────┬──────┘
      │                        │                          │
      ├── Buka Aplikasi ───────►                          │
      │                        │                          │
      │◄── Tampilkan Form ─────┤                          │
      │                        │                          │
      ├── Input Username/Pass ─►                          │
      │                        │                          │
      │                        ├── Validasi ──────────────►│
      │                        │                          │
      │                        │◄── Result ───────────────┤
      │                        │                          │
      │       ┌────────────────┴──────────────┐           │
      │       │      Apakah Valid?            │           │
      │       └────────┬──────────┬───────────┘           │
      │           VALID           TIDAK VALID             │
      │                ▼                ▼                 │
      │                │                │                 │
      │◄── Redirect ───┤                │                 │
      │   ke Dashboard  │                │                 │
      │                │   ◄── Tampilkan ──┤              │
      │                │        Error     │               │
      │                │                │                 │
      ▼                ▼                ▼                 ▼
```

### 4.2 Activity Diagram Peminjaman

```
┌──────────┐          ┌──────────────────┐          ┌─────────────┐
│  Admin/  │          │   Sistem         │          │  Database   │
│  Laboran │          │                  │          │             │
└─────┬────┘          └────────┬─────────┘          └──────┬──────┘
      │                        │                          │
      ├── Pilih Menu ──────────►                          │
      │   Peminjaman            │                          │
      │                        │                          │
      │                        ├── Load Data Referensi ──►│
      │                        │   Mhs, Dosen, Lab, Kunci │
      │                        │◄── Data ─────────────────┤
      │                        │                          │
      │◄── Tampilkan Form ─────┤                          │
      │                        │                          │
      ├── Isi Form ────────────►                          │
      │                        │                          │
      │                        ├── Cek Status Kunci ─────►│
      │                        │                          │
      │                        │◄── Result ───────────────┤
      │                        │                          │
      │       ┌────────────────┴──────────────┐           │
      │       │         Tersedia?             │           │
      │       └────────┬──────────┬───────────┘           │
      │            YA             TIDAK                    │
      │                ▼                ▼                 │
      │                │                │                 │
      │                ├── Simpan ───────►                │
      │                │   Peminjaman     │                │
      │                ├── Update Status ─►               │
      │                │   Kunci → Dipinjam               │
      │                │                  │                │
      │◄── Notif ──────┤   ◄── Tampilkan ──┤              │
      │   Sukses       │        Error     │               │
      │                │                │                 │
      ▼                ▼                ▼                 ▼
```

### 4.3 Activity Diagram Pengembalian

```
┌──────────┐          ┌──────────────────┐          ┌─────────────┐
│  Admin/  │          │   Sistem         │          │  Database   │
│  Laboran │          │                  │          │             │
└─────┬────┘          └────────┬─────────┘          └──────┬──────┘
      │                        │                          │
      ├── Pilih Menu ──────────►                          │
      │   Pengembalian          │                          │
      │                        │                          │
      │                        ├── Load Peminjaman ───────►│
      │                        │   Aktif                   │
      │                        │◄── Data ─────────────────┤
      │                        │                          │
      │◄── Tampilkan Daftar ───┤                          │
      │                        │                          │
      ├── Pilih Data ──────────►                          │
      │                        │                          │
      │◄── Tampilkan Detail ───┤                          │
      │                        │                          │
      ├── Konfirmasi ──────────►                          │
      │                        │                          │
      │                        ├── Update Peminjaman ─────►│
      │                        │   Status → Dikembalikan  │
      │                        ├── Update Kunci ──────────►│
      │                        │   Status → Tersedia      │
      │                        │                          │
      │◄── Notif Sukses ───────┤                          │
      │                        │                          │
      ▼                        ▼                          ▼
```

---

## 5. SEQUENCE DIAGRAM

### 5.1 Sequence Diagram Login

```
Admin/Laboran         View Login           AuthService          Database
      │                    │                    │                  │
      │  Akses Halaman     │                    │                  │
      ├───────────────────►│                    │                  │
      │                    │                    │                  │
      │  Tampilkan Form    │                    │                  │
      │◄───────────────────┤                    │                  │
      │                    │                    │                  │
      │  Input User & Pass │                    │                  │
      ├───────────────────►│                    │                  │
      │                    │   authenticate()   │                  │
      │                    ├───────────────────►│                  │
      │                    │                    │  check_credentials│
      │                    │                    ├─────────────────►│
      │                    │                    │                  │
      │                    │                    │◄─────────────────┤
      │                    │◄───────────────────┤   Result         │
      │◄───────────────────┤                    │                  │
      │  Sukses/Gagal      │                    │                  │
```

### 5.2 Sequence Diagram Peminjaman

```
Admin/Laboran      PeminjamanView     PeminjamanService     KeyService      Database
      │                    │                   │                │              │
      │  Buka Form         │                   │                │              │
      ├───────────────────►│                   │                │              │
      │                    │                   │                │              │
      │  Load Referensi    │                   │                │              │
      │◄───────────────────┤                   │                │              │
      │                    │                   │                │              │
      │  Kirim Data        │                   │                │              │
      ├───────────────────►│                   │                │              │
      │                    │                   │                │              │
      │                    │  check_available()│                │              │
      │                    ├──────────────────────────────────►│              │
      │                    │                   │                │              │
      │                    │                   │  get_status()  │              │
      │                    │                   │               ├─────────────►│
      │                    │                   │               │◄─────────────┤
      │                    │                   │◄──────────────┤              │
      │                    │◄──────────────────┤                │              │
      │                    │                   │                │              │
      │ ┌─── alt: Tersedia │                   │                │              │
      │ │                  │                   │                │              │
      │ │                  │  create_pinjam()  │                │              │
      │ │                  ├──────────────────►│                │              │
      │ │                  │                   │  update_status │              │
      │ │                  │                   ├───────────────►│              │
      │ │                  │                   │                ├─────────────►│
      │ │                  │◄──────────────────┤                │◄─────────────┤
      │ │                  │                   │                │              │
      │ │ Notif Sukses     │                   │                │              │
      │ │◄─────────────────┤                   │                │              │
      │ │                  │                   │                │              │
      │ └─── alt: Tidak    │                   │                │              │
      │   │                │                   │                │              │
      │   │ Notif Error    │                   │                │              │
      │   │◄───────────────┤                   │                │              │
```

### 5.3 Sequence Diagram Pengembalian

```
Admin/Laboran      PengembalianView      PeminjamanService       Database
      │                    │                     │                  │
      │  Buka Menu         │                     │                  │
      ├───────────────────►│                     │                  │
      │                    │                     │                  │
      │                    │  get_active_loans() │                  │
      │                    ├────────────────────►│                  │
      │                    │                     ├─────────────────►│
      │                    │                     │◄─────────────────┤
      │                    │◄────────────────────┤                  │
      │  Tampilkan Daftar  │                     │                  │
      │◄───────────────────┤                     │                  │
      │                    │                     │                  │
      │  Pilih Data        │                     │                  │
      ├───────────────────►│                     │                  │
      │                    │                     │                  │
      │  Tampilkan Detail  │                     │                  │
      │◄───────────────────┤                     │                  │
      │                    │                     │                  │
      │  Konfirmasi        │                     │                  │
      ├───────────────────►│                     │                  │
      │                    │                     │                  │
      │                    │  return_key()       │                  │
      │                    ├────────────────────►│                  │
      │                    │                     │                  │
      │                    │                     │ update loan      │
      │                    │                     ├─────────────────►│
      │                    │                     │                  │
      │                    │                     │ update key       │
      │                    │                     │ status → Tersedia│
      │                    │                     ├─────────────────►│
      │                    │◄────────────────────┤                  │
      │  Notif Sukses      │                     │                  │
      │◄───────────────────┤                     │                  │
```

---

## 6. ERD DATABASE

### Entity Relationship Diagram

```
┌─────────────────┐       ┌──────────────────────┐
│   Mahasiswa     │       │   Kunci              │
├─────────────────┤       ├──────────────────────┤
│ PK id           │       │ PK id                │
│ nim (unique)    │       │ FK id_lab            │
│ nama            │       │ nomor_kunci          │
│ program_studi   │       │ status               │
│ created_at      │       │   (Tersedia/         │
│ updated_at      │       │    Dipinjam)         │
└────────┬────────┘       │ created_at           │
         │                │ updated_at           │
         │ 1              └────────┬─────────────┘
         │                        │ N
         │                        │
         │ N              ┌───────┴───────┐
         │                │ Laboratorium  │
         │                ├───────────────┤
         ▼                │ PK id         │
┌─────────────────┐       │ kode_lab(uniq)│
│   Peminjaman    │       │ nama_lab      │
├─────────────────┤       │ gedung        │
│ PK id           │       │ lantai        │
│ FK id_mahasiswa │       │ created_at    │
│ FK id_dosen     │       │ updated_at    │
│ FK id_kunci     │       └───────────────┘
│ FK id_lab       │
│ tanggal_pinjam  │
│ jam_pinjam      │
│ tanggal_kembali │
│ jam_kembali     │
│ keperluan       │
│ status          │
│   (Dipinjam/    │
│    Dikembalikan)│
│ created_at      │
│ updated_at      │
└─────────────────┘
         ▲
         │
         │ 1
┌────────┴────────┐
│    Dosen        │
├─────────────────┤
│ PK id           │
│ nip (unique)    │
│ nama            │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

### Detail Entitas

**Mahasiswa**
| Kolom | Tipe Data | Keterangan |
|-------|-----------|------------|
| id | BigAutoField (PK) | Primary key |
| nim | CharField(20), Unique | Nomor Induk Mahasiswa |
| nama | CharField(100) | Nama lengkap |
| program_studi | CharField(100) | Program studi |
| created_at | DateTimeField(auto_now_add) | Waktu dibuat |
| updated_at | DateTimeField(auto_now) | Waktu diupdate |

**Dosen**
| Kolom | Tipe Data | Keterangan |
|-------|-----------|------------|
| id | BigAutoField (PK) | Primary key |
| nip | CharField(30), Unique | Nomor Induk Pegawai |
| nama | CharField(100) | Nama lengkap |
| created_at | DateTimeField(auto_now_add) | Waktu dibuat |
| updated_at | DateTimeField(auto_now) | Waktu diupdate |

**Laboratorium**
| Kolom | Tipe Data | Keterangan |
|-------|-----------|------------|
| id | BigAutoField (PK) | Primary key |
| kode_lab | CharField(20), Unique | Kode laboratorium |
| nama_lab | CharField(100) | Nama laboratorium |
| gedung | CharField(50) | Nama gedung |
| lantai | CharField(10) | Lantai |
| created_at | DateTimeField(auto_now_add) | Waktu dibuat |
| updated_at | DateTimeField(auto_now) | Waktu diupdate |

**Kunci**
| Kolom | Tipe Data | Keterangan |
|-------|-----------|------------|
| id | BigAutoField (PK) | Primary key |
| laboratorium | ForeignKey → Laboratorium | Relasi ke lab |
| nomor_kunci | CharField(20) | Nomor identitas kunci |
| status | CharField(20), Choises | 'Tersedia' / 'Dipinjam' |
| created_at | DateTimeField(auto_now_add) | Waktu dibuat |
| updated_at | DateTimeField(auto_now) | Waktu diupdate |

**Peminjaman**
| Kolom | Tipe Data | Keterangan |
|-------|-----------|------------|
| id | BigAutoField (PK) | Primary key |
| mahasiswa | ForeignKey → Mahasiswa | Peminjam |
| dosen | ForeignKey → Dosen | Dosen pengampu |
| laboratorium | ForeignKey → Laboratorium | Lab tujuan |
| kunci | ForeignKey → Kunci | Kunci yang dipinjam |
| tanggal_pinjam | DateField(auto_now_add) | Tanggal pinjam |
| jam_pinjam | TimeField | Jam pinjam |
| tanggal_kembali | DateField(null) | Tanggal kembali |
| jam_kembali | TimeField(null) | Jam kembali |
| keperluan | TextField | Tujuan peminjaman |
| status | CharField(20), Choises | 'Dipinjam' / 'Dikembalikan' |
| created_at | DateTimeField(auto_now_add) | Waktu dibuat |
| updated_at | DateTimeField(auto_now) | Waktu diupdate |

---

## 7. RELASI TABEL

| Tabel 1 | Tabel 2 | Tipe Relasi | Foreign Key | Penjelasan |
|---------|---------|-------------|-------------|------------|
| Laboratorium | Kunci | One to Many | `kunci.laboratorium_id` → `laboratorium.id` | Satu laboratorium dapat memiliki banyak kunci |
| Kunci | Peminjaman | One to Many | `peminjaman.kunci_id` → `kunci.id` | Satu kunci dapat dipinjam berkali-kali |
| Mahasiswa | Peminjaman | One to Many | `peminjaman.mahasiswa_id` → `mahasiswa.id` | Satu mahasiswa dapat meminjam berkali-kali |
| Dosen | Peminjaman | One to Many | `peminjaman.dosen_id` → `dosen.id` | Satu dosen dapat terkait banyak peminjaman |
| Laboratorium | Peminjaman | One to Many | `peminjaman.laboratorium_id` → `laboratorium.id` | Satu lab dapat dipinjam berkali-kali |

---

## 8. STRUKTUR FOLDER PROJECT

```
sistem-peminjaman-kunci-lab/
│
├── manage.py                          # Entry point Django CLI
├── requirements.txt                   # Dependensi Python
├── .env                               # Environment variables (gitignored)
├── .gitignore                         # Git ignore rules
├── README.md                          # Dokumentasi proyek
├── DOKUMEN_PERENCANAAN.md             # Dokumen perencanaan ini
│
├── config/                            # Konfigurasi Django
│   ├── __init__.py
│   ├── asgi.py                        # ASGI config
│   ├── settings.py                    # Settings utama
│   ├── urls.py                        # Root URLConf
│   └── wsgi.py                        # WSGI config
│
├── apps/                              # Kumpulan aplikasi Django
│   ├── __init__.py
│   │
│   ├── authentication/                # App Login/Logout
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── dashboard/                     # App Dashboard
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── master_data/                   # App CRUD Master Data
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py                  # Mahasiswa, Dosen, Lab, Kunci
│   │   ├── urls.py
│   │   ├── views.py                   # Class-Based Views
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── seed_data.py       # Command isi data awal
│   │   └── migrations/
│   │       └── 0001_initial.py
│   │
│   ├── transaction/                   # App Transaksi
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── filters.py                 # FilterSet untuk pencarian
│   │   ├── forms.py
│   │   ├── models.py                  # Peminjaman
│   │   ├── services.py                # Business logic layer
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── cleanup_old_records.py  # Hapus record > 30 hari
│   │   └── migrations/
│   │       └── 0001_initial.py
│   │
│   └── report/                        # App Laporan
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── urls.py
│       └── views.py                   # Filter + Export Excel/CSV
│
├── static/                            # File statis
│   ├── css/
│   │   └── style.css                  # Custom CSS
│   ├── js/
│   │   └── main.js                    # Custom JS
│   └── images/
│
├── templates/                         # Template HTML
│   ├── base.html                      # Template utama (navbar + content)
│   ├── base_auth.html                 # Template khusus login
│   ├── 404.html                       # Halaman error 404
│   ├── 500.html                       # Halaman error 500
│   ├── 403.html                       # Halaman error 403
│   │
│   ├── authentication/
│   │   └── login.html
│   │
│   ├── dashboard/
│   │   └── index.html
│   │
│   ├── master_data/
│   │   ├── mahasiswa_list.html
│   │   ├── mahasiswa_form.html
│   │   ├── dosen_list.html
│   │   ├── dosen_form.html
│   │   ├── laboratorium_list.html
│   │   ├── laboratorium_form.html
│   │   ├── kunci_list.html
│   │   ├── kunci_form.html
│   │   └── confirm_delete.html
│   │
│   ├── transaction/
│   │   ├── peminjaman_form.html
│   │   ├── pengembalian_list.html
│   │   ├── pengembalian_confirm.html
│   │   └── riwayat_list.html
│   │
│   └── report/
│       └── laporan.html
│
├── media/                             # File upload (kosong)
│
└── db.sqlite3                         # Database development (gitignored)
```

---

## 9. DAFTAR MODEL DJANGO

### 9.1 Model Mahasiswa

```python
from django.db import models

class Mahasiswa(models.Model):
    nim = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=100)
    program_studi = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Mahasiswa"
        ordering = ['nama']

    def __str__(self):
        return f"{self.nama} ({self.nim})"
```

### 9.2 Model Dosen

```python
class Dosen(models.Model):
    nip = models.CharField(max_length=30, unique=True)
    nama = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Dosen"
        ordering = ['nama']

    def __str__(self):
        return f"{self.nama} ({self.nip})"
```

### 9.3 Model Laboratorium

```python
class Laboratorium(models.Model):
    kode_lab = models.CharField(max_length=20, unique=True)
    nama_lab = models.CharField(max_length=100)
    gedung = models.CharField(max_length=50, blank=True)
    lantai = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Laboratorium"
        ordering = ['kode_lab']

    def __str__(self):
        return f"{self.kode_lab} - {self.nama_lab}"
```

### 9.4 Model Kunci

```python
class Kunci(models.Model):
    STATUS_CHOICES = [
        ('Tersedia', 'Tersedia'),
        ('Dipinjam', 'Dipinjam'),
    ]

    laboratorium = models.ForeignKey(
        Laboratorium, on_delete=models.CASCADE, related_name='kunci'
    )
    nomor_kunci = models.CharField(max_length=20)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Tersedia'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Kunci"
        unique_together = ['laboratorium', 'nomor_kunci']
        ordering = ['laboratorium', 'nomor_kunci']

    def __str__(self):
        return f"Kunci {self.nomor_kunci} - {self.laboratorium.kode_lab}"
```

### 9.5 Model Peminjaman

```python
class Peminjaman(models.Model):
    STATUS_CHOICES = [
        ('Dipinjam', 'Dipinjam'),
        ('Dikembalikan', 'Dikembalikan'),
    ]

    mahasiswa = models.ForeignKey(
        Mahasiswa, on_delete=models.CASCADE, related_name='peminjaman'
    )
    dosen = models.ForeignKey(
        Dosen, on_delete=models.CASCADE, related_name='peminjaman'
    )
    laboratorium = models.ForeignKey(
        Laboratorium, on_delete=models.CASCADE, related_name='peminjaman'
    )
    kunci = models.ForeignKey(
        Kunci, on_delete=models.CASCADE, related_name='peminjaman'
    )
    tanggal_pinjam = models.DateField(auto_now_add=True)
    jam_pinjam = models.TimeField()
    tanggal_kembali = models.DateField(null=True, blank=True)
    jam_kembali = models.TimeField(null=True, blank=True)
    keperluan = models.TextField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Dipinjam'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Peminjaman"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.mahasiswa.nama} - {self.kunci} ({self.tanggal_pinjam})"
```

---

## 10. DAFTAR URL / ROUTE

### Root URLConf (`config/urls.py`)

| URL Prefix | App | File Tujuan |
|-----------|-----|-------------|
| `/` | authentication | `apps/authentication/urls.py` |
| `/dashboard/` | dashboard | `apps/dashboard/urls.py` |
| `/master/` | master_data | `apps/master_data/urls.py` |
| `/transaksi/` | transaction | `apps/transaction/urls.py` |
| `/laporan/` | report | `apps/report/urls.py` |
| `/admin/` | django.contrib.admin | - |

### Authentication URLs

| Method | URL | View Name | Fungsi |
|--------|-----|-----------|--------|
| GET/POST | `/` | `login` | Login admin/laboran |
| GET | `/logout/` | `logout` | Logout dan redirect |

### Dashboard URLs

| Method | URL | View Name | Fungsi |
|--------|-----|-----------|--------|
| GET | `/dashboard/` | `dashboard` | Tampilkan statistik dashboard |

### Master Data URLs

| Method | URL | View Name | Fungsi |
|--------|-----|-----------|--------|
| GET | `/master/mahasiswa/` | `mahasiswa_list` | Daftar mahasiswa |
| GET/POST | `/master/mahasiswa/tambah/` | `mahasiswa_create` | Tambah mahasiswa |
| GET/POST | `/master/mahasiswa/edit/<pk>/` | `mahasiswa_update` | Edit mahasiswa |
| POST | `/master/mahasiswa/hapus/<pk>/` | `mahasiswa_delete` | Hapus mahasiswa |
| GET | `/master/dosen/` | `dosen_list` | Daftar dosen |
| GET/POST | `/master/dosen/tambah/` | `dosen_create` | Tambah dosen |
| GET/POST | `/master/dosen/edit/<pk>/` | `dosen_update` | Edit dosen |
| POST | `/master/dosen/hapus/<pk>/` | `dosen_delete` | Hapus dosen |
| GET | `/master/laboratorium/` | `laboratorium_list` | Daftar lab |
| GET/POST | `/master/laboratorium/tambah/` | `laboratorium_create` | Tambah lab |
| GET/POST | `/master/laboratorium/edit/<pk>/` | `laboratorium_update` | Edit lab |
| POST | `/master/laboratorium/hapus/<pk>/` | `laboratorium_delete` | Hapus lab |
| GET | `/master/kunci/` | `kunci_list` | Daftar kunci |
| GET/POST | `/master/kunci/tambah/` | `kunci_create` | Tambah kunci |
| GET/POST | `/master/kunci/edit/<pk>/` | `kunci_update` | Edit kunci |
| POST | `/master/kunci/hapus/<pk>/` | `kunci_delete` | Hapus kunci |

### Transaction URLs

| Method | URL | View Name | Fungsi |
|--------|-----|-----------|--------|
| GET/POST | `/transaksi/peminjaman/` | `peminjaman_create` | Form peminjaman |
| GET | `/transaksi/pengembalian/` | `pengembalian_list` | Daftar peminjaman aktif |
| GET/POST | `/transaksi/pengembalian/<pk>/` | `pengembalian_process` | Proses pengembalian |
| GET | `/transaksi/riwayat/` | `riwayat_list` | Riwayat peminjaman |
| GET | `/transaksi/api/get-mahasiswa/` | `get_mahasiswa` | API AJAX cari mahasiswa |
| GET | `/transaksi/api/get-kunci/` | `get_kunci` | API AJAX filter kunci |
| GET | `/transaksi/cari/` | `search` | API JSON pencarian |

### Report URLs

| Method | URL | View Name | Fungsi |
|--------|-----|-----------|--------|
| GET | `/laporan/` | `report_index` | Laporan dengan filter |
| GET | `/laporan/export/excel/` | `report_export_excel` | Export Excel (.xlsx) |
| GET | `/laporan/export/csv/` | `report_export_csv` | Export CSV |

---

## 11. DAFTAR VIEW

### Authentication Views

| View | Method | URL | Kelas/Fungsi | Deskripsi |
|------|--------|-----|--------------|-----------|
| `login_view` | GET/POST | `/` | Fungsi | Form login + validasi |
| `logout_view` | GET | `/logout/` | Fungsi | Logout user |

### Dashboard Views

| View | Method | URL | Kelas/Fungsi | Deskripsi |
|------|--------|-----|--------------|-----------|
| `index` | GET | `/dashboard/` | Fungsi | Statistik + aktivitas terbaru |

### Master Data Views

| View | Method | URL | Kelas/Fungsi | Deskripsi |
|------|--------|-----|--------------|-----------|
| `MahasiswaListView` | GET | `/master/mahasiswa/` | ListView | List + search + pagination |
| `MahasiswaCreateView` | GET/POST | `/master/mahasiswa/tambah/` | CreateView | Form tambah |
| `MahasiswaUpdateView` | GET/POST | `/master/mahasiswa/edit/<pk>/` | UpdateView | Form edit |
| `MahasiswaDeleteView` | POST | `/master/mahasiswa/hapus/<pk>/` | DeleteView | Hapus + cancel_url |
| `DosenListView` | GET | `/master/dosen/` | ListView | List + search |
| `DosenCreateView` | GET/POST | `/master/dosen/tambah/` | CreateView | Form tambah |
| `DosenUpdateView` | GET/POST | `/master/dosen/edit/<pk>/` | UpdateView | Form edit |
| `DosenDeleteView` | POST | `/master/dosen/hapus/<pk>/` | DeleteView | Hapus |
| `LaboratoriumListView` | GET | `/master/laboratorium/` | ListView | List + search |
| `LaboratoriumCreateView` | GET/POST | `/master/laboratorium/tambah/` | CreateView | Form tambah |
| `LaboratoriumUpdateView` | GET/POST | `/master/laboratorium/edit/<pk>/` | UpdateView | Form edit |
| `LaboratoriumDeleteView` | POST | `/master/laboratorium/hapus/<pk>/` | DeleteView | Hapus |
| `KunciListView` | GET | `/master/kunci/` | ListView | List + filter lab + search |
| `KunciCreateView` | GET/POST | `/master/kunci/tambah/` | CreateView | Form tambah |
| `KunciUpdateView` | GET/POST | `/master/kunci/edit/<pk>/` | UpdateView | Form edit |
| `KunciDeleteView` | POST | `/master/kunci/hapus/<pk>/` | DeleteView | Hapus |

### Transaction Views

| View | Method | URL | Kelas/Fungsi | Deskripsi |
|------|--------|-----|--------------|-----------|
| `peminjaman_create` | GET/POST | `/transaksi/peminjaman/` | Fungsi | Form + service layer |
| `get_mahasiswa` | GET | `/transaksi/api/get-mahasiswa/` | Fungsi | AJAX JSON |
| `get_kunci` | GET | `/transaksi/api/get-kunci/` | Fungsi | AJAX JSON |
| `pengembalian_list` | GET | `/transaksi/pengembalian/` | Fungsi | Daftar peminjaman aktif |
| `pengembalian_process` | GET/POST | `/transaksi/pengembalian/<pk>/` | Fungsi | Proses pengembalian |
| `riwayat_list` | GET | `/transaksi/riwayat/` | Fungsi | Riwayat + pagination |
| `search` | GET | `/transaksi/cari/` | Fungsi | API JSON search |

### Report Views

| View | Method | URL | Kelas/Fungsi | Deskripsi |
|------|--------|-----|--------------|-----------|
| `laporan_view` | GET | `/laporan/` | Fungsi | Filter + pagination |
| `export_excel` | GET | `/laporan/export/excel/` | Fungsi | Download .xlsx |
| `export_csv` | GET | `/laporan/export/csv/` | Fungsi | Download .csv |

---

## 12. RANCANGAN DASHBOARD

```
┌─────────────────────────────────────────────────────────────────────────┐
│  [Kunci Lab]  Dashboard  Master Data ▾  Peminjaman  Pengembalian       │
│  Riwayat  Laporan                                    [Admin ▾]         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐│
│  │   🔑 Total   │  │   ✅ Tersedia│  │   ❌ Dipinjam │  │  📅 Hari Ini ││
│  │    Kunci     │  │              │  │              │  │              ││
│  │     50       │  │     35       │  │     15       │  │     12       ││
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘│
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │  📋 Aktivitas Terbaru                                               ││
│  ├─────────────────────────────────────────────────────────────────────┤│
│  │  # │ Mahasiswa      │ Kunci  │ Lab    │ Jam Pinjam │ Status        ││
│  ├────┼────────────────┼────────┼────────┼────────────┼───────────────││
│  │  1 │ Andi Pratama   │ KC-001 │ LAB-01 │ 08:00      │ ⚠️ Dipinjam   ││
│  │  2 │ Budi Santoso   │ KC-002 │ LAB-02 │ 09:30      │ ✅ Dikembalikan││
│  │  3 │ Cici Dewi      │ KC-003 │ LAB-01 │ 10:00      │ ⚠️ Dipinjam   ││
│  └─────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────┘

Komponen:
1. Navbar utama dengan menu navigasi lengkap
2. 4 kartu statistik (Total, Tersedia, Dipinjam, Hari Ini)
3. Tabel aktivitas 10 peminjaman terbaru
4. Status badge: bg-success (Dikembalikan), bg-warning (Dipinjam)
```

---

## 13. RANCANGAN HALAMAN LOGIN

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                                                                         │
│                    ┌─────────────────────────────────────┐              │
│                    │                                     │              │
│                    │           🔐  SISTEM               │              │
│                    │         PEMINJAMAN KUNCI            │              │
│                    │          LABORATORIUM               │              │
│                    │                                     │              │
│                    │  ┌──────────────────────────────┐   │              │
│                    │  │ Username                     │   │              │
│                    │  └──────────────────────────────┘   │              │
│                    │                                     │              │
│                    │  ┌──────────────────────────────┐   │              │
│                    │  │ Password                     │   │              │
│                    │  └──────────────────────────────┘   │              │
│                    │                                     │              │
│                    │  ┌──────────────────────────────┐   │              │
│                    │  │       🔑  MASUK              │   │              │
│                    │  └──────────────────────────────┘   │              │
│                    │                                     │              │
│                    └─────────────────────────────────────┘              │
│                                                                         │
│                                     © 2026 - Laboratorium               │
└─────────────────────────────────────────────────────────────────────────┘

Karakteristik:
- Card di tengah layar dengan shadow
- Icon kunci di header
- Input username dan password (type=password)
- Tombol submit full-width
- Alert error jika gagal login
- Menggunakan template base_auth.html (tanpa navbar)
```

---

## 14. RANCANGAN HALAMAN DATA MAHASISWA

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Dashboard  ▸  Data Mahasiswa                        [+ Tambah]        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │  Cari: [............................]  [🔍 Cari]  [Reset]           ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │  # │ NIM        │ Nama              │ Program Studi     │ Aksi     ││
│  ├────┼────────────┼───────────────────┼───────────────────┼──────────││
│  │  1 │ 2201001    │ Andi Pratama      │ Informatika       │ ✏️ 🗑️   ││
│  │  2 │ 2201002    │ Budi Santoso      │ Sistem Informasi  │ ✏️ 🗑️   ││
│  │  3 │ 2201003    │ Cici Dewi Lestari │ Teknik Komputer   │ ✏️ 🗑️   ││
│  │  4 │ 2201004    │ Dadang Hermawan   │ Informatika       │ ✏️ 🗑️   ││
│  │  5 │ 2201005    │ Eka Putri Rahayu  │ Sistem Informasi  │ ✏️ 🗑️   ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│  Menampilkan 1-5 dari 12 data         [◀ 1 2 3 ▶]                      │
└─────────────────────────────────────────────────────────────────────────┘

Fitur:
- Pencarian berdasarkan NIM atau Nama
- Pagination (10 data per halaman)
- Tombol Tambah, Edit (icon pensil), Hapus (icon tong sampah)
- Konfirmasi hapus dengan modal/page terpisah
```

---

## 15. RANCANGAN HALAMAN DATA LABORATORIUM

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Dashboard  ▸  Data Laboratorium                    [+ Tambah Lab]     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │  Cari: [............................]  [🔍 Cari]  [Reset]           ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │  # │ Kode Lab  │ Nama Lab          │ Gedung  │ Lantai │ Aksi      ││
│  ├────┼───────────┼───────────────────┼─────────┼────────┼───────────││
│  │  1 │ LAB-01    │ Lab Komputer 1    │ A       │ 2      │ ✏️ 🗑️    ││
│  │  2 │ LAB-02    │ Lab Jaringan      │ A       │ 3      │ ✏️ 🗑️    ││
│  │  3 │ LAB-03    │ Lab Multimedia    │ B       │ 1      │ ✏️ 🗑️    ││
│  │  4 │ LAB-04    │ Lab Hardware      │ B       │ 2      │ ✏️ 🗑️    ││
│  │  5 │ LAB-05    │ Lab RPL           │ C       │ 1      │ ✏️ 🗑️    ││
│  └─────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 16. RANCANGAN HALAMAN DATA KUNCI

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Dashboard  ▸  Data Kunci                            [+ Tambah Kunci]  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │  Filter Lab: [📂 Semua Lab ▾]  Cari: [........]  [Filter] [Reset]  ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │  # │ No. Kunci  │ Laboratorium      │ Status            │ Aksi     ││
│  ├────┼────────────┼───────────────────┼───────────────────┼──────────││
│  │  1 │ LAB-01-K01 │ LAB-01-Lab Komp 1│ ✅ Tersedia       │ ✏️ 🗑️   ││
│  │  2 │ LAB-01-K02 │ LAB-01-Lab Komp 1│ ⚠️ Dipinjam       │ ✏️ 🗑️   ││
│  │  3 │ LAB-02-K01 │ LAB-02-Lab Jar   │ ✅ Tersedia       │ ✏️ 🗑️   ││
│  │  4 │ LAB-02-K02 │ LAB-02-Lab Jar   │ ✅ Tersedia       │ ✏️ 🗑️   ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│  Badge Status: ✅ Tersedia = bg-success  ⚠️ Dipinjam = bg-warning      │
└─────────────────────────────────────────────────────────────────────────┘

Fitur khusus:
- Filter dropdown berdasarkan laboratorium
- Status badge dengan warna berbeda
- Unique constraint: nomor_kunci + laboratorium
```

---

## 17. RANCANGAN HALAMAN PEMINJAMAN

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Dashboard  ▸  Peminjaman Kunci                                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │  FORM PEMINJAMAN KUNCI LABORATORIUM                                 ││
│  │                                                                     ││
│  │  ┌──────────────────────────────┐  ┌──────────────────────────────┐ ││
│  │  │ 👤 Mahasiswa                │  │ 👨‍🏫 Dosen                    │ ││
│  │  │ [📂 Pilih Mahasiswa ▾]      │  │ [📂 Pilih Dosen ▾]           │ ││
│  │  └──────────────────────────────┘  └──────────────────────────────┘ ││
│  │                                                                     ││
│  │  ┌──────────────────────────────┐  ┌──────────────────────────────┐ ││
│  │  │ 🏢 Laboratorium             │  │ 🔑 Kunci                    │ ││
│  │  │ [📂 Pilih Lab ▾]           │  │ [📂 Pilih Lab dulu ▾]       │ ││
│  │  └──────────────────────────────┘  └──────────────────────────────┘ ││
│  │                                                                     ││
│  │  ┌──────────────────────────────┐  ┌──────────────────────────────┐ ││
│  │  │ ⏰ Jam Pinjam               │  │ 📝 Keperluan                │ ││
│  │  │ [  :  ]                     │  │ [........................]   │ ││
│  │  └──────────────────────────────┘  └──────────────────────────────┘ ││
│  │                                                                     ││
│  │                                [🔑 PINJAM KUNCI]  [Batal]          ││
│  └─────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────┘

Logika:
1. Dropdown Kunci hanya menampilkan kunci berstatus "Tersedia"
2. Saat Lab dipilih → AJAX load kunci milik lab tersebut
3. Validasi server-side dengan @transaction.atomic
4. Jika kunci tidak tersedia → tampilkan error, cegah submit
```

---

## 18. RANCANGAN HALAMAN PENGEMBALIAN

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Dashboard  ▸  Pengembalian Kunci                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │  Peminjaman Aktif                                                   ││
│  │  Cari: [............................]  [🔍 Cari]  [Reset]           ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │  # │ Mahasiswa  │ NIM     │ Kunci  │ Lab    │ Jam     │ Aksi      ││
│  ├────┼────────────┼─────────┼────────┼────────┼─────────┼───────────││
│  │  1 │ Andi       │ 2201001 │ KC-001 │ LAB-01 │ 08:00  │ [↩ Kembali]││
│  │  2 │ Cici       │ 2201003 │ KC-003 │ LAB-01 │ 10:00  │ [↩ Kembali]││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│  ┌─ Detail Konfirmasi ─────────────────────────────────────────────────┐│
│  │                                                                     ││
│  │  Mahasiswa  : Andi Pratama (2201001)                                ││
│  │  Prodi      : Informatika                                           ││
│  │  Dosen      : Dr. Ahmad Fauzi, M.Kom.                               ││
│  │  Lab        : LAB-01 - Lab Komputer 1                                ││
│  │  Kunci      : KC-001                                                 ││
│  │  Jam Pinjam : 17/07/2026 08:00                                      ││
│  │  Keperluan  : Praktikum Basis Data                                  ││
│  │                                                                     ││
│  │  ⏰ Jam Kembali : [10:30]                                            ││
│  │                                                                     ││
│  │                    [✓ KONFIRMASI PENGEMBALIAN]  [Batal]             ││
│  └─────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────┘

Proses:
1. Klik "Kembalikan" → tampilkan detail peminjaman
2. Jam kembali default = jam sekarang
3. Konfirmasi → update status kunci = Tersedia
4. Redirect ke daftar dengan notifikasi sukses
```

---

## 19. RANCANGAN HALAMAN RIWAYAT

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Dashboard  ▸  Riwayat Peminjaman                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │  Cari NIM/Nama/No Kunci: [......................]  🔍              ││
│  │  Status: [📂 Semua Status ▾]                                       ││
│  │                    [Cari]  [Reset]                                  ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │ # │ Tgl Pinjam │ Mahasiswa │ Kunci │ Lab │ Jam P │ Jam K │ Status ││
│  ├──┼────────────┼──────────┼──────┼─────┼───────┼───────┼────────││
│  │ 1 │ 17/07/2026 │ Andi     │KC-001│L-01 │ 08:00 │ 10:30 │ ✅     ││
│  │ 2 │ 17/07/2026 │ Budi     │KC-002│L-02 │ 09:00 │ 11:00 │ ✅     ││
│  │ 3 │ 17/07/2026 │ Cici     │KC-003│L-01 │ 10:00 │   -   │ ⚠️     ││
│  │ 4 │ 16/07/2026 │ Dadang   │KC-001│L-01 │ 13:00 │ 15:30 │ ✅     ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│  Menampilkan 1-4 dari 12 data           [◀ 1 2 3 ▶]                    │
└─────────────────────────────────────────────────────────────────────────┘

Fitur:
- Pencarian multi-kriteria (NIM, Nama, No Kunci) via Q objects
- Filter status (Dipinjam / Dikembalikan / Semua)
- Pagination (10 data per halaman)
- Status badge: ✅ Dikembalikan (bg-success), ⚠️ Dipinjam (bg-warning)
- Search dipertahankan saat pindah halaman
```

---

## 20. BEST PRACTICE IMPLEMENTASI DJANGO

### 20.1 Struktur Proyek

Proyek menggunakan struktur **multi-app Django** di mana setiap modul dipisahkan ke dalam app sendiri:

- **authentication** — login/logout
- **dashboard** — halaman utama dengan statistik
- **master_data** — CRUD untuk Mahasiswa, Dosen, Laboratorium, Kunci
- **transaction** — peminjaman, pengembalian, riwayat
- **report** — laporan dan export

### 20.2 Class-Based Views (CBV)

Untuk CRUD master data menggunakan **Class-Based Views** dari Django:

```python
# Contoh penggunaan ListView, CreateView, UpdateView, DeleteView
class MahasiswaListView(LoginRequiredMixin, ListView):
    model = Mahasiswa
    template_name = 'master_data/mahasiswa_list.html'
    context_object_name = 'data'
    paginate_by = 10
```

**Keuntungan CBV:**
- Kode lebih singkat dan terstruktur
- Bawaan Django sudah handle form validation, pagination, konfirmasi delete
- Mudah di-extend dengan mixin seperti `LoginRequiredMixin`

### 20.3 Template Inheritance

Menggunakan sistem template inheritance Django dengan `base.html` sebagai kerangka utama:

```
base.html (navbar + sidebar + messages + scripts)
  ├── base_auth.html (tanpa navbar, untuk login)
  ├── dashboard/index.html
  ├── master_data/*.html
  ├── transaction/*.html
  └── report/laporan.html
```

**Block yang digunakan:**
- `{% block title %}` — judul halaman
- `{% block content %}` — konten utama
- `{% block extra_css %}` — CSS tambahan
- `{% block extra_js %}` — JS tambahan

### 20.4 Service Layer Pattern

Logika bisnis dipisahkan ke dalam **service layer** untuk menjaga views tetap tipis:

```python
# apps/transaction/services.py
class PeminjamanService:
    @staticmethod
    @transaction.atomic
    def pinjam_kunci(data):
        kunci = data['kunci']
        if kunci.status != 'Tersedia':
            raise ValueError("Kunci sedang dipinjam")
        peminjaman = Peminjaman.objects.create(**data)
        kunci.status = 'Dipinjam'
        kunci.save()
        return peminjaman
```

**Keuntungan:**
- Transaction atomic — jika satu operasi gagal, semua rollback
- Validasi sebelum eksekusi
- Mudah di-test secara terpisah

### 20.5 AJAX untuk Dropdown Dinamis

Dropdown kunci di form peminjaman menggunakan **AJAX** untuk memuat data berdasarkan laboratorium yang dipilih:

```javascript
// jQuery AJAX call
$('#id_laboratorium').on('change', function() {
    $.getJSON('/transaksi/api/get-kunci/', { lab_id: labId }, function(data) {
        // Update dropdown kunci
    });
});
```

### 20.6 Django Template Tags & Widget Tweaks

Menggunakan `django-widget-tweaks` untuk render form yang lebih bersih:

```django
{% load widget_tweaks %}
{{ form.nama|add_class:"form-control" }}
```

### 20.7 Auto-Cleanup Records

Records peminjaman yang sudah dikembalikan dan berusia > 30 hari otomatis dihapus menggunakan management command:

```bash
python manage.py cleanup_old_records
```

Juga dipanggil otomatis setiap kali halaman laporan diakses.

### 20.8 Export Laporan

Export ke **Excel** menggunakan `openpyxl` dan **CSV** menggunakan modul bawaan Python:

```python
# Export Excel
response['Content-Disposition'] = 'attachment; filename="laporan.xlsx"'
wb.save(response)

# Export CSV
writer = csv.writer(response)
writer.writerow(['No', 'Tanggal', 'NIM', ...])
```

### 20.9 Security Best Practices

| Praktik | Implementasi |
|---------|-------------|
| Login required | `@login_required` decorator atau `LoginRequiredMixin` |
| CSRF protection | `{% csrf_token %}` di semua form |
| Secret key | Disimpan di `.env`, tidak di commit |
| SQL injection | Prevented by Django ORM (query parameterized) |
| Password hashing | PBKDF2 (default Django) |
| XSS protection | Template auto-escaping |

### 20.10 Environment Configuration

```python
# config/settings.py
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Database switching: SQLite (dev) / MySQL (production)
if os.environ.get('USE_MYSQL', 'False') == 'True':
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        ...
    }
```

### 20.11 Seed Data

Management command untuk mengisi data awal demo:

```bash
python manage.py seed_data
```

Output:
```
Mengisi data awal...
  [OK] 12 mahasiswa
  [OK] 5 dosen
  [OK] 5 laboratorium
  [OK] 20 kunci
  [OK] 8 peminjaman contoh
Data awal berhasil diisi!
```

### 20.12 Custom Error Pages

Halaman error kustom untuk pengalaman pengguna yang lebih baik:

| Halaman | File | Kode |
|---------|------|------|
| Not Found | `templates/404.html` | `handler404` |
| Server Error | `templates/500.html` | `handler500` |
| Forbidden | `templates/403.html` | `handler403` |

---

## LAMPIRAN

### A. Teknologi yang Digunakan

| Teknologi | Versi | Fungsi |
|-----------|-------|--------|
| Python | 3.14 | Bahasa pemrograman |
| Django | 6.0 | Web framework MVC |
| SQLite / MySQL | - | Database |
| Bootstrap | 5.3 | CSS framework |
| jQuery | 3.7 | JavaScript library |
| openpyxl | 3.1 | Export Excel |
| django-widget-tweaks | 1.5 | Form rendering |
| django-filter | 26.1 | FilterSet |

### B. Cara Menjalankan Aplikasi

```bash
# 1. Clone repositori
git clone https://github.com/delvin07-hub/sistem-peminjaman-kunci-lab.git
cd sistem-peminjaman-kunci-lab

# 2. Virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate    # Linux/Mac

# 3. Install dependensi
pip install -r requirements.txt

# 4. Migrasi database
python manage.py migrate

# 5. Buat superuser
python manage.py createsuperuser

# 6. (Opsional) Isi data awal
python manage.py seed_data

# 7. Jalankan server
python manage.py runserver
```

### C. Lisensi

Proyek ini dilisensikan di bawah **MIT License**.

---

*Dokumen Perencanaan — Sistem Peminjaman Kunci Laboratorium*

*© 2026*
