### LAPORAN CAPSTONE DESIGN
### SISTEM INFORMASI PEMINJAMAN KUNCI LABORATORIUM BERBASIS WEB DENGAN NOTIFIKASI TELEGRAM

#### DOSEN PEMBIMBING
1. [Nama Dosen Pembimbing 1]

2. [Nama Dosen Pembimbing 2]

**Disusun Oleh :**

**1. [Nama Lengkap]**
**([NIM])**

**2. [Nama Lengkap]**
**([NIM])**

**3. [Nama Lengkap]**
**([NIM])**

#### PROGRAM STUDI TEKNIK INFORMATIKA
#### FAKULTAS TEKNIK
#### UNIVERSITAS DARUL 'ULUM JOMBANG
#### 2026
ii

**LEMBAR PENGESAHAN**

**LAPORAN CAPSTONE DESIGN**

**JUDUL: SISTEM INFORMASI PEMINJAMAN KUNCI LABORATORIUM BERBASIS WEB DENGAN NOTIFIKASI TELEGRAM**

**Anggota Tim :**

**1. [Nama Lengkap]**
**([NIM])**

**2. [Nama Lengkap]**
**([NIM])**

**3. [Nama Lengkap]**
**([NIM])**

Laporan ini disusun untuk memenuhi nilai pada Mata Kuliah **Capstone Design**

Mahasiswa Program Studi Teknik Informatika Fakultas Teknik

Universitas Darul 'Ulum Jombang

Jombang, [Tanggal Bulan Tahun]

Menyetujui,

Dosen Pembimbing 1
Dosen Pembimbing 2
___________________
**__________________.**
NIDN.
NIDN.

Ketua Program Studi

Teknik Informatika

**Budiman, S.Kom.,MM.,M.Kom.**

NPP. 204. 501. 115

iii

**RINGKASAN EKSEKUTIF**

Sistem Informasi Peminjaman Kunci Laboratorium merupakan sistem berbasis web yang dibangun untuk membantu penanggung jawab laboratorium dalam mengelola proses peminjaman dan pengembalian kunci secara digital. Sistem ini menggantikan pencatatan manual yang rawan kehilangan data, memakan waktu, dan sulit untuk dipantau. Fitur utama sistem meliputi pengelolaan data master (mahasiswa, dosen, laboratorium, kunci, dan penanggung jawab), proses peminjaman dan pengembalian kunci dengan validasi otomatis, riwayat transaksi, laporan yang dapat diekspor ke Excel/CSV, serta dashboard statistik. Sebagai inovasi, sistem dilengkapi notifikasi otomatis ke grup Telegram penanggung jawab setiap kali terjadi peminjaman atau pengembalian kunci sehingga pemantauan dapat dilakukan secara real-time. Sistem juga menyediakan aplikasi mobile berbasis Flutter sebagai pendamping untuk melihat status kunci dan riwayat notifikasi. Pengembangan sistem menggunakan metode Waterfall dengan pendekatan pemrograman berorientasi objek. Sistem diuji menggunakan Django Test Framework dengan total 56 kasus uji yang seluruhnya berhasil.

iv

**DAFTAR ISI**

RINGKASAN EKSEKUTIF ...................................................................................... iii
DAFTAR ISI............................................................................................................. iv
DAFTAR TABEL ...................................................................................................... v
DAFTAR GAMBAR ................................................................................................. vi
DAFTAR LAMPIRAN ............................................................................................. vii

**BAB I PENDAHULUAN ......................................................................................... 1**

A. Latar Belakang Masalah .............................................................................. 1
B. Rumusan Masalah ....................................................................................... 1
C. Tujuan........................................................................................................... 1
D. Batasan Masalah ......................................................................................... 1

**BAB II TINJAUAN PUSTAKA ............................................................................... 2**

A. Landasan Teori ........................................................................................... 2

**BAB III METODE PERANCANGAN ...................................................................... 3**

A. Metode yang Digunakan .............................................................................. 3
B. Tahapan Perancangan ................................................................................ 3

**BAB IV HASIL DAN PEMBAHASAN .................................................................... 4**

A. Implementasi ................................................................................................ 4
B. Pengujian Program ...................................................................................... 4
C. Analisis Dan Pembahasan ........................................................................... 4

**BAB V KESIMPULAN DAN SARAN ..................................................................... 5**

