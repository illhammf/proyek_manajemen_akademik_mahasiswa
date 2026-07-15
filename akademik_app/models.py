"""
models.py
Berisi kumpulan class inti untuk proyek Sistem Manajemen Akademik Mahasiswa.

Konsep OOP yang digunakan:
1. Class dan object
2. Constructor __init__()
3. Encapsulation dengan atribut protected/private
4. Inheritance dari Person ke Mahasiswa dan Dosen
5. Polymorphism melalui method tampilkan_info()
6. Composition, misalnya KRS memiliki object Mahasiswa, MataKuliah, dan Nilai
"""

from __future__ import annotations
from typing import List, Optional, Dict, Any


class Person:
    """Class induk untuk data manusia dalam sistem akademik."""

    def __init__(self, id_person: str, nama: str, email: str):
        # Atribut protected ditandai dengan satu underscore.
        # Atribut ini tidak sebaiknya diakses langsung dari luar class.
        self._id_person = id_person
        self._nama = nama
        self._email = email

    def get_id_person(self) -> str:
        return self._id_person

    def get_nama(self) -> str:
        return self._nama

    def set_nama(self, nama: str) -> None:
        if not nama.strip():
            raise ValueError("Nama tidak boleh kosong.")
        self._nama = nama

    def get_email(self) -> str:
        return self._email

    def set_email(self, email: str) -> None:
        if "@" not in email:
            raise ValueError("Format email tidak valid.")
        self._email = email

    def tampilkan_info(self) -> str:
        """Method ini dioverride pada class turunan sebagai bentuk polymorphism."""
        return f"{self._id_person} - {self._nama} ({self._email})"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_person": self._id_person,
            "nama": self._nama,
            "email": self._email,
        }


class Mahasiswa(Person):
    """Class turunan dari Person untuk menyimpan data mahasiswa."""

    def __init__(self, nim: str, nama: str, email: str, jurusan: str, angkatan: int):
        super().__init__(nim, nama, email)
        self.__nim = nim  # private attribute
        self.__jurusan = jurusan
        self.__angkatan = angkatan

    def get_nim(self) -> str:
        return self.__nim

    def get_jurusan(self) -> str:
        return self.__jurusan

    def set_jurusan(self, jurusan: str) -> None:
        if not jurusan.strip():
            raise ValueError("Jurusan tidak boleh kosong.")
        self.__jurusan = jurusan

    def get_angkatan(self) -> int:
        return self.__angkatan

    def set_angkatan(self, angkatan: int) -> None:
        if angkatan < 2000:
            raise ValueError("Angkatan tidak valid.")
        self.__angkatan = angkatan

    def tampilkan_info(self) -> str:
        # Polymorphism: method sama, perilaku berbeda dari class Person.
        return f"Mahasiswa | NIM: {self.__nim} | Nama: {self._nama} | Jurusan: {self.__jurusan} | Angkatan: {self.__angkatan}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nim": self.__nim,
            "nama": self._nama,
            "email": self._email,
            "jurusan": self.__jurusan,
            "angkatan": self.__angkatan,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Mahasiswa":
        return Mahasiswa(
            data["nim"],
            data["nama"],
            data["email"],
            data["jurusan"],
            int(data["angkatan"]),
        )


class Dosen(Person):
    """Class turunan dari Person untuk menyimpan data dosen."""

    def __init__(self, nip: str, nama: str, email: str, keahlian: str):
        super().__init__(nip, nama, email)
        self.__nip = nip
        self.__keahlian = keahlian
        self.__mata_kuliah_diampu: List[str] = []

    def get_nip(self) -> str:
        return self.__nip

    def get_keahlian(self) -> str:
        return self.__keahlian

    def set_keahlian(self, keahlian: str) -> None:
        if not keahlian.strip():
            raise ValueError("Keahlian tidak boleh kosong.")
        self.__keahlian = keahlian

    def tambah_mata_kuliah_diampu(self, kode_mk: str) -> None:
        if kode_mk not in self.__mata_kuliah_diampu:
            self.__mata_kuliah_diampu.append(kode_mk)

    def hapus_mata_kuliah_diampu(self, kode_mk: str) -> None:
        if kode_mk in self.__mata_kuliah_diampu:
            self.__mata_kuliah_diampu.remove(kode_mk)

    def get_mata_kuliah_diampu(self) -> List[str]:
        return list(self.__mata_kuliah_diampu)

    def tampilkan_info(self) -> str:
        return f"Dosen | NIP: {self.__nip} | Nama: {self._nama} | Keahlian: {self.__keahlian}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nip": self.__nip,
            "nama": self._nama,
            "email": self._email,
            "keahlian": self.__keahlian,
            "mata_kuliah_diampu": self.__mata_kuliah_diampu,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Dosen":
        dosen = Dosen(data["nip"], data["nama"], data["email"], data["keahlian"])
        for kode_mk in data.get("mata_kuliah_diampu", []):
            dosen.tambah_mata_kuliah_diampu(kode_mk)
        return dosen


