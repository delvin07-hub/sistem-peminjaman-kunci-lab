# Kunci Lab — Aplikasi Mobile (Penanggung Jawab)

Aplikasi Flutter untuk penanggung jawab (1–2 orang) memantau notifikasi
peminjaman kunci dan status kunci laboratorium melalui REST API backend.

## Fitur

- Login dengan username/password → token otomatis disimpan
- Daftar notifikasi (dipinjam / dikembalikan) + tandai dibaca (swipe atau tombol)
- Status kunci per laboratorium (Tersedia / Dipinjam)
- Logout

## Menjalankan

```bash
flutter pub get

# Web (untuk uji coba cepat di browser)
flutter run -d chrome

# Windows desktop
flutter run -d windows

# Android (wajib Android SDK / Android Studio terpasang)
flutter run -d android
```

## Menghubungkan ke Backend

Base URL API diatur lewat `--dart-define` saat run/build:

```bash
# Contoh: server di PC lain dengan IP 192.168.1.10
flutter run -d chrome --dart-define=API_URL=http://192.168.1.10:8000/api/
flutter build web --dart-define=API_URL=http://192.168.1.10:8000/api/
```

Tanpa flag, default: `http://localhost:8000/api/` (lihat `lib/api/api_service.dart`).

Backend harus aktif dengan REST API (`docs/ROADMAP_MOBILE.md`) dan penanggung
jawab sudah dibuat via Django Admin (`/admin/`), contoh: `pj1` / `pj12345`
(setelah `python manage.py seed_data`).

## Catatan Platform

- **Web/Windows**: untuk pengembangan & demo. API backend harus menerima request
  dari origin tersebut (untuk produksi cukup pakai CORS sesuai kebutuhan).
- **Android**: build APK butuh Android SDK. Token disimpan aman
  (`flutter_secure_storage`; di web memakai `shared_preferences` karena
  dukungan secure storage web belum penuh).