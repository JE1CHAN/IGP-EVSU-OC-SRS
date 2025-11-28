"""
EVSU-OC IGP Sales Record System
Main Application Entry Point

Eastern Visayas State University - Ormoc Campus
Income Generating Project Sales Record System
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import DatabaseManager
from modules.transaction_module import TransactionModule
from modules.inventory_module import InventoryModule
from modules.history_module import HistoryModule
from modules.reports_module import ReportsModule


class LoginWindow(tk.Toplevel):
    """Secure Login Window"""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # Configure window
        self.title("Login - EVSU-OC IGP SRS")
        # INCREASED HEIGHT FROM 450 TO 600 TO FIT CONTENT
        self.geometry("500x600")
        self.resizable(False, False)
        self.configure(bg="white")
        
        # Handle "X" button click
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Center the window
        self.center_window()
        
        # Create UI elements
        self.create_ui()
        
    def center_window(self):
        """Center the login window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_ui(self):
        """Create login interface elements"""
        # Main container
        main_frame = tk.Frame(self, bg="white", padx=40, pady=40)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # --- HEADER WITH LOGO BESIDE TITLE ---
        header_frame = tk.Frame(main_frame, bg="white")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        try:
            # Construct path to logo
            logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image", "logo.png")
            
            # Load image
            self.logo_img = tk.PhotoImage(file=logo_path)
            # Resize: INCREASED SUBSAMPLE TO MAKE LOGO SMALLER (5x smaller)
            self.logo_img = self.logo_img.subsample(5, 5) 
            
            # Logo + Title Label
            title_label = tk.Label(
                header_frame,
                text="  EVSU-OC IGP\n  SALES RECORD SYSTEM",
                image=self.logo_img,
                compound=tk.LEFT,  # Places image to the left of text
                font=("Arial", 14, "bold"),
                bg="white",
                fg="#800000",
                justify=tk.LEFT
            )
            title_label.pack()
            
        except Exception as e:
            print(f"Logo error: {e}")
            # Fallback text if logo fails
            tk.Label(
                header_frame,
                text="EVSU-OC IGP\nSALES RECORD SYSTEM",
                font=("Arial", 16, "bold"),
                bg="white",
                fg="#800000"
            ).pack()

        # --- LOGIN FORM ---
        login_frame = tk.LabelFrame(main_frame, text="Admin Login", font=("Arial", 10), bg="white", padx=20, pady=20)
        login_frame.pack(fill=tk.X)
        
        # Username
        tk.Label(
            login_frame,
            text="Username:",
            font=("Arial", 11),
            bg="white",
            fg="#555"
        ).pack(anchor="w")
        
        self.username_entry = tk.Entry(
            login_frame,
            font=("Arial", 12),
            bd=2,
            relief=tk.GROOVE
        )
        self.username_entry.pack(fill=tk.X, pady=(5, 15))
        self.username_entry.focus()
        
        # Password
        tk.Label(
            login_frame,
            text="Password:",
            font=("Arial", 11),
            bg="white",
            fg="#555"
        ).pack(anchor="w")
        
        self.password_entry = tk.Entry(
            login_frame,
            font=("Arial", 12),
            bd=2,
            relief=tk.GROOVE,
            show="•"
        )
        self.password_entry.pack(fill=tk.X, pady=(5, 20))
        
        # Bind Enter key
        self.bind('<Return>', lambda event: self.validate_login())
        
        # Login Button
        tk.Button(
            login_frame,
            text="LOGIN",
            font=("Arial", 11, "bold"),
            bg="#800000",
            fg="white",
            activebackground="#a00000",
            activeforeground="white",
            cursor="hand2",
            height=2,
            command=self.validate_login
        ).pack(fill=tk.X)
        
        # Footer
        tk.Label(
            main_frame,
            text="Authorized Access Only",
            font=("Arial", 8),
            bg="white",
            fg="#999"
        ).pack(side=tk.BOTTOM, pady=(20, 0))

    def validate_login(self):
        """Check credentials"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if username == "admin" and password == "admin123":
            self.parent.deiconify() # Show main app
            self.destroy()          # Close login
        else:
            messagebox.showerror(
                "Access Denied", 
                "Invalid Username or Password.\nPlease check your credentials."
            )
            self.password_entry.delete(0, tk.END)

    def on_close(self):
        """Handle window closing"""
        self.parent.destroy()
        sys.exit()


class MainApplication(tk.Tk):
    """Main application window with navigation"""
    
    def __init__(self):
        super().__init__()
        
        # Hide main window initially (wait for login)
        self.withdraw()
        
        # Initialize database
        self.db_manager = DatabaseManager()
        
        # Configure main window
        self.title("EVSU-OC IGP Sales Record System")
        self.geometry("1200x700")
        self.configure(bg="#f0f0f0")
        
        # Center window on screen
        self.center_window()
        
        # Create main UI
        self.create_header()
        self.create_navigation()
        self.create_content_area()
        
        # Show default module
        self.show_transaction_module()
        
        # Launch Login Window
        LoginWindow(self)
    
    def center_window(self):
        """Center the window on the screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_header(self):
        """Create application header with LOGO beside TITLE"""
        header_frame = tk.Frame(self, bg="#800000", height=90)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        # Container for centering content (optional, or just pack left/center)
        # Here we pack it into the header frame directly
        
        try:
            # Construct path to logo
            logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image", "logo.png")
            
            # Load image (Use a separate instance for main window to avoid reference issues)
            self.header_logo = tk.PhotoImage(file=logo_path)
            # Resize (UPDATED: Subsample 8x to make it smaller as requested)
            self.header_logo = self.header_logo.subsample(8, 8)
            
            # Title with Logo
            title_label = tk.Label(
                header_frame,
                text="  EVSU-OC IGP SALES RECORD SYSTEM",
                image=self.header_logo,
                compound=tk.LEFT,   # IMAGE BESIDE TITLE
                font=("Arial", 20, "bold"),
                bg="#800000",
                fg="white"
            )
            title_label.pack(pady=10)
            
        except Exception as e:
            print(f"Header logo error: {e}")
            # Fallback title without image
            title_label = tk.Label(
                header_frame,
                text="EVSU-OC IGP SALES RECORD SYSTEM",
                font=("Arial", 20, "bold"),
                bg="#800000",
                fg="white"
            )
            title_label.pack(pady=10)
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Eastern Visayas State University - Ormoc Campus",
            font=("Arial", 11),
            bg="#800000",
            fg="white"
        )
        subtitle_label.pack()
    
    def create_navigation(self):
        """Create left navigation panel"""
        nav_frame = tk.Frame(self, bg="#600000", width=220)
        nav_frame.pack(fill=tk.Y, side=tk.LEFT)
        nav_frame.pack_propagate(False)
        
        # Navigation title
        nav_title = tk.Label(
            nav_frame,
            text="MENU",
            font=("Arial", 14, "bold"),
            bg="#600000",
            fg="white",
            pady=15
        )
        nav_title.pack(fill=tk.X)
        
        # Navigation buttons
        self.nav_buttons = []
        
        buttons_config = [
            ("📝 Transaction Entry", self.show_transaction_module),
            ("📦 Inventory", self.show_inventory_module),
            ("📊 Sales History", self.show_history_module),
            ("📈 Reports", self.show_reports_module),
            ("❌ Exit", self.exit_application)
        ]
        
        for text, command in buttons_config:
            btn = tk.Button(
                nav_frame,
                text=text,
                font=("Arial", 12),
                bg="#600000",         # Normal bg: Dark Maroon
                fg="white",           # Normal text: White
                activebackground="#FFC107", # Active bg: Yellow (Accent)
                activeforeground="black",   # Active text: Black
                bd=0,
                padx=20,
                pady=15,
                cursor="hand2",
                anchor="w",
                command=command
            )
            btn.pack(fill=tk.X, padx=5, pady=2)
            self.nav_buttons.append(btn)
    
    def create_content_area(self):
        """Create main content area"""
        self.content_frame = tk.Frame(self, bg="white")
        self.content_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)
    
    def clear_content(self):
        """Clear the content area"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def highlight_button(self, active_index):
        """Highlight the active navigation button"""
        for i, btn in enumerate(self.nav_buttons):
            if i == active_index:
                # Active State: Yellow background, Black text
                btn.configure(bg="#FFC107", fg="black")
            else:
                # Inactive State: Dark Maroon background, White text
                btn.configure(bg="#600000", fg="white")
    
    def show_transaction_module(self):
        """Display Transaction Entry module"""
        self.clear_content()
        self.highlight_button(0)
        TransactionModule(self.content_frame, self.db_manager)
    
    def show_inventory_module(self):
        """Display Inventory Management module"""
        self.clear_content()
        self.highlight_button(1)
        InventoryModule(self.content_frame, self.db_manager)
    
    def show_history_module(self):
        """Display Sales History module"""
        self.clear_content()
        self.highlight_button(2)
        HistoryModule(self.content_frame, self.db_manager)
    
    def show_reports_module(self):
        """Display Reports module"""
        self.clear_content()
        self.highlight_button(3)
        ReportsModule(self.content_frame, self.db_manager)
    
    def exit_application(self):
        """Exit the application"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.destroy()


def main():
    """Main entry point"""
    try:
        app = MainApplication()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"Application error: {str(e)}")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()