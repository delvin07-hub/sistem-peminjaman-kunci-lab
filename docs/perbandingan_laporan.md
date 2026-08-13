# Perbandingan Laporan Awal vs Sistem Saat Ini

## SISTEM PEMINJAMAN KUNCI LABORATORIUM BERBASIS WEB
Tanggal analisis: 13 Agustus 2026

---

## A. FITUR YANG SUDAH ADA DI LAPORAN AWAL

| No | Fitur | Status di Laporan Awal |
|----|-------|------------------------|
| 1 | Login (session-based authentication) | ✅ Sudah ada |
| 2 | Dashboard (statistik kunci + aktivitas terbaru) | ✅ Sudah ada |
| 3 | CRUD Data Mahasiswa | ✅ Sudah ada |
| 4 | CRUD Data Dosen | ✅ Sudah ada |
| 5 | CRUD Data Laboratorium | ✅ Sudah ada |
| 6 | CRUD Data Kunci | ✅ Sudah ada |
| 7 | Form Peminjaman Kunci (AJAX dinamis) | ✅ Sudah ada |
| 8 | Pengembalian Kunci | ✅ Sudah ada |
| 9 | Riwayat Peminjaman (search + filter + pagination) | ✅ Sudah ada |
| 10 | Laporan Peminjaman (filter tanggal+status, export Excel/CSV) | ✅ Sudah ada |
| 11 | Notifikasi push (FCM) | ✅ Sudah ada (dalam laporan) |
| 12 | Black Box Testing (12 skenario) | ✅ Sudah ada |

---

## B. PERUBAHAN & TAMBAHAN FITUR SEJAK LAPORAN AWAL

### 1. Modul Autentikasi & Keamanan

| Fitur | Keterangan |
|-------|-----------|
| **Ubah Password** | Admin/laboran bisa mengubah password sendiri tanpa harus reset dari database. View `ubah_password_view` menggunakan `PasswordChangeForm` + `update_session_auth_hash`. URL: `/password/` |
| **Superuser-only web admin** | Semua halaman admin dibatasi hanya untuk superuser. Django admin default dihapus. |
| **CRUD Penanggung Jawab** | Penanggung Jawab (PJ) sekarang bisa ditambahkan/mengelola melalui antarmuka web. View: `PenanggungJawabListView`, `CreateView`, `UpdateView`, `DeleteView`. |

### 2. Master Data — Perubahan Implementasi

| Fitur | Keterangan |
|-------|-----------|
| **Auto-generate kode ruangan** | Kode ruangan dibuat otomatis: R1, R2, R3... (tidak perlu diisi manual). Fungsi `_next_kode_ruangan()` di `apps/master_data/views.py`. |
| **Auto-generate nomor kunci** | Nomor kunci dibuat otomatis sesuai ruangan: K1, K2, K3... Fungsi `_next_nomor_kunci(ruangan)` dan `_renumber_kunci(ruangan)`. |
| **Renumber kunci otomatis saat hapus** | Jika kunci dihapus, sistem secara otomatis menomori ulang kunci tersisa agar tidak ada loncatan nomor. |
| **Validasi hapus — kunci dipinjam** | Kunci dengan status `Dipinjam` TIDAK BISA dihapus. Ditampilkan pesan error. |
| **Validasi hapus — mahasiswa/dosen memiliki pinjaman aktif** | Mahasiswa atau dosen yang masih memiliki peminjaman aktif TIDAK BISA dihapus. |
| **Validasi hapus — laboratorium punya kunci atau pinjaman** | Laboratorium yang memiliki kunci atau masih ada transaksi aktif TIDAK BISA dihapus. |
| **Field SET_NULL (mahasiswa/dosen/laboratorium di Peminjaman)** | Ketiga field tersebut diubah menjadi `null=True` (SET_NULL). Artinya jika entitas dihapus, riwayat peminjaman tetap tersimpan namun referensi jadi NULL. Guard null diterapkan di semua layar/export/notifikasi. |
| **Import Excel Mahasiswa & Dosen** | Fitur impor massal data mahasiswa dan dosen dari file Excel (.xlsx). Ada juga template xlsx yang bisa diunduh. |
| **Istilah "Laboratorium" → "Ruangan"** | Label dan display di UI diubah dari "Laboratorium" menjadi "Ruangan". |

