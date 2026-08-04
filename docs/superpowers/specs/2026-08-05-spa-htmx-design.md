# SPA htmx untuk Sistem Peminjaman Kunci Laboratorium — Design Spec

## Ringkasan

Mengubah web server-rendered Django (Bootstrap + jQuery + template) menjadi
konsep Single Page Application (SPA) ringan menggunakan htmx agar navigasi
tidak melakukan reload halaman penuh. Backend Django tetap 100% server-rendered;
htmx menjadi lapisan AJAX pada sisi klien.

## Keputusan Arsitektur (dari sesi brainstorming)

- **Pendekatan:** htmx partial-loading (dipilih user).
- **Granularity:** konten-partial container (dipilih user): hanya konten
  `#main-content` yang di-swap, bukan seluruh body.
- **Teknik:** `hx-get` + `hx-target="#main-content"` + `hx-select="#main-content"`
  + `hx-push-url="true"`. Template tetap extend `base.html`; tidak ada perubahan
  pada views, forms, atau urls.

## Arsitektur

Satu kali full page load memuat `base.html` (+ CSS/JS/cache). Setiap link/aksi
navigasi memicu permintaan htmx ke URL yang sama seperti navigasi normal; htmx
mengekstrak fragmen `#main-content` dari respons HTML dan menukarnya ke dalam
container tanpa reload browser. URL diubah via `hx-push-url` sehingga tombol
Back/Forward dan bookmark tetap berfungsi.

### Komponen

1. **`base.html`** — Wrap `{% block content %}` dalam `<div id="main-content">`.
   Region messages diletakkan di dalam `#main-content` agar ter-swap bersama
   konten. Tambah `<script src="https://unpkg.com/htmx.org@1.9.12">` (defer).
2. **Navbar** — Setiap link menu & dropdown memakai atribut:
   `hx-get`, `hx-target="#main-content"`, `hx-select="#main-content"`,
   `hx-push-url="true"`. Brand dashboard dan semua menu (Master Data,
   Peminjaman, Pengembalian, Riwayat, Laporan). Logout tetap plain link.
3. **Paginasi & pencarian (list views)** — Link halaman (Awal/Prev/Next/Akhir)
   dan form search diberi atribut htmx serupa dengan `hx-target`/`hx-select`.
4. **Form Create/Update/Delete** — diberi `hx-post` + `hx-target` + `hx-select`.
   View melakukan redirect biasa; htmx mengikuti dan menukar fragmen hasil.
5. **Laporan export (Excel/CSV)** — Link download TIDAK boleh di-intercept
   (harus unduh file). Diberi `hx-boost="false"` agar berperilaku normal.
6. **Graceful degradation** — Link tetap menyimpan `href` asli; jika JS/hx gagal,
   fallback ke full page.

### Edge Cases

- Logout & halaman error (403/404/500): full page, tidak menyentuh `#main-content`.
- Form peminjaman (`peminjaman_form.html`) memakai jQuery AJAX
  (`get-kunci`/`get-mahasiswa`): jQuery tetap dipertahankan di `base.html`.
- Alert messages auto-close (`main.js`) tetap berfungsi karena alert di-render
  ulang dalam `#main-content` tiap navigasi.

## Kelebihan / Kekurangan

- **Kelebihan:** tidak menyentuh views/forms/urls; payload navigasi hanya konten;
  Browser Back/Forward & bookmark berfungsi.
- **Kekurangan:** `hx-select` tetap menerima HTML penuh lalu mengekstrak
  (sedikit overhead parsing); respons redirect ikut di-fetch.

## File yang Disentuh

- Modify: `templates/base.html`
- Modify: seluruh template yang memiliki navigasi link, paginasi, form, dan
  laporan export (mahasiswa, dosen, laboratorium, kunci, peminjaman,
  pengembalian, riwayat, laporan).
- Tidak ada perubahan: views, forms, urls, models, database.