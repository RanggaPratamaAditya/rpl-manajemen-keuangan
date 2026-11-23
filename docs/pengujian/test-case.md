# Dokumen Pengujian: Matriks Keterlacakan & Test Case

## 1. Matriks Keterlacakan Kebutuhan (RTM)

| KF | Kebutuhan Fungsional | Kriteria Penerimaan (PRD & Kamus Data) | Test Case |
|---|---|---|---|
| **KF-01** | Kelola Kategori (`pemilik`) | Pemilik dapat menambah, mengubah, dan menghapus kategori yang belum dipakai transaksi; nama kategori wajib (1–50 karakter) dan unik. | TC-13, TC-14, TC-15, TC-24 |
| **KF-02** | Catat Transaksi Harian | Pengguna dapat mencatat pemasukan/pengeluaran; tanggal wajib format `TTTT-BB-HH` valid; keterangan 1–50 karakter; nominal bilangan bulat `1..1.000.000.000`; kategori valid. | TC-01 s.d. TC-12, TC-16 s.d. TC-19, TC-21 |
| **KF-03** | Daftar Transaksi & Ringkasan Saldo | Riwayat transaksi tampil berurutan terbaru dengan nama kategori (`JOIN`), serta total pemasukan, total pengeluaran, dan saldo akhir terhitung akurat. | TC-21, TC-22 |
| **KF-04** | Ubah & Hapus Transaksi | Pemilik dan kasir dapat mengubah transaksi; hanya pemilik yang dapat menghapus transaksi lewat `POST` + token CSRF. | TC-22, TC-24 |
| **KF-05** | Pencarian & Penyaringan Transaksi | Pencarian keterangan (`?q=`) aman dari SQL injection dan karakter `%`/`_` di-escape; dapat digabung dengan filter `?jenis=` dan `?bulan=`. | TC-23 |
| **KF-06** | Ekspor Rekap CSV | Pemilik dapat mengunduh rekap transaksi dalam format `.csv` dengan header baku. | TC-24 |
| **KF-07** | Autentikasi & Otorisasi Peran | Pembuatan akun mewajibkan username 3–30 karakter (`[A-Za-z0-9_]`), sandi minimal 8 karakter ter-hash; akses rute ditegakkan di server untuk tamu, kasir, dan pemilik. | TC-20, TC-24 |

---

## 2. Tabel Test Case (EP, BVA, Pelanggaran, dan Normal)

