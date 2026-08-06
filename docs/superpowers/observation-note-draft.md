# Napas Proyek: sistem-peminjaman-kunci-lab

proyek: sistem-peminjaman-kunci-lab
status: pengembangan
repo: https://github.com/delvin07-hub/sistem-peminjaman-kunci-lab
domain: Manajemen peminjaman kunci laboratorium untuk admin/laboran kampus (capstone/TA)

## Deskripsi Singkat
Web internal satu-role (admin/laboran) untuk mencatat: kelola data mahasiswa/dosen/
laboratorium/kunci (CRUD), peminjaman & pengembalian kunci dengan validasi
ketersediaan otomatis, riwayat, dan laporan (filter + export Excel/CSV). Seluruh
UI berbahasa Indonesia. Sistem kini berperilaku SPA-ringan via htmx tanpa reload
halaman penuh.

## Stack
- **Python 3.14**, **Django 6.0** (`.venv` lokal), **requirements.txt**: django>=6.0,<7.0, mysqlclient>=2.2, python-dotenv>=1.0, django-filter>=26.1, django-widget-tweaks>=1.5, openpyxl>=3.1
- **DB**: SQLite default (`db.sqlite3`); MySQL aktif jika env `USE_MYSQL=true` (config/settings.py)
- **Frontend**: Bootstrap 5.3 + Bootstrap Icons + jQuery 3.7 + **htmx 1.9.12** (CDN)
- **WSGI** (`config/wsgi.py`), DEVELOPMENT pakai `runserver`; `start.bat` untuk auto-buka browser

## Arsitektur
- **Status: SERVER-RENDERED (bukan REST API)**. Views merender HTML lengkap; AJAX JSON hanya untuk dropdown dependen & pencarian (tiada REST framework).
- Monolit modular, 5 apps di folder `apps/`:
  - `authentication` — login/logout (FBV, session)
  - `dashboard` — statistik + aktivitas terbaru (FBV)
  - `master_data` — Mahasiswa, Dosen, Laboratorium, Kunci (CBV: List/Create/Update/Delete)
  - `transaction` — Peminjaman, Pengembalian, Riwayat + **service layer** (FBV)
  - `report` — laporan + export Excel/CSV (FBV)
- **Service layer** terpisah di `apps/transaction/services.py` class `PeminjamanService` dengan dua operasi atomic: `pinjam_kunci()` dan `kembalikan_kunci()`.
- **SPA htmx (baru)**: template statis `base.html` jadi shell `#main-content`; tiap tautan/pagegination/form memakai `hx-target="#main-content"` + `hx-select="#main-content"` sehingga hanya fragmen konten di-swap tanpa reload. Backend tak berubah.
- **Alur UI**: `base.html` (navbar) → swap konten ke `<div id="main-content">`. Login & halaman error pakai template terpisah (`base_auth.html`, `404/403/500`).

## Keputusan Desain
- **Atomic Peminjaman**: `pinjam_kunci` dan `kembalikan_kunci` dibungkus `@transaction.atomic` di service — jika step laign gagal, semuanya di-rollback (konsistensi status kunci).
- **Availability 3 lapis**: (1) queryset kunci `status='Tersedia'` di form; (2) `clean_kunci()` validasi form; (3) re-check `if kunci.status != 'Tersedia'` di service sebelum commit.
- **Pendek kombinasi CBV/FBV**: master_data pakai CBV (ringkas, DRY); transaction/report/dashboard pakai FBV (logika transaksi & export lebih eksplisit).
- **Auth kustom**: `login_view` pakai `auth.authenticate/login`; satu role admin/laboran; `LOGIN_URL='/'`, `LOGIN_REDIRECT_URL='/dashboard/'`.
- **DB portabel**: SQLite default, MySQL aktif via env. Settings berbasis `.env` (SECRET_KEY, DEBUG, ALLOWED_HOSTS, DB_*).
- **Tampilan nama lab**: kolom "Lab" di SEMUA tabel menampilkan `nama_lab` (e.g. "Lab Komputer 1") bukan `kode_lab`.

