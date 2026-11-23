# Catatan Perubahan

Format: [versi] - tanggal. Bagian: Ditambahkan, Diubah, Diperbaiki, Keamanan.

## [1.0.0] - 2026-11-23
### Ditambahkan
- Login dengan dua peran (`pemilik` dan `kasir`) serta pembatasan akses per peran di server.
- Kelola kategori pemasukan/pengeluaran (`pemilik`) dan pencatatan transaksi harian dengan ringkasan saldo otomatis.
- Pencarian keterangan aman (`LIKE ? ESCAPE '\'`) serta penyaringan jenis dan bulan.
- Ekspor rekap transaksi ke format CSV (`pemilik`) dan pencadangan basis data (`python cadangkan.py`).
### Diperbaiki
- Menolak digit angka Unicode (`²`) dan nominal di atas 1 miliar agar tidak memicu galat 500 (`D-01`, `D-02`).
- Mewajibkan format tanggal `TTTT-BB-HH` dengan tanda hubung (`D-03`).
### Keamanan
- Proteksi token CSRF pada seluruh formulir POST, pembatasan percobaan login (`429`), pencatatan log keamanan, header keamanan HTTP, dan konfigurasi `SECRET_KEY` dari lingkungan.