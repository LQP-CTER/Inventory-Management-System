import sqlite3
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from Userlogin import Login
from Admin_menu import Admin
from User_menu import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# MAIN CLASS
class Main(Login, Admin, User):
    def __init__(self):
        Login.__init__(self)
        self.loginw.mainloop()

        if not self.user_data:
            exit(0)

        self.username = self.user_data["username"]
        self.account_type = self.user_data["account_type"]

        # Set up the main window
        self.mainw = Toplevel(bg="#FFFFFF")
        width, height = 1400, 780
        screen_width, screen_height = self.mainw.winfo_screenwidth(), self.mainw.winfo_screenheight()
        x, y = (screen_width - width) // 2, (screen_height - height) // 2
        self.mainw.geometry(f"{width}x{height}+{x}+{y}")
        self.mainw.title("Inventory Management System")
        self.mainw.resizable(0, 0)
        self.mainw.protocol('WM_DELETE_WINDOW', self.__Main_del__)

        # Database connection setup
        self.engine = create_engine('sqlite:///inventory_management_system.db', echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        self.build_main_interface()

    def __Main_del__(self):
        """Xử lý khi người dùng tắt ứng dụng."""
        if messagebox.askyesno("Quit", "Leave System?"):
            self.session.close()
            self.mainw.quit()
            exit(0)

    def build_main_interface(self):
        """Xây dựng giao diện chính."""
        if self.account_type == 'ADMIN':
            Admin.__init__(self, self.mainw)
            self.admin_mainmenu(8, 8)
            self.show_dashboard()
        else:
            User.__init__(self, self.mainw)
            self.user_mainmenu(8, 8)

        # Cài đặt top frame
        self.setup_topframe()

    def setup_topframe(self):
        """Cài đặt top frame."""
        self.topframe = LabelFrame(self.mainw, width=1400, height=120, bg="#4267b2")
        self.topframe.place(x=0, y=0)
        store_name = 'PELT Solutions '
        store_label = Label(self.topframe, text=store_name + "[Inventory Management System]", bg="#4267b2", anchor="center")
        store_label.config(font="Roboto 30 bold", fg="snow")
        store_label.place(x=360, y=30)

        # Hiển thị thông tin người dùng
        mi = PhotoImage(file="images/myprofile.png").subsample(4, 4)
        self.myprofile = ttk.Label(self.topframe, text=self.username.capitalize(), image=mi, compound=TOP)
        self.myprofile.image = mi
        self.myprofile.place(x=1300, y=15)

    def change_user(self):
        """Chuyển đổi người dùng."""
        if messagebox.askyesno("Alert!", "Do you want to change user?"):
            self.session.close()
            self.mainw.destroy()
            self.loginw.destroy()
            self.__init__()

if __name__ == '__main__':
    w = Main()
    w.mainw.mainloop()
