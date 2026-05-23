import customtkinter as ctk
from sqlalchemy import func
import pandas as pd
from tkinter import filedialog, messagebox
from inventory_management import Warehouse, Inventory, InventoryBalance

class InventoryFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.session = controller.session

        self.header_label = ctk.CTkLabel(self, text="Inventory View", font=("Inter", 24, "bold"))
        self.header_label.pack(pady=(10, 20), anchor="w")

        # Top Bar for Buttons
        self.top_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.top_bar.pack(fill="x", padx=10, pady=5)
        
        self.btn_export = ctk.CTkButton(self.top_bar, text="Export to Excel", command=self.export_excel, width=120, fg_color="#10b981", hover_color="#059669")
        self.btn_export.pack(side="left")

        # Search Bar
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self.load_data)
        self.search_entry = ctk.CTkEntry(self.top_bar, textvariable=self.search_var, placeholder_text="Search Product or Warehouse...", width=300)
        self.search_entry.pack(side="left", padx=20)

        # Refresh Button
        self.btn_refresh = ctk.CTkButton(self.top_bar, text="Refresh Data", command=self.load_data, width=120)
        self.btn_refresh.pack(side="right")

        # Table Header
        self.table_header = ctk.CTkFrame(self, fg_color=("#e2e8f0", "#1e293b"), corner_radius=5)
        self.table_header.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(self.table_header, text="Warehouse", font=("Inter", 14, "bold")).pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(self.table_header, text="Product Name", font=("Inter", 14, "bold")).pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(self.table_header, text="Total Quantity", font=("Inter", 14, "bold")).pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(self.table_header, text="Status", font=("Inter", 14, "bold")).pack(side="left", fill="x", expand=True)

        # Scrollable Data Frame
        self.list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.load_data()

    def load_data(self, *args):
        # Clear old rows
        for w in self.list_frame.winfo_children():
            w.destroy()

        query = self.session.query(
            Warehouse.Name.label('Warehouse_Name'),
            Inventory.Product_Name,
            func.sum(InventoryBalance.initial_stock + InventoryBalance.quantity_imported - InventoryBalance.export_quantity).label('Total_Quantity')
        ).join(Warehouse, InventoryBalance.Warehouse_ID == Warehouse.Warehouse_ID)\
         .join(Inventory, InventoryBalance.Product_ID == Inventory.Product_ID)

        search_term = self.search_var.get().strip().lower()
        if search_term:
            query = query.filter(
                (func.lower(Warehouse.Name).contains(search_term)) |
                (func.lower(Inventory.Product_Name).contains(search_term))
            )

        stock_data = query.group_by(Warehouse.Name, Inventory.Product_Name).all()

        if not stock_data:
            ctk.CTkLabel(self.list_frame, text="No inventory data found.", text_color="gray").pack(pady=20)
            return

        for idx, row_data in enumerate(stock_data):
            wh_name, prod_name, total_qty = row_data
            bg_color = ("#f8fafc", "#0f172a") if idx % 2 == 0 else ("#f1f5f9", "#1e293b")
            
            row = ctk.CTkFrame(self.list_frame, fg_color=bg_color, corner_radius=5)
            row.pack(fill="x", pady=2)
            
            ctk.CTkLabel(row, text=wh_name, font=("Inter", 14)).pack(side="left", fill="x", expand=True, pady=10)
            ctk.CTkLabel(row, text=prod_name, font=("Inter", 14)).pack(side="left", fill="x", expand=True, pady=10)
            
            qty_color = "#10b981" if total_qty >= 20 else "#ef4444"
            status_text = "Good" if total_qty >= 20 else "Low Stock"
            
            ctk.CTkLabel(row, text=str(total_qty), font=("Inter", 14, "bold"), text_color=qty_color).pack(side="left", fill="x", expand=True, pady=10)
            ctk.CTkLabel(row, text=status_text, font=("Inter", 14, "bold"), text_color=qty_color).pack(side="left", fill="x", expand=True, pady=10)

    def export_excel(self):
        stock_data = self.session.query(
            Warehouse.Name.label('Warehouse_Name'),
            Inventory.Product_Name,
            func.sum(InventoryBalance.initial_stock + InventoryBalance.quantity_imported - InventoryBalance.export_quantity).label('Total_Quantity')
        ).join(Warehouse, InventoryBalance.Warehouse_ID == Warehouse.Warehouse_ID)\
         .join(Inventory, InventoryBalance.Product_ID == Inventory.Product_ID)\
         .group_by(Warehouse.Name, Inventory.Product_Name).all()

        if not stock_data:
            messagebox.showwarning("No Data", "No inventory data to export.")
            return

        df = pd.DataFrame(stock_data, columns=['Warehouse', 'Product Name', 'Total Quantity'])
        df['Status'] = df['Total Quantity'].apply(lambda x: 'Good' if x >= 20 else 'Low Stock')

        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title="Save Inventory Report"
        )
        
        if filepath:
            try:
                df.to_excel(filepath, index=False)
                messagebox.showinfo("Success", f"Data exported successfully to\n{filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{str(e)}")
