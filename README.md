# Sistem Manajemen Akademik Mahasiswa Berbasis OOP

Proyek ini dibuat untuk tugas Bahasa Pemrograman menggunakan Python dan konsep Object-Oriented Programming.

## Fitur Utama

1. Mengelola data mahasiswa.
2. Mengelola data dosen.
3. Mengelola data mata kuliah.
4. Menetapkan dosen pengampu mata kuliah.
5. Membuat KRS mahasiswa.
6. Menambahkan mata kuliah ke KRS.
7. Menginput nilai tugas, UTS, dan UAS.
8. Menghitung nilai akhir, huruf mutu, status lulus, dan IPS.
9. Menyimpan data ke file JSON.
10. Menampilkan laporan ringkas akademik.

## Cara Menjalankan di VS Code

Buka folder proyek ini di VS Code, lalu jalankan:

```bash
python main.py
```

Jika menggunakan Windows dan perintah `python` tidak aktif, gunakan:

```bash
py main.py
```

## Cara Menjalankan Testing

```bash
python -m unittest discover tests
```

## Penerapan OOP

- Class: Person, Mahasiswa, Dosen, MataKuliah, Nilai, KRS, Akademik, FileManager.
- Object: Dibuat dari setiap class pada program utama dan testing.
- Inheritance: Mahasiswa dan Dosen mewarisi Person.
- Encapsulation: Atribut private dan protected digunakan bersama getter/setter.
- Polymorphism: Method `tampilkan_info()` dioverride pada Mahasiswa dan Dosen.
- Composition: KRS memiliki object Mahasiswa, MataKuliah, dan Nilai. Akademik menyimpan object-object utama.
- Constructor: Semua class menggunakan `__init__()`.
