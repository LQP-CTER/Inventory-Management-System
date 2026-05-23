import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import calendar
from sqlalchemy import func
from inventory_management import InventoryBalance, Warehouse, Inventory

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.session = controller.session

        # Header
        self.header_label = ctk.CTkLabel(self, text="Dashboard Overview", font=("Inter", 24, "bold"))
        self.header_label.pack(pady=(10, 20), anchor="w")

        # Filters
        self.filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.filter_frame.pack(fill="x", pady=10)

        now = datetime.now()
        self.month_var = ctk.StringVar(value=str(now.month))
        self.year_var = ctk.StringVar(value=str(now.year))

        ctk.CTkLabel(self.filter_frame, text="Month:", font=("Inter", 14)).pack(side="left", padx=5)
        self.month_cb = ctk.CTkComboBox(self.filter_frame, values=[str(i) for i in range(1, 13)], 
                                        variable=self.month_var, width=80)
        self.month_cb.pack(side="left", padx=5)

        ctk.CTkLabel(self.filter_frame, text="Year:", font=("Inter", 14)).pack(side="left", padx=5)
        self.year_cb = ctk.CTkComboBox(self.filter_frame, values=[str(i) for i in range(now.year-5, now.year+1)], 
                                       variable=self.year_var, width=100)
        self.year_cb.pack(side="left", padx=5)

        self.btn_refresh = ctk.CTkButton(self.filter_frame, text="Refresh", command=self.load_data)
        self.btn_refresh.pack(side="left", padx=20)

        # Content Area (Scrollable)
        self.scrollable = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scrollable.pack(fill="both", expand=True)

        self.load_data()

    def load_data(self):
        # Clear old widgets in scrollable
        for w in self.scrollable.winfo_children():
            w.destroy()
            
        month = int(self.month_var.get())
        year = int(self.year_var.get())
        
        start_date = datetime(year, month, 1).date()
        end_date = datetime(year, month, calendar.monthrange(year, month)[1]).date()

        # Query data
        total_stock = self.session.query(func.sum(InventoryBalance.initial_stock)).scalar() or 0
        total_import = self.session.query(func.sum(InventoryBalance.quantity_imported)).filter(
            InventoryBalance.Date.between(start_date, end_date)
        ).scalar() or 0
        total_export = self.session.query(func.sum(InventoryBalance.export_quantity)).filter(
            InventoryBalance.Date.between(start_date, end_date)
        ).scalar() or 0

        # Create Cards
        cards_frame = ctk.CTkFrame(self.scrollable, fg_color="transparent")
        cards_frame.pack(fill="x", pady=10)
        
        self.create_stat_card(cards_frame, "Total Stock", total_stock, "#3b82f6").pack(side="left", fill="x", expand=True, padx=10)
        self.create_stat_card(cards_frame, "Total Inbound", total_import, "#10b981").pack(side="left", fill="x", expand=True, padx=10)
        self.create_stat_card(cards_frame, "Total Outbound", total_export, "#ef4444").pack(side="left", fill="x", expand=True, padx=10)

        # Charts Area
        charts_frame = ctk.CTkFrame(self.scrollable, fg_color="transparent")
        charts_frame.pack(fill="both", expand=True, pady=20)
        
        # Bar Chart
        fig_bar = Figure(figsize=(5, 4), dpi=100)
        ax_bar = fig_bar.add_subplot(111)
        ax_bar.bar(['Stock', 'Inbound', 'Outbound'], [total_stock, total_import, total_export], color=['#3b82f6', '#10b981', '#ef4444'])
        ax_bar.set_title(f"Overview {calendar.month_name[month]} {year}")
        
        # Pie Chart
        fig_pie = Figure(figsize=(5, 4), dpi=100)
        ax_pie = fig_pie.add_subplot(111)
        ax_pie.pie([total_stock, total_import, total_export], labels=['Stock', 'Inbound', 'Outbound'], autopct='%1.1f%%', colors=['#3b82f6', '#10b981', '#ef4444'])
        ax_pie.set_title(f"Distribution")

        # Embed in Tkinter
        canvas_bar = FigureCanvasTkAgg(fig_bar, master=charts_frame)
        canvas_bar.draw()
        canvas_bar.get_tk_widget().pack(side="left", fill="both", expand=True, padx=10)

        canvas_pie = FigureCanvasTkAgg(fig_pie, master=charts_frame)
        canvas_pie.draw()
        canvas_pie.get_tk_widget().pack(side="right", fill="both", expand=True, padx=10)

    def create_stat_card(self, parent, title, value, color):
        card = ctk.CTkFrame(parent, corner_radius=15, fg_color=("#f1f5f9", "#1e293b"))
        ctk.CTkLabel(card, text=title, font=("Inter", 16), text_color="gray").pack(pady=(15, 5))
        ctk.CTkLabel(card, text=str(value), font=("Inter", 32, "bold"), text_color=color).pack(pady=(0, 15))
        return card
