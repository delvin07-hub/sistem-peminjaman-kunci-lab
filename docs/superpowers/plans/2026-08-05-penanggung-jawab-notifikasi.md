# Penanggung Jawab + Notifikasi + API Mobile — Implementation Plan

**For agents:** Implement task-by-task. Steps use `- [ ]` checkboxes for tracking.

**Goal:** Tambah role "penanggung jawab" (dikelola lewat Django admin), notifikasi otomatis saat kunci dipinjam/dikembalikan, dan REST API JSON untuk mobile app.

**Architecture:** Auth tetap `auth.User` default; profile `PenanggungJawab` (OneToOne → User) di `apps.authentication`; notifikasi di app baru `apps.notifications`; dibangkitkan oleh `NotifikasiService` yang dipanggil di `apps/transaction/services.py` dalam blok `@transaction.atomic`; mobile via DRF + TokenAuthentication.

**Tech:** Django 6, DRF 3.17.2 (authtoken), SQLite. Template hx SPA tidak diubah.

## Global Constraints
- Bahasa Indonesia untuk semua nama model/view/field.
- Semua FK pakai `related_name` dan `on_delete` eksplisit.
- Model inti punya `created_at`/`updated_at`.
- `NotifikasiService.buat(peminjaman, tipe)` dipanggil di dalam blok `@transaction.atomic`.
- API pakai `IsAuthenticated` + permission kustom `IsPenanggungJawab`.
- `requirements.txt` tambah `djangorestframework>=3.17`.
- Commit per task: `feat:`/`refactor:` ringkas.

## File Structure
- **Create** `apps/notifications/`: `__init__.py`, `apps.py`, `models.py`, `services.py`, `admin.py`, `serializers.py`, `permissions.py`, `views.py`, `urls.py`, `tests.py`, `migrations/`
- **Modify** `apps/authentication/models.py` — model `PenanggungJawab`
- **Modify** `apps/authentication/admin.py` — custom form create user
- **Modify** `apps/transaction/services.py` — hook NotifikasiService
- **Modify** `config/settings.py` — INSTALLED_APPS + REST_FRAMEWORK
- **Modify** `config/urls.py` — mount `/api/`
- **Modify** `requirements.txt`
- **Modify** `apps/master_data/management/commands/seed_data.py` — contoh PJ
- **Create** `docs/ROADMAP_MOBILE.md`
- **Modify/test** `apps/authentication/tests.py`, `apps/notifications/tests.py`, `apps/transaction/tests.py`

---

### Task 1: Setup DRF + app notifications

- [ ] **Step 1: `requirements.txt`** — tambah `djangorestframework>=3.17`
- [ ] **Step 2: `apps/notifications/__init__.py`** — file kosong
- [ ] **Step 3: `apps/notifications/apps.py`** — `NotificationsConfig`
- [ ] **Step 4: `config/settings.py`** — tambah `rest_framework`, `rest_framework.authtoken`, `apps.notifications`; blok `REST_FRAMEWORK` (Token + Session auth, IsAuthenticated, PageNumberPagination PAGE_SIZE 20)
- [ ] **Step 5: `config/urls.py`** — `path('api/', include('apps.notifications.urls'))`
- [ ] **Step 6: `apps/notifications/urls.py`** — isi kosong dulu
- [ ] **Step 7: Verifikasi & migrasi** — `manage.py check` lalu `manage.py migrate` (tabel authtoken)
- [ ] **Step 8: Commit** `feat: setup DRF + aplikasi notifikasi`

## Task 2: Model PenanggungJawab

- [ ] **Step 1: tests.py** — model test: `__str__` nama_lengkap, reverse `user.penanggung_jawab`, `aktif` default True
- [ ] **Step 2: run test → FAIL**
- [ ] **Step 3: models.py** — `PenanggungJawab` (user OneToOne auth.User related_name='penanggung_jawab', nama_lengkap, telepon, aktif default True, created_at, updated_at; Meta verbose_name_plural 'Penanggung Jawab', ordering nama_lengkap)
- [ ] **Step 4: makemigrations + migrate + test → PASS**
- [ ] **Step 5: Commit** `feat: model PenanggungJawab`

