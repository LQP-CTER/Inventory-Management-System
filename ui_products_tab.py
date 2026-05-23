import customtkinter as ctk
from tkinter import messagebox
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func
from inventory_management import Inventory, AuditLog
from ui_components import show_toast

class ProductsFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.session: Session = controller.session

        self.header_label = ctk.CTkLabel(self, text="Manage Products", font=("Inter", 24, "bold"))
        self.header_label.pack(pady=(10, 20), anchor="w")

        # Top Bar
        self.top_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.top_bar.pack(fill="x", pady=5)

        # Search Bar
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self.load_data)
        self.search_entry = ctk.CTkEntry(self.top_bar, textvariable=self.search_var, placeholder_text="Search Product by ID or Name...", width=300)
        self.search_entry.pack(side="left", padx=20)
        
        self.btn_refresh = ctk.CTkButton(self.top_bar, text="Refresh Data", command=self.load_data, width=120)
        self.btn_refresh.pack(side="right", padx=10)

        # Content Area (Left: Form, Right: List)
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=3)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # --- Left: Form ---
        self.form_frame = ctk.CTkFrame(self.content_frame, corner_radius=15, fg_color=("#f1f5f9", "#1e293b"))
        self.form_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(self.form_frame, text="Product Details", font=("Inter", 18, "bold")).pack(pady=15)

        self.prod_id_var = ctk.StringVar()
        
        ctk.CTkLabel(self.form_frame, text="Product Name:", font=("Inter", 14)).pack(anchor="w", padx=15, pady=(10,0))
        self.name_entry = ctk.CTkEntry(self.form_frame)
        self.name_entry.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(self.form_frame, text="Category ID:", font=("Inter", 14)).pack(anchor="w", padx=15, pady=(10,0))
        self.cat_entry = ctk.CTkEntry(self.form_frame)
        self.cat_entry.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(self.form_frame, text="Unit Type:", font=("Inter", 14)).pack(anchor="w", padx=15, pady=(10,0))
        self.unit_entry = ctk.CTkEntry(self.form_frame)
        self.unit_entry.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(self.form_frame, text="Supplier ID:", font=("Inter", 14)).pack(anchor="w", padx=15, pady=(10,0))
        self.sup_entry = ctk.CTkEntry(self.form_frame)
        self.sup_entry.pack(fill="x", padx=15, pady=5)

        self.btn_save = ctk.CTkButton(self.form_frame, text="Save / Update", command=self.save_product, fg_color="#3b82f6")
        self.btn_save.pack(fill="x", padx=15, pady=20)
        
        self.btn_clear = ctk.CTkButton(self.form_frame, text="Clear Form", command=self.clear_form, fg_color="gray")
        self.btn_clear.pack(fill="x", padx=15, pady=5)

        # --- Right: Table ---
        self.table_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.table_container.grid(row=0, column=1, sticky="nsew")

        self.table_header = ctk.CTkFrame(self.table_container, fg_color=("#e2e8f0", "#1e293b"), corner_radius=5)
        self.table_header.pack(fill="x", pady=5)
        
        ctk.CTkLabel(self.table_header, text="ID", font=("Inter", 14, "bold")).pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(self.table_header, text="Name", font=("Inter", 14, "bold")).pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(self.table_header, text="Category", font=("Inter", 14, "bold")).pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(self.table_header, text="Unit", font=("Inter", 14, "bold")).pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(self.table_header, text="Supplier", font=("Inter", 14, "bold")).pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(self.table_header, text="Actions", font=("Inter", 14, "bold"), width=120).pack(side="right")

        self.list_frame = ctk.CTkScrollableFrame(self.table_container, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True, pady=5)

        self.load_data()

    def clear_form(self):
        self.prod_id_var.set("")
        self.name_entry.delete(0, 'end')
        self.cat_entry.delete(0, 'end')
        self.unit_entry.delete(0, 'end')
        self.sup_entry.delete(0, 'end')

    def load_data(self, *args):
        for w in self.list_frame.winfo_children():
            w.destroy()

        query = self.session.query(Inventory)
        search_term = self.search_var.get().strip().lower()
        if search_term:
            query = query.filter(
                (func.lower(Inventory.Product_Name).contains(search_term)) |
                (func.lower(Inventory.Product_ID).contains(search_term))
            )

        products = query.all()

        if not products:
            ctk.CTkLabel(self.list_frame, text="No products found.", text_color="gray").pack(pady=20)
            return

        for idx, prod in enumerate(products):
            bg_color = ("#f8fafc", "#0f172a") if idx % 2 == 0 else ("#f1f5f9", "#1e293b")
            row = ctk.CTkFrame(self.list_frame, fg_color=bg_color, corner_radius=5)
            row.pack(fill="x", pady=2)
            
            ctk.CTkLabel(row, text=prod.Product_ID, font=("Inter", 14)).pack(side="left", fill="x", expand=True, pady=10)
            ctk.CTkLabel(row, text=prod.Product_Name, font=("Inter", 14)).pack(side="left", fill="x", expand=True, pady=10)
            ctk.CTkLabel(row, text=prod.Category_ID or "N/A", font=("Inter", 14)).pack(side="left", fill="x", expand=True, pady=10)
            ctk.CTkLabel(row, text=prod.Unit_Type or "N/A", font=("Inter", 14)).pack(side="left", fill="x", expand=True, pady=10)
            ctk.CTkLabel(row, text=prod.Supplier_ID or "N/A", font=("Inter", 14)).pack(side="left", fill="x", expand=True, pady=10)

            actions = ctk.CTkFrame(row, fg_color="transparent", width=120)
            actions.pack(side="right", padx=10)
            actions.pack_propagate(False)

            ctk.CTkButton(actions, text="Edit", width=50, fg_color="#3b82f6", 
                          command=lambda p=prod: self.edit_product(p)).pack(side="left", padx=2)
            ctk.CTkButton(actions, text="Del", width=50, fg_color="#ef4444", 
                          command=lambda p=prod: self.delete_product(p)).pack(side="right", padx=2)

    def edit_product(self, prod):
        self.clear_form()
        self.prod_id_var.set(prod.Product_ID)
        self.name_entry.insert(0, prod.Product_Name)
        self.cat_entry.insert(0, prod.Category_ID or "")
        self.unit_entry.insert(0, prod.Unit_Type or "")
        self.sup_entry.insert(0, prod.Supplier_ID or "")

    def save_product(self):
        pid = self.prod_id_var.get()
        name = self.name_entry.get().strip()
        cat = self.cat_entry.get().strip()
        unit = self.unit_entry.get().strip()
        sup = self.sup_entry.get().strip()

        if not name:
            show_toast(self.controller, "Product Name is required.", type="warning")
            return

        try:
            username = self.controller.user_data.get('username', 'system')
            action_desc = ""

            if pid:
                # Update
                prod = self.session.query(Inventory).filter_by(Product_ID=pid).first()
                if prod:
                    prod.Product_Name = name
                    prod.Category_ID = cat if cat else None
                    prod.Unit_Type = unit if unit else None
                    prod.Supplier_ID = sup if sup else None
                    action_desc = f"Updated Product: {pid}"
            else:
                # Add
                new_id = "P" + str(uuid.uuid4())[:8].upper()
                new_prod = Inventory(
                    Product_ID=new_id,
                    Product_Name=name,
                    Category_ID=cat if cat else None,
                    Unit_Type=unit if unit else None,
                    Supplier_ID=sup if sup else None
                )
                self.session.add(new_prod)
                action_desc = f"Created Product: {name}"
            
            # Audit Log
            audit = AuditLog(Username=username, Action=action_desc, Table_Affected="inventory")
            self.session.add(audit)

            self.session.commit()
            show_toast(self.controller, "Product saved successfully!", type="success")
            self.clear_form()
            self.load_data()

        except Exception as e:
            self.session.rollback()
            show_toast(self.controller, f"Error: {str(e)}", type="error")

    def delete_product(self, prod):
        from tkinter import messagebox
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete {prod.Product_Name}?"):
            try:
                username = self.controller.user_data.get('username', 'system')
                audit = AuditLog(Username=username, Action=f"Deleted Product: {prod.Product_ID}", Table_Affected="inventory")
                self.session.add(audit)

                self.session.delete(prod)
                self.session.commit()
                show_toast(self.controller, "Product deleted.", type="success")
                self.load_data()
            except Exception as e:
                self.session.rollback()
                show_toast(self.controller, f"Error: {str(e)}", type="error")
