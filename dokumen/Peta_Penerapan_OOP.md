# Peta Penerapan OOP

## Class
Person, Mahasiswa, Dosen, MataKuliah, Nilai, KRS, Akademik, FileManager.

## Inheritance
Mahasiswa dan Dosen mewarisi atribut serta method dari Person.

## Encapsulation
Atribut protected memakai `_nama` dan `_email`. Atribut private memakai `__nim`, `__nip`, `__kode_mk`, `__nilai`, dan atribut lain yang perlu dikontrol melalui getter/setter.

## Polymorphism
Method `tampilkan_info()` tersedia pada Person, Mahasiswa, Dosen, MataKuliah, dan Nilai. Method tersebut memiliki keluaran berbeda sesuai class object yang memanggilnya.

## Composition
KRS memiliki object Mahasiswa, banyak object MataKuliah, dan banyak object Nilai. Akademik menyimpan kumpulan object Mahasiswa, Dosen, MataKuliah, dan KRS.

## Minimal 20 Method
Contoh method: `get_nim`, `set_jurusan`, `tampilkan_info`, `to_dict`, `from_dict`, `tambah_mata_kuliah`, `hapus_mata_kuliah`, `total_sks`, `hitung_ip_semester`, `tambah_mahasiswa`, `hapus_mahasiswa`, `tambah_dosen`, `tetapkan_dosen_pengampu`, `buat_krs`, `input_nilai`, `simpan_data`, `muat_data`, `baca_json`, `simpan_json`, dan `laporan_ringkas`.
