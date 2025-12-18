import customtkinter as ctk
from manajer_database import DatabaseManager
from gui import GuruFrame, SiswaFrame
from tkinter import messagebox

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("Dark")  
        ctk.set_default_color_theme("blue")
        
        self.title("Aplikasi Manajemen Rapor")
        self.geometry("1000x700") 
        self.resizable(True, True) 
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.db = DatabaseManager()
        self.current_user_nis = None
        self.frames = {}
        
        self.show_frame("login")

    def show_frame(self, frame_name, nis=None):
        for frame in self.frames.values():
            frame.destroy()
        self.frames = {}
        
        if frame_name == "login":
            frame = self.LoginFrame(self, self.db, self.show_frame)
        elif frame_name == "guru":
            frame = GuruFrame(self, self.db, self.show_frame)
        elif frame_name == "siswa":
            self.current_user_nis = nis
            frame = SiswaFrame(self, self.db, self.show_frame, nis)
        else:
            return

        self.frames[frame_name] = frame
        frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)

    class LoginFrame(ctk.CTkFrame):
        def __init__(self, master, db_manager, switch_callback):
            super().__init__(master, corner_radius=15)
            self.db = db_manager
            self.switch_callback = switch_callback
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure((0, 5), weight=1)

            ctk.CTkLabel(self, text="Aplikasi Manajemen Rapor", 
                         font=("Arial", 30, "bold")).grid(row=1, column=0, pady=(30, 10))
            
            ctk.CTkLabel(self, text="Akses Aplikasi Manajemen Rapor").grid(row=2, column=0, pady=(0, 20))

            self.username_entry = ctk.CTkEntry(self, placeholder_text="Username / NIS", width=350, height=40)
            self.username_entry.grid(row=3, column=0, pady=10, padx=40)
            
            self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=350, height=40)
            self.password_entry.grid(row=4, column=0, pady=10, padx=40)
            
            ctk.CTkButton(self, text="MASUK", command=self.login_action, width=350, height=45, 
                          font=("Arial", 16, "bold")).grid(row=5, column=0, pady=(30, 40), padx=40, sticky="n")

        def login_action(self):
            username = self.username_entry.get()
            password = self.password_entry.get()
            
            users = self.db.get_users()
            
            if username in users and users[username] == password:
                if username == "guru":
                    self.switch_callback("guru")
                else:
                    self.switch_callback("siswa", nis=username) 
            else:
                messagebox.showerror("Login Gagal", "Username atau Password salah!")
                self.password_entry.delete(0, 'end')

if __name__ == "__main__":
    app = App()
    app.mainloop()