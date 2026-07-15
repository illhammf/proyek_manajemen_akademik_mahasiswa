"""
main.py
Program utama Sistem Manajemen Akademik Mahasiswa berbasis OOP.
Jalankan file ini dari VS Code dengan perintah:
python main.py
"""

from akademik_app.models import Mahasiswa, Dosen, MataKuliah
from akademik_app.services import Akademik
from akademik_app.storage import FileManager

DATA_FILE = "data/akademik_data.json"


def input_int(pesan: str) -> int:
    """Helper untuk memastikan input angka tidak menyebabkan program error."""
    while True:
        try:
            return int(input(pesan))
        except ValueError:
            print("Input harus berupa angka.")


def input_float(pesan: str) -> float:
    while True:
        try:
            return float(input(pesan))
        except ValueError:
            print("Input harus berupa angka.")


def tampilkan_list(judul: str, data: list) -> None:
    print(f"\n=== {judul} ===")
    if not data:
        print("Data masih kosong.")
        return
    for nomor, item in enumerate(data, start=1):
        # Setiap object memiliki method tampilkan_info atau tampilkan_ringkasan.
        if hasattr(item, "tampilkan_info"):
            print(f"{nomor}. {item.tampilkan_info()}")
        else:
            print(f"{nomor}. {item.tampilkan_ringkasan()}")


def menu_mahasiswa(akademik: Akademik) -> None:
    while True:
        print("\n--- Menu Mahasiswa ---")
        print("1. Tambah mahasiswa")
        print("2. Lihat mahasiswa")
        print("3. Hapus mahasiswa")
        print("0. Kembali")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            nim = input("NIM: ")
            nama = input("Nama: ")
            email = input("Email: ")
            jurusan = input("Jurusan: ")
            angkatan = input_int("Angkatan: ")
            berhasil = akademik.tambah_mahasiswa(Mahasiswa(nim, nama, email, jurusan, angkatan))
            print("Mahasiswa berhasil ditambahkan." if berhasil else "NIM sudah terdaftar.")
        elif pilihan == "2":
            tampilkan_list("Daftar Mahasiswa", akademik.daftar_mahasiswa())
        elif pilihan == "3":
            nim = input("Masukkan NIM yang akan dihapus: ")
            print("Data dihapus." if akademik.hapus_mahasiswa(nim) else "Mahasiswa tidak ditemukan.")
        elif pilihan == "0":
            break
        else:
            print("Menu tidak tersedia.")


def menu_dosen(akademik: Akademik) -> None:
    while True:
        print("\n--- Menu Dosen ---")
        print("1. Tambah dosen")
        print("2. Lihat dosen")
        print("3. Tetapkan dosen pengampu")
        print("0. Kembali")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            nip = input("NIP: ")
            nama = input("Nama: ")
            email = input("Email: ")
            keahlian = input("Keahlian: ")
            berhasil = akademik.tambah_dosen(Dosen(nip, nama, email, keahlian))
            print("Dosen berhasil ditambahkan." if berhasil else "NIP sudah terdaftar.")
        elif pilihan == "2":
            tampilkan_list("Daftar Dosen", akademik.daftar_dosen())
        elif pilihan == "3":
            kode_mk = input("Kode mata kuliah: ")
            nip = input("NIP dosen: ")
            print("Dosen pengampu berhasil ditetapkan." if akademik.tetapkan_dosen_pengampu(kode_mk, nip) else "Data tidak ditemukan.")
        elif pilihan == "0":
            break
        else:
            print("Menu tidak tersedia.")


def menu_mata_kuliah(akademik: Akademik) -> None:
    while True:
        print("\n--- Menu Mata Kuliah ---")
        print("1. Tambah mata kuliah")
        print("2. Lihat mata kuliah")
        print("0. Kembali")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            kode_mk = input("Kode MK: ")
            nama_mk = input("Nama MK: ")
            sks = input_int("SKS: ")
            semester = input_int("Semester: ")
            berhasil = akademik.tambah_mata_kuliah(MataKuliah(kode_mk, nama_mk, sks, semester))
            print("Mata kuliah berhasil ditambahkan." if berhasil else "Kode MK sudah terdaftar.")
        elif pilihan == "2":
            tampilkan_list("Daftar Mata Kuliah", akademik.daftar_mata_kuliah())
        elif pilihan == "0":
            break
        else:
            print("Menu tidak tersedia.")