### 3. Transaksi Peminjaman & Pengembalian

| Fitur | Keterangan |
|-------|-----------|
| **Jam pinjam otomatis dari server** | Field `jam_pinjam` dan `tanggal_pinjam` diisi otomatis dari server time (bukan dari input pengguna). |
| **Validasi kunci harus sesuai ruangan** | Sistem menolak jika kunci yang dipilih tidak termasuk dalam ruangan yang dipilih. |
| **Blokir peminjaman ganda mahasiswa** | Mahasiswa yang masih memiliki peminjaman aktif (status='Dipinjam') DITOLAK jika mencoba meminjam kunci baru. |
| **Pesan sukses detail** | Setelah peminjaman berhasil, muncul pesan sukses menampilkan nama mahasiswa, nomor kunci, dan jam peminjaman. |
| **htmx:afterSwap untuk navigasi** | Script `refreshKunci()` dipindah ke `static/js/main.js` dengan delegation event `htmx:afterSwap` agar dropdown kunci tetap berfungsi setelah navigasi halaman via htmx. |

### 4. Riwayat & Laporan

| Fitur | Keterangan |
|-------|-----------|
| **Filter ruangan/dosen/program studi** | Riwayat dan laporan sekarang bisa difilter berdasarkan ruangan, dosen, dan program studi mahasiswa. |
| **Tanpa pagination** | Semua data ditampilkan tanpa pagination (sesuai permintaan). |
| **Export membawa param filter** | Export Excel/CSV membawa parameter filter yang sedang aktif. |
| **Notifikasi log (web)** | Notifikasi sekarang melacak status pengiriman (Menunggu/Terkirim/Gagal). Fitur Log Notifikasi di web (`/notifikasi-log/`). |

### 5. Notifikasi — Perubahan Besar

| Fitur | Keterangan |
|-------|-----------|
| **FCM → Telegram Bot** | Tidak lagi menggunakan Firebase Cloud Messaging (FCM). Sekarang mengirim notifikasi ke grup Telegram "PENANGGUNG JAWAB KUNCI". |
| **Styling notifikasi lebih menarik** | Format pesan Telegram menggunakan emoji, border karakter, dan layout terstruktur. |
| **Push notifikasi di background thread** | Pengiriman notifikasi berjalan di thread daemon agar tidak memblokir respons web. |

### 6. Dashboard

| Fitur | Keterangan |
|-------|-----------|
| **Hapus grafik Chart.js** | Grafik "7 Hari Terakhir" dan "Kunci per Ruangan" dihapus. Dashboard fokus pada "Aktivitas Hari Ini". |
| **Dashboard timezone-aware** | Menggunakan `timezone.localdate()` untuk menampilkan tanggal sesuai zona waktu Asia/Jakarta. |

### 7. Infrastruktur & Deploy

| Fitur | Keterangan |
|-------|-----------|
| **Waitress 8 thread** | Server produksi menggunakan waitress dengan `--threads=8`. |
| **start_prod.bat** | Script otomatis start: migrate → collectstatic → waitress serve. |
| **Custom error pages** | Halaman error 403, 404, 500 tersedia. |
| **Management command: cleanup_old_records** | Command Django `python manage.py cleanup_old_records` untuk menghapus transaksi lama (>90 hari, status dikembalikan). |

### 8. Mobile App (Flutter) — Perubahan

