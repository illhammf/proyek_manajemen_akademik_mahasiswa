"""Pengujian sederhana untuk memastikan fungsi inti berjalan."""

import tempfile
import unittest
from akademik_app.models import Mahasiswa, Dosen, MataKuliah
from akademik_app.services import Akademik
from akademik_app.storage import FileManager


class TestAkademik(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=True)
        self.akademik = Akademik("Test Akademik", FileManager(self.temp_file.name))
        self.akademik.tambah_mahasiswa(Mahasiswa("2024001", "Aulia", "aulia@mail.com", "SI", 2024))
        self.akademik.tambah_dosen(Dosen("D001", "Raka", "raka@mail.com", "OOP"))
        self.akademik.tambah_mata_kuliah(MataKuliah("MK001", "Bahasa Pemrograman", 3, 1))

    def test_tambah_mahasiswa(self):
        hasil = self.akademik.tambah_mahasiswa(Mahasiswa("2024002", "Bima", "bima@mail.com", "SI", 2024))
        self.assertTrue(hasil)
        self.assertEqual(len(self.akademik.daftar_mahasiswa()), 2)

    def test_dosen_pengampu(self):
        hasil = self.akademik.tetapkan_dosen_pengampu("MK001", "D001")
        self.assertTrue(hasil)
        self.assertEqual(self.akademik.cari_mata_kuliah("MK001").get_nip_dosen(), "D001")

    def test_buat_krs_dan_tambah_mk(self):
        krs = self.akademik.buat_krs("2024001", 1, "2024/2025")
        self.assertTrue(self.akademik.tambah_mk_ke_krs(krs.get_id_krs(), "MK001"))
        self.assertEqual(krs.total_sks(), 3)

    def test_input_nilai(self):
        krs = self.akademik.buat_krs("2024001", 1, "2024/2025")
        self.akademik.tambah_mk_ke_krs(krs.get_id_krs(), "MK001")
        self.akademik.input_nilai(krs.get_id_krs(), "MK001", 80, 85, 90)
        self.assertEqual(krs.get_nilai()[0].konversi_huruf(), "A")

    def test_simpan_dan_muat_data(self):
        self.akademik.simpan_data()
        akademik_baru = Akademik("Baru", FileManager(self.temp_file.name))
        akademik_baru.muat_data()
        self.assertEqual(len(akademik_baru.daftar_mahasiswa()), 1)


if __name__ == "__main__":
    unittest.main()
