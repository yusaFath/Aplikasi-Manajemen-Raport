import customtkinter as ctk
from manajer_database import DatabaseManager
from tkinter import messagebox

class BaseFrame(ctk.CTkFrame):
    def __init__(self, master, db_manager, switch_callback, **kwargs):
        super().__init__(master, corner_radius=15, **kwargs) 
        self.db = db_manager
        self.switch_callback = switch_callback
        self.grid_columnconfigure(0, weight=1)
        
    def create_header(self, title):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(header_frame, text=title, font=("Arial", 28, "bold")).grid(row=0, column=0, sticky="w")
        
        logout_button = ctk.CTkButton(header_frame, text="Logout 🚪", 
                                      command=lambda: self.switch_callback("login"), width=100)
        logout_button.grid(row=0, column=1, sticky="e")
        return 1 

class GuruFrame(BaseFrame):
    def __init__(self, master, db_manager, switch_callback):
        super().__init__(master, db_manager, switch_callback)
        
        current_row = self.create_header("GURU - Dashboard Manajemen Rapor") 
        
        self.grid_rowconfigure(current_row, weight=1) 

        self.tabview = ctk.CTkTabview(self, width=800)
        self.tabview.grid(row=current_row, column=0, padx=20, pady=10, sticky="nsew")

        self.tabview.add("Manajemen Siswa")
        self.tabview.add("Input Nilai")
        self.tabview.add("Mapel & KKM")

        self.tabview.tab("Manajemen Siswa").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Manajemen Siswa").grid_rowconfigure(2, weight=1) 
        
        self.tabview.tab("Input Nilai").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Input Nilai").grid_rowconfigure(0, weight=1)
        
        self.tabview.tab("Mapel & KKM").grid_columnconfigure((0, 1), weight=1)
        self.tabview.tab("Mapel & KKM").grid_rowconfigure(0, weight=1)


        self.setup_siswa_tab()
        self.setup_nilai_tab()
        self.setup_mapel_kkm_tab()

    def setup_siswa_tab(self):
        tab = self.tabview.tab("Manajemen Siswa")
        
        frame_tambah = ctk.CTkFrame(tab, corner_radius=10, border_width=1)
        frame_tambah.grid(row=0, column=0, sticky="ew", padx=10, pady=10) 
        
        ctk.CTkLabel(frame_tambah, text="➕ TAMBAH SISWA BARU", font=("Arial", 16, "bold")).pack(pady=5)
        self.entry_nis = ctk.CTkEntry(frame_tambah, placeholder_text="NIS")
        self.entry_nis.pack(fill="x", padx=20, pady=5)
        self.entry_nama = ctk.CTkEntry(frame_tambah, placeholder_text="Nama Siswa")
        self.entry_nama.pack(fill="x", padx=20, pady=5)
        self.entry_kelas = ctk.CTkEntry(frame_tambah, placeholder_text="Kelas (contoh: X-A)")
        self.entry_kelas.pack(fill="x", padx=20, pady=5)
        ctk.CTkButton(frame_tambah, text="Tambah Siswa", command=self._tambah_siswa_action).pack(padx=20, pady=10)
        
        ctk.CTkLabel(tab, text="📋 DAFTAR SISWA", font=("Arial", 16, "bold")).grid(row=1, column=0, pady=(20, 5))
        self.siswa_frame = ctk.CTkScrollableFrame(tab, height=250)
        self.siswa_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=5) 

        self._refresh_siswa_list()

    def _refresh_siswa_list(self):
        for widget in self.siswa_frame.winfo_children():
            widget.destroy()
            
        siswa_data = self.db.get_siswa()
        
        header_frame = ctk.CTkFrame(self.siswa_frame, fg_color=("gray70", "gray25"))
        header_frame.pack(fill="x", padx=5, pady=(5, 0))
        
        headers = ["NIS", "Nama Siswa", "Kelas", "Aksi"]
        widths = [100, 250, 100, 100]
        for i, h in enumerate(headers):
            ctk.CTkLabel(header_frame, text=h, font=("Arial", 12, "bold"), width=widths[i]).pack(side="left", padx=5, pady=5)

        if not siswa_data:
            ctk.CTkLabel(self.siswa_frame, text="Tidak ada data siswa.").pack(pady=10)
            return

        for nis, data in siswa_data.items():
            frame = ctk.CTkFrame(self.siswa_frame)
            frame.pack(fill="x", padx=5, pady=2)
            
            ctk.CTkLabel(frame, text=nis, width=100, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(frame, text=data['nama'], width=250, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(frame, text=data['kelas'], width=100, anchor="w").pack(side="left", padx=5)
            
            ctk.CTkButton(frame, text="Hapus", fg_color="red", hover_color="darkred", 
                          command=lambda n=nis: self._hapus_siswa_action(n), width=80).pack(side="left", padx=5)

    def _tambah_siswa_action(self):
        nis = self.entry_nis.get()
        nama = self.entry_nama.get()
        kelas = self.entry_kelas.get()
        
        if not all([nis, nama, kelas]):
            messagebox.showerror("Error", "Semua kolom harus diisi.")
            return

        success, msg = self.db.tambah_siswa(nis, nama, kelas)
        if success:
            messagebox.showinfo("Sukses", msg)
            self.entry_nis.delete(0, 'end')
            self.entry_nama.delete(0, 'end')
            self.entry_kelas.delete(0, 'end')
            self._refresh_siswa_list()
            self._refresh_nilai_form() 
        else:
            messagebox.showerror("Error", msg)

    def _hapus_siswa_action(self, nis):
        if messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus siswa dengan NIS {nis}?"):
            success, msg = self.db.hapus_siswa(nis)
            if success:
                messagebox.showinfo("Sukses", msg)
                self._refresh_siswa_list()
                self._refresh_nilai_form() 
            else:
                messagebox.showerror("Error", msg)

    def setup_nilai_tab(self):
        tab = self.tabview.tab("Input Nilai")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)

        self.nilai_scroll_frame = ctk.CTkScrollableFrame(tab, label_text="✍️ MASUKKAN / PERBARUI NILAI SISWA")
        self.nilai_scroll_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10) 

        self._refresh_nilai_form()

    def _refresh_nilai_form(self):
        for widget in self.nilai_scroll_frame.winfo_children():
            widget.destroy()

        siswa_data = self.db.get_siswa()
        mapel_list = self.db.get_mapel()

        if not siswa_data:
            ctk.CTkLabel(self.nilai_scroll_frame, text="Tidak ada siswa untuk diinput nilainya.").pack(pady=10)
            return

        ctk.CTkLabel(self.nilai_scroll_frame, text="Petunjuk: Masukkan nilai (0-100) dan tekan 'Simpan'").pack(pady=10)

        for nis, data in siswa_data.items():
            frame_siswa = ctk.CTkFrame(self.nilai_scroll_frame, border_width=1, corner_radius=10)
            frame_siswa.pack(fill="x", padx=10, pady=8)
            
            ctk.CTkLabel(frame_siswa, text=f"NIS: {nis} - {data['nama']} ({data['kelas']})", 
                         font=("Arial", 14, "bold")).pack(anchor="w", padx=15, pady=5)
            
            mapel_container = ctk.CTkFrame(frame_siswa, fg_color="transparent")
            mapel_container.pack(fill="x", padx=15, pady=5)
            mapel_container.grid_columnconfigure((0, 1), weight=1)
            
            for i, mapel in enumerate(mapel_list):
                frame_mapel = ctk.CTkFrame(mapel_container, fg_color="transparent")
                frame_mapel.grid(row=i // 2, column=i % 2, padx=10, pady=5, sticky="ew")
                
                ctk.CTkLabel(frame_mapel, text=f"{mapel}:", width=120, anchor="w").pack(side="left")
                
                entry = ctk.CTkEntry(frame_mapel, width=60)
                entry.insert(0, str(data["nilai"].get(mapel, 0))) 
                entry.pack(side="left", padx=5)
                
                ctk.CTkButton(frame_mapel, text="Simpan", width=70, 
                              command=lambda n=nis, m=mapel, e=entry: self._update_nilai_action(n, m, e)).pack(side="left", padx=5)
    
    def _update_nilai_action(self, nis, mapel, entry_widget):
        nilai = entry_widget.get()
        success, msg = self.db.update_nilai(nis, mapel, nilai)
        if success:
            messagebox.showinfo("Sukses", msg)
        else:
            messagebox.showerror("Error", msg)
            self._refresh_nilai_form() 

    def setup_mapel_kkm_tab(self):
        tab = self.tabview.tab("Mapel & KKM")
        tab.grid_columnconfigure((0, 1), weight=1)
        
        frame_kkm = ctk.CTkFrame(tab, corner_radius=10, border_width=1)
        frame_kkm.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(frame_kkm, text=f"🎯 KKM SAAT INI: {self.db.get_kkm()}", 
                     font=("Arial", 16, "bold")).pack(pady=10)
        self.entry_kkm = ctk.CTkEntry(frame_kkm, placeholder_text="KKM Baru (0-100)", width=200)
        self.entry_kkm.pack(fill="x", padx=20, pady=5)
        ctk.CTkButton(frame_kkm, text="SET KKM BARU", command=self._set_kkm_action).pack(padx=20, pady=15)

        frame_mapel = ctk.CTkFrame(tab, corner_radius=10, border_width=1)
        frame_mapel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(frame_mapel, text="📚 KELOLA MATA PELAJARAN", 
                     font=("Arial", 16, "bold")).pack(pady=10)
        
        self.entry_mapel = ctk.CTkEntry(frame_mapel, placeholder_text="Nama Mapel Baru", width=200)
        self.entry_mapel.pack(fill="x", padx=20, pady=5)
        ctk.CTkButton(frame_mapel, text="TAMBAH MAPEL", command=self._tambah_mapel_action).pack(padx=20, pady=10)

        ctk.CTkLabel(frame_mapel, text="Daftar Mapel Saat Ini:", font=("Arial", 12, "bold")).pack(anchor="w", padx=20, pady=(10, 0))
        self.mapel_list_label = ctk.CTkLabel(frame_mapel, text=", ".join(self.db.get_mapel()), wraplength=350)
        self.mapel_list_label.pack(anchor="w", padx=20, pady=(0, 10))


    def _set_kkm_action(self):
        new_kkm = self.entry_kkm.get()
        success, msg = self.db.set_kkm(new_kkm)
        if success:
            messagebox.showinfo("Sukses", msg)
            self._refresh_kkm_display()
            self._refresh_nilai_form()
            self.entry_kkm.delete(0, 'end')
        else:
            messagebox.showerror("Error", msg)

    def _refresh_kkm_display(self):
        kkm_frame = self.tabview.tab("Mapel & KKM").winfo_children()[0]
        kkm_label = kkm_frame.winfo_children()[0] 
        kkm_label.configure(text=f"🎯 KKM SAAT INI: {self.db.get_kkm()}")


    def _tambah_mapel_action(self):
        new_mapel = self.entry_mapel.get().strip()
        if not new_mapel:
            messagebox.showerror("Error", "Nama mata pelajaran tidak boleh kosong.")
            return

        success, msg = self.db.tambah_mapel(new_mapel)
        if success:
            messagebox.showinfo("Sukses", msg)
            self.entry_mapel.delete(0, 'end')
            self._refresh_mapel_list_label()
            self._refresh_nilai_form()
        else:
            messagebox.showerror("Error", msg)

    def _refresh_mapel_list_label(self):
        self.mapel_list_label.configure(text=", ".join(self.db.get_mapel()))
        
class SiswaFrame(BaseFrame):
    def __init__(self, master, db_manager, switch_callback, nis):
        super().__init__(master, db_manager, switch_callback)
        self.nis = nis
        self.siswa_data = self.db.get_siswa().get(nis, {})
        
        if not self.siswa_data:
            messagebox.showerror("Error", "Data siswa tidak ditemukan.")
            self.switch_callback("login")
            return
            
        current_row = self.create_header(" SISWA - Rapor Nilai")
        
        info_card = ctk.CTkFrame(self, fg_color=("gray85", "gray17"), corner_radius=10)
        info_card.grid(row=current_row, column=0, padx=20, pady=(5, 15), sticky="ew")
        info_card.grid_columnconfigure((0, 1), weight=1)
        
        ctk.CTkLabel(info_card, text=f"Nama: {self.siswa_data.get('nama', 'N/A')}", 
                     font=("Arial", 16, "bold")).grid(row=0, column=0, sticky="w", padx=20, pady=10)
        ctk.CTkLabel(info_card, text=f"NIS: {self.nis}", 
                     font=("Arial", 14)).grid(row=0, column=1, sticky="w", padx=20, pady=10)
        ctk.CTkLabel(info_card, text=f"Kelas: {self.siswa_data.get('kelas', '-')}", 
                     font=("Arial", 14)).grid(row=1, column=0, sticky="w", padx=20, pady=10)
        
        current_row += 1
        
        self.nilai_frame = ctk.CTkScrollableFrame(self, label_text="Tabel Rapor", 
                                                  label_font=("Arial", 18, "bold"), height=350)
        self.nilai_frame.grid(row=current_row, column=0, padx=20, pady=10, sticky="nsew")
        self.grid_rowconfigure(current_row, weight=1)

        self.display_nilai()
        
    def display_nilai(self):
        for widget in self.nilai_frame.winfo_children():
            widget.destroy()

        nilai_dict = self.siswa_data.get('nilai', {})
        kkm = self.db.get_kkm()

        header_frame = ctk.CTkFrame(self.nilai_frame, fg_color=("gray70", "gray25"))
        header_frame.pack(fill="x", padx=5, pady=(5, 0))
        
        headers = ["Mata Pelajaran", "Nilai Angka", "KKM", "Status"]
        widths = [200, 150, 100, 150]
        for i, h in enumerate(headers):
            ctk.CTkLabel(header_frame, text=h, font=("Arial", 14, "bold"), width=widths[i]).pack(side="left", padx=5, pady=5)
            
        total_nilai = 0
        jumlah_mapel = len(nilai_dict)
        
        for mapel, nilai in nilai_dict.items():
            total_nilai += nilai
            
            frame = ctk.CTkFrame(self.nilai_frame)
            frame.pack(fill="x", padx=5, pady=2)
            
            status = "LULUS" if nilai >= kkm else "REMIDI"
            
            nilai_color = "green" if nilai >= kkm else "red"
            
            ctk.CTkLabel(frame, text=mapel, width=200, anchor="w").pack(side="left", padx=5)
            
            ctk.CTkLabel(frame, text=str(nilai), width=150, text_color=nilai_color, font=("Arial", 14, "bold")).pack(side="left", padx=5)
            
            ctk.CTkLabel(frame, text=str(kkm), width=100).pack(side="left", padx=5)
            
            ctk.CTkLabel(frame, text=status, width=150, text_color=nilai_color, font=("Arial", 14, "italic")).pack(side="left", padx=5)
            
        if jumlah_mapel > 0:
            rata_rata = total_nilai / jumlah_mapel
            
            summary_frame = ctk.CTkFrame(self, fg_color="transparent")
            summary_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
            
            ctk.CTkLabel(summary_frame, text="📈 SUMMARY NILAI", 
                         font=("Arial", 18, "bold")).pack(anchor="w", pady=(10, 5))
            
            ctk.CTkLabel(summary_frame, text=f"Rata-rata Nilai Keseluruhan: {rata_rata:.2f}", 
                         font=("Arial", 16, "bold")).pack(anchor="w")
        else:
            ctk.CTkLabel(self.nilai_frame, text="Belum ada nilai yang diinputkan.").pack(pady=20)