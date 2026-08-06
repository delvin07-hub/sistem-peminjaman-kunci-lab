# Roadmap Integrasi Aplikasi Mobile

Dokumen ini menjelaskan API JSON yang sudah tersedia untuk dikonsumsi aplikasi mobile (misal: Flutter) beserta rencana pengembangannya.

## Endpoint API

Base URL: `http://<host>:8000/api/`

| Method | Path                    | Deskripsi                                               |
| ------ | ----------------------- | ------------------------------------------------------- |
| POST   | `/api/token/`           | Login, dapatkan token akses                             |
| GET    | `/api/notifikasi/`      | Daftar notifikasi milik penanggung jawab yang login     |
| PATCH  | `/api/notifikasi/<id>/baca/` | Tandai satu notifikasi sebagai dibaca             |
| GET    | `/api/status-kunci/`    | Status kunci (Tersedia / Dipinjam) per laboratorium     |

Semua endpoint (kecuali login) membutuhkan header: `Authorization: Token <token>`.
Hanya pengguna yang terdaftar sebagai `PenanggungJawab` aktif yang boleh mengakses.

## Alur Login

1. `POST /api/token/` dengan body JSON:
   ```json
   { "username": "pj1", "password": "pj12345" }
   ```
2. Respons:
   ```json
   { "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" }
   ```
3. Simpan token (mis. `flutter_secure_storage`) dan kirim pada setiap request berikutnya:
   `Authorization: Token 9944b09199c62bcf...`

## Contoh Respons

`GET /api/notifikasi/`
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 3,
      "tipe": "Dipinjam",
      "pesan": "Andi Demo meminjam kunci K1 (L99) jam 08:00:00",
      "dibaca": false,
      "peminjaman": 5,
      "tanggal": "2026-08-06T08:10:00+07:00"
    }
  ]
}
```

`GET /api/status-kunci/`
```json
{
  "count": 3,
  "results": [
    { "id": 1, "kode_lab": "LAB-01", "nama_lab": "Lab Komputer 1", "nomor_kunci": "LAB-01-K01", "status": "Tersedia" },
    { "id": 4, "kode_lab": "LAB-01", "nama_lab": "Lab Komputer 1", "nomor_kunci": "LAB-01-K04", "status": "Dipinjam" }
  ]
}
```

Filter notifikasi: `GET /api/notifikasi/?dibaca=true`

## Saran Implementasi (Flutter)

- Simpan token dengan `flutter_secure_storage`.
- Antarmuka pakai `Dio` dengan interceptor menambahkan header `Authorization`.
- List halaman notifikasi pakai `RefreshIndicator` + `infinite scroll` (API sudah paginasi 20 per halaman).
- Halaman status kunci pakai `FutureBuilder` + refresh otomatis tiap beberapa detik.

## Backlog

- [ ] Push notification real-time (Firebase Cloud Messaging / WebSocket) alih-alih polling.
- [ ] API untuk profil penanggung jawab sendiri (`GET /api/profil/`).
- [ ] Rate-limiting dan throttling pada endpoint token.
- [ ] Pagination custom + filter tanggal untuk riwayat peminjaman.
- [ ] Dokumentasi OpenAPI/Swagger (drf-spectacular).