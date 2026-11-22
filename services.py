from datetime import date

JENIS_KATEGORI_VALID = ("pemasukan", "pengeluaran", "umum")
JENIS_TRANSAKSI_VALID = ("pemasukan", "pengeluaran")


def validasi_kategori(form):
    """Kembalikan (data, daftar_galat) sesuai aturan kamus-data.md."""
    galat = []
    nama = (form.get("nama_kategori") or "").strip()
    jenis = (form.get("jenis_default") or "").strip()

    if not nama:
        galat.append("Nama kategori wajib diisi.")
    elif len(nama) > 50:
        galat.append("Nama kategori maksimal 50 karakter.")

    if jenis not in JENIS_KATEGORI_VALID:
        galat.append("Jenis bawaan harus dipilih (pemasukan, pengeluaran, atau umum).")

    data = {"nama_kategori": nama, "jenis_default": jenis}
    return data, galat


def validasi_transaksi(form):
    """Validasi masukan transaksi sesuai KF-02 dan kamus-data.md."""
    galat = []
    tanggal = (form.get("tanggal") or "").strip() or date.today().isoformat()
    jenis = (form.get("jenis") or "").strip()
    keterangan = (form.get("keterangan") or "").strip()
    nominal_teks = (form.get("nominal") or "").strip()
    kategori_teks = (form.get("kategori_id") or "").strip()

    if len(tanggal) != 10:
        galat.append("Tanggal harus berformat YYYY-MM-DD.")
    if jenis not in JENIS_TRANSAKSI_VALID:
        galat.append("Jenis transaksi harus pemasukan atau pengeluaran.")
    if not keterangan:
        galat.append("Keterangan wajib diisi.")
    elif len(keterangan) > 50:
        galat.append("Keterangan maksimal 50 karakter.")

    nominal = int(nominal_teks) if nominal_teks.isdigit() else None
    if nominal is None or nominal <= 0:
        galat.append("Nominal harus berupa angka bulat positif (> 0).")

    kategori_id = int(kategori_teks) if kategori_teks.isdigit() else None
    if kategori_id is None:
        galat.append("Kategori wajib dipilih.")

    data = {
        "tanggal": tanggal,
        "jenis": jenis,
        "keterangan": keterangan,
        "nominal": nominal,
        "kategori_id": kategori_id,
    }
    return data, galat