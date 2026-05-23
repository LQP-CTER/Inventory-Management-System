from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import ttkbootstrap as tb
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db_adapter import get_connection

class Login:
    def __init__(self):
        self.loginw = tb.Window(themename="lumen")  # Tạo cửa sổ đăng nhập chính với ttkbootstrap
        self.loginw.title("Login")

        # Xác định kích thước cửa sổ
        width = 500
        height = 600

        # Lấy kích thước màn hình và căn giữa cửa sổ
        screen_width = self.loginw.winfo_screenwidth()
        screen_height = self.loginw.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.loginw.geometry(f"{width}x{height}+{x}+{y}")

        # Không cho phép thay đổi kích thước cửa sổ
        self.loginw.resizable(0, 0)

        # Xử lý khi người dùng đóng cửa sổ
        self.loginw.protocol('WM_DELETE_WINDOW', self.__login_del__)

        # Cập nhật nền và màu sắc
        self.loginw.config(bg="#f4f6f9")

        # Khởi tạo bảng dữ liệu
        self.logintable()

        # Khởi tạo biến username và password
        self.username = StringVar(value="Username")
        self.password = StringVar(value="Password")

        # Khởi tạo giao diện
        self.obj()

    def __login_del__(self):
        if messagebox.askyesno("Quit", "Leave inventory?"):
            self.loginw.destroy()
            exit(0)  # Thoát khỏi chương trình hoàn toàn

    # LOGIN TABLE
    def logintable(self):
        # Kết nối hoặc tạo cơ sở dữ liệu
        engine = create_engine('sqlite:///inventory_management_system.db')
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.base = get_connection(self.session)
        self.cur = self.base.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username VARCHAR(20) PRIMARY KEY,
                password VARCHAR(20) NOT NULL,
                account_type VARCHAR(10) NOT NULL
            );
        """)
        self.base.commit()

    # WIDGET FUNCTION
    def obj(self):
        # Tạo khung đăng nhập
        self.loginframe = ttk.Frame(self.loginw, padding=30)
        self.loginframe.place(relx=0.5, rely=0.5, anchor="center")  # Đặt khung vào giữa cửa sổ

        # ** Tiêu đề với font đẹp **
        self.toplabel = ttk.Label(
            self.loginframe, text="Login", font=("Roboto", 30, "bold"), bootstyle="primary"
        )
        self.toplabel.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # ** Các ô nhập liệu **
        self.us = ttk.Entry(self.loginframe, width=25, textvariable=self.username, font=("Roboto", 12))
        self.us.grid(row=1, column=0, columnspan=2, pady=10)

        self.pa = ttk.Entry(self.loginframe, width=25, textvariable=self.password, font=("Roboto", 12), show="*")
        self.pa.grid(row=2, column=0, columnspan=2, pady=10)

        self.us.bind('<Button-1>', self.onclick)
        self.pa.bind('<Button-1>', self.onclick1)

        # ** Nút Đăng nhập **
        self.signin = ttk.Button(
            self.loginframe, width=20, text="Sign in", command=self.checkuser, bootstyle="success"
        )
        self.signin.grid(row=3, column=0, columnspan=2, pady=(20, 0))

        # Khi nhấn ENTER sẽ tự động login
        self.loginw.bind('<Return>', self.checkuser)

    # CHECK USER IN DATABASE
    def checkuser(self, event=0):
        s = self.username.get()
        s1 = self.password.get()
        s = s.upper()
        s1 = s1.upper()

        self.cur.execute("SELECT * FROM users WHERE username=? AND password=?", (s, s1))
        l = self.cur.fetchall()

        if len(l) > 0:
            self.success()
        else:
            self.fail()

    # LOGIN SUCCESS
    def success(self):
        self.cur.execute("SELECT username, account_type FROM users WHERE username=?",
                         (self.username.get().strip().upper(),))
        user_info = self.cur.fetchone()
        if user_info:
            self.user_data = {
                "username": user_info[0],
                "account_type": user_info[1],
            }
            self.loginw.quit()
            self.loginw.withdraw()
        else:
            messagebox.showerror("Error", "User data not found!")

    # LOGIN FAILURE
    def fail(self):
        messagebox.showerror("Error", "The username or password is incorrect")

    # ONCLICK EVENTS
    def onclick(self, event):
        if self.username.get() in ["Username", "Choose your username"]:
            self.us.delete(0, "end")

    def onclick1(self, event):
        if self.password.get() in ["Password", "Create a password"]:
            self.pa.delete(0, "end")
            self.pa.config(show="*")