## Task 3: Django admin PenanggungJawab

- [ ] **Step 1: tests.py** — admin create test: POST ke `/admin/authentication/penanggungjawab/add/` membuat User + password + profile
- [ ] **Step 2: run → FAIL**
- [ ] **Step 3: admin.py** — `PenanggungJawabAdminForm` (username, password fields; saat edit password opsional; save membuat `User` bila belum ada dan `set_password`)
- [ ] **Step 4: register** `@admin.register(PenanggungJawab)` list_display `['nama_lengkap','telepon','aktif','user']`, list_filter `['aktif']`, search_fields
- [ ] **Step 5: run test → PASS**
- [ ] **Step 6: Commit** `feat: admin PenanggungJawab dengan form create user`

## Task 4: Model & service Notifikasi

- [ ] **Step 1: tests.py** — `NotifikasiServiceTest`: buat PJ aktif + peminjaman; `NotifikasiService.buat(peminjaman,'Dipinjam')` menghasilkan 1 Notifikasi per PJ aktif
- [ ] **Step 2: run → FAIL**
- [ ] **Step 3: models.py** — `Notifikasi` (penanggung_jawab FK 'authentication.PenanggungJawab' related_name='notifikasi', peminjaman FK 'transaction.Peminjaman' null/blank related_name='notifikasi', tipe choices ['Dipinjam','Dikembalikan'], pesan CharField, dibaca BooleanField default False, created_at; Meta ordering ['-created_at'])
- [ ] **Step 4: services.py** — `NotifikasiService.buat(peminjaman, tipe)` + `_bentuk_pesan`; loop semua `PenanggungJawab.objects.filter(aktif=True)` create notifikasi
- [ ] **Step 5: makemigrations + migrate + test → PASS**
- [ ] **Step 6: Commit** `feat: model & service notifikasi`

## Task 5: Hook di PeminjamanService

- [ ] **Step 1: transaction/tests.py** — hook test: service `pinjam_kunci` menghasilkan notifikasi 'Dipinjam', `kembalikan_kunci` menghasilkan 'Dikembalikan'
- [ ] **Step 2: run → FAIL**
- [ ] **Step 3: transaction/services.py** — import NotifikasiService; panggil `NotifikasiService.buat(peminjaman, 'Dipinjam')` di akhir `pinjam_kunci`, `('Dikembalikan')` di akhir `kembalikan_kunci` (di dalam `@transaction.atomic`)
- [ ] **Step 4: run test → PASS**
- [ ] **Step 5: Commit** `feat: hook notifikasi di PeminjamanService`

## Task 6: REST API

- [ ] **Step 1: permissions.py** — `IsPenanggungJawab`: user authenticated && hasattr user.penanggung_jawab && aktif
- [ ] **Step 2: serializers.py** — `NotifikasiSerializer`, `KunciStatusSerializer` (kunci + lab), `PenanggungJawabSerializer`
- [ ] **Step 3: views.py** — `NotifikasiListView` (list milik user, filter `dibaca` query param), `NotifikasiBacaView` (RetrieveUpdate → set dibaca=True), `KunciStatusListView`
- [ ] **Step 4: urls.py** — `/api/token/` (obtain_auth_token), `/api/notifikasi/`, `/api/notifikasi/<pk>/baca/`, `/api/status-kunci/`
- [ ] **Step 5: API tests** — token login 200, list notifikasi pakai Token header, status-kunci 200
- [ ] **Step 6: check + test + migrate → Commit** `feat: API notifikasi & status kunci`

## Task 6: Seed + Roadmap

- [ ] **Step 1: seed_data.py** — buat user `pj1`/`pj12345` + PenanggungJawab `Penanggung Jawab Lab` bila belum ada
- [ ] **Step 2: `docs/ROADMAP_MOBILE.md`** — endpoint, contoh JSON, alur login token, saran Flutter, backlog (push FCM, realtime)
- [ ] **Step 3: Commit**

## Task 7: Final verification

- [ ] `python manage.py check` — no errors
- [ ] `python manage.py test apps.authentication apps.notifications apps.transaction -v 1` — all pass
- [ ] `git status` clean
- [ ] Ringkas hasil ke user