# Rekap Bahan Bab 4 (Pengujian, UAT, dan Refleksi Vibe Coding)

1. **Pengujian Fungsional & Otomatis:** 7 Kebutuhan Fungsional (`KF-01` s.d. `KF-07`) tercakup oleh 24 *test case* (`docs/pengujian/test-case.md`), 45 uji otomatis `pytest` (`45 passed`), dan uji regresi `tests/uji_cepat.py` (`SEMUA UJI LULUS`).
2. **Laporan Cacat & Perbaikan:** 3 cacat nyata (`D-01` digit Unicode, `D-02` batas atas nominal 1 miliar, `D-03` format tanggal tanpa tanda hubung) telah diperbaiki dengan alur merah -> hijau dan commit terpisah (`docs/pengujian/laporan-cacat.md`).
3. **Hasil UAT & Skor SUS:** Seluruh 6 skenario inti (`UAT-1` s.d. `UAT-6`) lulus tanpa cacat Kritis/Tinggi; rata-rata skor SUS dan triase umpan balik tercatat pada `docs/uat/hasil-uat.md`.
4. **Rekap Jurnal Vibe Coding:** Total 71 entri sejak awal proyek hingga rilis `v1.0.0` (Jobsheet 14 menambah 8 entri baru: Entri 64–71), menunjukkan disiplin tinjauan kode, pengujian mutasi, dan verifikasi dokumentasi terhadap keluaran AI.