| Fitur | Keterangan |
|-------|-----------|
| **FCM dihapus total** | Dependensi Firebase (firebase_core, firebase_messaging, flutter_local_notifications) dihapus dari pubspec.yaml. |
| **Endpoint device-token dihapus** | API `/api/device-token/` dan view `DeviceTokenView` dihapus dari backend. |
| **Mobile API cleaned** | Method `registerDeviceToken()` dan `unregisterDeviceToken()` dihapus dari `ApiService`. |
| **PushService dihapus** | File `push_service.dart` dihapus. Login/logout tidak lagi mendaftarkan token. |

---

## C. YANG PERLU DITAMBAHKAN DI LAPORAN

### BAB I — Latar Belakang & Batasan Masalah
- Tambahkan: kebutuhan akan fitur import data massal (karena data mahasiswa/dosen banyak)
- Tambahkan: kebutuhan akan pembatasan peminjaman ganda (keamanan sistem)
- Tambahkan: kebutuhan notifikasi real-time (Telegram) agar PJ dapat memantau tanpa harus login web
- Update batasan masalah: tambahkan batasan fitur notifikasi Telegram

### BAB II — Tinjauan Pustaka
- Tambahkan sub-bab: **Telegram Bot API** (penjelasan tentang bot, webhook, sendMessage endpoint)
- Tambahkan sub-bab: **htmx** (penjelasan singkat tentang library untuk AJAX tanpa reload)
- Tambahkan sub-bab: **Import/Export Excel** (library openpyxl/xlsxwriter yang digunakan)
- Update sub-bab metode: jelaskan bahwa FCM diganti Telegram karena keterbatasan jaringan LAN kampus

### BAB III — Metode Perancangan
- Tambahkan diagram **Sequence Diagram** untuk proses import Excel
- Tambahkan diagram **Activity Diagram** untuk alur validasi peminjaman ganda
- Update deskripsi Use Case: tambahkan actor "Penanggung Jawab" sebagai penerima notifikasi Telegram
- Tambahkan kebutuhan fungsional baru:
  - F-11: Import data mahasiswa/dosen dari Excel
  - F-12: Ubah password admin
  - F-13: Filter riwayat/laporan berdasarkan ruangan/dosen/prodi
  - F-14: Blokir peminjaman ganda mahasiswa
  - F-15: Notifikasi Telegram

### BAB IV — Hasil dan Pembahasan
- **Tambahkan subsection:** Implementasi Import Excel (screenshot + penjelasan)
- **Tambahkan subsection:** Implementasi Validasi Peminjaman Ganda (screenshot form error)
- **Tambahkan subsection:** Integrasi Telegram Bot (cara setup bot, format pesan, screenshot grup)
- **Tambahkan subsection:** Auto-generate kode ruangan & nomor kunci
- **Tambahkan subsection:** Fitur Penanggung Jawab CRUD
- **Update Tabel Black Box Testing:** tambahkan baris untuk setiap fitur baru
- **Update kelebihan sistem:** tambahkan poin tentang validasi peminjaman ganda, import massal, notifikasi Telegram
- **Update kekurangan sistem:** tambahkan catatan tentang ketergantungan pada koneksi internet untuk Telegram

### BAB V — Kesimpulan & Saran
- **Kesimpulan:** tambahkan bahwa sistem juga mengintegrasikan notifikasi Telegram dan fitur import data
- **Saran:** tambahkan saran untuk mengembangkan integrasi QR Code pada kunci, serta backup data otomatis

### Lampiran
- **Screenshot import Excel**
- **Screenshot validasi peminjaman ganda (pesan error)**
- **Screenshot notifikasi Telegram di grup**
- **Screenshot halaman ubah password**
- **Screenshot halaman penanggung jawab**
- **Script manajemen command cleanup_old_records**

---

## D. DAFTAR PUSTAKA TAMBAHAN

Perlu ditambahkan referensi untuk:
1. Telegram Bot API (docs.telegram.org)
2. htmx documentation (htmx.org)
3. OpenPyXL / XlsxWriter untuk export Excel
4. Waitress WSGI server
5. Flutter framework (flutter.dev)
