# Laporan Temuan Code Review dan Keamanan

## Bagian A — Lima Temuan Terpenting Kasus Latihan (`kasus_rentan.py`)

### T-01  Injeksi SQL pada proses login
- Lokasi   : `kasus_rentan.py` nomor (4) — rute `/login`
- Kategori : A05 Injection
- Deskripsi: Query SQL disambung langsung memakai f-string dengan masukan `username` dan `password_hash`.
- Bukti    : Mengirim `username = pemilik'--` dan sandi acak pada `POST /login` berhasil masuk sebagai `pemilik`.
- Dampak   : Penyerang dapat mengambil alih akun apa pun tanpa mengetahui kata sandi.
- Risiko   : Tinggi
- Perbaikan: Gunakan SQL berparameter (`WHERE username = ?`) dan verifikasi sandi dengan `check_password_hash`.
- Status   : Diperbaiki (pada latihan)

### T-02  Hapus data lewat GET tanpa login, peran, dan CSRF
- Lokasi   : `kasus_rentan.py` nomor (7) — rute `/barang/<int:id>/hapus`
- Kategori : A01 Broken Access Control
- Deskripsi: Penghapusan data memakai metode `GET` dan tidak memeriksa sesi login maupun peran pengguna.
- Bukti    : Membuka `/barang/1/hapus` di peramban tanpa login langsung menghapus baris `Semen`.
- Dampak   : Siapa pun atau tautan lintas situs dapat menghapus data penting secara diam-diam.
- Risiko   : Tinggi
- Perbaikan: Ubah ke `methods=["POST"]`, pasang decorator peran, dan wajibkan token CSRF.
- Status   : Diperbaiki (pada latihan)

### T-03  Kunci rahasia ditulis di kode dan hash kata sandi memakai MD5
- Lokasi   : `kasus_rentan.py` nomor (2) dan (3)
- Kategori : A04 Cryptographic Failures
- Deskripsi: `app.secret_key = "rahasia123"` tertulis di kode dan kata sandi di-hash dengan `hashlib.md5` tanpa garam.
- Bukti    : `md5('sandi-karangan-1')` selalu menghasilkan nilai sama; kunci rahasia terbaca di kode sumber.
- Dampak   : Cookie sesi dapat dipalsukan dan kata sandi mudah dipecahkan bila basis data bocor.
- Risiko   : Tinggi
- Perbaikan: Baca `SECRET_KEY` dari lingkungan dan pakai `werkzeug.security.generate_password_hash`.
- Status   : Diperbaiki (pada latihan)

### T-04  Mode debug aktif dan mengikat ke seluruh jaringan (`0.0.0.0`)
- Lokasi   : `kasus_rentan.py` nomor (10) — `app.run(host="0.0.0.0", debug=True)`
- Kategori : A02 Security Misconfiguration
- Deskripsi: Server dibuka ke seluruh jaringan lokal dengan debugger interaktif aktif.
- Bukti    : Menjalankan skrip membuka port pada semua antarmuka jaringan dengan debugger aktif.
- Dampak   : Pihak di jaringan yang sama dapat mengeksekusi kode Python jarak jauh melalui konsol debugger.
- Risiko   : Tinggi
- Perbaikan: Jangan pakai `host="0.0.0.0"`; aktifkan debug hanya bila `FLASK_DEBUG=1` dan bukan produksi.
- Status   : Diperbaiki (pada latihan)

### T-05  Pesan galat membocorkan rincian internal basis data
- Lokasi   : `kasus_rentan.py` nomor (9) — rute `/laporan` (`f"Galat: {e!r}"`)
- Kategori : A10 Mishandling of Exceptional Conditions
- Deskripsi: Objek pengecualian Python ditampilkan langsung ke peramban pengguna.
- Bukti    : Membuka `/laporan` menampilkan `Galat: OperationalError('no such table: penjualan')`.
- Dampak   : Membantu penyerang memetakan nama tabel dan struktur internal basis data.
- Risiko   : Rendah–Sedang
- Perbaikan: Tampilkan pesan umum ke pengguna dan catat rincian galat ke `app.logger`.
- Status   : Diperbaiki (pada latihan)

---

## Bagian B — Tinjauan Mandiri Proyek `rpl-manajemen-keuangan` (Langkah 7)

