import customtkinter as ctk
import pandas as pd
from datetime import datetime
import uuid
from tkinter import filedialog, messagebox
from sqlalchemy.orm import Session
from inventory_management import InventoryTransaction, InventoryTransactionDetail, Warehouse, Employee, Inventory, InventoryBalance, AuditLog
from ui_components import show_toast

class TransactionsFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.session: Session = controller.session

        self.header_label = ctk.CTkLabel(self, text="Transactions History", font=("Inter", 24, "bold"))
        self.header_label.pack(pady=(10, 20), anchor="w")

        # Top Bar
        self.top_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.top_bar.pack(fill="x", padx=10, pady=5)
        
        # Filters
        ctk.CTkLabel(self.top_bar, text="Status:", font=("Inter", 12)).pack(side="left", padx=5)
        self.status_var = ctk.StringVar(value="All")
        self.status_cb = ctk.CTkComboBox(self.top_bar, values=["All", "Draft", "Completed"], variable=self.status_var, width=100, command=self.load_data)
        self.status_cb.pack(side="left", padx=5)

        ctk.CTkLabel(self.top_bar, text="Type:", font=("Inter", 12)).pack(side="left", padx=(15,5))
        self.type_var = ctk.StringVar(value="All")
        self.type_cb = ctk.CTkComboBox(self.top_bar, values=["All", "Inbound", "Outbound"], variable=self.type_var, width=100, command=self.load_data)
        self.type_cb.pack(side="left", padx=5)

        self.btn_export = ctk.CTkButton(self.top_bar, text="Export Excel", command=self.export_excel, width=100, fg_color="#10b981", hover_color="#059669")
        self.btn_export.pack(side="right", padx=5)

        self.btn_refresh = ctk.CTkButton(self.top_bar, text="Refresh Data", command=self.load_data, width=100)
        self.btn_refresh.pack(side="right", padx=5)

        # Table Header
        self.table_header = ctk.CTkFrame(self, fg_color=("#e2e8f0", "#1e293b"), corner_radius=5)
        self.table_header.pack(fill="x", pady=5)
        
        ctk.CTkLabel(self.table_header, text="ID / Date", font=("Inter", 14, "bold")).pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(self.table_header, text="Type", font=("Inter", 14, "bold")).pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(self.table_header, text="Warehouse", font=("Inter", 14, "bold")).pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(self.table_header, text="Product", font=("Inter", 14, "bold")).pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(self.table_header, text="Qty", font=("Inter", 14, "bold")).pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(self.table_header, text="Status", font=("Inter", 14, "bold")).pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(self.table_header, text="Action", font=("Inter", 14, "bold"), width=80).pack(side="right", padx=5)

        # Scrollable Data Frame
        self.list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True, pady=5)

        self.load_data()

    def load_data(self, *args):
        for w in self.list_frame.winfo_children():
            w.destroy()

        query = self.session.query(
            InventoryTransaction.Transaction_ID,
            InventoryTransaction.Transaction_Date,
            InventoryTransaction.Transaction_Type,
            InventoryTransaction.Status,
            Warehouse.Name.label('Warehouse_Name'),
            Inventory.Product_Name,
            InventoryTransactionDetail.Quantity,
            Employee.Employee_Name,
            InventoryTransaction.Warehouse_ID,
            Inventory.Product_ID,
            InventoryTransactionDetail.Total_Price
        ).join(InventoryTransactionDetail, InventoryTransaction.Transaction_ID == InventoryTransactionDetail.Transaction_ID)\
         .join(Warehouse, InventoryTransaction.Warehouse_ID == Warehouse.Warehouse_ID)\
         .join(Inventory, InventoryTransactionDetail.Product_ID == Inventory.Product_ID)\
         .join(Employee, InventoryTransaction.Employee_ID == Employee.Employee_ID)

        if self.status_var.get() != "All":
            query = query.filter(InventoryTransaction.Status == self.status_var.get())
        if self.type_var.get() != "All":
            query = query.filter(InventoryTransaction.Transaction_Type == self.type_var.get())

        transactions = query.order_by(InventoryTransaction.Transaction_Date.desc()).all()

        if not transactions:
            ctk.CTkLabel(self.list_frame, text="No transactions found.", text_color="gray").pack(pady=20)
            return

        for idx, row_data in enumerate(transactions):
            t_id, t_date, t_type, t_status, wh_name, prod_name, qty, emp_name, wh_id, prod_id, total_price = row_data
            
            bg_color = ("#f8fafc", "#0f172a") if idx % 2 == 0 else ("#f1f5f9", "#1e293b")
            type_color = "#3b82f6" if t_type == "Inbound" else "#ef4444"
            status_color = "#10b981" if t_status == "Completed" else "#f59e0b"
            
            row = ctk.CTkFrame(self.list_frame, fg_color=bg_color, corner_radius=5)
            row.pack(fill="x", pady=2)
            
            date_str = f"{t_id[:8]}...\n{t_date.strftime('%Y-%m-%d') if hasattr(t_date, 'strftime') else str(t_date)}"

            ctk.CTkLabel(row, text=date_str, font=("Inter", 12)).pack(side="left", fill="x", expand=True, pady=5)
            ctk.CTkLabel(row, text=t_type, font=("Inter", 14, "bold"), text_color=type_color).pack(side="left", fill="x", expand=True, pady=5)
            ctk.CTkLabel(row, text=wh_name, font=("Inter", 14)).pack(side="left", fill="x", expand=True, pady=5)
            ctk.CTkLabel(row, text=prod_name, font=("Inter", 14)).pack(side="left", fill="x", expand=True, pady=5)
            ctk.CTkLabel(row, text=str(qty), font=("Inter", 14, "bold")).pack(side="left", fill="x", expand=True, pady=5)
            ctk.CTkLabel(row, text=t_status, font=("Inter", 13, "bold"), text_color=status_color).pack(side="left", fill="x", expand=True, pady=5)

            # Action Frame
            action_frame = ctk.CTkFrame(row, fg_color="transparent", width=80)
            action_frame.pack(side="right", padx=5)
            action_frame.pack_propagate(False)

            is_admin = self.controller.user_data.get('account_type', '').upper() == 'ADMIN'
            if t_status == "Draft" and is_admin:
                btn_approve = ctk.CTkButton(action_frame, text="Approve", width=70, height=28, fg_color="#10b981", hover_color="#059669",
                                            command=lambda tid=t_id: self.approve_transaction(tid))
                btn_approve.pack(pady=10)

    def approve_transaction(self, trans_id):
        try:
            trans = self.session.query(InventoryTransaction).filter_by(Transaction_ID=trans_id).first()
            if not trans or trans.Status == "Completed":
                return
            
            # Update balances based on details
            details = self.session.query(InventoryTransactionDetail).filter_by(Transaction_ID=trans_id).all()
            for detail in details:
                bal = self.session.query(InventoryBalance).filter_by(Warehouse_ID=trans.Warehouse_ID, Product_ID=detail.Product_ID).first()
                if trans.Transaction_Type == "Inbound":
                    if bal:
                        bal.quantity_imported += detail.Quantity
                        bal.Total_Price_Import = (bal.Total_Price_Import or 0) + (detail.Total_Price or 0)
                    else:
                        new_bal = InventoryBalance(
                            Inventory_Balance_ID=str(uuid.uuid4())[:15], Warehouse_ID=trans.Warehouse_ID, 
                            Product_ID=detail.Product_ID, quantity_imported=detail.Quantity, Date=datetime.now().date(),
                            Total_Price_Import=detail.Total_Price
                        )
                        self.session.add(new_bal)
                elif trans.Transaction_Type == "Outbound":
                    if bal:
                        bal.export_quantity += detail.Quantity
                        bal.Total_Price_Export = (bal.Total_Price_Export or 0) + (detail.Total_Price or 0)
            
            trans.Status = "Completed"
            
            # Audit
            username = self.controller.user_data.get('username', 'system')
            audit = AuditLog(Username=username, Action=f"Approved {trans.Transaction_Type} Transaction", Table_Affected="inventory_transaction", Details=f"Transaction ID: {trans_id}")
            self.session.add(audit)
            
            self.session.commit()
            show_toast(self.controller, "Transaction Approved Successfully!", type="success")
            self.load_data()
        except Exception as e:
            self.session.rollback()
            show_toast(self.controller, f"Approval Error: {str(e)}", type="error")

    def export_excel(self):
        transactions = self.session.query(
            InventoryTransaction.Transaction_Date,
            InventoryTransaction.Transaction_Type,
            Warehouse.Name.label('Warehouse_Name'),
            Inventory.Product_Name,
            InventoryTransactionDetail.Quantity,
            Employee.Employee_Name
        ).join(InventoryTransactionDetail, InventoryTransaction.Transaction_ID == InventoryTransactionDetail.Transaction_ID)\
         .join(Warehouse, InventoryTransaction.Warehouse_ID == Warehouse.Warehouse_ID)\
         .join(Inventory, InventoryTransactionDetail.Product_ID == Inventory.Product_ID)\
         .join(Employee, InventoryTransaction.Employee_ID == Employee.Employee_ID)\
         .order_by(InventoryTransaction.Transaction_Date.desc()).all()

        if not transactions:
            messagebox.showwarning("No Data", "No transactions to export.")
            return

        df = pd.DataFrame(transactions, columns=['Date', 'Type', 'Status', 'Warehouse', 'Product', 'Quantity', 'Employee'])
        df['Date'] = df['Date'].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if hasattr(x, 'strftime') else str(x))

        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title="Save Transactions Report"
        )
        
        if filepath:
            try:
                df.to_excel(filepath, index=False)
                show_toast(self.controller, f"Data exported successfully to\n{filepath}", type="success")
            except Exception as e:
                show_toast(self.controller, f"Could not save file:\n{str(e)}", type="error")