class MataKuliah:
    """Class untuk merepresentasikan satu mata kuliah."""

    def __init__(self, kode_mk: str, nama_mk: str, sks: int, semester: int, nip_dosen: Optional[str] = None):
        self.__kode_mk = kode_mk
        self.__nama_mk = nama_mk
        self.__sks = sks
        self.__semester = semester
        self.__nip_dosen = nip_dosen

    def get_kode_mk(self) -> str:
        return self.__kode_mk

    def get_nama_mk(self) -> str:
        return self.__nama_mk

    def set_nama_mk(self, nama_mk: str) -> None:
        if not nama_mk.strip():
            raise ValueError("Nama mata kuliah tidak boleh kosong.")
        self.__nama_mk = nama_mk

    def get_sks(self) -> int:
        return self.__sks

    def set_sks(self, sks: int) -> None:
        if sks <= 0:
            raise ValueError("SKS harus lebih dari 0.")
        self.__sks = sks

    def get_semester(self) -> int:
        return self.__semester

    def set_semester(self, semester: int) -> None:
        if semester <= 0:
            raise ValueError("Semester harus lebih dari 0.")
        self.__semester = semester

    def set_dosen_pengampu(self, nip_dosen: str) -> None:
        self.__nip_dosen = nip_dosen

    def get_nip_dosen(self) -> Optional[str]:
        return self.__nip_dosen

    def tampilkan_info(self) -> str:
        dosen = self.__nip_dosen if self.__nip_dosen else "Belum ditentukan"
        return f"{self.__kode_mk} | {self.__nama_mk} | {self.__sks} SKS | Semester {self.__semester} | Dosen: {dosen}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "kode_mk": self.__kode_mk,
            "nama_mk": self.__nama_mk,
            "sks": self.__sks,
            "semester": self.__semester,
            "nip_dosen": self.__nip_dosen,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "MataKuliah":
        return MataKuliah(
            data["kode_mk"],
            data["nama_mk"],
            int(data["sks"]),
            int(data["semester"]),
            data.get("nip_dosen"),
        )


class Nilai:
    """Class untuk menyimpan nilai mahasiswa pada satu mata kuliah."""

    def __init__(self, nim: str, kode_mk: str, tugas: float, uts: float, uas: float):
        self.__nim = nim
        self.__kode_mk = kode_mk
        self.__tugas = tugas
        self.__uts = uts
        self.__uas = uas

    def get_nim(self) -> str:
        return self.__nim

    def get_kode_mk(self) -> str:
        return self.__kode_mk

    def set_nilai(self, tugas: float, uts: float, uas: float) -> None:
        for nilai in (tugas, uts, uas):
            if nilai < 0 or nilai > 100:
                raise ValueError("Nilai harus berada pada rentang 0 sampai 100.")
        self.__tugas = tugas
        self.__uts = uts
        self.__uas = uas

    def hitung_nilai_akhir(self) -> float:
        # Bobot dapat disesuaikan sesuai kebijakan kampus.
        return round((self.__tugas * 0.30) + (self.__uts * 0.30) + (self.__uas * 0.40), 2)

    def konversi_huruf(self) -> str:
        nilai_akhir = self.hitung_nilai_akhir()
        if nilai_akhir >= 85:
            return "A"
        if nilai_akhir >= 75:
            return "B"
        if nilai_akhir >= 65:
            return "C"
        if nilai_akhir >= 50:
            return "D"
        return "E"

    def status_lulus(self) -> str:
        return "Lulus" if self.hitung_nilai_akhir() >= 65 else "Tidak Lulus"

    def tampilkan_info(self) -> str:
        return f"{self.__nim} | {self.__kode_mk} | Akhir: {self.hitung_nilai_akhir()} | Huruf: {self.konversi_huruf()} | {self.status_lulus()}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nim": self.__nim,
            "kode_mk": self.__kode_mk,
            "tugas": self.__tugas,
            "uts": self.__uts,
            "uas": self.__uas,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Nilai":
        return Nilai(
            data["nim"],
            data["kode_mk"],
            float(data["tugas"]),
            float(data["uts"]),
            float(data["uas"]),
        )