A. KESIMPULAN .............................................................................................. 5
B. SARAN ......................................................................................................... 5
DAFTAR PUSTAKA ................................................................................................ 6
LAMPIRAN .............................................................................................................. 7

v

**DAFTAR TABEL**

Tabel 1. Spesifikasi Perangkat Keras
Tabel 2. Spesifikasi Perangkat Lunak
Tabel 3. Hasil Pengujian Program

vi

**DAFTAR GAMBAR**

Gambar 1. Use Case Diagram Sistem
Gambar 2. Arsitektur Sistem
Gambar 3. ERD / Relasi Antar Tabel
Gambar 4. Halaman Dashboard
Gambar 5. Form Peminjaman Kunci
Gambar 6. Halaman Pengembalian Kunci
Gambar 7. Halaman Riwayat Transaksi
Gambar 8. Notifikasi Telegram

vii

**DAFTAR LAMPIRAN**

Lampiran 1. Dokumentasi (Foto-Foto Setiap Tahapan)
Lampiran 2. Bukti Uji Kelayakan
Lampiran 3. Screen Shoot Upload Video Presentasi berikut link nya
Lampiran 4. Barcode Coding

1

**BAB I PENDAHULUAN**

**A. Latar Belakang Masalah**

Laboratorium merupakan salah satu sarana penting dalam mendukung kegiatan praktikum dan penelitian di lingkungan kampus. Setiap laboratorium memiliki kunci yang harus dikelola oleh penanggung jawab (PJ) laboratorium. Saat ini, proses peminjaman dan pengembalian kunci laboratorium masih dilakukan secara manual menggunakan buku catatan. Cara ini memiliki berbagai kendala, antara lain: data mudah hilang atau rusak, pencatatan membutuhkan waktu, kesulitan memantau kunci yang sedang dipinjam dan oleh siapa, tidak ada peringatan otomatis ketika terjadi peminjaman, serta penyusunan laporan rekapitulasi yang membutuhkan waktu lama.

Jika permasalahan tersebut tidak diatasi, maka risiko kehilangan kunci, kesalahan pencatatan, dan kesulitan audit akan terus terjadi. Selain itu, penanggung jawab laboratorium yang hanya berjumlah satu hingga dua orang akan kesulitan memantau kondisi kunci secara real-time, terutama ketika sedang tidak berada di tempat.

Berdasarkan kendala tersebut, mitra membutuhkan sistem yang mampu mencatat peminjaman dan pengembalian kunci secara digital, memvalidasi ketersediaan kunci, membatasi peminjaman ganda oleh mahasiswa, menyajikan riwayat transaksi, serta memberikan notifikasi otomatis kepada penanggung jawab. Solusi yang ditawarkan adalah Sistem Informasi Peminjaman Kunci Laboratorium berbasis web yang dilengkapi dengan notifikasi Telegram.

**B. Rumusan Masalah**

Berdasarkan latar belakang masalah di atas, rumusan masalah pada proyek ini adalah:

1. Bagaimana merancang dan membangun sistem informasi peminjaman kunci laboratorium berbasis web yang mampu mencatat transaksi peminjaman dan pengembalian kunci secara digital?
2. Bagaimana sistem dapat memberikan notifikasi otomatis kepada penanggung jawab laboratorium setiap terjadi peminjaman dan pengembalian kunci melalui Telegram?

**C. Tujuan**

Berdasarkan rumusan masalah tersebut, tujuan dari proyek ini adalah:

1. Merancang dan membangun sistem informasi peminjaman kunci laboratorium berbasis web yang mampu mencatat transaksi peminjaman dan pengembalian kunci secara digital, dilengkapi dengan validasi ketersediaan kunci dan pembatasan peminjaman ganda.
2. Mengintegrasikan notifikasi otomatis melalui Telegram kepada penanggung jawab laboratorium setiap terjadi peminjaman dan pengembalian kunci.

**D. Batasan Masalah**

Batasan masalah dalam proyek ini adalah:

1) Pengguna sistem terdiri dari admin (petugas laboratorium) yang mengelola seluruh data, dan penanggung jawab laboratorium yang menerima notifikasi serta memantau status kunci melalui aplikasi mobile. Data yang diinput meliputi data mahasiswa, dosen, laboratorium (ruangan), kunci, dan penanggung jawab. Tahapan proses yang ada meliputi pencatatan peminjaman, pengembalian, dan penyusunan laporan. Luaran sistem berupa riwayat transaksi, laporan yang dapat diekspor, dan notifikasi otomatis.
2) Metode pengembangan perangkat lunak yang digunakan adalah Waterfall dengan pendekatan pemrograman berorientasi objek.
3) Perangkat lunak yang dibutuhkan antara lain Python 3, Django, Bootstrap 5, htmx, jQuery, Flutter, dan Telegram Bot API. Perangkat keras yang dibutuhkan adalah komputer server dan perangkat Android.
4) Teknik pengujian yang digunakan adalah pengujian otomatis menggunakan Django Test Framework dan pengujian langsung oleh pengguna (black box).

2

**BAB II TINJAUAN PUSTAKA**

**A. Landasan Teori**

1. Sistem Informasi
Sistem informasi adalah kombinasi dari teknologi informasi dan aktivitas manusia yang menggunakan teknologi tersebut untuk mendukung operasi dan manajemen. Dalam konteks proyek ini, sistem informasi digunakan untuk mengelola proses peminjaman kunci laboratorium secara terkomputerisasi.

2. Django
Django adalah kerangka kerja (framework) web berbasis bahasa pemrograman Python yang mengikuti pola arsitektur Model-View-Template (MVT). Django menyediakan berbagai fitur bawaan seperti Object Relational Mapping (ORM), autentikasi pengguna, formulir, dan sistem migrasi database yang mempercepat proses pengembangan aplikasi web.

3. REST API dan Django REST Framework
REST API (Representational State Transfer Application Programming Interface) adalah gaya arsitektur antarmuka yang memungkinkan komunikasi data antar aplikasi menggunakan metode HTTP. Django REST Framework (DRF) digunakan dalam proyek ini untuk menyediakan layanan API bagi aplikasi mobile agar dapat mengakses data status kunci dan notifikasi.

4. htmx dan AJAX
htmx adalah pustaka JavaScript yang memungkinkan halaman web melakukan permintaan HTTP secara dinamis tanpa melakukan reload penuh. Dalam proyek ini, htmx digunakan untuk memperbarui konten halaman (seperti filter kunci berdasarkan ruangan) secara real-time.

5. Bot Telegram
Telegram Bot API adalah antarmuka yang disediakan oleh Telegram untuk membuat bot otomatis yang dapat mengirim pesan ke pengguna atau grup. Bot Telegram digunakan untuk mengirim notifikasi peminjaman dan pengembalian kunci ke grup penanggung jawab secara real-time.

6. Flutter
Flutter adalah framework pengembangan aplikasi mobile yang menggunakan bahasa pemrograman Dart. Flutter digunakan untuk membangun aplikasi mobile pendamping yang berfungsi melihat status kunci dan riwayat notifikasi.

7. Waterfall
Metode Waterfall adalah model pengembangan perangkat lunak yang bersifat sekuensial, yaitu setiap tahap harus diselesaikan terlebih dahulu sebelum melanjutkan ke tahap berikutnya. Tahapannya meliputi analisis kebutuhan, desain, implementasi, pengujian, dan pemeliharaan.

3

**BAB III METODE PERANCANGAN**

**A. Metode yang Digunakan**

Metode pengembangan perangkat lunak yang digunakan pada proyek ini adalah metode Waterfall. Metode ini dipilih karena kebutuhan sistem telah didefinisikan dengan jelas di awal, sehingga proses pengembangan dapat berjalan secara terstruktur dan mudah dipahami oleh seluruh anggota tim. Pendekatan pemrograman yang digunakan adalah Pemrograman Berorientasi Objek (OOP) yang diimplementasikan melalui model, view, dan service pada framework Django.

**B. Tahapan Perancangan**

Tahapan perancangan yang dilakukan pada proyek ini sesuai dengan metode Waterfall adalah:

1. Analisis Kebutuhan
Pada tahap ini dilakukan identifikasi kebutuhan sistem melalui observasi dan wawancara dengan penanggung jawab laboratorium. Dihasilkan kebutuhan fungsional berupa pengelolaan data master, pencatatan peminjaman/pengembalian, validasi ketersediaan kunci, pembatasan peminjaman ganda, penyusunan laporan, dan notifikasi Telegram.

2. Desain Sistem
Pada tahap ini dilakukan perancangan arsitektur sistem, struktur database (ERD), antarmuka pengguna, serta alur proses peminjaman dan pengembalian. Desain mencakup halaman dashboard, form peminjaman, halaman pengembalian, riwayat, laporan, dan modul notifikasi.

