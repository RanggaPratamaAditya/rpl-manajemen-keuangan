# Laporan Cacat dan Permintaan Perubahan

## Bagian A — Daftar Cacat (Defects)

### D-01  Angka Unicode pada nominal transaksi memicu galat internal (ValueError / HTTP 500)
- Ditemukan : 2026-11-23 oleh Rangga Pratama Aditya lewat TC-12 & uji eksploratif no. 1
- Langkah   : 1) Buka `/transaksi/tambah`. 2) Isi nominal dengan karakter angka Unicode `"²"` (pangkat dua). 3) Kirim formulir.
- Aktual    : `nominal_teks.isdigit()` bernilai `True`, lalu `int("²")` memicu `ValueError: invalid literal for int() with base 10: '²'` (galat 500).
- Diharapkan: Ditolak oleh validasi server dengan pesan `"Nominal harus berupa angka lebih dari 0 (maksimal 1.000.000.000)."` tanpa galat 500.
- Keparahan : Sedang (menyebabkan galat 500 untuk masukan tertentu, tidak merusak data tersimpan)
- Prioritas : Segera (Sprint 3)
- Penyebab  : Metode `str.isdigit()` pada Python mengembalikan `True` untuk karakter digit non-ASCII seperti `'²'` dan `'٣'`, padahal `int()` hanya menerima digit ASCII `0-9`.
- Perbaikan : Menambahkan pemeriksaan `teks.isascii() and teks.isdigit()` pada helper `_bilangan_positif()` di `services.py`. (Status awal: Terbuka -> diperbarui setelah commit perbaikan)
- Status    : Terbuka

### D-02  Nominal raksasa di atas 1 miliar lolos validasi dan berisiko memicu OverflowError di SQLite
- Ditemukan : 2026-11-23 oleh Rangga Pratama Aditya lewat TC-11 & uji eksploratif no. 2
- Langkah   : 1) Buka `/transaksi/tambah`. 2) Isi nominal dengan `"1000000001"` atau 30 digit angka `"9"`. 3) Kirim formulir.
- Aktual    : Validasi `services.py` meloloskan angka di atas 1 miliar; untuk 30 digit memicu `OverflowError: Python int too large to convert to SQLite INTEGER`.
- Diharapkan: Ditolak oleh validasi server karena melampaui batas atas `1.000.000.000` yang disepakati pada kamus data.
- Keparahan : Sedang (melanggar batas kamus data dan memicu galat 500 untuk bilangan > 64-bit)
- Prioritas : Segera (Sprint 3)
- Penyebab  : Fungsi `validasi_transaksi()` hanya memeriksa `nominal <= 0` tanpa batas panjang digit maupun konstanta batas atas `BATAS_NOMINAL = 1_000_000_000`.
- Perbaikan : Menetapkan `BATAS_NOMINAL = 1_000_000_000` dan memeriksa `len(teks) <= 10` serta `1 <= angka <= BATAS_NOMINAL` di `services.py`.
- Status    : Terbuka

### D-03  Tanggal ISO tanpa tanda hubung (`20261123`) diterima oleh validasi
- Ditemukan : 2026-11-23 oleh Rangga Pratama Aditya lewat TC-19 & uji eksploratif no. 3
- Langkah   : 1) Buka `/transaksi/tambah` (atau kirim POST). 2) Isi tanggal dengan `"20261123"` (tanpa `-`).
- Aktual    : Validasi menerima masukan dan menyimpan `"20261123"`, merusak konsistensi format `TTTT-BB-HH` serta filter `substr(tanggal, 1, 7)` pada pencarian per bulan.
- Diharapkan: Ditolak dengan pesan `"Tanggal harus berformat TTTT-BB-HH."`.
- Keparahan : Rendah (data tersimpan, namun format tanggal tidak seragam dan memengaruhi filter bulanan)
- Prioritas : Sprint ini (Sprint 3)
- Penyebab  : Pada Python 3.11+, `date.fromisoformat()` menerima format ISO dasar `YYYYMMDD` tanpa tanda hubung.
- Perbaikan : Menambahkan pemeriksaan pola regex `^[0-9]{4}-[0-9]{2}-[0-9]{2}$` sebelum memanggil `date.fromisoformat(tanggal)` di `services.py`.
- Status    : Terbuka

---

## Bagian B — Permintaan Perubahan (Change Requests — Di Luar Cacat)

### CR-01  Penolakan nama kategori duplikat yang hanya berbeda huruf besar-kecil
- Sumber    : Uji eksploratif no. 5 (`"Penjualan"` dan `"penjualan"` dapat disimpan bersamaan).
- Analisis  : Secara spesifikasi saat ini, kendala `UNIQUE` SQLite bersifat peka huruf besar-kecil (*case-sensitive*), sehingga bukan cacat kode, melainkan keputusan aturan bisnis yang akan dikonfirmasi ke klien saat UAT Minggu 14 (`COLLATE NOCASE`).