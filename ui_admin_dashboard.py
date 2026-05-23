import customtkinter as ctk
import pywinstyles
from ui_dashboard_tab import DashboardFrame
from ui_inbound_tab import InboundFrame
from ui_outbound_tab import OutboundFrame
from ui_inventory_tab import InventoryFrame
from ui_transfer_tab import TransferFrame
from ui_products_tab import ProductsFrame
from ui_users_tab import UsersFrame
from ui_audit_tab import AuditLogsFrame
import webbrowser
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db_adapter import get_connection

class AdminDashboard(ctk.CTk):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        
        # Setup session for the entire dashboard
        engine = create_engine('sqlite:///inventory_management_system.db')
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.base = get_connection(self.session)
        self.cur = self.base.cursor()
        
        # --- Window Setup ---
        self.title("Admin Dashboard - Inventory Management System")
        self.geometry("1400x800")
        
        # Center the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 1400) // 2
        y = (screen_height - 800) // 2
        self.geometry(f"1400x800+{x}+{y}")

        try:
            pywinstyles.apply_style(self, "optimised")
        except:
            pass

        # Configure Grid Layout (1x2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Build Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        # Sidebar Frame configured to hold more buttons
        self.sidebar_frame.grid_rowconfigure(12, weight=1)
        self.sidebar_expanded = True

        # Hamburger Button (Toggle Sidebar)
        self.btn_toggle = ctk.CTkButton(self.sidebar_frame, text="☰", width=40, font=("Inter", 18), fg_color="transparent", command=self.toggle_sidebar)
        self.btn_toggle.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="GNH \nInventory", font=("Inter", 20, "bold"))
        self.logo_label.grid(row=1, column=0, padx=20, pady=(10, 20))
        
        self.user_label = ctk.CTkLabel(self.sidebar_frame, text=f"Welcome, {user_data['username'].capitalize()}", font=("Inter", 14))
        self.user_label.grid(row=2, column=0, padx=20, pady=(0, 30))

        # Buttons
        self.btn_dashboard = ctk.CTkButton(self.sidebar_frame, text="Dashboard", command=self.show_dashboard_tab)
        self.btn_dashboard.grid(row=3, column=0, padx=20, pady=5)
        
        self.btn_inbound = ctk.CTkButton(self.sidebar_frame, text="Inbound Stock", command=self.show_inbound_tab)
        self.btn_inbound.grid(row=4, column=0, padx=20, pady=5)

        self.btn_outbound = ctk.CTkButton(self.sidebar_frame, text="Outbound Stock", command=self.show_outbound_tab)
        self.btn_outbound.grid(row=5, column=0, padx=20, pady=5)

        self.btn_transfer = ctk.CTkButton(self.sidebar_frame, text="Transfer Stock", command=self.show_transfer_tab)
        self.btn_transfer.grid(row=6, column=0, padx=20, pady=5)

        self.btn_inventory = ctk.CTkButton(self.sidebar_frame, text="Inventory View", command=self.show_inventory_tab)
        self.btn_inventory.grid(row=7, column=0, padx=20, pady=5)

        self.btn_products = ctk.CTkButton(self.sidebar_frame, text="Manage Products", command=self.show_products_tab)
        self.btn_products.grid(row=8, column=0, padx=20, pady=5)

        self.btn_users = ctk.CTkButton(self.sidebar_frame, text="Manage Users", command=self.show_users_tab)
        self.btn_users.grid(row=9, column=0, padx=20, pady=5)

        self.btn_audit = ctk.CTkButton(self.sidebar_frame, text="Audit Logs", command=self.show_audit_tab)
        self.btn_audit.grid(row=10, column=0, padx=20, pady=5)

        self.btn_transactions = ctk.CTkButton(self.sidebar_frame, text="Transactions", command=self.show_transactions_tab)
        self.btn_transactions.grid(row=11, column=0, padx=20, pady=5)

        self.btn_powerbi = ctk.CTkButton(self.sidebar_frame, text="Power BI", command=self.open_power_bi_dashboard, fg_color="#10b981", hover_color="#059669")
        self.btn_powerbi.grid(row=12, column=0, padx=20, pady=20)

        self.btn_logout = ctk.CTkButton(self.sidebar_frame, text="Logout", command=self.logout, fg_color="transparent", border_width=2)
        self.btn_logout.grid(row=13, column=0, padx=20, pady=20)

        # Apply RBAC (Role-Based Access Control)
        if self.user_data.get('account_type', '').upper() != 'ADMIN':
            self.btn_dashboard.grid_remove()
            self.btn_products.grid_remove()
            self.btn_users.grid_remove()
            self.btn_powerbi.grid_remove()
            self.btn_audit.grid_remove()

        # Build Main Content Area
        self.main_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        self.current_frame = None
        if self.user_data.get('account_type', '').upper() == 'ADMIN':
            self.show_dashboard_tab()
        else:
            self.show_inbound_tab()

    def switch_frame(self, frame_class):
        if self.current_frame is not None:
            self.current_frame.destroy()
        
        self.current_frame = frame_class(self.main_frame, self)
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    def show_dashboard_tab(self):
        self.switch_frame(DashboardFrame)

    def show_inbound_tab(self):
        self.switch_frame(InboundFrame)

    def show_outbound_tab(self):
        self.switch_frame(OutboundFrame)
        
    def show_inventory_tab(self):
        self.switch_frame(InventoryFrame)

    def show_transfer_tab(self):
        self.switch_frame(TransferFrame)

    def show_products_tab(self):
        self.switch_frame(ProductsFrame)

    def show_users_tab(self):
        self.switch_frame(UsersFrame)

    def show_audit_tab(self):
        self.switch_frame(AuditLogsFrame)

    def show_transactions_tab(self):
        self.switch_frame(TransactionsFrame)

    def toggle_sidebar(self):
        if self.sidebar_expanded:
            self.sidebar_frame.configure(width=60)
            self.logo_label.configure(text="GNH")
            for btn in [self.btn_dashboard, self.btn_inbound, self.btn_outbound, self.btn_inventory, self.btn_transfer, 
                        self.btn_products, self.btn_users, self.btn_audit, self.btn_transactions, self.btn_powerbi, self.btn_logout]:
                # In a real app we'd swap text for icons. Here we just hide text to simulate collapse
                if hasattr(btn, "cget") and btn.cget("text") != "":
                    # Store original text in a custom attribute to restore later
                    btn._original_text = btn.cget("text")
                    btn.configure(text=btn.cget("text")[0]) # Show first letter as icon
            self.sidebar_expanded = False
        else:
            self.sidebar_frame.configure(width=250)
            self.logo_label.configure(text="GNH \nInventory")
            for btn in [self.btn_dashboard, self.btn_inbound, self.btn_outbound, self.btn_inventory, self.btn_transfer, 
                        self.btn_products, self.btn_users, self.btn_audit, self.btn_transactions, self.btn_powerbi, self.btn_logout]:
                if hasattr(btn, "_original_text"):
                    btn.configure(text=btn._original_text)
            self.sidebar_expanded = True

    def open_power_bi_dashboard(self):
        power_bi_url = "https://app.powerbi.com/groups/me/reports/0e3f0efd-570a-42c2-b3da-8e7c10b7f642/ReportSection418919af0647c4587db3?experience=power-bi"
        webbrowser.open_new(power_bi_url)

    def logout(self):
        self.session.close()
        self.destroy()

if __name__ == "__main__":
    app = AdminDashboard({"username": "RITA", "account_type": "ADMIN"})
    app.mainloop()
