import customtkinter as ctk

class ToastNotification(ctk.CTkFrame):
    def __init__(self, master, message, type="success", duration=3000, **kwargs):
        """
        type: 'success', 'error', 'info', 'warning'
        """
        # Determine colors based on type
        bg_color = "#10b981" # Default Success (Green)
        icon = "✔️"
        if type == "error":
            bg_color = "#ef4444"
            icon = "❌"
        elif type == "warning":
            bg_color = "#f59e0b"
            icon = "⚠️"
        elif type == "info":
            bg_color = "#3b82f6"
            icon = "ℹ️"

        super().__init__(master, fg_color=bg_color, corner_radius=8, **kwargs)
        self.duration = duration

        # Layout
        self.lbl_icon = ctk.CTkLabel(self, text=icon, font=("Inter", 16), text_color="white")
        self.lbl_icon.pack(side="left", padx=(10, 5), pady=10)

        self.lbl_msg = ctk.CTkLabel(self, text=message, font=("Inter", 14, "bold"), text_color="white")
        self.lbl_msg.pack(side="left", padx=(0, 15), pady=10)

        # Place toast at bottom right
        self.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)

        # Slide animation (simple)
        self.target_y = -20
        self.current_y = 50
        self.place_configure(y=self.current_y)
        self.animate_in()

    def animate_in(self):
        if self.current_y > self.target_y:
            self.current_y -= 5
            self.place_configure(y=self.current_y)
            self.after(10, self.animate_in)
        else:
            self.after(self.duration, self.animate_out)

    def animate_out(self):
        if self.current_y < 50:
            self.current_y += 5
            self.place_configure(y=self.current_y)
            self.after(10, self.animate_out)
        else:
            self.destroy()

def show_toast(master, message, type="success", duration=3000):
    ToastNotification(master, message, type=type, duration=duration)
