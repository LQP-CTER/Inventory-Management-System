import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import uuid
from sqlalchemy.orm import Session
from inventory_management import Warehouse, Inventory, InventoryTransaction, InventoryTransactionDetail, InventoryBalance

class TransferFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.session: Session = controller.session
        self.added_items = []  # List of dicts

        self.header_label = ctk.CTkLabel(self, text="Transfer Stock", font=("Inter", 24, "bold"))
        self.header_label.pack(pady=(10, 20), anchor="w")

        # Form Frame
        self.form_frame = ctk.CTkFrame(self, corner_radius=15, fg_color=("#f1f5f9", "#1e293b"))
        self.form_frame.pack(fill="x", pady=10, padx=10)

        # From Warehouse
        ctk.CTkLabel(self.form_frame, text="From Warehouse:", font=("Inter", 14)).grid(row=0, column=0, padx=15, pady=15, sticky="w")
        self.from_wh_cb = ctk.CTkComboBox(self.form_frame, values=self.get_warehouses(), width=150)
        self.from_wh_cb.grid(row=0, column=1, padx=15, pady=15)

        # To Warehouse
        ctk.CTkLabel(self.form_frame, text="To Warehouse:", font=("Inter", 14)).grid(row=0, column=2, padx=15, pady=15, sticky="w")
        self.to_wh_cb = ctk.CTkComboBox(self.form_frame, values=self.get_warehouses(), width=150)
        self.to_wh_cb.grid(row=0, column=3, padx=15, pady=15)

        # Product Selection
        ctk.CTkLabel(self.form_frame, text="Product:", font=("Inter", 14)).grid(row=1, column=0, padx=15, pady=15, sticky="w")
        self.product_cb = ctk.CTkComboBox(self.form_frame, values=self.get_products(), width=150)
        self.product_cb.grid(row=1, column=1, padx=15, pady=15)

        # Quantity
        ctk.CTkLabel(self.form_frame, text="Quantity:", font=("Inter", 14)).grid(row=1, column=2, padx=15, pady=15, sticky="w")
        self.qty_entry = ctk.CTkEntry(self.form_frame, width=150)
        self.qty_entry.grid(row=1, column=3, padx=15, pady=15)

        # Add Button
        self.btn_add = ctk.CTkButton(self.form_frame, text="Add to List", command=self.add_to_list, fg_color="#3b82f6")
        self.btn_add.grid(row=2, column=0, columnspan=4, pady=20)

        # Items List Frame
        self.list_frame = ctk.CTkScrollableFrame(self, fg_color=("#f8fafc", "#0f172a"), corner_radius=10)
        self.list_frame.pack(fill="both", expand=True, pady=10, padx=10)

        self.update_list_view()

        # Submit Button
        self.btn_submit = ctk.CTkButton(self, text="Confirm Transfer", command=self.submit_transfer, 
                                        font=("Inter", 16, "bold"), fg_color="#f59e0b", hover_color="#d97706", height=45)
        self.btn_submit.pack(pady=20, fill="x", padx=10)

    def get_warehouses(self):
        warehouses = self.session.query(Warehouse.Name).all()
        return [row[0] for row in warehouses] if warehouses else ["No Warehouse"]

    def get_products(self):
        products = self.session.query(Inventory.Product_Name).all()
        return [row[0] for row in products] if products else ["No Product"]

    def add_to_list(self):
        from_wh = self.from_wh_cb.get()
        to_wh = self.to_wh_cb.get()
        prod = self.product_cb.get()
        qty = self.qty_entry.get()

        if from_wh == to_wh:
            messagebox.showwarning("Warning", "Source and Destination warehouse cannot be the same.")
            return

        if not qty.isdigit() or int(qty) <= 0:
            messagebox.showwarning("Warning", "Quantity must be a positive integer.")
            return
            
        self.added_items.append({
            "from": from_wh,
            "to": to_wh,
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
            
            text = f"📦 {item['product']} | 🚚 {item['from']} ➡️ {item['to']} | Qty: {item['qty']}"
            ctk.CTkLabel(row, text=text, font=("Inter", 14)).pack(side="left", padx=10)
            
            btn_del = ctk.CTkButton(row, text="Remove", width=60, fg_color="#ef4444", 
                                    command=lambda idx=i: self.remove_item(idx))
            btn_del.pack(side="right", padx=10)

    def remove_item(self, index):
        self.added_items.pop(index)
        self.update_list_view()

    def submit_transfer(self):
        if not self.added_items:
            messagebox.showwarning("Warning", "No items to transfer!")
            return

        try:
            emp_id = 'E01'
            trans_date = datetime.now()
            
            for item in self.added_items:
                from_wh_id = self.session.query(Warehouse.Warehouse_ID).filter_by(Name=item["from"]).scalar()
                to_wh_id = self.session.query(Warehouse.Warehouse_ID).filter_by(Name=item["to"]).scalar()
                prod_id = self.session.query(Inventory.Product_ID).filter_by(Product_Name=item["product"]).scalar()
                
                # Deduct from Source
                bal_from = self.session.query(InventoryBalance).filter_by(Warehouse_ID=from_wh_id, Product_ID=prod_id).first()
                if not bal_from:
                    messagebox.showerror("Error", f"No stock found for {item['product']} in {item['from']}.")
                    return
                
                available_stock = bal_from.initial_stock + bal_from.quantity_imported - bal_from.export_quantity
                if item["qty"] > available_stock:
                    messagebox.showerror("Error", f"Not enough stock for {item['product']} in {item['from']}. Available: {available_stock}")
                    return

                bal_from.export_quantity += item["qty"]

                # Add to Destination
                bal_to = self.session.query(InventoryBalance).filter_by(Warehouse_ID=to_wh_id, Product_ID=prod_id).first()
                if bal_to:
                    bal_to.quantity_imported += item["qty"]
                else:
                    new_bal = InventoryBalance(
                        Inventory_Balance_ID=str(uuid.uuid4())[:15], Warehouse_ID=to_wh_id, 
                        Product_ID=prod_id, initial_stock=0, quantity_imported=item["qty"], 
                        export_quantity=0, Date=trans_date.date()
                    )
                    self.session.add(new_bal)

                # Record Outbound Transaction
                trans_out_id = str(uuid.uuid4())[:15]
                trans_out = InventoryTransaction(
                    Transaction_ID=trans_out_id, Transaction_Type='Outbound', 
                    Warehouse_ID=from_wh_id, Employee_ID=emp_id, Transaction_Date=trans_date
                )
                self.session.add(trans_out)
                
                detail_out = InventoryTransactionDetail(
                    Detail_ID=str(uuid.uuid4())[:15], Transaction_ID=trans_out_id, 
                    Product_ID=prod_id, Quantity=item["qty"], Total_Price=0
                )
                self.session.add(detail_out)

                # Record Inbound Transaction
                trans_in_id = str(uuid.uuid4())[:15]
                trans_in = InventoryTransaction(
                    Transaction_ID=trans_in_id, Transaction_Type='Inbound', 
                    Warehouse_ID=to_wh_id, Employee_ID=emp_id, Transaction_Date=trans_date
                )
                self.session.add(trans_in)
                
                detail_in = InventoryTransactionDetail(
                    Detail_ID=str(uuid.uuid4())[:15], Transaction_ID=trans_in_id, 
                    Product_ID=prod_id, Quantity=item["qty"], Total_Price=0
                )
                self.session.add(detail_in)

            self.session.commit()
            messagebox.showinfo("Success", "Transfer recorded successfully!")
            self.added_items.clear()
            self.update_list_view()

        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Database Error", str(e))