3. Implementasi
Pada tahap ini sistem diimplementasikan menggunakan Python Django untuk backend, Bootstrap 5 dan htmx untuk frontend, serta Flutter untuk aplikasi mobile. Integrasi notifikasi dilakukan menggunakan Telegram Bot API. Fitur validasi seperti kesesuaian kunci dengan ruangan dan pembatasan peminjaman ganda mahasiswa diimplementasikan pada lapisan form dan service.

4. Pengujian
Pada tahap ini dilakukan pengujian sistem menggunakan Django Test Framework untuk menguji fungsi utama seperti peminjaman, pengembalian, validasi, dan notifikasi. Pengujian juga dilakukan secara langsung oleh penanggung jawab laboratorium untuk memastikan sistem sesuai kebutuhan.

5. Pemeliharaan
Pada tahap ini dilakukan pemantauan dan perbaikan sistem setelah digunakan, termasuk pemeliharaan data dan penyesuaian terhadap kebutuhan baru.

4

**BAB IV HASIL DAN PEMBAHASAN**

**A. Implementasi**

Implementasi sistem dilakukan sesuai dengan desain yang telah dibuat. Halaman-halaman yang diimplementasikan antara lain:

1. Halaman Login
Halaman login digunakan untuk mengautentikasi pengguna sebelum mengakses sistem. [Screenshot Halaman Login]

2. Halaman Dashboard
Halaman dashboard menampilkan statistik total kunci, jumlah kunci tersedia, jumlah kunci dipinjam, jumlah peminjaman hari ini, serta tabel aktivitas. [Screenshot Halaman Dashboard]

3. Halaman Master Data
Halaman master data digunakan untuk mengelola data mahasiswa, dosen, laboratorium (ruangan), kunci, dan penanggung jawab. Tersedia fitur pencarian, tambah, ubah, hapus, serta import data dari Excel. [Screenshot Halaman Master Data]

4. Halaman Peminjaman
Halaman form peminjaman digunakan untuk mencatat peminjaman kunci. Sistem memvalidasi kesesuaian kunci dengan ruangan dan menolak peminjaman apabila mahasiswa masih memiliki peminjaman aktif. [Screenshot Halaman Peminjaman]

5. Halaman Pengembalian
Halaman pengembalian menampilkan daftar kunci yang sedang dipinjam dan digunakan untuk mencatat proses pengembalian. [Screenshot Halaman Pengembalian]

6. Halaman Riwayat
Halaman riwayat menampilkan seluruh transaksi peminjaman dan pengembalian dengan filter berdasarkan status, ruangan, dosen, dan program studi. [Screenshot Halaman Riwayat]

7. Halaman Laporan
Halaman laporan menyediakan rekapitulasi transaksi yang dapat diekspor ke format Excel dan CSV. [Screenshot Halaman Laporan]

8. Notifikasi Telegram
Setiap kali terjadi peminjaman atau pengembalian kunci, sistem mengirim notifikasi otomatis ke grup Telegram penanggung jawab dengan format yang informatif, meliputi nama mahasiswa, nomor kunci, nama laboratorium, dan jam kejadian. [Screenshot Notifikasi Telegram]

9. Aplikasi Mobile
Aplikasi mobile berbasis Flutter menampilkan status kunci dan riwayat notifikasi kepada penanggung jawab. [Screenshot Aplikasi Mobile]

**B. Pengujian Program**

Pengujian program dilakukan menggunakan Django Test Framework untuk menguji fungsi-fungsi utama sistem. Total terdapat 56 kasus uji yang seluruhnya berhasil (OK). Beberapa pengujian yang dilakukan antara lain:

Tabel 1. Hasil Pengujian Program

| No | Modul | Kasus Uji | Hasil |
|----|-------|-----------|-------|
| 1 | Autentikasi | Login dengan kredensial benar | Berhasil |
| 2 | Autentikasi | Login dengan kredensial salah | Ditolak |
| 3 | Master Data | Tambah/ubah/hapus mahasiswa | Berhasil |
| 4 | Master Data | Import data mahasiswa dari Excel | Berhasil |
| 5 | Transaksi | Peminjaman kunci tersedia | Berhasil |
| 6 | Transaksi | Penolakan kunci tidak sesuai ruangan | Ditolak |
| 7 | Transaksi | Penolakan peminjaman ganda mahasiswa | Ditolak |
| 8 | Transaksi | Pengembalian kunci | Berhasil |
| 9 | Transaksi | Peminjaman mencatat jam server otomatis | Berhasil |
| 10 | Notifikasi | Pembuatan notifikasi peminjaman | Berhasil |
| 11 | Notifikasi | Pembuatan notifikasi pengembalian | Berhasil |
| 12 | Laporan | Filter dan ekspor laporan | Berhasil |

