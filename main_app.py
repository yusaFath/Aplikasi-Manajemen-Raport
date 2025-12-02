import os
from user_data import KelasDB, SiswaDB, PelajaranDB, NilaiDB, UserDB

VERSION = "1.0.0"
JudulAplikasi = "Aplikasi Manajemen Rapor"

class AppController:
    def __init__(self):
        self.current_user = None
        self.user_role = None
        self.kelas_data = KelasDB
        self.siswa_data = SiswaDB
        self.pelajaran_data = PelajaranDB
        self.nilai_data = NilaiDB
        self.users = UserDB

    def load_users(self):
        return self.users

    def proses_login(self, username: str, password: str):
        users = self.load_users()
        username = username.strip().upper()
        if username in users and users[username]["pass"] == password:
            self.current_user = users[username]
            self.user_role = users[username]["role"]
            return True, f"Selamat datang, {self.current_user['nama']}!"
        else:
            return False, "ID atau Kata Sandi salah!"

    def logout(self):
        self.current_user = None
        self.user_role = None
        print("Anda telah logout.")

    def ubah_password(self, id_pengguna, password_lama, password_baru):
        if id_pengguna in self.users and self.users[id_pengguna]['pass'] == password_lama:
            self.users[id_pengguna]['pass'] = password_baru
            return True
        return False

    def get_siswa_by_kelas(self, nama_kelas):
        list_id = self.kelas_data.get(nama_kelas, [])
        return [self.siswa_data[id] for id in list_id if id in self.siswa_data]

    def get_data_nilai(self, siswa_id):
        return self.nilai_data.get(siswa_id, {})

    def update_nilai(self, siswa_id, mapel_id, nilai):
        if siswa_id not in self.nilai_data:
            self.nilai_data[siswa_id] = {}
        self.nilai_data[siswa_id][mapel_id] = nilai
        return True

    def get_kkm_mapel(self, mapel_id):
        return self.pelajaran_data.get(mapel_id, {}).get("kkm", 0)

    def update_kkm(self, mapel_id, kkm):
        if mapel_id in self.pelajaran_data:
            self.pelajaran_data[mapel_id]['kkm'] = kkm
            return True
        return False

    def cetak_raport(self, siswa_id):
        siswa = self.siswa_data.get(siswa_id, {"nama": "Tidak Ditemukan"})
        print(f"[DEBUG] Mencetak rapor untuk {siswa['nama']}...")
        return True

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def login_menu(controller):
    clear_screen()
    print(f"===== {JudulAplikasi} =====")
    print("Login")
    username = input("ID Pengguna: ").strip()
    password = input("Kata Sandi: ").strip()
    success, message = controller.proses_login(username, password)
    print(message)
    if success:
        input("Tekan Enter untuk melanjutkan...")
        return True
    else:
        input("Tekan Enter untuk mencoba lagi...")
        return False

def dashboard(controller):
    clear_screen()
    print("Dashboard Utama")
    print(f"Halo, {controller.current_user['nama']}! Anda masuk sebagai {controller.current_user['role'].upper()}.")
    print(f"STATUS SISTEM: Aktif (V. {VERSION})")
    input("Tekan Enter untuk kembali...")