## Model & Relasi (apps/master_data/models.py, apps/transaction/models.py)
- **Mahasiswa**: `nim` (unique), `nama`, `program_studi`; timestamp `created_at`/`updated_at`; `ordering=['nama']`.
- **Dosen**: `nidn` (unique, verbose "NIDN"), `nama`.
- **Laboratorium**: `kode_lab` (unique), `nama_lab`, `gedung`, `lantai`; `ordering=['kode_lab']`.
- **Kunci**: `laboratorium` (FK→Laboratorium, related_name='kunci'), `nomor_kunci`, `status` ('Tersedia'|'Dipinjam'); `unique_together=['laboratorium','nomor_kunci']`. 1 lab → banyak kunci.
- **Peminjaman**: FK ke `mahasiswa`, `dosen`, `laboratorium`, `kunci` (masing-masing related_name='peminjaman'), `tanggal_pinjam` (auto hari ini), `jam_pinjam` (TimeField), `tanggal_kembali`/`jam_kembali` (nullable), `keperluan` (Text), `status` ('Dipinjam'|'Dikembalikan' default Dipinjam); `ordering=['-created_at']`.
- Relasi tambahan: `Peminjaman.kunci → Kunci.status` saling terikat oleh service.
- Semua model diberi `created_at`/`updated_at`; semua FK pakai `related_name`.

## URL Lengkap
Prefix root `config/urls.py`: `admin/`, ``→auth, `dashboard/`, `master/`, `transaksi/`, `laporan/`.

**authentication**: `/` (`login`), `/logout/` (`logout`)
**dashboard**: `/dashboard/` (`dashboard`)
**master_data** (`apps/master_data/urls.py`): tiap entitas 4 route: list `/` (`*_list`), tambah `/tambah/` (`*_create`), edit `/edit/<int:pk>/` (`*_update`), hapus `/hapus/<int:pk>/` (`*_delete`) untuk mahasiswa/dosen/laboratorium/kunci → nama view: `mahasiswa_list/create/update/delete`, `dosen_*`, `laboratorium_*`, `kunci_*`.
**transaction** (`apps/transaction/urls.py`):
- `/transaksi/peminjaman/` → `peminjaman_create` (GET form, POST catat)
- `/transaksi/api/get-mahasiswa/` → `get_mahasiswa` (JSON, `?term=`)
- `/transaksi/api/get-kunci/` → `get_kunci` (JSON, `?lab_id=`)
- `/transaksi/pengembalian/` → `pengembalian_list`
- `/transaksi/pengembalian/<int:pk>/` → `pengembalian_process`
- `/transaksi/riwayat/` → `riwayat_list`
- `/transaksi/cari/` → `search` (JSON `?q=`)
**report** (`apps/report/urls.py`): `/laporan/` (`report_index`), `/laporan/export/excel/` (`report_export_excel`), `/laporan/export/csv/` (`report_export_csv`).

## Views & Alur (acuan cepat)
- `authentication/login_view`: redirect dashboard jika sudah login; authenticate; else error.
- `dashboard.index`: aggregate total/tersedia/dipinjam kunci + `peminjaman_hari_ini` + 10 `peminjaman_terbaru` (`select_related`).
- `transaction` (FBV):
  - `peminjaman_create`: validasi `PeminjamanForm`; panggil `Service.pinjam_kunci`; sukses→redirect + `messages.success`; `ValueError`→messages.error.
  - `get_mahasiswa`/`get_kunci`: JSON `{results:[{id,text}]}` untuk select2-style dropdown.
  - `pengembalian_list`: list status='Dipinjam' + search via `_search_peminjaman_q`.
  - `pengembalian_process`: get_object_or_404(status='Dipinjam'); POST→`Service.kembalikan_kunci`.
  - `riwayat_list`: search + filter status + `Paginator` 10/halaman.
  - `search`: JSON segera 20 hasil.
- `transaction.services`: `PeminjamanService.pinjam_kunci(data)`, `PeminjamanService.kembalikan_kunci(id, jam_kembali)`. Keduanya dibungkus `@transaction.atomic`.
- `report`: `_get_filtered_data` filter `tgl_awal`/`tgl_akhir`/`status`; `laporan_view` paginate 50; `export_excel`/`export_csv` pakai `EXPORT_HEADERS` + `_peminjaman_to_row`, `export_excel` styling openpyxl.
- `master_data` CBV: ListView (search + `paginate_by=10`, kunci juga filter `lab`), CreateView/UpdateView (`success_url` ke list), DeleteView (confirm template, `cancel_url`).

