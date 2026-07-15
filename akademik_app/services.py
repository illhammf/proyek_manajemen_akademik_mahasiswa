"""
services.py
Class Akademik menjadi pengelola utama sistem.
Class ini menyimpan koleksi object Mahasiswa, Dosen, MataKuliah, dan KRS.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Any
from .models import Mahasiswa, Dosen, MataKuliah, KRS, Nilai
from .storage import FileManager


class Akademik:
    def __init__(self, nama_institusi: str, file_manager: FileManager):
        self.__nama_institusi = nama_institusi
        self.__file_manager = file_manager
        self.__mahasiswa: Dict[str, Mahasiswa] = {}
        self.__dosen: Dict[str, Dosen] = {}
        self.__mata_kuliah: Dict[str, MataKuliah] = {}
        self.__krs: Dict[str, KRS] = {}

    def get_nama_institusi(self) -> str:
        return self.__nama_institusi

    def tambah_mahasiswa(self, mahasiswa: Mahasiswa) -> bool:
        if mahasiswa.get_nim() in self.__mahasiswa:
            return False
        self.__mahasiswa[mahasiswa.get_nim()] = mahasiswa
        return True

    def cari_mahasiswa(self, nim: str) -> Optional[Mahasiswa]:
        return self.__mahasiswa.get(nim)

    def hapus_mahasiswa(self, nim: str) -> bool:
        if nim not in self.__mahasiswa:
            return False
        del self.__mahasiswa[nim]
        self.__krs = {id_krs: krs for id_krs, krs in self.__krs.items() if krs.get_mahasiswa().get_nim() != nim}
        return True

    def daftar_mahasiswa(self) -> List[Mahasiswa]:
        return list(self.__mahasiswa.values())

    def tambah_dosen(self, dosen: Dosen) -> bool:
        if dosen.get_nip() in self.__dosen:
            return False
        self.__dosen[dosen.get_nip()] = dosen
        return True

    def cari_dosen(self, nip: str) -> Optional[Dosen]:
        return self.__dosen.get(nip)

    def hapus_dosen(self, nip: str) -> bool:
        if nip not in self.__dosen:
            return False
        del self.__dosen[nip]
        for mk in self.__mata_kuliah.values():
            if mk.get_nip_dosen() == nip:
                mk.set_dosen_pengampu("")
        return True

    def daftar_dosen(self) -> List[Dosen]:
        return list(self.__dosen.values())

    def tambah_mata_kuliah(self, mata_kuliah: MataKuliah) -> bool:
        if mata_kuliah.get_kode_mk() in self.__mata_kuliah:
            return False
        self.__mata_kuliah[mata_kuliah.get_kode_mk()] = mata_kuliah
        return True

    def cari_mata_kuliah(self, kode_mk: str) -> Optional[MataKuliah]:
        return self.__mata_kuliah.get(kode_mk)

    def daftar_mata_kuliah(self) -> List[MataKuliah]:
        return list(self.__mata_kuliah.values())

    def tetapkan_dosen_pengampu(self, kode_mk: str, nip: str) -> bool:
        mk = self.cari_mata_kuliah(kode_mk)
        dosen = self.cari_dosen(nip)
        if mk is None or dosen is None:
            return False
        mk.set_dosen_pengampu(nip)
        dosen.tambah_mata_kuliah_diampu(kode_mk)
        return True

    def buat_krs(self, nim: str, semester: int, tahun_akademik: str) -> KRS:
        mahasiswa = self.cari_mahasiswa(nim)
        if mahasiswa is None:
            raise ValueError("Mahasiswa tidak ditemukan.")
        id_krs = f"KRS-{nim}-{semester}-{tahun_akademik.replace('/', '-') }"
        if id_krs in self.__krs:
            return self.__krs[id_krs]
        krs = KRS(id_krs, mahasiswa, semester, tahun_akademik)
        self.__krs[id_krs] = krs
        return krs

    def cari_krs(self, id_krs: str) -> Optional[KRS]:
        return self.__krs.get(id_krs)

    def cari_krs_mahasiswa(self, nim: str) -> List[KRS]:
        return [krs for krs in self.__krs.values() if krs.get_mahasiswa().get_nim() == nim]

    def daftar_krs(self) -> List[KRS]:
        return list(self.__krs.values())

    def tambah_mk_ke_krs(self, id_krs: str, kode_mk: str) -> bool:
        krs = self.cari_krs(id_krs)
        mk = self.cari_mata_kuliah(kode_mk)
        if krs is None or mk is None:
            return False
        return krs.tambah_mata_kuliah(mk)

    def input_nilai(self, id_krs: str, kode_mk: str, tugas: float, uts: float, uas: float) -> None:
        krs = self.cari_krs(id_krs)
        if krs is None:
            raise ValueError("KRS tidak ditemukan.")
        nilai = Nilai(krs.get_mahasiswa().get_nim(), kode_mk, tugas, uts, uas)
        krs.tambah_atau_update_nilai(nilai)

    def laporan_ringkas(self) -> str:
        return (
            f"Laporan {self.__nama_institusi}\n"
            f"Total mahasiswa: {len(self.__mahasiswa)}\n"
            f"Total dosen: {len(self.__dosen)}\n"
            f"Total mata kuliah: {len(self.__mata_kuliah)}\n"
            f"Total KRS: {len(self.__krs)}"
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nama_institusi": self.__nama_institusi,
            "mahasiswa": [m.to_dict() for m in self.__mahasiswa.values()],
            "dosen": [d.to_dict() for d in self.__dosen.values()],
            "mata_kuliah": [mk.to_dict() for mk in self.__mata_kuliah.values()],
            "krs": [krs.to_dict() for krs in self.__krs.values()],
        }

    def simpan_data(self) -> None:
        self.__file_manager.simpan_json(self.to_dict())

    def muat_data(self) -> None:
        data = self.__file_manager.baca_json()
        if not data:
            return
        self.__nama_institusi = data.get("nama_institusi", self.__nama_institusi)
        self.__mahasiswa = {m["nim"]: Mahasiswa.from_dict(m) for m in data.get("mahasiswa", [])}
        self.__dosen = {d["nip"]: Dosen.from_dict(d) for d in data.get("dosen", [])}
        self.__mata_kuliah = {mk["kode_mk"]: MataKuliah.from_dict(mk) for mk in data.get("mata_kuliah", [])}
        self.__krs = {}
        for item in data.get("krs", []):
            mahasiswa = self.cari_mahasiswa(item["nim"])
            if mahasiswa is None:
                continue
            krs = KRS(item["id_krs"], mahasiswa, int(item["semester"]), item["tahun_akademik"])
            for kode_mk in item.get("mata_kuliah", []):
                mk = self.cari_mata_kuliah(kode_mk)
                if mk:
                    krs.tambah_mata_kuliah(mk)
            for nilai_data in item.get("nilai", []):
                krs.tambah_atau_update_nilai(Nilai.from_dict(nilai_data))
            self.__krs[krs.get_id_krs()] = krs

    def isi_data_awal(self) -> None:
        """Data contoh agar aplikasi dapat langsung didemonstrasikan."""
        self.tambah_mahasiswa(Mahasiswa("2024001", "Aulia Rahma", "aulia@mail.com", "Sistem Informasi", 2024))
        self.tambah_mahasiswa(Mahasiswa("2024002", "Bima Pratama", "bima@mail.com", "Sistem Informasi", 2024))
        self.tambah_dosen(Dosen("D001", "Dr. Raka Prasetya", "raka@kampus.ac.id", "Pemrograman"))
        self.tambah_dosen(Dosen("D002", "Dr. Nisa Kartika", "nisa@kampus.ac.id", "Basis Data"))
        self.tambah_mata_kuliah(MataKuliah("MK001", "Bahasa Pemrograman", 3, 1))
        self.tambah_mata_kuliah(MataKuliah("MK002", "Basis Data", 3, 1))
        self.tetapkan_dosen_pengampu("MK001", "D001")
        self.tetapkan_dosen_pengampu("MK002", "D002")
        krs = self.buat_krs("2024001", 1, "2024/2025")
        self.tambah_mk_ke_krs(krs.get_id_krs(), "MK001")
        self.tambah_mk_ke_krs(krs.get_id_krs(), "MK002")
        self.input_nilai(krs.get_id_krs(), "MK001", 85, 88, 90)