Selain pengujian otomatis, dilakukan pengujian langsung oleh penanggung jawab laboratorium (uji kelayakan dengan mitra) dengan dokumentasi terlampir.

**C. Analisis Dan Pembahasan**

Berdasarkan hasil implementasi dan pengujian, sistem yang dibangun mampu mengatasi permasalahan yang dihadapi oleh mitra. Pencatatan peminjaman dan pengembalian kunci yang sebelumnya manual kini terkomputerisasi dengan validasi otomatis, sehingga risiko kesalahan pencatatan dan peminjaman ganda dapat diminimalkan. Notifikasi Telegram memungkinkan penanggung jawab memantau aktivitas secara real-time meskipun tidak berada di lokasi.

**1. Kelebihan Sistem**

a) Proses peminjaman dan pengembalian kunci tercatat secara digital dan rapi.
b) Validasi otomatis mencegah peminjaman kunci yang tidak tersedia, kunci yang tidak sesuai ruangan, dan peminjaman ganda oleh mahasiswa.
c) Notifikasi otomatis melalui Telegram memudahkan pemantauan real-time.
d) Laporan rekapitulasi dapat diekspor ke Excel dan CSV dengan mudah.
e) Fitur import data dari Excel mempercepat pengelolaan data master.
f) Tersedia aplikasi mobile sebagai pendamping pemantauan status kunci.

**2. Kekurangan Sistem**

a) Akses sistem melalui aplikasi mobile masih terbatas pada jaringan lokal (LAN) dan belum dapat diakses dari luar kampus.
b) Notifikasi Telegram membutuhkan koneksi internet agar dapat terkirim.
c) Belum terdapat fitur manajemen denda keterlambatan pengembalian.
d) Belum terdapat fitur pencadangan (backup) data otomatis.

5

**BAB V KESIMPULAN DAN SARAN**

**A. KESIMPULAN**

Berdasarkan hasil perancangan, implementasi, dan pengujian yang telah dilakukan, dapat disimpulkan bahwa:

1. Sistem Informasi Peminjaman Kunci Laboratorium berbasis web berhasil dirancang dan dibangun menggunakan Django dengan fitur pengelolaan data master, pencatatan peminjaman dan pengembalian, validasi ketersediaan kunci dan kesesuaian ruangan, pembatasan peminjaman ganda mahasiswa, riwayat transaksi, serta laporan yang dapat diekspor ke Excel dan CSV.
2. Sistem berhasil diintegrasikan dengan notifikasi otomatis Telegram yang mengirim pesan ke grup penanggung jawab setiap terjadi peminjaman dan pengembalian kunci, sehingga pemantauan dapat dilakukan secara real-time.
3. Tujuan proyek tercapai ditunjukkan dengan seluruh 56 kasus uji berhasil, dan sistem telah diuji kelayakannya oleh penanggung jawab laboratorium.

**B. SARAN**

Untuk pengembangan sistem selanjutnya, disarankan:

1. Mengembangkan akses aplikasi mobile agar dapat diakses dari luar jaringan lokal melalui server publik atau teknologi tunnel sehingga penanggung jawab dapat memantau dari mana saja.
2. Menambahkan fitur manajemen denda keterlambatan pengembalian kunci.
3. Menambahkan fitur pencadangan (backup) data otomatis untuk mencegah kehilangan data.
4. Mengembangkan notifikasi tambahan seperti email sebagai alternatif apabila Telegram tidak dapat diakses.

6

**DAFTAR PUSTAKA**

DAFTAR PUSTAKA DITULIS MENGGUNAKAN HARVARD STYLE

7

**LAMPIRAN**

**1.** Dokumentasi (Foto-Foto Setiap Tahapan)

**2.** Bukti Uji Kelayakan

**3.** Screen Shoot Upload Video Presentasi berikut link nya

**4.** Barcode Coding
