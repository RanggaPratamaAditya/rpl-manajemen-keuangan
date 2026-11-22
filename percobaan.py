"""Pembatasan percobaan login (disimpan di memori; berlaku per proses).

Untuk rilis dengan beberapa proses, ganti penyimpanan dengan yang dipakai bersama
(mis. basis data atau cache); logika di sini tetap menjadi acuan."""
import time

BATAS = 5        # jumlah kegagalan yang diizinkan
JENDELA = 300    # detik (5 menit); kegagalan lebih lama dari ini dilupakan

_gagal = {}


def _bersihkan(kunci, sekarang):
    _gagal[kunci] = [t for t in _gagal.get(kunci, []) if sekarang - t < JENDELA]


def terkunci(kunci, sekarang=None):
    sekarang = time.monotonic() if sekarang is None else sekarang
    _bersihkan(kunci, sekarang)
    return len(_gagal[kunci]) >= BATAS


def catat_gagal(kunci, sekarang=None):
    sekarang = time.monotonic() if sekarang is None else sekarang
    _bersihkan(kunci, sekarang)
    _gagal[kunci].append(sekarang)


def reset(kunci):
    _gagal.pop(kunci, None)