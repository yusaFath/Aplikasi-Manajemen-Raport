# Aplikasi Manajemen Raport

Aplikasi desktop sederhana untuk membantu guru dan administrator sekolah dalam mengelola data siswa, menginput nilai, menetapkan Kriteria Ketuntasan Minimal (KKM), dan mencetak rapor.
Aplikasi ini dibangun menggunakan Python dan framework GUI CustomTkinter(rencana).

Fitur Utama
Aplikasi ini menyediakan modul-modul berikut:

1. Dashboard
Menyambut pengguna yang login.
Menampilkan peran pengguna dan versi aplikasi.
Modul Input Nilai
Pemilihan kelas untuk input nilai.
Tabel interaktif untuk menginput nilai mata pelajaran per siswa.
Fitur untuk menetapkan dan menyimpan KKM per mata pelajaran.
Aksi dummy untuk menambah/mengurangi siswa dan mata pelajaran.
Fungsi untuk menyimpan semua nilai yang diinput.

2. Modul Data Siswa
Menampilkan daftar siswa berdasarkan kelas yang dipilih.
Tombol aksi untuk simulasi pencetakan rapor dalam format PDF (membutuhkan implementasi library eksternal seperti reportlab).

3. Pengaturan Akun
Menampilkan ID dan Nama pengguna saat ini.
Fungsi untuk mengubah kata sandi akun (hanya disimpan di memori/file data dummy).