### P-01  Formulir POST belum dilindungi token CSRF
- Lokasi   : `app.py` (seluruh rute `POST`: `/login`, `/logout`, `/kategori/*`, `/transaksi/*`) dan templat formulir
- Kategori : A01 Broken Access Control
- Deskripsi: Tidak ada verifikasi token CSRF pada permintaan `POST` yang mengubah data atau sesi.
- Bukti    : Permintaan `POST` tanpa field `csrf_token` tetap diproses oleh server selama cookie sesi aktif.
- Dampak   : Situs pihak ketiga dapat memicu penghapusan atau perubahan transaksi saat pengguna sedang login.
- Risiko   : Tinggi
- Perbaikan: Tambahkan token CSRF per sesi (`secrets.token_hex`), input tersembunyi di semua form POST, dan validasi `secrets.compare_digest` di `@app.before_request`.
- Status   : Terbuka (Diperbaiki pada Langkah 11)

### P-02  Belum ada pembatasan percobaan login dan pencatatan kejadian keamanan
- Lokasi   : `app.py` — rute `/login` dan `errorhandler(403)`
- Kategori : A07 Authentication Failures & A09 Security Logging Failures
- Deskripsi: Percobaan login gagal tidak dibatasi dan tidak dicatat ke log aplikasi.
- Bukti    : Pengujian mengirim `POST /login` berulang kali dengan sandi salah selalu dijawab `200` tanpa penguncian atau log.
- Dampak   : Rentan terhadap serangan *brute force* dan aktivitas mencurigakan tidak terdeteksi.
- Risiko   : Tinggi
- Perbaikan: Buat modul `percobaan.py` (batas 5 gagal / 5 menit -> status `429`) dan catat kejadian login/403 lewat `app.logger` tanpa kata sandi.
- Status   : Terbuka (Diperbaiki pada Langkah 12)

### P-03  Konfigurasi produksi belum menegakkan `SECRET_KEY`, `SESSION_COOKIE_SECURE`, dan mode debug
- Lokasi   : `app.py` bagian konfigurasi awal dan `if __name__ == "__main__":`
- Kategori : A02 Security Misconfiguration
- Deskripsi: `SECRET_KEY` masih memiliki *fallback* lokal tanpa memeriksa `APP_ENV=production`, `SESSION_COOKIE_SECURE` belum diatur, dan `debug=True` tertulis tetap.
- Bukti    : Aplikasi tetap berjalan dengan kunci bawaan walau `APP_ENV=production` tanpa `SECRET_KEY`.
- Dampak   : Risiko kebocoran sesi dan aktifnya debugger interaktif bila lupa diubah saat rilis.
- Risiko   : Tinggi
- Perbaikan: Hentikan aplikasi (`RuntimeError`) bila produksi tanpa `SECRET_KEY`, aktifkan `SESSION_COOKIE_SECURE=PRODUKSI`, dan kontrol `debug` lewat `FLASK_DEBUG`.
- Status   : Terbuka (Diperbaiki pada Langkah 13)

### P-04  Header keamanan HTTP dasar belum ditambahkan pada respons
- Lokasi   : `app.py` (belum ada `@app.after_request`)
- Kategori : A02 Security Misconfiguration
- Deskripsi: Respons HTTP belum menyertakan `X-Content-Type-Options`, `X-Frame-Options`, dan `Referrer-Policy`.
- Bukti    : Pemeriksaan header respons `GET /transaksi` tidak memuat ketiga header keamanan tersebut.
- Dampak   : Aplikasi lebih rentan terhadap *clickjacking* dan *MIME sniffing*.
- Risiko   : Sedang
- Perbaikan: Tambahkan `@app.after_request` yang menyetel ketiga header keamanan tersebut.
- Status   : Terbuka (Diperbaiki pada Langkah 13)

### P-05  Header Content-Security-Policy (CSP) ketat belum dapat diterapkan karena `onsubmit` sebaris
- Lokasi   : `templates/kategori_list.html` dan `templates/transaksi_list.html` (atribut `onsubmit="return confirm(...)"`)
- Kategori : A02 Security Misconfiguration / Kualitas Kode
- Deskripsi: Konfirmasi hapus masih menggunakan JavaScript sebaris (*inline handler*) yang menghambat penerapan CSP ketat.
- Bukti    : Atribut `onsubmit` tertulis langsung pada tag `<form>` di kedua templat daftar.
- Dampak   : Mempersulit penerapan `Content-Security-Policy: script-src 'self'` pada rilis produksi.
- Risiko   : Rendah
- Perbaikan: Pindahkan skrip konfirmasi ke berkas JS terpisah dan terapkan CSP pada tahap rilis.
- Status   : Ditunda (Sprint 3 / Pertemuan 14)