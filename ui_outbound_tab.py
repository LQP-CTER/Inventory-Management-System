import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import uuid
from sqlalchemy.orm import Session
from inventory_management import Warehouse, Inventory, InventoryTransaction, InventoryTransactionDetail, InventoryBalance, AuditLog
from ui_components import show_toast

class OutboundFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.session: Session = controller.session
        self.added_items = []  # List of dicts

        self.header_label = ctk.CTkLabel(self, text="Outbound Stock", font=("Inter", 24, "bold"))
        self.header_label.pack(pady=(10, 20), anchor="w")

        # Form Frame
        self.form_frame = ctk.CTkFrame(self, corner_radius=15, fg_color=("#f1f5f9", "#1e293b"))
        self.form_frame.pack(fill="x", pady=10, padx=10)

        # Warehouse Selection
        ctk.CTkLabel(self.form_frame, text="Warehouse:", font=("Inter", 14)).grid(row=0, column=0, padx=15, pady=15, sticky="w")
        self.warehouse_cb = ctk.CTkComboBox(self.form_frame, values=self.get_warehouses(), width=200)
        self.warehouse_cb.grid(row=0, column=1, padx=15, pady=15)

        # Product Selection
        ctk.CTkLabel(self.form_frame, text="Product:", font=("Inter", 14)).grid(row=0, column=2, padx=15, pady=15, sticky="w")
        self.product_cb = ctk.CTkComboBox(self.form_frame, values=self.get_products(), width=200)
        self.product_cb.grid(row=0, column=3, padx=15, pady=15)

        # Quantity
        ctk.CTkLabel(self.form_frame, text="Quantity:", font=("Inter", 14)).grid(row=1, column=0, padx=15, pady=15, sticky="w")
        self.qty_entry = ctk.CTkEntry(self.form_frame, width=200)
        self.qty_entry.grid(row=1, column=1, padx=15, pady=15)

        # Add Button
        self.btn_add = ctk.CTkButton(self.form_frame, text="Add to List", command=self.add_to_list, fg_color="#3b82f6")
        self.btn_add.grid(row=2, column=0, columnspan=4, pady=20)

        # Items List Frame
        self.list_frame = ctk.CTkScrollableFrame(self, fg_color=("#f8fafc", "#0f172a"), corner_radius=10)
        self.list_frame.pack(fill="both", expand=True, pady=10, padx=10)

        self.update_list_view()

        # Submit Button
        self.btn_submit = ctk.CTkButton(self, text="Confirm Outbound", command=self.submit_outbound, 
                                        font=("Inter", 16, "bold"), fg_color="#ef4444", hover_color="#dc2626", height=45)
        self.btn_submit.pack(pady=20, fill="x", padx=10)

    def get_warehouses(self):
        warehouses = self.session.query(Warehouse.Name).all()
        return [row[0] for row in warehouses] if warehouses else ["No Warehouse"]

    def get_products(self):
        products = self.session.query(Inventory.Product_Name).all()
        return [row[0] for row in products] if products else ["No Product"]

    def add_to_list(self):
        wh = self.warehouse_cb.get()
        prod = self.product_cb.get()
        qty = self.qty_entry.get()

        if not qty.isdigit() or int(qty) <= 0:
            show_toast(self.controller, "Quantity must be a positive integer.", type="warning")
            return
            
        self.added_items.append({
            "warehouse": wh,
            "product": prod,
            "qty": int(qty)
        })
        
        self.qty_entry.delete(0, 'end')
        self.update_list_view()

    def update_list_view(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        if not self.added_items:
            ctk.CTkLabel(self.list_frame, text="No items added yet.", text_color="gray").pack(pady=20)
            return

        for i, item in enumerate(self.added_items):
            row = ctk.CTkFrame(self.list_frame, fg_color="transparent")
            row.pack(fill="x", pady=5)
            
            text = f"📦 {item['product']} | 🏭 {item['warehouse']} | Qty: {item['qty']}"
            ctk.CTkLabel(row, text=text, font=("Inter", 14)).pack(side="left", padx=10)
            
            btn_del = ctk.CTkButton(row, text="Remove", width=60, fg_color="#ef4444", 
                                    command=lambda idx=i: self.remove_item(idx))
            btn_del.pack(side="right", padx=10)

    def remove_item(self, index):
        self.added_items.pop(index)
        self.update_list_view()

    def submit_outbound(self):
        if not self.added_items:
            show_toast(self.controller, "No items to outbound!", type="warning")
            return

        try:
            emp_id = self.controller.user_data.get('employee_id', 'E01')
            username = self.controller.user_data.get('username', 'system')
            trans_date = datetime.now()
            
            for item in self.added_items:
                wh_id = self.session.query(Warehouse.Warehouse_ID).filter_by(Name=item["warehouse"]).scalar()
                prod_id = self.session.query(Inventory.Product_ID).filter_by(Product_Name=item["product"]).scalar()
                
                # Check available stock
                bal = self.session.query(InventoryBalance).filter_by(Warehouse_ID=wh_id, Product_ID=prod_id).first()
                if not bal:
                    show_toast(self.controller, f"No stock found for {item['product']} in {item['warehouse']}.", type="error")
                    return
                
                available_stock = bal.initial_stock + bal.quantity_imported - bal.export_quantity
                if item["qty"] > available_stock:
                    show_toast(self.controller, f"Not enough stock for {item['product']}. Available: {available_stock}", type="error")
                    return

                # Transaction
                trans_id = str(uuid.uuid4())[:15]
                trans = InventoryTransaction(
                    Transaction_ID=trans_id, Transaction_Type='Outbound', 
                    Warehouse_ID=wh_id, Employee_ID=emp_id, Transaction_Date=trans_date, Status='Draft'
                )
                self.session.add(trans)
                
                # Detail
                # Outbound uses Unit_Cost to calculate value (Weighted Average), we'll do this on Approval, 
                # or we can grab the current Average Cost if available.
                unit_cost = 0
                if bal.quantity_imported > 0 and bal.Total_Price_Import:
                    unit_cost = float(bal.Total_Price_Import) / bal.quantity_imported

                detail = InventoryTransactionDetail(
                    Detail_ID=str(uuid.uuid4())[:15], Transaction_ID=trans_id, 
                    Product_ID=prod_id, Quantity=item["qty"], 
                    Total_Price=unit_cost * item["qty"], Unit_Price=unit_cost
                )
                self.session.add(detail)
                
                # Balance update is OMITTED here for Draft status.
                
                # Audit Log
                audit = AuditLog(Username=username, Action=f"Created Outbound Draft: {item['product']} (Qty: {item['qty']})", Table_Affected="inventory_transaction", Timestamp=trans_date)
                self.session.add(audit)

            self.session.commit()
            show_toast(self.controller, "Outbound draft recorded successfully!", type="success")
            self.added_items.clear()
            self.update_list_view()

        except Exception as e:
            self.session.rollback()
            show_toast(self.controller, f"Database Error: {str(e)}", type="error")