def input_nilai(controller):
    clear_screen()
    print("Modul Input Nilai")
    print("Daftar Kelas: " + ", ".join(controller.kelas_data.keys()))
    kelas_pilihan = input("Pilih Kelas: ").strip()
    if kelas_pilihan not in controller.kelas_data:
        print("Kelas tidak ditemukan!")
        input("Tekan Enter untuk kembali...")
        return

    siswa_list = controller.get_siswa_by_kelas(kelas_pilihan)
    mapel_list = list(controller.pelajaran_data.keys())

    print("\nTabel Nilai:")
    header = "Nama Siswa\t" + "\t".join([f"{PelajaranDB[m]['nama']} (KKM: {controller.get_kkm_mapel(m)})" for m in mapel_list])
    print(header)
    for siswa in siswa_list:
        siswa_id = [k for k, v in SiswaDB.items() if v['nama'] == siswa['nama']][0]
        nilai_siswa = controller.get_data_nilai(siswa_id)
        row = siswa['nama'] + "\t"
        for m in mapel_list:
            row += str(nilai_siswa.get(m, "")) + "\t"
        print(row)

    while True:
        print("\nAksi: 1. Update Nilai | 2. Edit KKM | 3. Tambah Siswa (dummy) | 4. Hapus Siswa (dummy) | 5. Tambah Mapel (dummy) | 0. Kembali")
        pilihan = input("Pilih aksi: ").strip()
        if pilihan == '0':
            break
        elif pilihan == '1':
            siswa_nama = input("Nama Siswa: ").strip()
            siswa_id = next((k for k, v in SiswaDB.items() if v['nama'] == siswa_nama), None)
            if not siswa_id:
                print("Siswa tidak ditemukan!")
                continue
            mapel_id = input("Kode Mapel (e.g., MTK): ").strip().upper()
            if mapel_id not in mapel_list:
                print("Mapel tidak ditemukan!")
                continue
            nilai_str = input("Nilai Baru (0-100): ").strip()
            try:
                nilai = int(nilai_str)
                if 0 <= nilai <= 100:
                    controller.update_nilai(siswa_id, mapel_id, nilai)
                    print("Nilai diperbarui!")
                else:
                    print("Nilai tidak valid!")
            except ValueError:
                print("Input harus angka!")
        elif pilihan == '2':
            mapel_id = input("Kode Mapel: ").strip().upper()
            kkm_str = input("KKM Baru: ").strip()
            try:
                kkm = int(kkm_str)
                if controller.update_kkm(mapel_id, kkm):
                    print("KKM diperbarui!")
                else:
                    print("Mapel tidak ditemukan!")
            except ValueError:
                print("Input harus angka!")
        else:
            print("Aksi dummy: Fitur belum diimplementasikan.")

    input("Tekan Enter untuk kembali...")

def data_siswa(controller):
    clear_screen()
    print("Modul Data Siswa")
    print("Daftar Kelas: " + ", ".join(controller.kelas_data.keys()))
    kelas_pilihan = input("Pilih Kelas: ").strip()
    if kelas_pilihan not in controller.kelas_data:
        print("Kelas tidak ditemukan!")
        input("Tekan Enter untuk kembali...")
        return

    siswa_list = controller.get_siswa_by_kelas(kelas_pilihan)
    print("\nDaftar Siswa:")
    for siswa in siswa_list:
        siswa_id = [k for k, v in SiswaDB.items() if v['nama'] == siswa['nama']][0]
        print(f"- {siswa['nama']} (ID: {siswa_id})")

    while True:
        siswa_nama = input("Nama Siswa untuk Cetak Rapor (atau 0 untuk kembali): ").strip()
        if siswa_nama == '0':
            break
        siswa_id = next((k for k, v in SiswaDB.items() if v['nama'] == siswa_nama), None)
        if siswa_id:
            if controller.cetak_raport(siswa_id):
                print("Rapor berhasil dicetak (simulasi)!")
        else:
            print("Siswa tidak ditemukan!")

    input("Tekan Enter untuk kembali...")

def pengaturan(controller):
    clear_screen()
    print("Pengaturan Akun")
    current_user_id = next(k for k, v in controller.users.items() if v['nama'] == controller.current_user['nama'])
    print(f"ID Pengguna: {current_user_id}")
    print(f"Nama Pengguna: {controller.current_user['nama']}")

    old_pass = input("Kata Sandi Lama: ").strip()
    new_pass = input("Kata Sandi Baru: ").strip()
    confirm_pass = input("Konfirmasi Sandi Baru: ").strip()

    if new_pass != confirm_pass:
        print("Sandi baru tidak cocok!")
    elif len(new_pass) < 6:
        print("Sandi baru minimal 6 karakter!")
    elif controller.ubah_password(current_user_id, old_pass, new_pass):
        print("Kata Sandi berhasil diubah!")
    else:
        print("Kata Sandi lama salah!")

    input("Tekan Enter untuk kembali...")

def main_menu(controller):
    while True:
        clear_screen()
        print(f"===== {JudulAplikasi} =====")
        print(f"Selamat datang, {controller.current_user['nama']} ({controller.user_role})")
        print("1. Dashboard")
        print("2. Input Nilai")
        print("3. Data Siswa")
        print("4. Pengaturan")
        print("0. Logout")
        pilihan = input("Pilih menu: ").strip()
        if pilihan == '0':
            controller.logout()
            break
        elif pilihan == '1':
            dashboard(controller)
        elif pilihan == '2':
            input_nilai(controller)
        elif pilihan == '3':
            data_siswa(controller)
        elif pilihan == '4':
            pengaturan(controller)
        else:
            print("Pilihan tidak valid!")
            input("Tekan Enter untuk melanjutkan...")

if __name__ == "__main__":
    controller = AppController()
    while True:
        if login_menu(controller):
            main_menu(controller)