| ID | KF | Teknik | Masukan / Langkah | Hasil Diharapkan (dari Spesifikasi) | Hasil Aktual | Status |
|---|---|---|---|---|---|---|
| **TC-01** | KF-02 | BVA | `nominal = "1"` (batas bawah valid) | Diterima (`galat == []`, `nominal == 1`) | `galat == []`, `nominal == 1` | Lulus |
| **TC-02** | KF-02 | BVA | `nominal = "2"` (tepat di atas batas bawah) | Diterima (`galat == []`, `nominal == 2`) | `galat == []`, `nominal == 2` | Lulus |
| **TC-03** | KF-02 | EP | `nominal = "150000"` (nilai tipikal valid) | Diterima (`galat == []`, `nominal == 150000`) | `galat == []`, `nominal == 150000` | Lulus |
| **TC-04** | KF-02 | EP | `nominal = " 5000 "` (spasi di pinggir) | Diterima setelah dipangkas (`nominal == 5000`) | `galat == []`, `nominal == 5000` | Lulus |
| **TC-05** | KF-02 | BVA | `nominal = "1000000000"` (batas atas 1 miliar) | Diterima (`galat == []`, `nominal == 1000000000`) | `galat == []`, `nominal == 1000000000` | Lulus |
| **TC-06** | KF-02 | BVA | `nominal = "0"` (tepat di bawah batas bawah) | Ditolak dengan pesan nominal harus lebih dari 0 | Ditolak sesuai pesan | Lulus |
| **TC-07** | KF-02 | Pelanggaran | `nominal = "-500"` (bilangan negatif) | Ditolak dengan pesan nominal harus lebih dari 0 | Ditolak sesuai pesan | Lulus |
| **TC-08** | KF-02 | Pelanggaran | `nominal = "12.5"` (bilangan pecahan) | Ditolak dengan pesan nominal harus lebih dari 0 | Ditolak sesuai pesan | Lulus |
| **TC-09** | KF-02 | Pelanggaran | `nominal = "abc"` (bukan angka) | Ditolak dengan pesan nominal harus lebih dari 0 | Ditolak sesuai pesan | Lulus |
| **TC-10** | KF-02 | Pelanggaran | `nominal = ""` (kosong) | Ditolak dengan pesan nominal harus lebih dari 0 | Ditolak sesuai pesan | Lulus |
| **TC-11** | KF-02 | BVA | `nominal = "1000000001"` (tepat di atas batas atas) | Ditolak oleh validasi (bukan galat 500) | **Diterima salah (`galat == []`) -> Calon Cacat D-02** | **Gagal** |
| **TC-12** | KF-02 | Pelanggaran | `nominal = "²"` (angka Unicode pangkat dua) | Ditolak oleh validasi (bukan `ValueError` 500) | **Memicu `ValueError` -> Calon Cacat D-01** | **Gagal** |
| **TC-13** | KF-01 | Normal | `nama_kategori = "Penjualan"`, `jenis_default = "pemasukan"` | Diterima (`galat == []`) | `galat == []` | Lulus |
| **TC-14** | KF-01 | BVA | `nama_kategori = "a" * 50` vs `"a" * 51` | 50 karakter diterima; 51 karakter ditolak | 50 diterima; 51 ditolak | Lulus |
| **TC-15** | KF-01 | Pelanggaran | `nama_kategori = "   "` (hanya spasi) | Ditolak dengan pesan nama kategori wajib diisi | Ditolak sesuai pesan | Lulus |
| **TC-16** | KF-02 | Normal | `tanggal = "2026-11-23"` (format ISO `TTTT-BB-HH`) | Diterima (`galat == []`) | `galat == []` | Lulus |
| **TC-17** | KF-02 | Pelanggaran | `tanggal = "2026-02-30"` (tanggal tidak ada di kalender) | Ditolak dengan pesan format tanggal | Ditolak sesuai pesan | Lulus |
| **TC-18** | KF-02 | Pelanggaran | `tanggal = "23-11-2026"` (urutan `HH-BB-TTTT`) | Ditolak dengan pesan format tanggal | Ditolak sesuai pesan | Lulus |
| **TC-19** | KF-02 | Pelanggaran | `tanggal = "20261123"` (tanpa tanda hubung) | Ditolak dengan pesan format tanggal `TTTT-BB-HH` | **Diterima salah (`galat == []`) -> Calon Cacat D-03** | **Gagal** |
| **TC-20** | KF-07 | BVA | `username` (2, 3, 30, 31 karakter) & `password` (7, 8 karakter) | `3..30` & `>= 8` diterima; `2`, `31`, dan sandi `7` ditolak | Sesuai harapan | Lulus |
| **TC-21** | KF-02, KF-03 | Normal | Pemilik mencatat pemasukan `250000` & pengeluaran `50000` lewat HTTP | Tersimpan, tampil di daftar dengan nama kategori, saldo `200000` | Tersimpan & saldo `200000` | Lulus |
| **TC-22** | KF-03, KF-04 | EP | Pemilik mengubah nominal transaksi lalu menghapus transaksi lewat POST | Saldo terbarui otomatis setelah ubah dan kembali `0` setelah hapus | Sesuai harapan | Lulus |
| **TC-23** | KF-05 | Pelanggaran | Cari `?q=%25` (persen harfiah) dan `?q=' OR 1=1 --` | `%25` hanya cocok dengan `"Diskon 100%"`; SQLi tidak mengembalikan data | Sesuai harapan | Lulus |
| **TC-24** | KF-01, KF-04, KF-06, KF-07 | Pelanggaran | Matriks akses rute × peran (`tamu`, `kasir`, `pemilik`) & POST tanpa CSRF | Tamu -> `302`; Kasir -> `403` pada `/kategori`, `/ekspor`, hapus; tanpa CSRF -> `400` | Sesuai harapan | Lulus |