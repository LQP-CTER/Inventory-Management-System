from ui_login import ModernLogin
from ui_admin_dashboard import AdminDashboard

def run_app():
    # 1. Start Login Screen
    login_app = ModernLogin()
    login_app.mainloop()
    
    # 2. Check if login was successful
    if login_app.user_data:
        user_data = login_app.user_data
        
        # 3. Start Dashboard
        if user_data["account_type"] == "ADMIN":
            dashboard_app = AdminDashboard(user_data)
            dashboard_app.mainloop()
        else:
            # Employee Dashboard (Using AdminDashboard template for now)
            dashboard_app = AdminDashboard(user_data)
            dashboard_app.mainloop()

if __name__ == "__main__":
    run_app()