class KRS:
    """Class KRS menghubungkan mahasiswa dengan daftar mata kuliah yang diambil."""

    def __init__(self, id_krs: str, mahasiswa: Mahasiswa, semester: int, tahun_akademik: str):
        self.__id_krs = id_krs
        self.__mahasiswa = mahasiswa  # composition: KRS memiliki object Mahasiswa
        self.__semester = semester
        self.__tahun_akademik = tahun_akademik
        self.__mata_kuliah: List[MataKuliah] = []  # composition: KRS memiliki banyak object MataKuliah
        self.__nilai: List[Nilai] = []  # composition: KRS memiliki banyak object Nilai

    def get_id_krs(self) -> str:
        return self.__id_krs

    def get_mahasiswa(self) -> Mahasiswa:
        return self.__mahasiswa

    def get_semester(self) -> int:
        return self.__semester

    def get_tahun_akademik(self) -> str:
        return self.__tahun_akademik

    def tambah_mata_kuliah(self, mata_kuliah: MataKuliah, batas_sks: int = 24) -> bool:
        if self.cari_mata_kuliah(mata_kuliah.get_kode_mk()) is not None:
            return False
        if self.total_sks() + mata_kuliah.get_sks() > batas_sks:
            raise ValueError(f"Total SKS melebihi batas maksimal {batas_sks} SKS.")
        self.__mata_kuliah.append(mata_kuliah)
        return True

    def hapus_mata_kuliah(self, kode_mk: str) -> bool:
        mk = self.cari_mata_kuliah(kode_mk)
        if mk is None:
            return False
        self.__mata_kuliah.remove(mk)
        self.__nilai = [nilai for nilai in self.__nilai if nilai.get_kode_mk() != kode_mk]
        return True

    def cari_mata_kuliah(self, kode_mk: str) -> Optional[MataKuliah]:
        for mk in self.__mata_kuliah:
            if mk.get_kode_mk() == kode_mk:
                return mk
        return None

    def get_mata_kuliah(self) -> List[MataKuliah]:
        return list(self.__mata_kuliah)

    def total_sks(self) -> int:
        return sum(mk.get_sks() for mk in self.__mata_kuliah)

    def tambah_atau_update_nilai(self, nilai: Nilai) -> None:
        if self.cari_mata_kuliah(nilai.get_kode_mk()) is None:
            raise ValueError("Nilai hanya dapat diinput untuk mata kuliah yang ada di KRS.")
        for index, item in enumerate(self.__nilai):
            if item.get_kode_mk() == nilai.get_kode_mk():
                self.__nilai[index] = nilai
                return
        self.__nilai.append(nilai)

    def get_nilai(self) -> List[Nilai]:
        return list(self.__nilai)

    def hitung_ip_semester(self) -> float:
        if not self.__nilai:
            return 0.0
        bobot = {"A": 4, "B": 3, "C": 2, "D": 1, "E": 0}
        total_bobot = 0
        total_sks = 0
        for nilai in self.__nilai:
            mk = self.cari_mata_kuliah(nilai.get_kode_mk())
            if mk:
                total_bobot += bobot[nilai.konversi_huruf()] * mk.get_sks()
                total_sks += mk.get_sks()
        return round(total_bobot / total_sks, 2) if total_sks else 0.0

    def tampilkan_ringkasan(self) -> str:
        return (
            f"KRS: {self.__id_krs} | Mahasiswa: {self.__mahasiswa.get_nama()} | "
            f"Semester: {self.__semester} | Tahun: {self.__tahun_akademik} | "
            f"Total SKS: {self.total_sks()} | IPS: {self.hitung_ip_semester()}"
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_krs": self.__id_krs,
            "nim": self.__mahasiswa.get_nim(),
            "semester": self.__semester,
            "tahun_akademik": self.__tahun_akademik,
            "mata_kuliah": [mk.get_kode_mk() for mk in self.__mata_kuliah],
            "nilai": [nilai.to_dict() for nilai in self.__nilai],
        }
