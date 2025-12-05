"""
Transaction Entry Module
Handles recording of sales transactions with validation and stock management
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry


class TransactionModule:
    """Transaction entry form with validation"""
    
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db = db_manager
        
        # Create main frame
        self.main_frame = tk.Frame(parent, bg="white")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.create_ui()
    
    def create_ui(self):
        """Create transaction entry interface"""
        # Title
        title_label = tk.Label(
            self.main_frame,
            text="📝 TRANSACTION ENTRY",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#800000"  # Maroon
        )
        title_label.pack(pady=(0, 20))
        
        # Form frame
        form_frame = tk.Frame(self.main_frame, bg="white")
        form_frame.pack(pady=10)
        
        # --- Row 0: Buyer Name ---
        tk.Label(
            form_frame,
            text="Buyer Name:",
            font=("Arial", 12, "bold"),
            bg="white"
        ).grid(row=0, column=0, sticky="w", pady=10, padx=10)
        
        self.buyer_name_entry = tk.Entry(
            form_frame,
            font=("Arial", 12),
            width=35
        )
        self.buyer_name_entry.grid(row=0, column=1, pady=10, padx=10)
        
        # --- Row 1: Program/Course (NEW) ---
        tk.Label(
            form_frame,
            text="Program/Course:",
            font=("Arial", 12, "bold"),
            bg="white"
        ).grid(row=1, column=0, sticky="w", pady=10, padx=10)
        
        self.course_combo = ttk.Combobox(
            form_frame,
            font=("Arial", 12),
            width=33,
            state="readonly"
        )
        self.course_combo.grid(row=1, column=1, pady=10, padx=10)
        
        # Cleaned list based on your input
        course_list = [
            "BSIT",
            "BEED",
            "BSEd (Math)",
            "BSEd (Science)",
            "BPEd",
            "BTVTEd",
            "DTS",
            "BSHM",
            "BSCE ",
            "BSEE",
            "BSME",
            "BIT (Culinary Arts)",
            "BIT (Electronics)",   
        ]
        self.course_combo['values'] = sorted(course_list)
        
        # --- Row 2: Product ---
        tk.Label(
            form_frame,
            text="Product:",
            font=("Arial", 12, "bold"),
            bg="white"
        ).grid(row=2, column=0, sticky="w", pady=10, padx=10)
        
        self.product_combo = ttk.Combobox(
            form_frame,
            font=("Arial", 12),
            width=33,
            state="readonly"
        )
        self.product_combo.grid(row=2, column=1, pady=10, padx=10)
        self.product_combo.bind("<<ComboboxSelected>>", self.on_product_selected)
        
        # --- Row 3: Size ---
        tk.Label(
            form_frame,
            text="Size:",
            font=("Arial", 12, "bold"),
            bg="white"
        ).grid(row=3, column=0, sticky="w", pady=10, padx=10)
        
        self.size_combo = ttk.Combobox(
            form_frame,
            font=("Arial", 12),
            width=33,
            state="readonly"
        )
        self.size_combo.grid(row=3, column=1, pady=10, padx=10)
        self.size_combo.bind("<<ComboboxSelected>>", self.on_size_selected)
        
        # Available Stock Display
        self.stock_label = tk.Label(
            form_frame,
            text="Available Stock: --",
            font=("Arial", 11, "italic"),
            bg="white",
            fg="#e74c3c"
        )
        self.stock_label.grid(row=4, column=1, pady=0, padx=0)
        
        # --- Row 5: Quantity ---
        tk.Label(
            form_frame,
            text="Quantity:",
            font=("Arial", 12, "bold"),
            bg="white"
        ).grid(row=5, column=0, sticky="w", pady=10, padx=10)
        
        # Spinbox for quantity (only positive integers)
        vcmd = (form_frame.register(self._validate_positive_int), '%P')
        self.quantity_entry = tk.Spinbox(
            form_frame,
            from_=1,
            to=999999,
            font=("Arial", 12),
            width=34,
            validate='key',
            validatecommand=vcmd,
            command=self.calculate_amount
        )
        self.quantity_entry.grid(row=5, column=1, pady=10, padx=10)
        # Also recalc when user types directly
        self.quantity_entry.bind("<KeyRelease>", self.calculate_amount)
        
        # --- Row 6: Price ---
        tk.Label(
            form_frame,
            text="Price per Unit:",
            font=("Arial", 12, "bold"),
            bg="white"
        ).grid(row=6, column=0, sticky="w", pady=10, padx=10)
        
        self.price_entry = tk.Entry(
            form_frame,
            font=("Arial", 12),
            width=35,
            state="readonly"
        )
        self.price_entry.grid(row=6, column=1, pady=10, padx=10)
        
        # --- Row 7: Total Amount ---
        tk.Label(
            form_frame,
            text="Total Amount:",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#800000"
        ).grid(row=7, column=0, sticky="w", pady=10, padx=10)
        
        self.amount_entry = tk.Entry(
            form_frame,
            font=("Arial", 14, "bold"),
            width=35,
            state="readonly",
            fg="#800000"
        )
        self.amount_entry.grid(row=7, column=1, pady=10, padx=10)
        
        # --- Row 8: OR Number ---
        tk.Label(
            form_frame,
            text="OR Number:",
            font=("Arial", 12, "bold"),
            bg="white"
        ).grid(row=8, column=0, sticky="w", pady=10, padx=10)
        
        self.or_number_entry = tk.Entry(
            form_frame,
            font=("Arial", 12),
            width=35
        )
        self.or_number_entry.grid(row=8, column=1, pady=10, padx=10)
        
        # --- Row 9: Date ---
        # Date (Calendar Picker)
        tk.Label(
            form_frame,
            text="Date:",
            font=("Arial", 12, "bold"),
            bg="white"
        ).grid(row=9, column=0, sticky="w", pady=10, padx=10)

        self.date_entry = DateEntry(
            form_frame,
            font=("Arial", 12),
            width=33,
            background="maroon",
            foreground="white",
            borderwidth=2,
            date_pattern="yyyy-mm-dd",
            showweeknumbers=False
        )
        self.date_entry.grid(row=9, column=1, pady=10, padx=10)
        
        # Buttons frame
        button_frame = tk.Frame(self.main_frame, bg="white")
        button_frame.pack(pady=20)
        
        # Save button
        save_btn = tk.Button(
            button_frame,
            text="💾 SAVE TRANSACTION",
            font=("Arial", 13, "bold"),
            bg="#FFC107",  # Yellow
            fg="black",
            padx=30,
            pady=15,
            cursor="hand2",
            command=self.save_transaction
        )
        save_btn.pack(side=tk.LEFT, padx=10)
        
        # Clear button
        clear_btn = tk.Button(
            button_frame,
            text="🔄 CLEAR FORM",
            font=("Arial", 13, "bold"),
            bg="#800000",  # Maroon
            fg="white",
            padx=30,
            pady=15,
            cursor="hand2",
            command=self.clear_form
        )
        clear_btn.pack(side=tk.LEFT, padx=10)
        
        # Load products
        self.load_products()
    
    def load_products(self):
        """Load available products from database"""
        products = self.db.get_unique_products()
        self.product_combo['values'] = products
        
        if not products:
            messagebox.showwarning(
                "No Products",
                "No products found in inventory. Please add products first."
            )
    
    def on_product_selected(self, event=None):
        """Handle product selection"""
        product = self.product_combo.get()
        if product:
            sizes = self.db.get_sizes_for_product(product)
            self.size_combo['values'] = sizes
            self.size_combo.set('')
            self.stock_label.config(text="Available Stock: --")
            self.price_entry.config(state="normal")
            self.price_entry.delete(0, tk.END)
            self.price_entry.config(state="readonly")
            self.amount_entry.config(state="normal")
            self.amount_entry.delete(0, tk.END)
            self.amount_entry.config(state="readonly")
    
    def on_size_selected(self, event=None):
        """Handle size selection and display stock"""
        product = self.product_combo.get()
        size = self.size_combo.get()
        
        if product and size:
            # Get product details
            product_data = self.db.get_product_by_name_size(product, size)
            
            if product_data:
                # product_data: (item_id, product_name, size, batch, stock, price)
                item_id, prod_name, prod_size, batch, stock, price = product_data
                
                # Update stock label
                stock_color = "#27ae60" if stock > 10 else "#e74c3c"
                self.stock_label.config(
                    text=f"Available Stock: {stock}",
                    fg=stock_color
                )
                
                # Update price
                self.price_entry.config(state="normal")
                self.price_entry.delete(0, tk.END)
                self.price_entry.insert(0, f"₱{price:.2f}")
                self.price_entry.config(state="readonly")

                # Set initial quantity to 1
                self.quantity_entry.delete(0, tk.END)
                self.quantity_entry.insert(0, "1")
                
                # Calculate amount if quantity is already entered
                self.calculate_amount()
    
    def calculate_amount(self, event=None):
        """Calculate total amount based on quantity and price"""
        try:
            quantity_text = self.quantity_entry.get()
            if quantity_text == "":
                raise ValueError()
            quantity = int(quantity_text)
            price_text = self.price_entry.get().replace('₱', '').replace(',', '')
            
            if price_text:
                price = float(price_text)
                total = quantity * price
                
                self.amount_entry.config(state="normal")
                self.amount_entry.delete(0, tk.END)
                self.amount_entry.insert(0, f"₱{total:,.2f}")
                self.amount_entry.config(state="readonly")
        except ValueError:
            self.amount_entry.config(state="normal")
            self.amount_entry.delete(0, tk.END)
            self.amount_entry.config(state="readonly")

    def _validate_positive_int(self, proposed: str) -> bool:
        """Validate that the Spinbox input is a positive integer or empty during edit."""
        if proposed == "":
            return True
        if proposed.isdigit():
            try:
                return int(proposed) > 0
            except Exception:
                return False
        return False
    
    def validate_form(self):
        """Validate all form fields"""
        # Check buyer name
        if not self.buyer_name_entry.get().strip():
            messagebox.showerror("Validation Error", "Please enter buyer name")
            self.buyer_name_entry.focus()
            return False
        
        # Check course/program (Optional but good to have)
        if not self.course_combo.get().strip():
            messagebox.showerror("Validation Error", "Please select a Program/Course")
            return False

        # Check product
        if not self.product_combo.get():
            messagebox.showerror("Validation Error", "Please select a product")
            return False
        
        # Check size
        if not self.size_combo.get():
            messagebox.showerror("Validation Error", "Please select a size")
            return False
        
        # Check quantity
        try:
            quantity = int(self.quantity_entry.get())
            if quantity <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Validation Error", "Please enter a valid quantity")
            self.quantity_entry.focus()
            return False
        
        # Check stock availability
        product = self.product_combo.get()
        size = self.size_combo.get()
        available_stock = self.db.get_available_stock(product, size)
        
        if quantity > available_stock:
            messagebox.showerror(
                "Insufficient Stock",
                f"Only {available_stock} items available in stock"
            )
            return False
        
        # Check OR number
        if not self.or_number_entry.get().strip():
            messagebox.showerror("Validation Error", "Please enter OR number")
            self.or_number_entry.focus()
            return False
        
        # Check date
        try:
            date_str = self.date_entry.get()
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror(
                "Validation Error",
                "Please enter a valid date (YYYY-MM-DD)"
            )
            self.date_entry.focus()
            return False
        
        return True
    
    def save_transaction(self):
        """Save transaction to database"""
        if not self.validate_form():
            return
        
        try:
            # Get form data
            buyer_name = self.buyer_name_entry.get().strip()
            program_course = self.course_combo.get().strip() # Get course
            product = self.product_combo.get()
            size = self.size_combo.get()
            quantity = int(self.quantity_entry.get())
            amount = float(self.amount_entry.get().replace('₱', '').replace(',', ''))
            or_number = self.or_number_entry.get().strip()
            date = self.date_entry.get()
            
            # Save to database (Pass program_course)
            success = self.db.add_transaction(
                buyer_name, product, size, quantity, amount, or_number, date, program_course
            )
            
            if success:
                messagebox.showinfo(
                    "Success",
                    "Transaction saved successfully!"
                )
                self.clear_form()
            else:
                messagebox.showerror(
                    "Error",
                    "Failed to save transaction. Please try again."
                )
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def clear_form(self):
        """Clear all form fields"""
        self.buyer_name_entry.delete(0, tk.END)
        self.course_combo.set('') # Clear course
        self.product_combo.set('')
        self.size_combo.set('')
        self.size_combo['values'] = []
        # Reset quantity to default 1
        try:
            self.quantity_entry.delete(0, tk.END)
        except Exception:
            pass
        self.quantity_entry.insert(0, "1")
        self.price_entry.config(state="normal")
        self.price_entry.delete(0, tk.END)
        self.price_entry.config(state="readonly")
        self.amount_entry.config(state="normal")
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.config(state="readonly")
        self.or_number_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.stock_label.config(text="Available Stock: --")
        self.buyer_name_entry.focus()