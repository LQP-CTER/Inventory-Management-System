from tkinter import *
from tkinter import messagebox  # Để sử dụng messagebox
from tkinter import ttk  # Để sử dụng Treeview


class User:
    def __init__(self, mainw):
        self.mainw = mainw

    def user_mainmenu(self, a, b):
        """Main menu for the user."""
        self.mainframe = LabelFrame(self.mainw, width=1200, height=145, bg="#f7f7f7")
        self.mainframe.place(x=100, y=100)

        # Start x position and spacing for buttons
        start_x = 50
        button_spacing = 180

        # Dashboard Button
        dashboard_img = PhotoImage(file="images/dashboard.png").subsample(a, b)
        self.dashboard_button = Button(
            self.mainframe, text="Dashboard", font="roboto 11 bold", bd=5,
            image=dashboard_img, compound=TOP, command=self.show_dashboard)
        self.dashboard_button.image = dashboard_img
        self.dashboard_button.place(x=start_x, y=20)

        # Inbound Button
        inbound_img = PhotoImage(file="images/inbound.png").subsample(a, b)
        self.inbound_button = Button(
            self.mainframe, text="Inbound", font="roboto 11 bold", bd=5,
            image=inbound_img, compound=TOP, command=self.builditemtable)
        self.inbound_button.image = inbound_img
        self.inbound_button.place(x=start_x + button_spacing, y=20)

        # Outbound Button
        outbound_img = PhotoImage(file="images/outbound.png").subsample(a, b)
        self.outbound_button = Button(
            self.mainframe, text="Outbound", font="roboto 11 bold", bd=5,
            image=outbound_img, compound=TOP, command=self.outbound_transaction)
        self.outbound_button.image = outbound_img
        self.outbound_button.place(x=start_x + 2 * button_spacing, y=20)

        # Transfer Button
        transfer_img = PhotoImage(file="images/transfer.png").subsample(a, b)
        self.transfer_button = Button(
            self.mainframe, text="Transfer", font="roboto 11 bold", bd=5,
            image=transfer_img, compound=TOP, command=self.transfer_stock)
        self.transfer_button.image = transfer_img
        self.transfer_button.place(x=start_x + 3 * button_spacing, y=20)

        # Inventory Button
        inventory_img = PhotoImage(file="images/inventory.png").subsample(a, b)
        self.inventory_button = Button(
            self.mainframe, text="Inventory", font="roboto 11 bold", bd=5,
            image=inventory_img, compound=TOP, command=self.show_inventory)
        self.inventory_button.image = inventory_img
        self.inventory_button.place(x=start_x + 4 * button_spacing, y=20)

        # Change User Button
        change_user_img = PhotoImage(file="images/change1.png").subsample(a, b)
        self.changeuser_button = Button(
            self.mainframe, text="Change User", font="roboto 11 bold", bd=5,
            image=change_user_img, compound=TOP, command=self.change_user)
        self.changeuser_button.image = change_user_img
        self.changeuser_button.place(x=start_x + 5 * button_spacing, y=20)

        # Quit Button
        quit_img = PhotoImage(file="images/Door_Out-512.png").subsample(a, b)
        self.quit_button = Button(
            self.mainframe, text="Quit", font="roboto 11 bold", bd=5,
            image=quit_img, compound=TOP, command=self.quit_app)
        self.quit_button.image = quit_img
        self.quit_button.place(x=start_x + 6 * button_spacing, y=20)

    def builditemtable(self):
        """Hiển thị bảng với màu sắc tùy chỉnh."""
        try:
            # Tạo cửa sổ mới để hiển thị bảng
            item_table_window = Toplevel(self.mainw)
            item_table_window.title("Inbound Stock Table")
            item_table_window.geometry("900x600")
            item_table_window.configure(bg="#ecf0f1")

            # Khung chứa bảng
            table_frame = Frame(item_table_window, bg="#ecf0f1", relief=SOLID, bd=1)
            table_frame.pack(fill=BOTH, expand=True, padx=15, pady=15)

            # Scrollbar dọc
            tree_scroll_y = Scrollbar(table_frame, orient=VERTICAL)
            tree_scroll_y.pack(side=RIGHT, fill=Y)

            # Scrollbar ngang
            tree_scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
            tree_scroll_x.pack(side=BOTTOM, fill=X)

            # Cột và tiêu đề bảng
            columns = ["ID", "Name", "Category", "Quantity", "Unit Price"]
            tree = ttk.Treeview(
                table_frame,
                columns=columns,
                show="headings",
                yscrollcommand=tree_scroll_y.set,
                xscrollcommand=tree_scroll_x.set,
                style="Colored.Treeview"
            )
            tree.pack(fill=BOTH, expand=True)

            # Kết nối scrollbar
            tree_scroll_y.config(command=tree.yview)
            tree_scroll_x.config(command=tree.xview)

            # Định dạng tiêu đề và cột
            for col in columns:
                tree.heading(col, text=col, anchor=CENTER)  # Tiêu đề cột
                tree.column(col, anchor=CENTER, width=150)  # Căn giữa nội dung cột

            # Thêm dữ liệu mẫu
            sample_data = [
                [1, "Product A", "Category 1", 100, "$10.00"],
                [2, "Product B", "Category 2", 200, "$15.50"],
                [3, "Product C", "Category 3", 150, "$20.00"],
                [4, "Product D", "Category 1", 75, "$8.50"],
                [5, "Product E", "Category 2", 300, "$12.00"],
                [6, "Product F", "Category 3", 250, "$18.00"]
            ]

            for index, row in enumerate(sample_data):
                # Sử dụng màu nền thay thế
                bg_color = "#ffffff" if index % 2 == 0 else "#ecf0f1"
                tree.insert("", "end", values=row, tags=(bg_color,))

            # Tùy chỉnh màu sắc hàng
            tree.tag_configure("#ffffff", background="#ffffff")
            tree.tag_configure("#ecf0f1", background="#ecf0f1")

            # Hiệu ứng hover (khi di chuột qua hàng)
            def on_hover(event):
                row_id = tree.identify_row(event.y)
                tree.tag_configure("hover", background="#d5f5e3")
                if row_id:
                    tree.item(row_id, tags="hover")

            def on_leave(event):
                for index, item in enumerate(tree.get_children()):
                    bg_color = "#ffffff" if index % 2 == 0 else "#ecf0f1"
                    tree.item(item, tags=(bg_color,))

            tree.bind("<Motion>", on_hover)
            tree.bind("<Leave>", on_leave)

            # Thêm nút đóng cửa sổ
            close_button = Button(
                item_table_window,
                text="Close",
                font="Roboto 12 bold",
                bg="#e74c3c",
                fg="white",
                command=item_table_window.destroy,
                relief=SOLID,
                bd=1
            )
            close_button.pack(pady=10)

            # Tùy chỉnh giao diện Treeview
            style = ttk.Style()
            style.configure("Colored.Treeview.Heading",
                            font=("Roboto", 13, "bold"), background="#2c3e50", foreground="white", borderwidth=1)
            style.map("Colored.Treeview.Heading", background=[("active", "#3498db")])

            style.configure("Colored.Treeview",
                            font=("Roboto", 12), rowheight=35, background="#f4f6f9", fieldbackground="#f4f6f9",
                            borderwidth=0, highlightthickness=0)

        except Exception as e:
            messagebox.showerror("Error", f"Unable to open table: {e}")

    def show_dashboard(self):
        """Placeholder function for showing the dashboard."""
        messagebox.showinfo("Dashboard", "Dashboard functionality is under development.")

    def outbound_transaction(self):
        """Placeholder function for outbound transactions."""
        messagebox.showinfo("Outbound", "Outbound functionality is under development.")

    def transfer_stock(self):
        """Placeholder function for handling stock transfers."""
        messagebox.showinfo("Transfer", "Transfer functionality is under development.")

    def show_inventory(self):
        """Placeholder function for showing inventory."""
        messagebox.showinfo("Inventory", "Inventory functionality is under development.")

    def change_user(self):
        """Change the current user."""
        if messagebox.askyesno("Change User", "Are you sure you want to change user?"):
            self.mainw.destroy()

    def quit_app(self):
        """Quit the application."""
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.mainw.quit()
            exit(0)
