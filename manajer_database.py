import json
import os

DB_FILE = "data.json"

class DatabaseManager:
    def __init__(self):
        if not os.path.exists(DB_FILE):
            self._create_initial_db()
        self.data = self._load_data()

    def _create_initial_db(self):
        initial_data = {
            "users": {
                "guru": "12345"
            },
            "kkm": 75,
            "mata_pelajaran": [
                "Matematika",
                "Bahasa Indonesia"
            ],
            "siswa": {}
        }
        with open(DB_FILE, 'w') as f:
            json.dump(initial_data, f, indent=4)

    def _load_data(self):
        try:
            with open(DB_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Error: File data.json tidak valid atau kosong.")
            return {}
        except FileNotFoundError:
            self._create_initial_db()
            return self._load_data()

    def _save_data(self):
        """Menyimpan data ke JSON."""
        with open(DB_FILE, 'w') as f:
            json.dump(self.data, f, indent=4)


    def get_users(self):
        return self.data.get("users", {})

    def get_siswa(self):
        return self.data.get("siswa", {})

    def get_mapel(self):
        return self.data.get("mata_pelajaran", [])

    def get_kkm(self):
        return self.data.get("kkm", 75)
    

    def tambah_siswa(self, nis, nama, kelas):
        if nis in self.data["siswa"]:
            return False, "NIS sudah terdaftar."
        
        nilai_awal = {mapel: 0 for mapel in self.get_mapel()}

        self.data["siswa"][nis] = {
            "nama": nama,
            "kelas": kelas,
            "nilai": nilai_awal
        }
        self.data["users"][nis] = nis
        self._save_data()
        return True, "Siswa berhasil ditambahkan."

    def hapus_siswa(self, nis):
        if nis in self.data["siswa"]:
            del self.data["siswa"][nis]
            if nis in self.data["users"]:
                del self.data["users"][nis]
            self._save_data()
            return True, "Siswa berhasil dihapus."
        return False, "NIS tidak ditemukan."

    def update_nilai(self, nis, mapel, nilai):
        if nis not in self.data["siswa"]:
            return False, "NIS tidak ditemukan."
        if mapel not in self.data["mata_pelajaran"]:
             return False, "Mata pelajaran tidak ditemukan di daftar mapel sekolah."

        try:
            nilai_int = int(nilai)
            if 0 <= nilai_int <= 100:
                self.data["siswa"][nis]["nilai"][mapel] = nilai_int
                self._save_data()
                return True, "Nilai berhasil diperbarui."
            else:
                return False, "Nilai harus antara 0 dan 100."
        except ValueError:
            return False, "Nilai harus berupa angka."
            
    def tambah_mapel(self, mapel_baru):
        if mapel_baru not in self.data["mata_pelajaran"]:
            self.data["mata_pelajaran"].append(mapel_baru)
            for nis in self.data["siswa"]:
                self.data["siswa"][nis]["nilai"][mapel_baru] = 0 
            self._save_data()
            return True, "Mata pelajaran berhasil ditambahkan."
        return False, "Mata pelajaran sudah ada."

    def set_kkm(self, new_kkm):
        try:
            kkm_int = int(new_kkm)
            if 0 <= kkm_int <= 100:
                self.data["kkm"] = kkm_int
                self._save_data()
                return True, "KKM berhasil diperbarui."
            else:
                return False, "KKM harus antara 0 dan 100."
        except ValueError:
            return False, "KKM harus berupa angka."