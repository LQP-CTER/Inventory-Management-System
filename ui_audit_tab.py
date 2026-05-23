import customtkinter as ctk
from sqlalchemy.orm import Session
from inventory_management import AuditLog
import pandas as pd
from tkinter import filedialog, messagebox
from ui_components import show_toast

class AuditLogsFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.session: Session = controller.session

        self.header_label = ctk.CTkLabel(self, text="Audit Logs (System Trail)", font=("Inter", 24, "bold"))
        self.header_label.pack(pady=(10, 20), anchor="w")

        # Top Bar
        self.top_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.top_bar.pack(fill="x", pady=5)
        
        self.btn_export = ctk.CTkButton(self.top_bar, text="Export Excel", command=self.export_excel, width=120, fg_color="#10b981", hover_color="#059669")
        self.btn_export.pack(side="left")

        self.btn_refresh = ctk.CTkButton(self.top_bar, text="Refresh Data", command=self.load_data, width=120)
        self.btn_refresh.pack(side="right", padx=10)

        # Table Header
        self.table_header = ctk.CTkFrame(self, fg_color=("#e2e8f0", "#1e293b"), corner_radius=5)
        self.table_header.pack(fill="x", pady=5)
        
        ctk.CTkLabel(self.table_header, text="Log ID", font=("Inter", 14, "bold"), width=80).pack(side="left")
        ctk.CTkLabel(self.table_header, text="Timestamp", font=("Inter", 14, "bold"), width=150).pack(side="left")
        ctk.CTkLabel(self.table_header, text="User", font=("Inter", 14, "bold"), width=120).pack(side="left")
        ctk.CTkLabel(self.table_header, text="Action", font=("Inter", 14, "bold")).pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(self.table_header, text="Target Table", font=("Inter", 14, "bold"), width=150).pack(side="left")

        self.list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True, pady=5)

        self.load_data()

    def load_data(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        logs = self.session.query(AuditLog).order_by(AuditLog.Timestamp.desc()).limit(100).all()

        if not logs:
            ctk.CTkLabel(self.list_frame, text="No audit logs found.", text_color="gray").pack(pady=20)
            return

        for idx, log in enumerate(logs):
            bg_color = ("#f8fafc", "#0f172a") if idx % 2 == 0 else ("#f1f5f9", "#1e293b")
            row = ctk.CTkFrame(self.list_frame, fg_color=bg_color, corner_radius=5)
            row.pack(fill="x", pady=2)
            
            ts_str = log.Timestamp.strftime("%Y-%m-%d %H:%M:%S") if hasattr(log.Timestamp, 'strftime') else str(log.Timestamp)

            ctk.CTkLabel(row, text=str(log.Log_ID), font=("Inter", 13), width=80).pack(side="left")
            ctk.CTkLabel(row, text=ts_str, font=("Inter", 13), width=150).pack(side="left")
            ctk.CTkLabel(row, text=log.Username, font=("Inter", 13, "bold")).pack(side="left", width=120)
            ctk.CTkLabel(row, text=log.Action, font=("Inter", 13)).pack(side="left", fill="x", expand=True, anchor="w", padx=10)
            ctk.CTkLabel(row, text=log.Table_Affected or "N/A", font=("Inter", 13), width=150).pack(side="left")

    def export_excel(self):
        logs = self.session.query(AuditLog).order_by(AuditLog.Timestamp.desc()).all()
        if not logs:
            show_toast(self.controller, "No logs to export.", type="warning")
            return

        data = []
        for l in logs:
            data.append({
                'Log ID': l.Log_ID,
                'Timestamp': l.Timestamp.strftime("%Y-%m-%d %H:%M:%S") if hasattr(l.Timestamp, 'strftime') else str(l.Timestamp),
                'User': l.Username,
                'Action': l.Action,
                'Target Table': l.Table_Affected,
                'Details': l.Details
            })

        df = pd.DataFrame(data)
        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title="Save Audit Logs"
        )
        if filepath:
            try:
                df.to_excel(filepath, index=False)
                show_toast(self.controller, f"Logs exported to\n{filepath}", type="success")
            except Exception as e:
                show_toast(self.controller, f"Could not save file:\n{str(e)}", type="error")
