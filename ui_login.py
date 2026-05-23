import customtkinter as ctk
import pywinstyles
from PIL import Image
from tkinter import messagebox
from db_adapter import get_connection
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class ModernLogin(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("System Login")
        self.geometry("900x600")
        self.resizable(False, False)
        
        # Center the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 900) // 2
        y = (screen_height - 600) // 2
        self.geometry(f"900x600+{x}+{y}")

        # Try to apply mica/acrylic effect
        try:
            pywinstyles.apply_style(self, "acrylic")
        except:
            pass

        # Database Setup
        self.engine = create_engine('sqlite:///inventory_management_system.db')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.base = get_connection(self.session)
        self.cur = self.base.cursor()
        
        # Ensure Users table exists
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username VARCHAR(20) PRIMARY KEY,
                password VARCHAR(20) NOT NULL,
                account_type VARCHAR(10) NOT NULL
            );
        """)
        self.base.commit()

        self.user_data = None
        self.build_ui()

    def build_ui(self):
        # Background Image
        try:
            bg_image = ctk.CTkImage(Image.open("images/bg.png"), size=(900, 600))
            self.bg_label = ctk.CTkLabel(self, text="", image=bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print("Background image not found.", e)
            self.configure(fg_color="#0d1b2a") # Fallback color

        # Glassmorphism Login Frame
        self.login_frame = ctk.CTkFrame(self, width=400, height=450, corner_radius=20, 
                                        fg_color=("#ffffff", "#1e293b"), bg_color="transparent")
        # To make it translucent
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Label Title
        self.title_label = ctk.CTkLabel(self.login_frame, text="Welcome Back", font=("Inter", 28, "bold"))
        self.title_label.place(relx=0.5, y=50, anchor="center")
        
        self.subtitle = ctk.CTkLabel(self.login_frame, text="Inventory Management System", font=("Inter", 14), text_color="gray")
        self.subtitle.place(relx=0.5, y=85, anchor="center")

        # Username Entry
        self.username_entry = ctk.CTkEntry(self.login_frame, width=300, height=45, corner_radius=10, 
                                           placeholder_text="Username", font=("Inter", 14))
        self.username_entry.place(relx=0.5, y=160, anchor="center")

        # Password Entry
        self.password_entry = ctk.CTkEntry(self.login_frame, width=300, height=45, corner_radius=10, 
                                           placeholder_text="Password", font=("Inter", 14), show="*")
        self.password_entry.place(relx=0.5, y=230, anchor="center")

        # Role Combobox
        self.role_combo = ctk.CTkComboBox(self.login_frame, width=300, height=45, corner_radius=10, 
                                          values=["Admin", "Employee"], font=("Inter", 14))
        self.role_combo.place(relx=0.5, y=300, anchor="center")
        self.role_combo.set("Admin")

        # Login Button
        self.login_btn = ctk.CTkButton(self.login_frame, text="Log In", width=300, height=45, corner_radius=10, 
                                       font=("Inter", 16, "bold"), command=self.attempt_login, 
                                       fg_color="#0066ff", hover_color="#0052cc")
        self.login_btn.place(relx=0.5, y=380, anchor="center")

    def attempt_login(self):
        user = self.username_entry.get().strip().upper()
        pwd = self.password_entry.get().strip()
        role = self.role_combo.get().upper()

        if not user or not pwd:
            messagebox.showwarning("Warning", "Please fill all fields!")
            return

        self.cur.execute("SELECT * FROM users WHERE username=? AND password=? AND account_type=?", 
                         (user, pwd, role))
        match = self.cur.fetchone()

        if match:
            self.user_data = {
                "username": match[0],
                "account_type": match[2],
            }
            self.quit()  # Break mainloop
            self.withdraw() # Hide login window
        else:
            messagebox.showerror("Error", "Invalid Credentials!")

if __name__ == "__main__":
    app = ModernLogin()
    app.mainloop()
    if app.user_data:
        print("Logged in as:", app.user_data)