## Management Commands
- `python manage.py seed_data` — isi demo: superuser `admin/admin123` + 12 mahasiswa + 5 dosen + 5 lab (LAB-01..05) + kunci + peminjaman contoh. Idempotent (`get_or_create`).
- `python manage.py cleanup_old_records` — hapus peminjaman `status='Dikembalikan'` yang berusia > 30 hari.

## Struktur Folder
```
config/            # settings, urls, wsgi, asgi
apps/              # authentication, dashboard, master_data, transaction, report
templates/         # base.html (shell SPA), base_auth.html, dashboard/, master_data/, transaction/, report/, 404/403/500
static/js/main.js  # auto-close alert
docs/superpowers/specs/  # desain spec
docs/superpowers/plans/  # plan
.venv, db.sqlite3, .env, manage.py, requirements.txt, start.bat
```

## Pola yang Dipakai
- **Bahasa Indonesia** untuk seluruh naming, teks UI, label, komentar.
- **`_BootstrapFormMixin`** (`apps/master_data/forms.py`) — auto-apply class `form-select`/`form-control` ke semua field (DRY). `PeminjamanForm` juga inline CSS.
- **Memberi dan CBV vs FBV** konsisten per app; `success_url` `reverse_lazy`.
- **`select_related`** di semua list/riwayat/laporan (anti N+1); `Paginator` konsisten (10 per daftar, 50 laporan).
- **`related_name`** pada tiap FK; timestamp `created_at`/`updated_at` di model inti.
- **SPA htmx pola tetap**: `hx-get`/`hx-post` + `hx-target="#main-content"` + `hx-select="#main-content"` + `hx-push-url="true"` untuk navigasi/pagination/form; **`hx-boost="false"`** pada link export Excel/CSV; **`hx-post=""`** untuk form create & update yang berbagi template (POST ke URL saat itu).

## Riwayat Sesi (entri terbaru)
- **Sesi 1 (SPA htmx + nama lab)** — selesai. Refactor htmx SPA di semua template + ubah kolom Lab → nama_lab. Diubah: `templates/base.html`, `dashboard/index.html`, `report/laporan.html`, `transaction/pengembalian_list.html`, `transaction/riwayat_list.html`, `transaction/pengembalian_confirm.html`, `master_data/kunci_list.html`, dan template master/transaksi lainnya + docs/superpowers/specs & plans. Branch: `feature/spa-htmx` (SPA) & `feature/tampilkan-nama-lab` (nama lab). Keduanya sudah di-**push** (belum PR).
- **Sesi 2 (Penanggung jawab + notifikasi + API)** — selesai di branch `feature/penanggung-jawab-int` (8 commit): model `PenanggungJawab` (OneToOne → auth.User) + admin create-user, app `apps.notifications` (Notifikasi + NotifikasiService), hook di PeminjamanService, REST API DRF (token/notifikasi/status-kunci) + `docs/ROADMAP_MOBILE.md`. API terverifikasi end-to-end (login → list → mark baca → status kunci).
- **Sesi 3 (Integrasi + README + mobile + deployment)** — selesai di `main`: merge `feature/spa-htmx` + `feature/tampilkan-nama-lab` + `feature/penanggung-jawab-int` (clean, no conflict; main sudah di-push ke origin). README diperbarui. Aplikasi Flutter `mobile/` (login token, notifikasi, status kunci; web/Windows; `--dart-define=API_URL=...`). Deployment produksi Windows: waitress + whitenoise + CORS + `start_prod.bat` (terverifikasi: halaman login + static 200 di DEBUG=False).

## Task Terbuka
- ~~Membuat PR via GitHub UI untuk `feature/spa-htmx` dan `feature/tampilkan-nama-lab`~~ — selesai, sudah di-merge ke `main` (PR #1 untuk spa-htmx dibuat di GitHub; sisanya di-merge lokal lalu push).
- `apps/transaction/filters.py` (`PeminjamanFilter` django-filter) belum dihubungkan ke view (riwayat masih memakai filter manual).
- `nssm.exe` belum di-download (untuk install service `start.bat`/`start_prod.bat` di production, bila perlu).
- Build APK Android butuh Android SDK / Android Studio (belum terpasang).
- Ganti `shared_preferences` ke `flutter_secure_storage` bila token dianggap sensitif.