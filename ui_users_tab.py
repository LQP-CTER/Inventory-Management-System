import customtkinter as ctk
from tkinter import messagebox
from sqlalchemy.orm import Session
from inventory_management import User

class UsersFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.session: Session = controller.session

        self.header_label = ctk.CTkLabel(self, text="Manage Users", font=("Inter", 24, "bold"))
        self.header_label.pack(pady=(10, 20), anchor="w")

        # Top Bar
        self.top_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.top_bar.pack(fill="x", pady=5)
        
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

        ctk.CTkLabel(self.form_frame, text="User Details", font=("Inter", 18, "bold")).pack(pady=15)
        
        ctk.CTkLabel(self.form_frame, text="Username:", font=("Inter", 14)).pack(anchor="w", padx=15, pady=(10,0))
        self.user_entry = ctk.CTkEntry(self.form_frame)
        self.user_entry.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(self.form_frame, text="Password:", font=("Inter", 14)).pack(anchor="w", padx=15, pady=(10,0))
        self.pass_entry = ctk.CTkEntry(self.form_frame, show="*")
        self.pass_entry.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(self.form_frame, text="Account Type:", font=("Inter", 14)).pack(anchor="w", padx=15, pady=(10,0))
        self.type_cb = ctk.CTkComboBox(self.form_frame, values=["ADMIN", "USER"])
        self.type_cb.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(self.form_frame, text="Employee ID:", font=("Inter", 14)).pack(anchor="w", padx=15, pady=(10,0))
        self.emp_entry = ctk.CTkEntry(self.form_frame)
        self.emp_entry.pack(fill="x", padx=15, pady=5)

        self.btn_save = ctk.CTkButton(self.form_frame, text="Save / Update", command=self.save_user, fg_color="#3b82f6")
        self.btn_save.pack(fill="x", padx=15, pady=20)
        
        self.btn_clear = ctk.CTkButton(self.form_frame, text="Clear Form", command=self.clear_form, fg_color="gray")
        self.btn_clear.pack(fill="x", padx=15, pady=5)

        # --- Right: Table ---
        self.table_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.table_container.grid(row=0, column=1, sticky="nsew")

        self.table_header = ctk.CTkFrame(self.table_container, fg_color=("#e2e8f0", "#1e293b"), corner_radius=5)
        self.table_header.pack(fill="x", pady=5)
        
        ctk.CTkLabel(self.table_header, text="Username", font=("Inter", 14, "bold")).pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(self.table_header, text="Account Type", font=("Inter", 14, "bold")).pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(self.table_header, text="Employee ID", font=("Inter", 14, "bold")).pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(self.table_header, text="Actions", font=("Inter", 14, "bold"), width=120).pack(side="right")

        self.list_frame = ctk.CTkScrollableFrame(self.table_container, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True, pady=5)

        self.load_data()

    def clear_form(self):
        self.user_entry.configure(state="normal")
        self.user_entry.delete(0, 'end')
        self.pass_entry.delete(0, 'end')
        self.emp_entry.delete(0, 'end')
        self.type_cb.set("USER")

    def load_data(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        users = self.session.query(User).all()

        if not users:
            ctk.CTkLabel(self.list_frame, text="No users found.", text_color="gray").pack(pady=20)
            return

        for idx, u in enumerate(users):
            bg_color = ("#f8fafc", "#0f172a") if idx % 2 == 0 else ("#f1f5f9", "#1e293b")
            row = ctk.CTkFrame(self.list_frame, fg_color=bg_color, corner_radius=5)
            row.pack(fill="x", pady=2)
            
            ctk.CTkLabel(row, text=u.username, font=("Inter", 14)).pack(side="left", fill="x", expand=True, pady=10)
            
            type_color = "#3b82f6" if u.account_type == "ADMIN" else "gray"
            ctk.CTkLabel(row, text=u.account_type, font=("Inter", 14, "bold"), text_color=type_color).pack(side="left", fill="x", expand=True, pady=10)
            ctk.CTkLabel(row, text=u.Employee_ID or "N/A", font=("Inter", 14)).pack(side="left", fill="x", expand=True, pady=10)

            actions = ctk.CTkFrame(row, fg_color="transparent", width=120)
            actions.pack(side="right", padx=10)
            actions.pack_propagate(False)

            ctk.CTkButton(actions, text="Edit", width=50, fg_color="#3b82f6", 
                          command=lambda u_obj=u: self.edit_user(u_obj)).pack(side="left", padx=2)
            ctk.CTkButton(actions, text="Del", width=50, fg_color="#ef4444", 
                          command=lambda u_obj=u: self.delete_user(u_obj)).pack(side="right", padx=2)

    def edit_user(self, user_obj):
        self.clear_form()
        self.user_entry.insert(0, user_obj.username)
        self.user_entry.configure(state="disabled") # Username shouldn't be changed easily as it's PK
        self.pass_entry.insert(0, user_obj.password)
        self.type_cb.set(user_obj.account_type)
        self.emp_entry.insert(0, user_obj.Employee_ID or "")

    def save_user(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        acc_type = self.type_cb.get().strip()
        emp_id = self.emp_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Warning", "Username and Password are required.")
            return

        try:
            user = self.session.query(User).filter_by(username=username).first()
            if user:
                # Update
                user.password = password
                user.account_type = acc_type
                user.Employee_ID = emp_id if emp_id else None
            else:
                # Add
                new_user = User(
                    username=username,
                    password=password,
                    account_type=acc_type,
                    Employee_ID=emp_id if emp_id else None
                )
                self.session.add(new_user)
            
            self.session.commit()
            messagebox.showinfo("Success", "User saved successfully!")
            self.clear_form()
            self.load_data()

        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Error", str(e))

    def delete_user(self, user_obj):
        if user_obj.username == self.controller.user_data['username']:
            messagebox.showerror("Error", "You cannot delete your own account.")
            return
            
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete user {user_obj.username}?"):
            try:
                self.session.delete(user_obj)
                self.session.commit()
                self.load_data()
            except Exception as e:
                self.session.rollback()
                messagebox.showerror("Error", str(e))
