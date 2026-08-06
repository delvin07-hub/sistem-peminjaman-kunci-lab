# Design: Push Notifikasi FCM + Layar Detail Mobile

Tanggal: 2026-08-06
Status: Disetujui user (langsung eksekusi)

## Tujuan

1. Notifikasi peminjaman/pengembalian kunci muncul sebagai popup & bilah notifikasi di HP penanggung jawab (FCM), meskipun app ditutup total.
2. Item di menu Notifikasi dan menu Kunci bisa diklik → layar detail lengkap: nama, NIM, dosen, nama lab, nama kunci, dsb.

## Arsitektur

```
Admin pinjam/kembali kunci (web)
  -> PeminjamanService (transaction.atomic)
    -> NotifikasiService.buat() -> simpan DB + transaction.on_commit
      -> PushNotifikasiService -> FCM API (firebase-admin)
        -> Google server -> HP PJ (popup + bilah notifikasi)
          -> tap notifikasi -> buka app -> layar detail peminjaman
```

## Backend (Django)

- Model baru `DeviceToken` (apps.notifications): `penanggung_jawab` FK, `token` (unique), `created_at`, `updated_at`. Endpoint:
  - `POST /api/device-token/` — daftarkan token (dipanggil app saat login & saat token berubah)
  - `DELETE /api/device-token/` — hapus token (dipanggil app saat logout)
- `PushNotifikasiService` (apps.notifications.services):
  - Init `firebase_admin` lazy saat pertama dipakai; path key dari env `FCM_SERVICE_ACCOUNT_JSON`; jika file tidak ada, push dilewati tanpa error (agar dev/test tetap jalan)
  - `kirim(notifikasi)`: kirim FCM ke semua token PJ terkait; payload notification `{title, body}` + data `{notifikasi_id, peminjaman_id, tipe}`; try/except per token
  - Dipanggil dari `NotifikasiService.buat` via `transaction.on_commit`
- Serializer diperkaya (nested detail, read-only):
  - `NotifikasiSerializer` + `peminjaman_detail`: `{id, status, tanggal_pinjam, jam_pinjam, tanggal_kembali, jam_kembali, keperluan, mahasiswa{nim, nama, program_studi}, dosen{nidn, nama}, laboratorium{kode_lab, nama_lab, gedung, lantai}, kunci{id, nomor_kunci}}`
  - `KunciStatusSerializer` + `peminjaman_aktif` (jika Dipinjam)
- Endpoint baru: `GET /api/status-kunci/<id>/` → info lab + peminjam aktif + riwayat 10 peminjaman terakhir
- Dep baru: `firebase-admin` (requirements.txt)

## Mobile (Flutter)

- Dep baru: `firebase_core`, `firebase_messaging`, `flutter_local_notifications`; plugin `google-services` + `google-services.json` di `mobile/android/app/`
- Push: init Firebase + minta izin `POST_NOTIFICATIONS`; `onMessage` (foreground) -> popup lokal; background/terminated -> sistem; tap notifikasi -> layar detail
- Login: `getToken()` -> `POST /api/device-token/`; Logout -> `DELETE`
- Layar Detail Notifikasi: nama, NIM, dosen, lab (kode/nama/gedung/lantai), kunci, jam, keperluan, status, tanggal
- Layar Detail Kunci: info lab + status; jika Dipinjam -> peminjam aktif + riwayat 10 terakhir

## Setup Firebase (aksi user, dipandu)

1. console.firebase.google.com -> Add project
2. Add app Android -> package `com.delvin07.kunci_lab_mobile` -> unduh google-services.json -> `mobile/android/app/`
3. Project settings -> Service accounts -> Generate new private key -> serviceAccountKey.json di folder proyek

## Pengujian

- Backend: unit test PushNotifikasiService (mock), DeviceToken endpoint, serializer detail, 20 test lama tetap hijau
- Mobile: flutter analyze + widget test + E2E (pinjam via web -> notif muncul di HP)

## Batasan

- FCM butuh internet di HP & server (sudah dikonfirmasi ada); saat offline, notif tetap tercatat di DB
- Push mati jika server dimatikan