def menu_krs(akademik: Akademik) -> None:
    while True:
        print("\n--- Menu KRS ---")
        print("1. Buat KRS")
        print("2. Tambah mata kuliah ke KRS")
        print("3. Lihat semua KRS")
        print("4. Lihat KRS mahasiswa")
        print("0. Kembali")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            nim = input("NIM: ")
            semester = input_int("Semester: ")
            tahun = input("Tahun akademik, contoh 2024/2025: ")
            try:
                krs = akademik.buat_krs(nim, semester, tahun)
                print(f"KRS berhasil dibuat. ID KRS: {krs.get_id_krs()}")
            except ValueError as error:
                print(error)
        elif pilihan == "2":
            id_krs = input("ID KRS: ")
            kode_mk = input("Kode MK: ")
            try:
                print("Mata kuliah berhasil ditambahkan." if akademik.tambah_mk_ke_krs(id_krs, kode_mk) else "KRS atau mata kuliah tidak ditemukan.")
            except ValueError as error:
                print(error)
        elif pilihan == "3":
            tampilkan_list("Daftar KRS", akademik.daftar_krs())
        elif pilihan == "4":
            nim = input("NIM: ")
            tampilkan_list("KRS Mahasiswa", akademik.cari_krs_mahasiswa(nim))
        elif pilihan == "0":
            break
        else:
            print("Menu tidak tersedia.")


def menu_nilai(akademik: Akademik) -> None:
    while True:
        print("\n--- Menu Nilai ---")
        print("1. Input atau update nilai")
        print("2. Lihat nilai pada KRS")
        print("0. Kembali")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            id_krs = input("ID KRS: ")
            kode_mk = input("Kode MK: ")
            tugas = input_float("Nilai tugas: ")
            uts = input_float("Nilai UTS: ")
            uas = input_float("Nilai UAS: ")
            try:
                akademik.input_nilai(id_krs, kode_mk, tugas, uts, uas)
                print("Nilai berhasil disimpan.")
            except ValueError as error:
                print(error)
        elif pilihan == "2":
            id_krs = input("ID KRS: ")
            krs = akademik.cari_krs(id_krs)
            if krs is None:
                print("KRS tidak ditemukan.")
            else:
                tampilkan_list("Daftar Nilai", krs.get_nilai())
        elif pilihan == "0":
            break
        else:
            print("Menu tidak tersedia.")


def main() -> None:
    file_manager = FileManager(DATA_FILE)
    akademik = Akademik("Sistem Manajemen Akademik Mahasiswa", file_manager)
    akademik.muat_data()

    # Jika file data masih kosong, sistem akan mengisi data contoh.
    if not akademik.daftar_mahasiswa():
        akademik.isi_data_awal()
        akademik.simpan_data()

    while True:
        print("\n========================================")
        print(" SISTEM MANAJEMEN AKADEMIK MAHASISWA")
        print("========================================")
        print("1. Kelola mahasiswa")
        print("2. Kelola dosen")
        print("3. Kelola mata kuliah")
        print("4. Kelola KRS")
        print("5. Kelola nilai")
        print("6. Laporan ringkas")
        print("7. Simpan data")
        print("0. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            menu_mahasiswa(akademik)
        elif pilihan == "2":
            menu_dosen(akademik)
        elif pilihan == "3":
            menu_mata_kuliah(akademik)
        elif pilihan == "4":
            menu_krs(akademik)
        elif pilihan == "5":
            menu_nilai(akademik)
        elif pilihan == "6":
            print("\n" + akademik.laporan_ringkas())
        elif pilihan == "7":
            akademik.simpan_data()
            print("Data berhasil disimpan.")
        elif pilihan == "0":
            akademik.simpan_data()
            print("Data disimpan. Program selesai.")
            break
        else:
            print("Menu tidak tersedia.")


if __name__ == "__main__":
    main()
