# Sistem Manajemen Keuangan UMKM

Aplikasi web sederhana untuk mencatat transaksi pemasukan dan pengeluaran harian, memantau ringkasan saldo, mengelola kategori, serta mengekspor rekap laporan ke CSV.
Dibuat sebagai proyek mata kuliah Rekayasa Perangkat Lunak, Prodi D3 Teknologi Informasi Politeknik Sampit.
Versi saat ini: **1.0.0** (lihat [CHANGELOG.md](CHANGELOG.md)).

## Fitur
- **Login dua peran:** `pemilik` (akses penuh: transaksi, kategori, hapus transaksi, ekspor CSV) dan `kasir` (lihat riwayat, catat dan ubah transaksi).
- **Kelola kategori:** tambah, ubah, dan hapus kategori pemasukan/pengeluaran/umum (khusus `pemilik`).
- **Riwayat & ringkasan saldo:** catat transaksi harian, pencarian keterangan aman, penyaringan jenis/bulan, serta perhitungan total pemasukan, pengeluaran, dan saldo akhir otomatis.
- **Ekspor CSV & cadangan:** unduh rekap transaksi ke `.csv` dan pencadangan basis data aman (`cadangkan.py`).

## Kebutuhan
- Python 3.10 atau lebih baru
- Git

## Instalasi
```powershell
git clone [https://github.com/RanggaPratamaAditya/rpl-manajemen-keuangan.git](https://github.com/RanggaPratamaAditya/rpl-manajemen-keuangan.git)
cd rpl-manajemen-keuangan
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt