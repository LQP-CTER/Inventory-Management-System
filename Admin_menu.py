from tkinter import *
import sqlite3
from tkinter import ttk, Toplevel, Label, Entry, Button, messagebox
from Addtional_features import mycombobox, myentry
import webbrowser
from decimal import Decimal
from tkinter import ttk
import calendar
from inventory_management import engine, InventoryBalance, InventoryCategory, Inventory
from inventory_management import InventoryTransaction, InventoryTransactionDetail, Warehouse, Employee
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sqlalchemy import create_engine, func, distinct
from tkinter import messagebox
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, date


engine = create_engine('sqlite:///inventory_management_system.db')
Session = sessionmaker(bind=engine)
session = Session()


class Admin:
    def __init__(self, mainw):
        # Lưu tham chiếu đến cửa sổ chính
        self.mainw = mainw

        # Khởi tạo các biến cần thiết
        self.products_list = []  # Danh sách sản phẩm
        self.warehouse_var = StringVar()  # Biến chứa thông tin kho hàng đã chọn
        self.employee_var = StringVar()  # Biến chứa thông tin nhân viên đã chọn
        self.date_var = StringVar()  # Biến chứa ngày đã chọn
        self.product_entries = []  # Danh sách các entry sản phẩm

        # Tạo frame để chứa các sản phẩm và các widget khác
        self.products_frame = ttk.Frame(self.mainw)
        self.products_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Kết nối với cơ sở dữ liệu và tạo cursor
        self.conn = sqlite3.connect('./inventory_management_system.db')  # Đảm bảo đường dẫn cơ sở dữ liệu chính xác
        self.cur = self.conn.cursor()

        # Gọi phương thức setup_ui để tạo giao diện
        self.setup_ui()

    def setup_ui(self):
        """Set up giao diện."""
        # Khởi tạo các widgets trên giao diện như labels, comboboxes, entrys, buttons
        self.create_warehouse_dropdown()
        self.create_employee_dropdown()
        self.create_date_entry()

    def create_warehouse_dropdown(self):
        """Tạo dropdown để chọn kho hàng."""
        Label(self.products_frame, text="Select Warehouse:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.warehouse_combobox = ttk.Combobox(self.products_frame, textvariable=self.warehouse_var)
        self.warehouse_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.get_warehouses()

    def create_employee_dropdown(self):
        """Tạo dropdown để chọn nhân viên."""
        Label(self.products_frame, text="Select Employee:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.employee_combobox = ttk.Combobox(self.products_frame, textvariable=self.employee_var)
        self.employee_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.get_employees()  # Gọi hàm này mà không cần truyền tham số

    def create_date_entry(self):
        """Tạo entry để nhập ngày."""
        Label(self.products_frame, text="Select Date:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        date_entry = Entry(self.products_frame, textvariable=self.date_var)
        date_entry.grid(row=2, column=1, padx=5, pady=5)

    def close_connection(self):
        """Đảm bảo đóng kết nối khi không sử dụng."""
        self.conn.close()
#---------------------------------------DASHBOARD--------------------------------------------------------
    def show_dashboard(self):
        """Hiển thị Dashboard với thanh Scrollbar và hỗ trợ cuộn bằng chuột."""
        try:
            # Kiểm tra nếu Dashboard đã tồn tại
            if hasattr(self, 'dashboard_window') and self.dashboard_window.winfo_exists():
                self.dashboard_window.lift()  # Đưa cửa sổ Dashboard lên trên nếu đã mở
                return

            # Tạo cửa sổ Toplevel cho Dashboard
            self.dashboard_window = Toplevel(self.mainw)
            self.dashboard_window.title("📊 Dashboard Tổng Quan")
            self.dashboard_window.geometry("1200x800")
            self.dashboard_window.config(bg="#f7f9fc")  # Màu nền sáng dịu

            # Khóa cửa sổ chính khi Dashboard đang mở
            self.mainw.attributes("-disabled", True)

            # Hàm đóng Dashboard và mở lại cửa sổ chính
            def close_dashboard():
                self.dashboard_window.unbind_all("<MouseWheel>")
                self.mainw.attributes("-disabled", False)
                self.dashboard_window.destroy()

            self.dashboard_window.protocol("WM_DELETE_WINDOW", close_dashboard)

            # Tạo khung tiêu đề và bộ lọc trên cùng
            top_frame = Frame(self.dashboard_window, bg="#ffffff", relief="groove", bd=2)
            top_frame.pack(side=TOP, fill=X, padx=20, pady=20)

            # Tiêu đề Dashboard
            Label(
                top_frame,
                text="📊 DASHBOARD TỔNG QUAN",
                bg="#ffffff",
                font="Roboto 22 bold",
                fg="#1f78b4",
            ).grid(row=0, column=0, columnspan=6, pady=10)

            # Dropdown chọn tháng
            Label(top_frame, text="Chọn tháng:", bg="#ffffff", font="Roboto 12").grid(
                row=1, column=0, padx=10, pady=10
            )
            month_var = ttk.Combobox(
                top_frame, values=[str(m) for m in range(1, 13)], width=10, state="readonly"
            )
            month_var.set(str(datetime.now().month))
            month_var.grid(row=1, column=1, padx=10, pady=10)

            # Dropdown chọn năm
            Label(top_frame, text="Chọn năm:", bg="#ffffff", font="Roboto 12").grid(
                row=1, column=2, padx=10, pady=10
            )
            year_var = ttk.Combobox(
                top_frame,
                values=[str(y) for y in range(2000, datetime.now().year + 1)],
                width=10,
                state="readonly",
            )
            year_var.set(str(datetime.now().year))
            year_var.grid(row=1, column=3, padx=10, pady=10)

            # Nút "Xem" để cập nhật dữ liệu
            view_button = Button(
                top_frame,
                text="Xem",
                bg="#1f78b4",
                fg="white",
                font="Roboto 12 bold",
                command=lambda: self.update_dashboard(scrollable_frame, int(month_var.get()), int(year_var.get())),
                activebackground="#64b5f6",
                activeforeground="#ffffff",
                cursor="hand2",
                relief=SOLID,
                bd=2,
            )
            view_button.grid(row=1, column=4, padx=10, pady=10)

            # Tạo khung Canvas có scrollbar
            canvas = Canvas(self.dashboard_window, bg="#f7f9fc", highlightthickness=0)
            scrollbar = Scrollbar(self.dashboard_window, orient="vertical", command=canvas.yview)
            canvas.configure(yscrollcommand=scrollbar.set)

            # Tạo khung chứa nội dung Dashboard
            scrollable_frame = Frame(canvas, bg="#f7f9fc")
            scrollable_frame.bind(
                "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.pack(side=LEFT, fill=BOTH, expand=True)
            scrollbar.pack(side=RIGHT, fill=Y)

            # **Hỗ trợ cuộn bằng con lăn chuột**
            def on_mouse_wheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            self.dashboard_window.bind_all("<MouseWheel>", on_mouse_wheel)

            # Hiển thị dữ liệu mặc định
            self.update_dashboard(scrollable_frame, datetime.now().month, datetime.now().year)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi hiển thị Dashboard: {e}")

    def update_dashboard(self, scrollable_frame, month, year):
        """Cập nhật dữ liệu và hiển thị trên Dashboard với nhiều biểu đồ và bảng có scrollbar."""
        try:
            # Xóa toàn bộ nội dung cũ trong scrollable_frame
            for widget in scrollable_frame.winfo_children():
                widget.destroy()

            # Xác định khoảng thời gian
            start_date = datetime(year, month, 1).date()
            end_date = datetime(year, month, calendar.monthrange(year, month)[1]).date()

            # Truy vấn tổng tồn kho, nhập, và xuất
            total_stock = self.session.query(func.sum(InventoryBalance.initial_stock)).scalar() or 0
            total_import = self.session.query(func.sum(InventoryBalance.quantity_imported)).filter(
                InventoryBalance.Date.between(start_date, end_date)
            ).scalar() or 0
            total_export = self.session.query(func.sum(InventoryBalance.export_quantity)).filter(
                InventoryBalance.Date.between(start_date, end_date)
            ).scalar() or 0

            # **Hiển thị dữ liệu tổng quan**
            summary_frame = Frame(scrollable_frame, bg="#f7f9fc")
            summary_frame.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

            Label(summary_frame, text=f"Tồn kho tổng: {total_stock}", font="Roboto 14 bold", bg="#e8f5fe",
                  fg="#333", relief="solid", bd=1).grid(row=0, column=0, padx=10, pady=10, sticky="w")
            Label(summary_frame, text=f"Tổng nhập: {total_import}", font="Roboto 14 bold", bg="#e8f5fe",
                  fg="#4caf50", relief="solid", bd=1).grid(row=0, column=1, padx=10, pady=10, sticky="w")
            Label(summary_frame, text=f"Tổng xuất: {total_export}", font="Roboto 14 bold", bg="#e8f5fe",
                  fg="#f44336", relief="solid", bd=1).grid(row=0, column=2, padx=10, pady=10, sticky="w")

            # **Biểu đồ cột - Tổng quan nhập, xuất, tồn kho**
            figure_bar = Figure(figsize=(6, 3), dpi=100)
            ax_bar = figure_bar.add_subplot(111)
            categories = ['Tồn kho', 'Nhập', 'Xuất']
            values = [total_stock, total_import, total_export]
            ax_bar.bar(categories, values, color=['#42a5f5', '#4caf50', '#f44336'])
            ax_bar.set_title(f"Tổng quan {calendar.month_name[month]} {year}", fontsize=14)
            ax_bar.set_ylabel("Số lượng")
            ax_bar.set_xlabel("Danh mục")

            # **Biểu đồ Pie - Phân bổ nhập xuất tồn kho**
            figure_pie = Figure(figsize=(6, 3), dpi=100)
            ax_pie = figure_pie.add_subplot(111)
            ax_pie.pie([total_stock, total_import, total_export], labels=['Tồn kho', 'Nhập', 'Xuất'],
                       autopct='%1.1f%%', startangle=90, colors=['#42a5f5', '#4caf50', '#f44336'])
            ax_pie.set_title(f"Phân bổ {calendar.month_name[month]} {year}", fontsize=14)

            # **Hiển thị biểu đồ cột và pie trong cùng một hàng**
            chart_frame = Frame(scrollable_frame, bg="#f7f9fc")
            chart_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

            canvas_bar = FigureCanvasTkAgg(figure_bar, chart_frame)
            canvas_bar.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)

            canvas_pie = FigureCanvasTkAgg(figure_pie, chart_frame)
            canvas_pie.get_tk_widget().grid(row=0, column=1, padx=10, pady=10)

            # **Biểu đồ đường - Nhập kho theo ngày**
            figure_line = Figure(figsize=(6, 3), dpi=100)
            ax_line = figure_line.add_subplot(111)
            daily_imports = self.session.query(
                func.date(InventoryBalance.Date).label('day'),
                func.sum(InventoryBalance.quantity_imported).label('total_import')
            ).filter(InventoryBalance.Date.between(start_date, end_date)) \
                .group_by(func.date(InventoryBalance.Date)) \
                .all()

            dates = [entry.day for entry in daily_imports]
            imports = [entry.total_import for entry in daily_imports]

            ax_line.plot(dates, imports, marker='o', color='green', label="Nhập kho", linewidth=2)
            ax_line.set_title("Nhập kho theo ngày", fontsize=14)
            ax_line.set_xlabel("Ngày")
            ax_line.set_ylabel("Số lượng nhập")
            ax_line.legend()

            # Hiển thị biểu đồ đường và bảng dữ liệu
            line_chart_frame = Frame(scrollable_frame, bg="#f7f9fc")
            line_chart_frame.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")

            canvas_line = FigureCanvasTkAgg(figure_line, line_chart_frame)
            canvas_line.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)

            # **Bảng dữ liệu từ Inventory Transaction với scrollbar**
            table_frame = Frame(scrollable_frame, bg="#f7f9fc", relief="solid", bd=1)
            table_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

            # Scrollbar
            tree_scroll = Scrollbar(table_frame, orient="vertical")
            tree_scroll.pack(side=RIGHT, fill=Y)

            # Bảng Treeview
            columns = ["Transaction_ID", "Transaction_Type", "Warehouse_ID", "Employee_ID", "Transaction_Date"]
            tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10,
                                yscrollcommand=tree_scroll.set)
            tree.pack(side=LEFT, fill=BOTH, expand=True)
            tree_scroll.config(command=tree.yview)

            # Đặt tiêu đề cho các cột
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor="center", width=120)

            # Lấy dữ liệu từ InventoryTransaction và hiển thị
            transactions = self.session.query(InventoryTransaction).all()
            if transactions:
                for transaction in transactions:
                    # Lấy giá trị ngày từ Transaction_Date
                    transaction_date = transaction.Transaction_Date
                    formatted_date = str(transaction_date) if transaction_date else "Không xác định"

                    # Thêm dữ liệu vào bảng
                    tree.insert("", "end", values=(
                        transaction.Transaction_ID,
                        transaction.Transaction_Type,
                        transaction.Warehouse_ID,
                        transaction.Employee_ID,
                        formatted_date
                    ))
            else:
                # Nếu không có dữ liệu
                tree.insert("", "end", values=("Không có dữ liệu", "", "", "", ""))

            # **Thêm nút mở Power BI**
            powerbi_button = Button(
                scrollable_frame,
                text="Power BI",
                bg="#4caf50",
                fg="white",
                font="Roboto 12 bold",
                command=self.open_power_bi_dashboard,
                cursor="hand2",
                relief=SOLID,
                bd=2
            )
            powerbi_button.grid(row=3, column=0, columnspan=2, pady=20)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi cập nhật Dashboard: {e}")

    def open_power_bi_dashboard(self):
        """Mở Power BI."""
        try:
            power_bi_url = "https://app.powerbi.com/links/7_Q7WkghpA?ctid=2f927364-2461-4f96-8c6a-bffe0bd18175&pbi_source=linkShare&bookmarkGuid=52206233-179a-4046-8c9d-1530f9fda858"
            import webbrowser
            webbrowser.open(power_bi_url)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở Dashboard Power BI: {e}")

    def ensure_connection(self):
        if not hasattr(self, 'conn') or self.conn is None:
            self.conn = sqlite3.connect('inventory_management_system.db')
            self.cur = self.conn.cursor()
        elif self.conn:
            try:
                self.cur.execute("SELECT 1")  # Test connection
            except sqlite3.ProgrammingError:
                self.conn = sqlite3.connect('inventory_management_system.db')
                self.cur = self.conn.cursor()

    def update_dropdown_values(self, dropdown, value_dict, key_var, display_var):
        key_var.set(value_dict.get(display_var.get(), ""))
#------------------------------------INBOUND------------------------------------------------------------------------

    def inbound_stock(self, product_details, selected_warehouse_id, selected_employee_id):
        try:
            transaction_id = f"GD{datetime.now().strftime('%Y%m%d%H%M%S')}"
            transaction_date = datetime.now()

            # Thêm giao dịch nhập kho
            new_transaction = InventoryTransaction(
                Transaction_ID=transaction_id,
                Transaction_Type="Nhập kho",
                Warehouse_ID=selected_warehouse_id,
                Employee_ID=selected_employee_id,
                Transaction_Date=transaction_date,
            )
            self.session.add(new_transaction)

            for idx, product in enumerate(product_details):
                product_name = product["product_var"]
                quantity = int(product["quantity_var"])
                unit_price = Decimal(product["unit_price_var"])  # Chuyển đổi sang Decimal
                unit_type = product["unit_type_var"]

                # Lấy Product_ID từ Product_Name
                product_query = self.session.query(Inventory).filter_by(Product_Name=product_name).first()
                if not product_query:
                    raise ValueError(f"Sản phẩm '{product_name}' không tồn tại trong cơ sở dữ liệu.")
                product_id = product_query.Product_ID

                detail_id = f"DT{product_id}{idx + 1}{datetime.now().strftime('%Y%m%d%H%M%S')}"

                # Thêm chi tiết giao dịch
                new_detail = InventoryTransactionDetail(
                    Detail_ID=detail_id,
                    Transaction_ID=transaction_id,
                    Product_ID=product_id,
                    Product_Name=product_name,
                    Unit_Type=unit_type,
                    Quantity=quantity,
                    Unit_Price=unit_price,
                    Total_Price=quantity * unit_price,
                )
                self.session.add(new_detail)

                # Cập nhật hoặc thêm bản ghi tồn kho
                balance_query = self.session.query(InventoryBalance).filter_by(
                    Product_ID=product_id, Warehouse_ID=selected_warehouse_id
                ).first()

                if balance_query:
                    # Nếu đã tồn tại, cập nhật số lượng và giá trị
                    balance_query.initial_stock += quantity
                    balance_query.quantity_imported += quantity
                    balance_query.Total_Price_Import += quantity * unit_price
                else:
                    # Nếu chưa tồn tại, thêm bản ghi mới
                    inventory_balance_id = f"IB{product_id}{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    new_balance = InventoryBalance(
                        Inventory_Balance_ID=inventory_balance_id,
                        Warehouse_ID=selected_warehouse_id,
                        Product_ID=product_id,
                        Date=transaction_date,
                        Product_Name=product_name,
                        Unit_Type=unit_type,
                        initial_stock=quantity,
                        quantity_imported=quantity,
                        Unit_Price_Import=unit_price,
                        Total_Price_Import=quantity * unit_price,
                    )
                    self.session.add(new_balance)

            # Commit dữ liệu
            self.session.commit()
            messagebox.showinfo("Thông báo", "Nhập kho thành công!")

        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

    def inbound_stock_window(self):
        try:
            inbound_window = Toplevel(self.mainw)
            inbound_window.title("📦 Nhập Kho")
            inbound_window.geometry("1000x800")
            inbound_window.config(bg="#f2f5f8")

            # Kết nối cơ sở dữ liệu để lấy danh sách sản phẩm, kho hàng và nhân viên
            conn = sqlite3.connect('inventory_management_system.db')
            cursor = conn.cursor()

            cursor.execute("SELECT Product_Name FROM inventory")
            products = [row[0] for row in cursor.fetchall()]

            cursor.execute("SELECT Warehouse_ID, Name FROM warehouses")
            warehouses = {row[1]: row[0] for row in cursor.fetchall()}  # Tên kho -> Mã kho

            cursor.execute("SELECT Employee_ID, Employee_Name FROM employees")
            employees = {row[1]: row[0] for row in cursor.fetchall()}  # Tên nhân viên -> Mã nhân viên

            conn.close()

            products_list = []

            # Khung chọn kho hàng và nhân viên
            general_frame = Frame(inbound_window, bg="#e8f5fe", relief="solid", borderwidth=1, padx=10, pady=10)
            general_frame.pack(fill="x", padx=15, pady=15)

            Label(general_frame, text="Kho hàng:", font="Roboto 12 bold", bg="#e8f5fe").grid(row=0, column=0, padx=10,
                                                                                             pady=5, sticky="w")
            selected_warehouse_name = StringVar()
            warehouse_combobox = ttk.Combobox(
                general_frame, textvariable=selected_warehouse_name, values=list(warehouses.keys()), state="readonly",
                width=30
            )
            warehouse_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="w")

            Label(general_frame, text="Nhân viên:", font="Roboto 12 bold", bg="#e8f5fe").grid(row=1, column=0, padx=10,
                                                                                              pady=5, sticky="w")
            selected_employee_name = StringVar()
            employee_combobox = ttk.Combobox(
                general_frame, textvariable=selected_employee_name, values=list(employees.keys()), state="readonly",
                width=30
            )
            employee_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="w")

            # Hàm thêm sản phẩm mới vào danh sách
            def add_product_row():
                row_index = len(products_list) + 1
                product_var = StringVar()
                quantity_var = StringVar()
                unit_price_var = StringVar()
                unit_type_var = StringVar()

                frame = Frame(products_frame, bg="#ffffff")
                frame.grid(row=row_index, column=0, columnspan=8, sticky="w", pady=5)

                Label(frame, text=f"{row_index}.", bg="#ffffff", font="Roboto 11").grid(row=0, column=0, padx=5)

                product_combobox = ttk.Combobox(frame, textvariable=product_var, values=products, state="readonly",
                                                width=25)
                product_combobox.grid(row=0, column=1, padx=5)

                quantity_entry = Entry(frame, textvariable=quantity_var, width=10, font="Roboto 11")
                quantity_entry.grid(row=0, column=2, padx=5)

                unit_price_entry = Entry(frame, textvariable=unit_price_var, width=15, font="Roboto 11")
                unit_price_entry.grid(row=0, column=3, padx=5)

                unit_type_entry = Entry(frame, textvariable=unit_type_var, width=15, font="Roboto 11")
                unit_type_entry.grid(row=0, column=4, padx=5)

                # Nút xóa dòng
                delete_button = Button(frame, text="Xóa", bg="#e74c3c", fg="white", font="Roboto 11",
                                       command=lambda: delete_product_row(frame))
                delete_button.grid(row=0, column=5, padx=10)

                products_list.append({
                    "frame": frame,
                    "product_var": product_var,
                    "quantity_var": quantity_var,
                    "unit_price_var": unit_price_var,
                    "unit_type_var": unit_type_var,
                })

            # Hàm xóa dòng sản phẩm
            def delete_product_row(frame):
                for product in products_list:
                    if product["frame"] == frame:
                        products_list.remove(product)
                        break
                frame.destroy()

            # Khung hiển thị danh sách sản phẩm
            products_frame = Frame(inbound_window, bg="#ffffff", relief="solid", borderwidth=1, padx=10, pady=10)
            products_frame.pack(fill=BOTH, expand=True, padx=15, pady=15)

            # Tiêu đề danh sách sản phẩm
            header_frame = Frame(products_frame, bg="#f1f1f1")
            header_frame.grid(row=0, column=0, columnspan=6, sticky="w", pady=5)

            Label(header_frame, text="Tên sản phẩm", bg="#f1f1f1", font="Roboto 11 bold", width=25).grid(row=0,
                                                                                                         column=1)
            Label(header_frame, text="Số lượng", bg="#f1f1f1", font="Roboto 11 bold", width=10).grid(row=0, column=2)
            Label(header_frame, text="Đơn giá", bg="#f1f1f1", font="Roboto 11 bold", width=15).grid(row=0, column=3)
            Label(header_frame, text="Đơn vị", bg="#f1f1f1", font="Roboto 11 bold", width=15).grid(row=0, column=4)
            Label(header_frame, text="", bg="#f1f1f1", width=8).grid(row=0, column=5)  # Để nút xóa

            # Nút thêm sản phẩm
            add_product_button = Button(inbound_window, text="Thêm sản phẩm", command=add_product_row, bg="#4caf50",
                                        fg="#fff", font="Roboto 12 bold")
            add_product_button.pack(pady=10)

            # Nút xác nhận nhập kho
            submit_button = Button(
                inbound_window,
                text="Nhập kho",
                font="Roboto 14 bold",
                bg="#2196f3",
                fg="#fff",
                command=lambda: self.inbound_stock(
                    product_details=[
                        {
                            "product_var": p["product_var"].get(),
                            "quantity_var": p["quantity_var"].get(),
                            "unit_price_var": p["unit_price_var"].get(),
                            "unit_type_var": p["unit_type_var"].get(),
                        }
                        for p in products_list
                    ],
                    selected_warehouse_id=warehouses[selected_warehouse_name.get()],
                    selected_employee_id=employees[selected_employee_name.get()],
                ),
            )
            submit_button.pack(pady=20)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

    def calculate_total_export_value(self, selected_product, selected_warehouse, quantity_var, total_value_label):
        try:
            product_name = selected_product.get()
            warehouse_name = selected_warehouse.get()
            quantity = quantity_var.get()

            if not product_name or not warehouse_name or not quantity.isdigit():
                total_value_label.config(text="Vui lòng chọn sản phẩm, kho hàng và nhập số lượng hợp lệ.")
                return

            quantity = int(quantity)
            if quantity <= 0:
                total_value_label.config(text="Số lượng phải lớn hơn 0.")
                return

            # Lấy giá trị đơn giá sản phẩm
            self.cur.execute(
                """
                SELECT Unit_Price 
                FROM inventory_balance
                WHERE Product_ID = (SELECT Product_ID FROM inventory WHERE Product_Name = ?)
                  AND Warehouse_ID = (SELECT Warehouse_ID FROM warehouses WHERE Name = ?)
                """, (product_name, warehouse_name))
            unit_price = self.cur.fetchone()

            if not unit_price or unit_price[0] is None:
                total_value_label.config(text="Không tìm thấy đơn giá cho sản phẩm trong kho.")
                return

            # Tính tổng giá trị
            total_value = unit_price[0] * quantity
            total_value_label.config(text=f"Tổng giá trị xuất: {total_value:.2f} VNĐ")

        except Exception as e:
            total_value_label.config(text=f"Lỗi khi tính giá trị: {e}")
#------------------------Outbound Stock-------------------------------------

    def outbound_stock(self):
        """ Setup the Outbound tab in a new window with enhanced UI and delete using Backspace """
        outbound_window = Toplevel(self.mainw)
        outbound_window.title("Outbound Stock Management")
        outbound_window.geometry("1000x700")

        # Đặt lại font và màu sắc cho tiêu đề
        Label(outbound_window, text="Outbound Stock Management", font=("Arial", 20, "bold"),
              bg="#4CAF50", fg="white").pack(fill=X)

        # === Tạo layout hai khung chính ===
        left_frame = Frame(outbound_window, bg="#f0f0f0", width=500, relief=GROOVE, bd=2)
        left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

        right_frame = Frame(outbound_window, bg="#f0f0f0", width=500, relief=GROOVE, bd=2)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        # === LEFT FRAME: STOCK INFORMATION ===
        Label(left_frame, text="Stock Information", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
        stock_treeview = ttk.Treeview(left_frame, columns=("Warehouse", "Product", "Quantity"), show="headings")
        stock_treeview.heading("Warehouse", text="Warehouse")
        stock_treeview.heading("Product", text="Product")
        stock_treeview.heading("Quantity", text="Quantity")
        stock_treeview.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Fetch stock information
        self.update_stock_information(stock_treeview)

        # === RIGHT FRAME: OUTBOUND OPERATIONS ===
        Label(right_frame, text="Outbound Operations", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
        form_frame = Frame(right_frame, bg="#f0f0f0")
        form_frame.pack(pady=20)

        # Warehouse selection
        Label(form_frame, text="Warehouse:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5, sticky=W)
        warehouse_var = StringVar()
        warehouse_combobox = ttk.Combobox(form_frame, textvariable=warehouse_var, state="readonly")
        warehouse_combobox.grid(row=0, column=1, padx=5, pady=5)
        warehouse_combobox['values'] = self.get_warehouses()

        # Product selection
        Label(form_frame, text="Product:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5, sticky=W)
        product_var = StringVar()
        product_combobox = ttk.Combobox(form_frame, textvariable=product_var, state="readonly")
        product_combobox.grid(row=1, column=1, padx=5, pady=5)
        product_combobox['values'] = self.get_products()

        # Employee selection
        Label(form_frame, text="Employee:", bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self.employee_var = StringVar()
        employee_combobox = ttk.Combobox(form_frame, textvariable=self.employee_var, state="readonly")
        employee_combobox.grid(row=2, column=1, padx=5, pady=5)
        employee_combobox['values'] = self.get_employees()

        # Quantity entry
        Label(form_frame, text="Quantity:", bg="#f0f0f0").grid(row=3, column=0, padx=5, pady=5, sticky=W)
        quantity_var = IntVar()
        quantity_entry = Entry(form_frame, textvariable=quantity_var, font="Roboto 12", width=15)
        quantity_entry.grid(row=3, column=1, padx=5, pady=5)

        # === Outbound products listbox ===
        self.outbound_listbox = Listbox(right_frame, height=15, width=60, font=("Arial", 12))
        self.outbound_listbox.pack(pady=10)

        # Gán phím Backspace để xóa giống chức năng Transfer
        self.outbound_listbox.bind("<BackSpace>", lambda event: self.delete_selected_item(self.outbound_listbox))

        # === BUTTONS ===
        # Button thêm vào danh sách outbound
        add_button = Button(form_frame, text="Add to Outbound",
                            command=lambda: self.add_outbound_product(product_combobox, warehouse_combobox,
                                                                      quantity_entry),
                            bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        add_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Button xác nhận xuất kho
        confirm_button = Button(form_frame, text="Confirm Outbound",
                                command=lambda: self.confirm_outbound(self.outbound_listbox, stock_treeview),
                                bg="#FF5722", fg="white", font=("Arial", 12, "bold"))
        confirm_button.grid(row=6, column=0, columnspan=2, pady=10)

    def get_warehouses(self):
        """ Fetch the list of warehouse names from the database """
        self.cur.execute("SELECT Name FROM warehouses")
        warehouses = [row[0] for row in self.cur.fetchall()]
        return warehouses

    def get_products(self):
        """ Fetch the list of products from the database """
        self.cur.execute("SELECT Product_Name FROM inventory")
        products = [product[0] for product in self.cur.fetchall()]
        return products

    def get_employees(self):
        """ Lấy danh sách nhân viên từ database """
        self.cur.execute("SELECT Employee_ID, Employee_Name FROM employees")
        employees = self.cur.fetchall()
        return [f"{emp[0]} - {emp[1]}" for emp in employees]

    def update_stock_information(self, treeview):
        """ Fetch and display the stock information in the Treeview """
        self.cur.execute("""
            SELECT w.Name AS Warehouse_Name, i.Product_Name, 
                   SUM(b.initial_stock + b.quantity_imported - b.export_quantity) AS Total_Quantity
            FROM inventory_balance b
            JOIN warehouses w ON b.Warehouse_ID = w.Warehouse_ID
            JOIN inventory i ON b.Product_ID = i.Product_ID
            GROUP BY w.Name, i.Product_Name
        """)
        stock_data = self.cur.fetchall()

        # Clear previous data in Treeview
        treeview.delete(*treeview.get_children())

        # Insert all new data from the database
        for row in stock_data:
            treeview.insert("", "end", values=row)  # Add each row from the result set

    def add_outbound_product(self, product_combobox, warehouse_combobox, quantity_entry):
        try:
            product_name = product_combobox.get()
            warehouse_name = warehouse_combobox.get()
            quantity = quantity_entry.get()

            if not product_name or not warehouse_name or not quantity:
                messagebox.showerror("Error", "Please fill in all fields")
                return

            if not quantity.isdigit():
                messagebox.showerror("Error", "Quantity must be a valid integer")
                return
            quantity = int(quantity)

            # Thêm sản phẩm vào danh sách xuất kho
            self.outbound_listbox.insert(
                END, f"{product_name} ({warehouse_name}) - {quantity} units"
            )
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while adding outbound product: {e}")

    def confirm_outbound(self, outbound_listbox, stock_treeview):
        try:
            products_to_export = outbound_listbox.get(0, 'end')

            if not products_to_export:
                messagebox.showerror("Error", "No products selected for outbound")
                return

            employee_id_full = self.employee_var.get()
            if not employee_id_full:
                messagebox.showerror("Error", "Please select an employee.")
                return

            # Lấy mã nhân viên
            employee_id = employee_id_full.split(" - ")[0]
            transaction_id = 'GD' + str(datetime.now().timestamp()).replace('.', '')

            for index, product_entry in enumerate(products_to_export, start=1):
                product_name, details = product_entry.split(" (")
                warehouse_name, rest_details = details.split(") - ")
                quantity_details = rest_details.split(" units")[0]
                quantity = int(quantity_details.strip())

                # Truy vấn Product_ID và Warehouse_ID
                self.cur.execute("SELECT Product_ID FROM inventory WHERE Product_Name = ?", (product_name,))
                product_id = self.cur.fetchone()[0]

                self.cur.execute("SELECT Warehouse_ID FROM warehouses WHERE Name = ?", (warehouse_name,))
                warehouse_id = self.cur.fetchone()[0]

                # Tính toán Unit_Price theo bình quân gia quyền
                self.cur.execute("""
                    SELECT SUM(initial_stock + quantity_imported - export_quantity) AS Total_Quantity,
                           SUM(Total_Price + Total_Price_Import - Total_Price_Export) AS Total_Value
                    FROM inventory_balance
                    WHERE Product_ID = ? AND Warehouse_ID = ?
                """, (product_id, warehouse_id))
                total_quantity, total_value = self.cur.fetchone()

                unit_price = total_value / total_quantity if total_quantity > 0 else 0
                total_price = unit_price * quantity

                # Kiểm tra tồn kho đủ số lượng không
                if quantity > total_quantity:
                    messagebox.showerror("Error", f"Not enough stock for {product_name} in {warehouse_name}.")
                    return

                # Ghi nhận giao dịch xuất kho vào bảng `inventory_transaction`
                self.cur.execute("""
                    INSERT INTO inventory_transaction (Transaction_ID, Transaction_Type, Warehouse_ID, Employee_ID, Transaction_Date)
                    VALUES (?, 'Xuất kho', ?, ?, ?)
                """, (transaction_id, warehouse_id, employee_id, datetime.now().date()))

                # Ghi nhận chi tiết giao dịch vào bảng `inventory_transaction_detail`
                detail_id = f"DT{int(datetime.now().timestamp())}{index}"
                self.cur.execute("""
                    INSERT INTO inventory_transaction_detail 
                    (Detail_ID, Transaction_ID, Product_ID, Product_Name, Unit_Type, Quantity, Unit_Price, Total_Price)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (detail_id, transaction_id, product_id, product_name, 'unit', quantity, unit_price, total_price))

                # Cập nhật bảng `inventory_balance`
                # Thêm bản ghi xuất kho mới và cập nhật tồn kho
                balance_id = f"IB{int(datetime.now().timestamp())}{index}"
                self.cur.execute("""
                    INSERT INTO inventory_balance 
                    (Inventory_Balance_ID, Warehouse_ID, Product_ID, Date, Product_Name, Unit_Type, 
                     initial_stock, quantity_imported, export_quantity, Unit_Price, Total_Price, 
                     Unit_Price_Export, Total_Price_Export)
                    VALUES (?, ?, ?, ?, ?, ?, 0, 0, ?, ?, ?, ?, ?)
                """, (balance_id, warehouse_id, product_id, datetime.now().date(), product_name, 'unit',
                      quantity, unit_price, total_price, unit_price, total_price))

            # Commit dữ liệu vào cả 3 bảng
            self.conn.commit()
            self.update_stock_information(stock_treeview)
            messagebox.showinfo("Success", "Outbound process completed successfully")

        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", f"An error occurred while confirming outbound: {e}")

    def delete_selected_item(self, outbound_listbox):
        try:
            selected_index = outbound_listbox.curselection()
            if selected_index:
                outbound_listbox.delete(selected_index)
            else:
                messagebox.showinfo("Info", "No item selected to delete.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while deleting the item: {e}")

    #---------------------------------------------------------------------------------------------
    def check_stock(self, warehouse_id, product_id, quantity):
        # Check the available stock for a specific product in a warehouse
        self.cur.execute(
            "SELECT initial_stock + quantity_imported - export_quantity AS available_stock "
            "FROM inventory_balance WHERE Warehouse_ID = ? AND Product_ID = ?",
            (warehouse_id, product_id),
        )
        result = self.cur.fetchone()
        if result and result[0] >= quantity:
            return True
        return False

    def update_outbound_transaction(self, employee_id, warehouse_id, product_id, quantity, total_price):
        """Cập nhật thông tin xuất kho vào cơ sở dữ liệu."""
        # Insert vào bảng inventory_transaction
        self.cur.execute(
            "INSERT INTO inventory_transaction (Transaction_Type, Warehouse_ID, Employee_ID, Transaction_Date) "
            "VALUES ('Outbound', ?, ?, ?)", (warehouse_id, employee_id, datetime.today().strftime('%Y-%m-%d')))
        transaction_id = self.cur.lastrowid  # Get the ID of the last inserted transaction

        # Insert vào bảng inventory_transaction_detail
        self.cur.execute("INSERT INTO inventory_transaction_detail (Transaction_ID, Product_ID, Quantity, Total_Price) "
                         "VALUES (?, ?, ?, ?)", (transaction_id, product_id, quantity, total_price))

        # Cập nhật số lượng tồn kho trong bảng inventory_balance
        self.cur.execute(
            "UPDATE inventory_balance SET export_quantity = export_quantity + ? WHERE Warehouse_ID = ? AND Product_ID = ?",
            (quantity, warehouse_id, product_id))

        self.conn.commit()


    #--------------------------------------------------Transfer Stock--------------------------------------------------
    def transfer_stock(self):
        """ Setup the Transfer tab in a new window """
        transfer_window = Toplevel(self.mainw)
        transfer_window.title("Transfer Stock Management")
        transfer_window.geometry("900x600")

        Label(transfer_window, text="Transfer Stock", font=("Arial", 16, "bold"),
              bg="#4CAF50", fg="white").pack(fill=X)

        left_frame = Frame(transfer_window, bg="#ffffff", width=450)
        left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

        right_frame = Frame(transfer_window, bg="#ffffff", width=450)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=5)

        # Left Frame: Stock Information
        Label(left_frame, text="Stock Information", font=("Arial", 16, "bold"), bg="#ffffff").pack(pady=10)
        stock_treeview = ttk.Treeview(left_frame, columns=("Warehouse", "Product", "Quantity"), show="headings")
        stock_treeview.heading("Warehouse", text="Warehouse")
        stock_treeview.heading("Product", text="Product")
        stock_treeview.heading("Quantity", text="Quantity")
        stock_treeview.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.update_stock_information(stock_treeview)

        # Right Frame: Transfer Functionality
        Label(right_frame, text="Transfer Operations", font=("Arial", 16, "bold"), bg="#ffffff").pack(pady=10)
        form_frame = Frame(right_frame, bg="#ffffff")
        form_frame.pack(pady=20)

        # From Warehouse selection
        Label(form_frame, text="From Warehouse:", bg="#ffffff").grid(row=0, column=0, padx=5, pady=5, sticky=W)
        from_warehouse_var = StringVar()
        from_warehouse_combobox = ttk.Combobox(form_frame, textvariable=from_warehouse_var, state="readonly")
        from_warehouse_combobox.grid(row=0, column=1, padx=5, pady=5)
        from_warehouse_combobox['values'] = self.get_warehouses()

        # To Warehouse selection
        Label(form_frame, text="To Warehouse:", bg="#ffffff").grid(row=1, column=0, padx=5, pady=5, sticky=W)
        to_warehouse_var = StringVar()
        to_warehouse_combobox = ttk.Combobox(form_frame, textvariable=to_warehouse_var, state="readonly")
        to_warehouse_combobox.grid(row=1, column=1, padx=5, pady=5)
        to_warehouse_combobox['values'] = self.get_warehouses()

        # Product selection
        Label(form_frame, text="Product:", bg="#ffffff").grid(row=2, column=0, padx=5, pady=5, sticky=W)
        product_var = StringVar()
        product_combobox = ttk.Combobox(form_frame, textvariable=product_var, state="readonly")
        product_combobox.grid(row=2, column=1, padx=5, pady=5)
        product_combobox['values'] = self.get_products()

        # Employee selection
        Label(form_frame, text="Employee:", bg="#ffffff").grid(row=3, column=0, padx=5, pady=5, sticky=W)
        employee_var = StringVar()
        employee_combobox = ttk.Combobox(form_frame, textvariable=employee_var, state="readonly")
        employee_combobox.grid(row=3, column=1, padx=5, pady=5)
        employee_combobox['values'] = self.get_employees()

        # Quantity entry
        Label(form_frame, text="Quantity:", bg="#ffffff").grid(row=4, column=0, padx=5, pady=5, sticky=W)
        quantity_var = IntVar()
        quantity_entry = Entry(form_frame, textvariable=quantity_var, font="Roboto 12", width=10)
        quantity_entry.grid(row=4, column=1, padx=5, pady=5)

        # Add to Transfer List Button
        add_button = Button(form_frame, text="Add to Transfer List",
                            command=lambda: self.add_transfer_product(
                                product_combobox, from_warehouse_combobox, to_warehouse_combobox, quantity_entry),
                            bg="#4CAF50", fg="white")
        add_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Transfer products listbox
        transfer_listbox = Listbox(right_frame, height=10, width=50)
        transfer_listbox.pack(pady=10)

        # Allow deletion of selected items using Backspace key
        transfer_listbox.bind("<BackSpace>", lambda event: self.delete_selected_item(transfer_listbox))

        # Confirm button to update the database with transfer products
        confirm_button = Button(form_frame, text="Confirm Transfer",
                                command=lambda: self.confirm_transfer(transfer_listbox, stock_treeview, employee_var),
                                bg="#FF5722", fg="white")
        confirm_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.transfer_listbox = transfer_listbox

    def delete_selected_item(self, transfer_listbox):
        try:
            selected_index = transfer_listbox.curselection()
            if selected_index:
                transfer_listbox.delete(selected_index)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while deleting the item: {e}")

    def add_transfer_product(self, product_combobox, from_warehouse_combobox, to_warehouse_combobox, quantity_entry):
        try:
            # Lấy thông tin từ các combobox và entry
            product_name = product_combobox.get()
            from_warehouse_name = from_warehouse_combobox.get()
            to_warehouse_name = to_warehouse_combobox.get()
            quantity = quantity_entry.get()

            # Kiểm tra các trường có dữ liệu hay không
            if not product_name or not from_warehouse_name or not to_warehouse_name or not quantity:
                messagebox.showerror("Error", "Please fill in all fields")
                return

            # Kiểm tra nếu số lượng nhập vào là hợp lệ (phải là số nguyên)
            try:
                quantity = int(quantity)
            except ValueError:
                messagebox.showerror("Error", "Quantity must be a valid integer")
                return

            # Thêm sản phẩm vào danh sách chuyển kho (listbox)
            self.transfer_listbox.insert(
                END, f"{product_name} (From: {from_warehouse_name} To: {to_warehouse_name}) - {quantity} units"
            )

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while adding transfer product: {e}")

    def confirm_transfer(self, transfer_listbox, stock_treeview, employee_var):
        """Xác nhận chuyển kho và ghi nhận đầy đủ vào các bảng inventory_balance, inventory_transaction, inventory_transaction_detail"""
        try:
            # Lấy danh sách sản phẩm từ transfer_listbox
            transfer_products = transfer_listbox.get(0, END)
            if not transfer_products:
                messagebox.showerror("Error", "No products selected for transfer")
                return

            # Lấy Employee_ID từ employee_var (format: "EMP001 - Name")
            employee_id_full = employee_var.get()
            if not employee_id_full:
                messagebox.showerror("Error", "Please select an employee")
                return

            employee_id = employee_id_full.split(" - ")[0]
            transaction_id = f"TR{int(datetime.now().timestamp())}"

            # Duyệt qua từng sản phẩm trong danh sách
            for index, product_entry in enumerate(transfer_products, start=1):
                product_name, details = product_entry.split(" (From: ")
                from_warehouse, rest_details = details.split(" To: ")
                to_warehouse, quantity_details = rest_details.split(") - ")
                quantity = int(quantity_details.split(" units")[0])

                # Truy vấn Product_ID và Warehouse_ID
                self.cur.execute("SELECT Product_ID FROM inventory WHERE Product_Name = ?", (product_name,))
                product_id = self.cur.fetchone()[0]

                self.cur.execute("SELECT Warehouse_ID FROM warehouses WHERE Name = ?", (from_warehouse,))
                from_warehouse_id = self.cur.fetchone()[0]

                self.cur.execute("SELECT Warehouse_ID FROM warehouses WHERE Name = ?", (to_warehouse,))
                to_warehouse_id = self.cur.fetchone()[0]

                # Tính toán unit_price bằng bình quân gia quyền
                self.cur.execute("""
                    SELECT SUM(initial_stock + quantity_imported - export_quantity) AS Total_Quantity,
                           SUM(Total_Price + Total_Price_Import - Total_Price_Export) AS Total_Value
                    FROM inventory_balance WHERE Product_ID = ? AND Warehouse_ID = ?
                """, (product_id, from_warehouse_id))
                total_quantity, total_value = self.cur.fetchone()
                unit_price = total_value / total_quantity if total_quantity > 0 else 0

                # Kiểm tra tồn kho có đủ không
                if quantity > total_quantity:
                    messagebox.showerror("Error", f"Not enough stock for {product_name} in {from_warehouse}")
                    return

                # Thêm giao dịch vào bảng `inventory_transaction`
                self.cur.execute("""
                    INSERT INTO inventory_transaction (Transaction_ID, Transaction_Type, Warehouse_ID, To_Warehouse_ID, Employee_ID, Transaction_Date)
                    VALUES (?, 'Chuyển kho', ?, ?, ?, ?)
                """, (transaction_id, from_warehouse_id, to_warehouse_id, employee_id, datetime.now().date()))

                # Thêm chi tiết giao dịch vào `inventory_transaction_detail`
                detail_id = f"DT{int(datetime.now().timestamp())}{index}"
                total_price = unit_price * quantity
                self.cur.execute("""
                    INSERT INTO inventory_transaction_detail 
                    (Detail_ID, Transaction_ID, Product_ID, Product_Name, Unit_Type, Quantity, Unit_Price, Total_Price)
                    VALUES (?, ?, ?, ?, 'Thùng', ?, ?, ?)
                """, (detail_id, transaction_id, product_id, product_name, quantity, unit_price, total_price))

                # === Cập nhật bảng `inventory_balance` ===
                # 1. Giảm tồn kho tại kho nguồn
                from_balance_id = f"IB{transaction_id}_FROM_{index}"
                self.cur.execute("""
                    INSERT INTO inventory_balance 
                    (Inventory_Balance_ID, Warehouse_ID, Product_ID, Date, Product_Name, Unit_Type, initial_stock, 
                    quantity_imported, export_quantity, Unit_Price_Export, Total_Price_Export)
                    VALUES (?, ?, ?, ?, ?, 'Thùng', 0, 0, ?, ?, ?)
                """, (from_balance_id, from_warehouse_id, product_id, datetime.now().date(), product_name, quantity,
                      unit_price, total_price))

                # 2. Tăng tồn kho tại kho đích
                to_balance_id = f"IB{transaction_id}_TO_{index}"
                self.cur.execute("""
                    INSERT INTO inventory_balance 
                    (Inventory_Balance_ID, Warehouse_ID, Product_ID, Date, Product_Name, Unit_Type, initial_stock, 
                    quantity_imported, export_quantity, Unit_Price_Import, Total_Price_Import)
                    VALUES (?, ?, ?, ?, ?, 'unit', 0, ?, 0, ?, ?)
                """, (
                to_balance_id, to_warehouse_id, product_id, datetime.now().date(), product_name, quantity, unit_price,
                total_price))

            # Xác nhận lưu dữ liệu vào database
            self.conn.commit()
            self.update_stock_information(stock_treeview)
            messagebox.showinfo("Success", "Transfer process completed successfully!")

        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", f"An error occurred during transfer: {e}")

    def perform_transfer(self, product_name, from_warehouse_name, to_warehouse_name, quantity, transaction_id,
                         employee_id, unit_price):
        try:
            cursor = self.conn.cursor()

            # Lấy Product_ID từ inventory
            cursor.execute("SELECT Product_ID FROM inventory WHERE Product_Name = ?", (product_name,))
            product = cursor.fetchone()
            if not product:
                raise ValueError(f"Product '{product_name}' not found in the inventory.")
            product_id = product[0]

            # Lấy Warehouse_ID của kho nguồn và kho đích
            cursor.execute("SELECT Warehouse_ID FROM warehouses WHERE Name = ?", (from_warehouse_name,))
            from_warehouse = cursor.fetchone()
            if not from_warehouse:
                raise ValueError(f"Source warehouse '{from_warehouse_name}' not found.")
            from_warehouse_id = from_warehouse[0]

            cursor.execute("SELECT Warehouse_ID FROM warehouses WHERE Name = ?", (to_warehouse_name,))
            to_warehouse = cursor.fetchone()
            if not to_warehouse:
                raise ValueError(f"Target warehouse '{to_warehouse_name}' not found.")
            to_warehouse_id = to_warehouse[0]

            # Kiểm tra tồn kho trong kho nguồn
            cursor.execute("""
                SELECT SUM(initial_stock + quantity_imported - export_quantity)
                FROM inventory_balance
                WHERE Warehouse_ID = ? AND Product_ID = ?
            """, (from_warehouse_id, product_id))
            available_stock = cursor.fetchone()[0]
            if available_stock < quantity:
                raise ValueError(f"Not enough stock in {from_warehouse_name} for {product_name}")

            # Ghi giao dịch vào bảng inventory_transaction
            transaction_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("""
                INSERT INTO inventory_transaction (Transaction_ID, Transaction_Type, Warehouse_ID, To_Warehouse_ID, Employee_ID, Transaction_Date)
                VALUES (?, 'Chuyển kho', ?, ?, ?, ?)
            """, (transaction_id, from_warehouse_id, to_warehouse_id, employee_id, transaction_date))

            # Ghi chi tiết giao dịch vào bảng inventory_transaction_detail
            detail_id = f"{transaction_id}_DETAIL"
            cursor.execute("""
                INSERT INTO inventory_transaction_detail (Detail_ID, Transaction_ID, Product_ID, Product_Name, Unit_Type, Quantity, Unit_Price, Total_Price)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                detail_id, transaction_id, product_id, product_name, 'Unit', quantity, unit_price,
                quantity * unit_price))

            # Tạo Inventory_Balance_ID cho kho nguồn và cập nhật tồn kho
            from_balance_id = f"{transaction_id}_FROM"
            cursor.execute("""
                UPDATE inventory_balance
                SET export_quantity = export_quantity + ?
                WHERE Warehouse_ID = ? AND Product_ID = ?
            """, (quantity, from_warehouse_id, product_id))
            if cursor.rowcount == 0:  # Nếu không có bản ghi tồn tại, thêm mới
                cursor.execute("""
                    INSERT INTO inventory_balance (Inventory_Balance_ID, Warehouse_ID, Product_ID, Date, Product_Name, Unit_Type, initial_stock, quantity_imported, export_quantity, Unit_Price_Export, Total_Price_Export)
                    VALUES (?, ?, ?, ?, ?, 'Unit', 0, 0, ?, ?, ?)
                """, (
                    from_balance_id, from_warehouse_id, product_id, transaction_date, product_name, quantity,
                    unit_price,
                    quantity * unit_price))

            # Tạo Inventory_Balance_ID cho kho đích và cập nhật tồn kho
            to_balance_id = f"{transaction_id}_TO"
            cursor.execute("""
                SELECT COUNT(*)
                FROM inventory_balance
                WHERE Warehouse_ID = ? AND Product_ID = ?
            """, (to_warehouse_id, product_id))
            count = cursor.fetchone()[0]

            if count == 0:
                cursor.execute("""
                    INSERT INTO inventory_balance (Inventory_Balance_ID, Warehouse_ID, Product_ID, Date, Product_Name, Unit_Type, initial_stock, quantity_imported, export_quantity, Unit_Price_Import, Total_Price_Import)
                    VALUES (?, ?, ?, ?, ?, 'Thùng', 0, ?, 0, ?, ?)
                """, (to_balance_id, to_warehouse_id, product_id, transaction_date, product_name, quantity, unit_price,
                      quantity * unit_price))
            else:
                cursor.execute("""
                    UPDATE inventory_balance
                    SET quantity_imported = quantity_imported + ?
                    WHERE Warehouse_ID = ? AND Product_ID = ?
                """, (quantity, to_warehouse_id, product_id))

            # Commit thay đổi
            self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            raise e

    #------------------------------------------------------------------------------------------------------------------
    def show_balance_calculation(self):
        # Tạo cửa sổ mới cho giao diện tính toán số dư
        self.balance_window = Toplevel(self.mainw)
        self.balance_window.title("Calculate Inventory Balance")

        Label(self.balance_window, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=10)
        self.start_date_entry = Entry(self.balance_window)
        self.start_date_entry.grid(row=0, column=1, padx=10, pady=10)

        Label(self.balance_window, text="End Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=10)
        self.end_date_entry = Entry(self.balance_window)
        self.end_date_entry.grid(row=1, column=1, padx=10, pady=10)

        Label(self.balance_window, text="Warehouse ID (optional):").grid(row=2, column=0, padx=10, pady=10)
        self.warehouse_id_entry = Entry(self.balance_window)
        self.warehouse_id_entry.grid(row=2, column=1, padx=10, pady=10)

        calculate_button = Button(self.balance_window, text="Calculate Balance",
                                  command=self.calculate_and_display_balance)
        calculate_button.grid(row=3, column=0, columnspan=2, pady=20)

    def calculate_and_display_balance(self):
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        warehouse_id = self.warehouse_id_entry.get() or None

        try:
            start_date = date.fromisoformat(start_date)
            end_date = date.fromisoformat(end_date)
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

        balance_data = self.calculate_balance(start_date, end_date, warehouse_id)

        # Hiển thị kết quả trong cửa sổ
        row = 5
        for product_id, data in balance_data.items():
            Label(self.balance_window, text=f"Product ID: {product_id}").grid(row=row, column=0, padx=10, pady=5,
                                                                              sticky="w")
            Label(self.balance_window, text=f"Beginning Balance Quantity: {data['beginning_balance_quantity']}").grid(
                row=row, column=1, padx=10, pady=5, sticky="w")
            Label(self.balance_window, text=f"Beginning Balance Value: {data['beginning_balance_value']}").grid(row=row,
                                                                                                                column=2,
                                                                                                                padx=10,
                                                                                                                pady=5,
                                                                                                                sticky="w")
            Label(self.balance_window, text=f"Ending Balance Quantity: {data['ending_balance_quantity']}").grid(
                row=row + 1, column=1, padx=10, pady=5, sticky="w")
            Label(self.balance_window, text=f"Ending Balance Value: {data['ending_balance_value']}").grid(row=row + 1,
                                                                                                          column=2,
                                                                                                          padx=10,
                                                                                                          pady=5,
                                                                                                          sticky="w")
            row += 2

    def admin_mainmenu(self, a, b):
        """Main menu for admin."""
        # Tạo frame chính chứa các nút menu
        self.mainframe = LabelFrame(self.mainw, width=1200, height=145, bg="#f7f7f7")
        self.mainframe.place(x=100, y=100)

        start_x = 50
        button_spacing = 160

        # Nút Inbound
        inbound_img = PhotoImage(file="images/inbound.png").subsample(a, b)
        self.inbound = Button(
            self.mainframe, text="Inbound", bd=5, font="roboto 11 bold", image=inbound_img,
            compound=TOP, command=self.inbound_stock_window
        )
        self.inbound.image = inbound_img
        self.inbound.place(x=start_x, y=20)

        # Nút Outbound
        outbound_img = PhotoImage(file="images/outbound.png").subsample(a, b)
        self.outbound = Button(
            self.mainframe, text="Outbound", bd=5, font="roboto 11 bold", image=outbound_img,
            compound=TOP, command=self.outbound_stock  # Cập nhật ở đây
        )
        self.outbound.image = outbound_img
        self.outbound.place(x=start_x + button_spacing, y=20)

        # Nút Transfer
        transfer_img = PhotoImage(file="images/transfer.png").subsample(a, b)
        self.transfer = Button(
            self.mainframe, text="Transfer", bd=5, font="roboto 11 bold", image=transfer_img,
            compound=TOP, command=self.transfer_stock
        )
        self.transfer.image = transfer_img
        self.transfer.place(x=start_x + button_spacing * 2, y=20)

        # Nút Inventory
        inventory_img = PhotoImage(file="images/inventory.png").subsample(a, b)
        self.inventory = Button(
            self.mainframe, text="Inventory", bd=5, font="roboto 11 bold", image=inventory_img,
            compound=TOP, command=self.buildprodtable
        )
        self.inventory.image = inventory_img
        self.inventory.place(x=start_x + button_spacing * 3, y=20)

        # Nút Dashboard
        dashboard_img = PhotoImage(file="images/dashboard.png").subsample(a, b)
        self.dashboard_button = Button(
            self.mainframe, text="Dashboard", font="roboto 11 bold", bd=5,
            image=dashboard_img, compound=TOP, command=self.show_dashboard
        )
        self.dashboard_button.image = dashboard_img
        self.dashboard_button.place(x=start_x + button_spacing * 4, y=20)

        # Nút Sign Out
        signout_img = PhotoImage(file="images/change1.png").subsample(a, b)
        self.changeuser = Button(
            self.mainframe, text="Sign out", bd=5, font="roboto 11 bold", image=signout_img,
            compound=TOP, command=self.__Main_del__
        )
        self.changeuser.image = signout_img
        self.changeuser.place(x=start_x + button_spacing * 5, y=20)

        # Nút Quit
        quit_img = PhotoImage(file="images/Door_Out-512.png").subsample(a, b)
        self.logout = Button(
            self.mainframe, text="Quit", bd=5, font="roboto 11 bold", image=quit_img,
            compound=TOP, command=self.__Main_del__
        )
        self.logout.image = quit_img
        self.logout.place(x=start_x + button_spacing * 6, y=20)

        # Thiết lập giao diện phụ
        self.formframe = Frame(self.mainw, width=500, height=550, bg="#FFFFFF")
        self.formframe.place(x=100, y=315)
        self.formframeinfo = self.formframe.place_info()

        self.tableframe1 = LabelFrame(self.mainw, width=350, height=700)
        self.tableframe1.place(x=1200, y=315, anchor=NE)
        self.tableframe1info = self.tableframe1.place_info()

        self.tableframe = LabelFrame(self.mainw, width=350, height=700)
        self.tableframe.place(x=1300, y=315, anchor=NE)
        self.tableframeinfo = self.tableframe.place_info()

        self.itemframe = Frame(self.mainw, bg="#FFFFFF", width=600, height=300)
        self.itemframe.place(x=420, y=280, anchor=NW)
        self.itemframeinfo = self.itemframe.place_info()

        self.formframe1 = Frame(self.mainw, width=500, height=445, bg="#FFFFFF")
        self.formframe1.place(x=100, y=275)
        self.formframe1info = self.formframe1.place_info()

        self.searchframe = Frame(self.mainw, width=720, height=70, bg="#FFFFFF")
        self.searchframe.place(x=575, y=260)
        self.searchframeinfo = self.searchframe.place_info()

        # Nút Search
        self.searchbut = Button(
            self.searchframe, text="Search Description", font="roboto 14", bg="#FFFFFF", bd=5,
            command=self.searchprod
        )
        self.searchbut.place(x=0, y=20, height=40)

        # Thanh nhập cho tìm kiếm
        self.searchvar = StringVar()
        self.searchentry = Entry(
            self.searchframe, textvariable=self.searchvar, font="roboto 14", width=25, bg="#FFFFFF"
        )
        self.searchentry.place(x=210, y=20, height=40)

        # Nút Reset
        self.resetbut = Button(
            self.searchframe, text="Reset", font="roboto 14", bd=5, width=8, bg="#FFFFFF",
            command=self.resetprodtabel
        )
        self.resetbut.place(x=510, y=18, height=40)

        # Cài đặt ban đầu
        self.cond = 0
        self.buildprodtable()

#---------------BUILD PRODUCT TABLE AT INVENTORY---------------------------------------------
    def buildprodtable(self):
        self.searchframe.place_forget()
        self.tableframe.place(self.tableframeinfo)
        self.formframe.place(self.formframeinfo)
        self.tableframe1.place_forget()
        self.formframe1.place_forget()
        self.itemframe.place_forget()

        if hasattr(self, 'tree') and self.tree:
            self.tree.delete(*self.tree.get_children())
            self.tree.grid_remove()
            self.tree.destroy()

        # Tạo mới 'tree' cho bảng giao dịch tồn kho
        scrollbarx = Scrollbar(self.tableframe, orient=HORIZONTAL)
        scrollbary = Scrollbar(self.tableframe, orient=VERTICAL)
        self.tree = ttk.Treeview(
            self.tableframe,
            columns=("Transaction_ID", "Transaction_Type", "Warehouse_ID",
                     "To_Warehouse_ID", "Employee_ID", "Transaction_Date"),
            selectmode="browse",
            height=18,
            yscrollcommand=scrollbary.set,
            xscrollcommand=scrollbarx.set
        )

        # Cấu hình các cột và tiêu đề của 'tree'
        self.tree.heading('Transaction_ID', text="Transaction ID", anchor=W)
        self.tree.heading('Transaction_Type', text="Transaction Type", anchor=W)
        self.tree.heading('Warehouse_ID', text="Warehouse ID", anchor=W)
        self.tree.heading('To_Warehouse_ID', text="To Warehouse ID", anchor=W)
        self.tree.heading('Employee_ID', text="Employee ID", anchor=W)
        self.tree.heading('Transaction_Date', text="Transaction Date", anchor=W)

        # Định cấu hình chiều rộng cho các cột
        self.tree.column('Transaction_ID', width=120)
        self.tree.column('Transaction_Type', width=150)
        self.tree.column('Warehouse_ID', width=120)
        self.tree.column('To_Warehouse_ID', width=120)
        self.tree.column('Employee_ID', width=120)
        self.tree.column('Transaction_Date', width=180)

        # Thiết lập giao diện cho Treeview
        style = ttk.Style()
        style.configure("Treeview",
                        font=("Arial", 10),
                        rowheight=30,
                        background="#f7f9fc",
                        foreground="black",
                        fieldbackground="#f7f9fc")

        # Thiết lập màu sắc cho tiêu đề cột (background xanh, chữ trắng)
        style.configure("Treeview.Heading",
                        font=("Arial", 10, "bold"),
                        background="#1f77b4",  # Nền màu xanh đậm
                        foreground="black",
                        relief="solid")

        style.map("Treeview",
                  background=[('selected', '#2ca02c')],
                  foreground=[('selected', 'white')])

        self.tree.grid(row=1, column=0, sticky="W")
        scrollbary.config(command=self.tree.yview)
        scrollbarx.config(command=self.tree.xview)
        scrollbary.grid(row=1, column=1, sticky="ns", pady=30)
        scrollbarx.grid(row=2, column=0, sticky="we")

        # Khu vực bộ lọc bên phải
        filter_frame = Frame(self.tableframe, bg="#e3f2fd", relief=RIDGE, bd=2)
        filter_frame.grid(row=1, column=2, padx=20, pady=10, sticky="N")

        Label(filter_frame, text="Filter Options", font=("Arial", 12, "bold"), bg="#e3f2fd", fg="#0d47a1").pack(pady=10)

        # Bộ lọc Transaction Type
        Label(filter_frame, text="Transaction Type", font=("Arial", 10), bg="#e3f2fd", fg="#0d47a1").pack(anchor="w")
        self.transaction_type_var = StringVar()
        transaction_type_dropdown = ttk.Combobox(filter_frame, textvariable=self.transaction_type_var)
        transaction_type_dropdown['values'] = ["All", "Nhập kho", "Xuất kho", "Chuyển kho"]
        transaction_type_dropdown.current(0)
        transaction_type_dropdown.pack(fill="x", pady=5)

        # Bộ lọc Warehouse ID
        Label(filter_frame, text="Warehouse ID", font=("Arial", 10), bg="#e3f2fd", fg="#0d47a1").pack(anchor="w")
        self.warehouse_id_var = StringVar()
        warehouse_dropdown = ttk.Combobox(filter_frame, textvariable=self.warehouse_id_var)
        warehouse_dropdown['values'] = ["All"] + self.get_unique_warehouse_ids()
        warehouse_dropdown.current(0)
        warehouse_dropdown.pack(fill="x", pady=5)

        # Bộ lọc Employee ID
        Label(filter_frame, text="Employee ID", font=("Arial", 10), bg="#e3f2fd", fg="#0d47a1").pack(anchor="w")
        self.employee_id_var = StringVar()
        employee_dropdown = ttk.Combobox(filter_frame, textvariable=self.employee_id_var)
        employee_dropdown['values'] = ["All"] + self.get_unique_employee_ids()
        employee_dropdown.current(0)
        employee_dropdown.pack(fill="x", pady=5)

        # Nút áp dụng bộ lọc
        Button(filter_frame, text="Apply Filter", command=self.apply_filters, bg="#64b5f6", fg="white",
               font=("Arial", 10, "bold"), relief=RAISED).pack(pady=10)

        # Lấy dữ liệu giao dịch từ database và chèn vào 'tree'
        self.gettransactions()

    def get_unique_warehouse_ids(self):
        self.cur.execute("SELECT DISTINCT Warehouse_ID FROM inventory_transaction")
        return [row[0] for row in self.cur.fetchall()]

    def get_unique_employee_ids(self):
        self.cur.execute("SELECT DISTINCT Employee_ID FROM inventory_transaction")
        return [row[0] for row in self.cur.fetchall()]

    def apply_filters(self):
        transaction_type = self.transaction_type_var.get()
        warehouse_id = self.warehouse_id_var.get()
        employee_id = self.employee_id_var.get()

        query = """
            SELECT Transaction_ID, Transaction_Type, Warehouse_ID, To_Warehouse_ID, Employee_ID, Transaction_Date
            FROM inventory_transaction
            WHERE 1=1
        """

        params = []

        if transaction_type != "All":
            query += " AND Transaction_Type = ?"
            params.append(transaction_type)

        if warehouse_id != "All":
            query += " AND Warehouse_ID = ?"
            params.append(warehouse_id)

        if employee_id != "All":
            query += " AND Employee_ID = ?"
            params.append(employee_id)

        self.cur.execute(query, params)
        transactionlist = self.cur.fetchall()

        # Xóa dữ liệu cũ trong `Treeview`
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Chèn dữ liệu mới vào `Treeview`
        for index, transaction in enumerate(transactionlist):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.tree.insert('', 'end', values=transaction, tags=(tag,))

        self.tree.tag_configure("evenrow", background="#eaf2f8")
        self.tree.tag_configure("oddrow", background="#ffffff")

    def gettransactions(self):
        # Truy vấn SQL để lấy dữ liệu từ bảng `inventory_transaction`
        self.cur.execute("""
            SELECT 
                Transaction_ID, 
                Transaction_Type, 
                Warehouse_ID, 
                To_Warehouse_ID, 
                Employee_ID, 
                Transaction_Date 
            FROM 
                inventory_transaction
        """)

        # Lấy tất cả các dòng dữ liệu từ truy vấn
        transactionlist = self.cur.fetchall()

        # Sắp xếp danh sách giao dịch theo ngày từ mới nhất đến cũ nhất
        transactionlist.sort(key=lambda x: datetime.strptime(x[5].split()[0], '%Y-%m-%d'), reverse=True)

        # Xóa dữ liệu cũ trong `Treeview` nếu có
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Chèn từng giao dịch vào `Treeview` theo đúng thứ tự cột
        for index, transaction in enumerate(transactionlist):
            # Đổi màu nền cho dòng lẻ và dòng chẵn
            if index % 2 == 0:
                self.tree.insert('', 'end', values=(
                    transaction[0],  # Transaction ID
                    transaction[1],  # Transaction Type
                    transaction[2],  # Warehouse ID
                    transaction[3],  # To Warehouse ID
                    transaction[4],  # Employee ID
                    transaction[5]  # Transaction Date
                ), tags=("evenrow",))
            else:
                self.tree.insert('', 'end', values=(
                    transaction[0],  # Transaction ID
                    transaction[1],  # Transaction Type
                    transaction[2],  # Warehouse ID
                    transaction[3],  # To Warehouse ID
                    transaction[4],  # Employee ID
                    transaction[5]  # Transaction Date
                ), tags=("oddrow",))

        # Định nghĩa các style cho các dòng
        self.tree.tag_configure("evenrow", background="#eaf2f8")
        self.tree.tag_configure("oddrow", background="#ffffff")

    def changeprodtable(self):
        # Code for updating products modified for the inventory table
        cur = self.tree.selection()
        cur = self.tree.item(cur)
        li = cur['values']
        if len(li) == 6:
            if self.itemeditv.get() == '' or self.itemeditdescv.get() == '':
                messagebox.showerror("Error", "Please Fill All Fields")
                return
            elif self.itemeditcatv.get() == '' or self.itemeditstockv.get() == '' or self.itemeditpricev.get() == '':
                messagebox.showerror("Error", "Please Fill All Fields")
                return
            else:
                l = [self.itemeditpricev.get(), self.itemeditstockv.get()]
                for i in range(0, len(l)):
                    if not l[i].isdigit():
                        messagebox.showerror("Error", "Invalid Data Provided")
                        return
                    elif int(l[i]) < 0:
                        messagebox.showerror("Error", "Invalid Data Provided")
                        return
            if self.addstock.get() == '':
                self.addstock.set('0')

            self.cur.execute("""
                UPDATE inventory SET Product_Name=?, CategoryID=?, UnitType=?, SupplierID=? WHERE Product_ID=?
            """, (
            self.itemeditv.get(), self.itemeditdescv.get(), self.itemeditcatv.get(), int(self.itemeditpricev.get()),
            li[0]))
            self.base.commit()
            self.addstock.set('')
            self.tree.delete(*self.tree.get_children())
            cur = self.getproducts(li[0])
            self.tree.selection_set(cur)

    def delproduct(self):
        # Code for deleting from the inventory table
        cur = self.tree.focus()
        cur = self.tree.item(cur)
        li = cur['values']
        if messagebox.askyesno('Alert!', 'Do you want to remove product from inventory?') == True and len(li) == 6:
            self.cur.execute("DELETE FROM inventory WHERE Product_ID = ?", (li[0],))
            self.base.commit()
            self.tree.delete(*self.tree.get_children())
            self.getproducts()
            self.itemeditv.set('')
            self.itemeditdescv.set('')
            self.itemeditcatv.set('')
            self.itemeditstockv.set('')
            self.itemeditpricev.set('')

    def searchprod(self):
        if self.searchvar.get() == '':
            return
        self.tree.delete(*self.tree.get_children())
        self.cur.execute("SELECT Product_ID, Product_Name, CategoryID, UnitType, SupplierID FROM inventory")
        li = self.cur.fetchall()
        for i in li:
            if i[1] == self.searchvar.get():  # assuming search by Product_Name
                self.tree.insert('', 'end', values=(i))

    def resetprodtabel(self):
        self.searchvar.set('')
        self.tree.delete(*self.tree.get_children())
        self.getproducts()

    #BUILD USER TABLE
    def buildusertable(self):
         self.searchframe.place_forget()
         self.formframe.place_forget()
         self.tableframe.place_forget()
         self.itemframe.place_forget()
         self.formframe1.place(self.formframe1info)
         self.tableframe1.place(self.tableframe1info)
         self.tree.delete(*self.tree.get_children())
         self.tree.grid_remove()
         self.tree.destroy()
         scrollbarx = Scrollbar(self.tableframe1, orient=HORIZONTAL)
         scrollbary = Scrollbar(self.tableframe1, orient=VERTICAL)
         self.tree = ttk.Treeview(self.tableframe1, columns=("Username", "Password", "Account Type"),
         selectmode="browse", height=17,yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
         self.tree.column('#0', stretch=NO, minwidth=0, width=0)
         self.tree.column('#1', stretch=NO, minwidth=0, width=170)
         self.tree.column('#2', stretch=NO, minwidth=0, width=170)
         self.tree.column('#3', stretch=NO, minwidth=0, width=170)
         self.tree.heading('Username', text="Username", anchor=W)
         self.tree.heading('Password', text="Password", anchor=W)
         self.tree.heading('Account Type', text="Account Type", anchor=W)
         self.tree.grid(row=1, column=0, sticky="W")
         scrollbary.config(command=self.tree.yview)
         scrollbarx.grid(row=2, column=0, sticky="we")
         scrollbarx.config(command=self.tree.xview)
         scrollbary.grid(row=1, column=1, sticky="ns", pady=30)
         self.getusers()
         self.tree.bind("<<TreeviewSelect>>", self.clickusertable)
         self.formframe1.focus_set()
         self.usernamedit = StringVar()
         self.passwordedit = StringVar()
         self.accedit = StringVar()
         va = 110
         l1 = ['Username', 'Password','Profile Type']
         for i in range(0,3):
             Label(self.formframe1, text=l1[i], font="roboto 14 bold", bg="#FFFFFF").place(x=0, y=va)
             va += 70
         Entry(self.formframe1, textvariable=self.usernamedit, font="roboto 14", bg="#FFFFFF", width=25,state='readonly').place(x=162, y=105, height=40)
         Entry(self.formframe1, textvariable=self.passwordedit, font="roboto 14", bg="#FFFFFF", width=25).place(x=162, y=175, height=40)
         profiles=mycombobox(self.formframe1, font="robot 14", width=23, textvariable=self.accedit)
         profiles.place(x=162,y=245,height=40)
         profiles.set_completion_list(['ADMIN','USER'])
         Button(self.formframe1, text="Create a User", font="robot 12 bold", bg="#FFFFFF", bd=5, width=12, height=2,
                command=self.adduser).place(x=0, y=10)
         Button(self.formframe1, text="Update", font="robot 12 bold", bg="#FFFFFF", bd=5, width=10, height=2,
                command=self.changeusertable).place(x=145, y=381)
         Button(self.formframe1, text="Remove", font="robot 12 bold", bg="#FFFFFF", bd=5, width=10, height=2,
                command=self.deluser).place(x=345, y=381)

         self.mainsearch(0)

    # BUILD SALES TABLE
    def buildsalestable(self):
        # Xóa bỏ các khung UI không cần thiết trước khi hiển thị bảng sales
        self.searchframe.place_forget()
        self.formframe.place_forget()
        self.tableframe.place_forget()
        self.itemframe.place_forget()
        self.formframe1.place_forget()
        self.tableframe1.place(x=1280, y=315, anchor=NE)

        # Tạo các thanh cuộn
        scrollbarx = Scrollbar(self.tableframe1, orient=HORIZONTAL)
        scrollbary = Scrollbar(self.tableframe1, orient=VERTICAL)

        # Định nghĩa cấu trúc bảng Treeview
        self.tree = ttk.Treeview(
            self.tableframe1,
            columns=(
            "Transaction_ID", "Invoice_No", "Product_ID", "Description", "Quantity", "Total_Price", "Date", "Time"),
            selectmode="browse",
            height=16,
            yscrollcommand=scrollbary.set,
            xscrollcommand=scrollbarx.set
        )

        # Định cấu hình cột
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('Transaction_ID', stretch=NO, minwidth=0, width=140)
        self.tree.column('Invoice_No', stretch=NO, minwidth=0, width=140)
        self.tree.column('Product_ID', stretch=NO, minwidth=0, width=150)
        self.tree.column('Description', stretch=NO, minwidth=0, width=170)
        self.tree.column('Quantity', stretch=NO, minwidth=0, width=130)
        self.tree.column('Total_Price', stretch=NO, minwidth=0, width=130)
        self.tree.column('Date', stretch=NO, minwidth=0, width=130)
        self.tree.column('Time', stretch=NO, minwidth=0, width=130)

        # Đặt tiêu đề cho các cột
        self.tree.heading('Transaction_ID', text="Transaction ID", anchor=W)
        self.tree.heading('Invoice_No', text="Invoice No", anchor=W)
        self.tree.heading('Product_ID', text="Product ID", anchor=W)
        self.tree.heading('Description', text="Description", anchor=W)
        self.tree.heading('Quantity', text="Quantity", anchor=W)
        self.tree.heading('Total_Price', text="Total Price", anchor=W)
        self.tree.heading('Date', text="Date", anchor=W)
        self.tree.heading('Time', text="Time", anchor=W)

        # Đặt Treeview vào bảng và cấu hình thanh cuộn
        self.tree.grid(row=1, column=0, sticky="W")
        scrollbarx.grid(row=2, column=0, sticky="we")
        scrollbary.grid(row=1, column=1, sticky="ns", pady=30)
        scrollbarx.config(command=self.tree.xview)
        scrollbary.config(command=self.tree.yview)

        # Gọi hàm lấy dữ liệu để hiển thị trong bảng Treeview
        self.getsales()

        # Gán tổng doanh thu (nếu có)
        self.totalsales = Label(self.tableframe1, text="Total Sales", font="roboto 14 bold").place(x=0, y=400)
