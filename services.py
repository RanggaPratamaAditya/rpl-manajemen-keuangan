JENIS_KATEGORI_VALID = ("pemasukan", "pengeluaran", "umum")


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