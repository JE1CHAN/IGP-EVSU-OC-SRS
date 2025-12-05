"""
Inventory Management Module
Handles product inventory, stock tracking, and product management
"""

import tkinter as tk
from tkinter import ttk, messagebox


class InventoryModule:
    """Inventory management interface"""
    
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db = db_manager
        self.selected_item = None
        
        # Create main frame
        self.main_frame = tk.Frame(parent, bg="white")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.create_ui()
        self.load_inventory()
    
    def create_ui(self):
        """Create inventory management interface"""
        # Title
        title_label = tk.Label(
            self.main_frame,
            text="📦 INVENTORY MANAGEMENT",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#800000"  # Maroon
        )
        title_label.pack(pady=(0, 20))
        
        # --- Search Bar Section ---
        search_frame = tk.Frame(self.main_frame, bg="white")
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            search_frame,
            text="Search Product:",
            font=("Arial", 11, "bold"),
            bg="white"
        ).pack(side=tk.LEFT, padx=(5, 5))
        
        self.search_entry = tk.Entry(
            search_frame,
            font=("Arial", 11),
            width=30,
            bd=2,
            relief=tk.GROOVE
        )
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<KeyRelease>", self.filter_inventory)
        
        # --- Controls Frame ---
        controls_frame = tk.Frame(self.main_frame, bg="white")
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Add Product button (Yellow)
        add_btn = tk.Button(
            controls_frame,
            text="➕ Add New Product",
            font=("Arial", 11, "bold"),
            bg="#FFC107",  # Yellow
            fg="black",    # Black text
            padx=15,
            pady=10,
            cursor="hand2",
            command=self.show_add_dialog
        )
        add_btn.pack(side=tk.LEFT, padx=5)

        # Add Stock button (Green)
        add_stock_btn = tk.Button(
            controls_frame,
            text="📈 Add Stock",
            font=("Arial", 11, "bold"),
            bg="#27ae60",  # Green
            fg="white",    # White text
            padx=15,
            pady=10,
            cursor="hand2",
            command=self.show_add_stock_dialog
        )
        add_stock_btn.pack(side=tk.LEFT, padx=5)
        
        # Update Product button (Maroon)
        update_btn = tk.Button(
            controls_frame,
            text="✏️ Update Product",
            font=("Arial", 11, "bold"),
            bg="#800000",  # Maroon
            fg="white",    # White text
            padx=15,
            pady=10,
            cursor="hand2",
            command=self.show_update_dialog
        )
        update_btn.pack(side=tk.LEFT, padx=5)
        
        # Delete Product button (Danger - Dark Red)
        delete_btn = tk.Button(
            controls_frame,
            text="🗑️ Delete Product",
            font=("Arial", 11, "bold"),
            bg="#c0392b",  # Dark Red
            fg="white",
            padx=15,
            pady=10,
            cursor="hand2",
            command=self.delete_product
        )
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Refresh button (Neutral - Gray)
        refresh_btn = tk.Button(
            controls_frame,
            text="🔄 Refresh",
            font=("Arial", 11, "bold"),
            bg="#95a5a6",
            fg="white",
            padx=15,
            pady=10,
            cursor="hand2",
            command=self.load_inventory
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Table frame
        table_frame = tk.Frame(self.main_frame, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create Treeview
        columns = ("Product Name", "Size", "Batch", "Stock", "Price")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15
        )
        
        # Define column headings
        self.tree.heading("Product Name", text="Product Name")
        self.tree.heading("Size", text="Size")
        self.tree.heading("Batch", text="Batch")
        self.tree.heading("Stock", text="Available Stock")
        self.tree.heading("Price", text="Price (₱)")
        
        # Define column widths
        self.tree.column("Product Name", width=350, anchor="w")
        self.tree.column("Size", width=100, anchor="center")
        self.tree.column("Batch", width=120, anchor="center")
        self.tree.column("Stock", width=120, anchor="center")
        self.tree.column("Price", width=120, anchor="e")
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Pack tree and scrollbars
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        # Configure tags for low stock warning
        self.tree.tag_configure("low_stock", background="#ffe6e6")
        self.tree.tag_configure("out_of_stock", background="#ffcccc", foreground="#e74c3c")
    
    def load_inventory(self):
        """Load inventory data into table"""
        # Clear search box when reloading full inventory
        if hasattr(self, 'search_entry'):
             self.search_entry.delete(0, tk.END)

        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load from database
        inventory = self.db.get_all_inventory()
        self.populate_tree(inventory)

    def filter_inventory(self, event=None):
        """Filter inventory based on search text"""
        search_text = self.search_entry.get().lower()
        
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Get all inventory from DB
        all_inventory = self.db.get_all_inventory()
        
        # Filter in memory
        filtered_items = []
        for item in all_inventory:
            # item structure: (item_id, product_name, size, stock, price)
            prod_name = str(item[1]).lower()
            if search_text in prod_name:
                filtered_items.append(item)
                
        self.populate_tree(filtered_items)

    def populate_tree(self, inventory_list):
        """Helper to insert items into treeview"""
        for item in inventory_list:
            # item structure: (item_id, product_name, size, batch, stock, price)
            item_id, product_name, size, batch, stock, price = item
            
            # Format price
            price_str = f"₱{price:,.2f}"
            
            # Determine tag based on stock level
            tag = ""
            if stock == 0:
                tag = "out_of_stock"
            elif stock < 10:
                tag = "low_stock"
            
            # Insert into tree - skip item_id from display
            self.tree.insert(
                "",
                tk.END,
                values=(product_name, size, batch, stock, price_str),
                tags=(tag,) if tag else ()
            )
    
    def on_select(self, event):
        """Handle tree selection"""
        selection = self.tree.selection()
        if selection:
            self.selected_item = self.tree.item(selection[0])['values']
    
    def show_add_stock_dialog(self):
        """Show dialog to quickly add stock to existing product"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add Stock")
        dialog.geometry("400x350")
        dialog.resizable(False, False)
        dialog.configure(bg="white")
        
        dialog.transient(self.parent)
        dialog.grab_set()
        
        tk.Label(
            dialog,
            text="Add Stock",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#27ae60"  # Green
        ).pack(pady=15)
        
        form_frame = tk.Frame(dialog, bg="white")
        form_frame.pack(pady=10)
        
        # 1. Product Dropdown
        tk.Label(form_frame, text="Product:", font=("Arial", 11, "bold"), bg="white").grid(row=0, column=0, sticky="w", pady=10, padx=10)
        
        product_combo = ttk.Combobox(form_frame, font=("Arial", 11), width=23, state="readonly")
        product_combo.grid(row=0, column=1, pady=10, padx=10)
        
        # Populate Products
        products = self.db.get_unique_products()
        product_combo['values'] = products
        
        # 2. Size Dropdown
        tk.Label(form_frame, text="Size:", font=("Arial", 11, "bold"), bg="white").grid(row=1, column=0, sticky="w", pady=10, padx=10)
        
        size_combo = ttk.Combobox(form_frame, font=("Arial", 11), width=23, state="readonly")
        size_combo.grid(row=1, column=1, pady=10, padx=10)
        
        # Event: When product selected, load sizes
        def on_product_change(event):
            selected_prod = product_combo.get()
            if selected_prod:
                sizes = self.db.get_sizes_for_product(selected_prod)
                size_combo['values'] = sizes
                size_combo.set('')
        
        product_combo.bind("<<ComboboxSelected>>", on_product_change)
        
        # 3. Quantity Entry
        tk.Label(form_frame, text="Quantity to Add:", font=("Arial", 11, "bold"), bg="white").grid(row=2, column=0, sticky="w", pady=10, padx=10)
        
        qty_entry = tk.Entry(form_frame, font=("Arial", 11), width=25)
        qty_entry.grid(row=2, column=1, pady=10, padx=10)
        
        # Logic to Save
        def save_stock():
            prod = product_combo.get()
            size = size_combo.get()
            qty_str = qty_entry.get().strip()
            
            if not prod or not size:
                messagebox.showerror("Error", "Please select a product and size")
                return
            
            try:
                qty = int(qty_str)
                if qty <= 0:
                    messagebox.showerror("Error", "Quantity must be positive")
                    return
                    
                # Update Database
                if self.db.update_stock(prod, size, qty):
                    messagebox.showinfo("Success", f"Added {qty} stock to {prod} ({size})")
                    dialog.destroy()
                    self.load_inventory()
                else:
                    messagebox.showerror("Error", "Failed to update stock")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")

        # Buttons
        btn_frame = tk.Frame(dialog, bg="white")
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame,
            text="💾 Add Stock",
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2",
            command=save_stock
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            btn_frame,
            text="❌ Cancel",
            font=("Arial", 11, "bold"),
            bg="#95a5a6",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2",
            command=dialog.destroy
        ).pack(side=tk.LEFT, padx=10)

    def show_add_dialog(self):
        """Show dialog to add new product"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add New Product")
        dialog.geometry("450x400")
        dialog.resizable(False, False)
        dialog.configure(bg="white")
        
        # Center dialog
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Title
        tk.Label(
            dialog,
            text="Add New Product",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#800000"  # Maroon
        ).pack(pady=15)
        
        # Form frame
        form_frame = tk.Frame(dialog, bg="white")
        form_frame.pack(pady=10)
        
        # Product Name
        tk.Label(
            form_frame,
            text="Product Name:",
            font=("Arial", 11, "bold"),
            bg="white"
        ).grid(row=0, column=0, sticky="w", pady=10, padx=10)
        
        product_entry = tk.Entry(form_frame, font=("Arial", 11), width=25)
        product_entry.grid(row=0, column=1, pady=10, padx=10)
        
        # Size
        tk.Label(
            form_frame,
            text="Size:",
            font=("Arial", 11, "bold"),
            bg="white"
        ).grid(row=1, column=0, sticky="w", pady=10, padx=10)
        
        size_entry = tk.Entry(form_frame, font=("Arial", 11), width=25)
        size_entry.grid(row=1, column=1, pady=10, padx=10)
        
        # Batch
        tk.Label(
            form_frame,
            text="Batch:",
            font=("Arial", 11, "bold"),
            bg="white"
        ).grid(row=2, column=0, sticky="w", pady=10, padx=10)
        
        batch_entry = tk.Entry(form_frame, font=("Arial", 11), width=25)
        batch_entry.grid(row=2, column=1, pady=10, padx=10)
        
        # Initial Stock
        tk.Label(
            form_frame,
            text="Initial Stock:",
            font=("Arial", 11, "bold"),
            bg="white"
        ).grid(row=3, column=0, sticky="w", pady=10, padx=10)
        
        stock_entry = tk.Entry(form_frame, font=("Arial", 11), width=25)
        stock_entry.grid(row=3, column=1, pady=10, padx=10)
        
        # Price
        tk.Label(
            form_frame,
            text="Price (₱):",
            font=("Arial", 11, "bold"),
            bg="white"
        ).grid(row=4, column=0, sticky="w", pady=10, padx=10)
        
        price_entry = tk.Entry(form_frame, font=("Arial", 11), width=25)
        price_entry.grid(row=4, column=1, pady=10, padx=10)
        
        # Button frame
        btn_frame = tk.Frame(dialog, bg="white")
        btn_frame.pack(pady=20)
        
        def save_product():
            """Validate and save product"""
            product = product_entry.get().strip()
            size = size_entry.get().strip()
            batch = batch_entry.get().strip()

            try:
                stock = int(stock_entry.get())
                price = float(price_entry.get())
                
                if not product or not size:
                    messagebox.showerror("Error", "Please fill all fields")
                    return
                
                if stock < 0 or price < 0:
                    messagebox.showerror("Error", "Stock and price must be positive")
                    return
                
                # Check if product already exists
                existing = self.db.get_product_by_name_size(product, size)
                if existing:
                    messagebox.showerror(
                        "Error",
                        f"Product '{product}' with size '{size}' already exists"
                    )
                    return
                
                # Save to database
                if self.db.add_product(product, size, stock, price, batch):
                    messagebox.showinfo("Success", "Product added successfully!")
                    dialog.destroy()
                    self.load_inventory()
                else:
                    messagebox.showerror("Error", "Failed to add product")
            
            except ValueError:
                messagebox.showerror("Error", "Invalid stock or price value")
        
        # Save button (Yellow)
        tk.Button(
            btn_frame,
            text="💾 Save",
            font=("Arial", 11, "bold"),
            bg="#FFC107",  # Yellow
            fg="black",    # Black
            padx=30,
            pady=10,
            cursor="hand2",
            command=save_product
        ).pack(side=tk.LEFT, padx=10)
        
        # Cancel button (Gray)
        tk.Button(
            btn_frame,
            text="❌ Cancel",
            font=("Arial", 11, "bold"),
            bg="#95a5a6",
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2",
            command=dialog.destroy
        ).pack(side=tk.LEFT, padx=10)
    
    def show_update_dialog(self):
        """Show dialog to update selected product"""
        if not self.selected_item:
            messagebox.showwarning("Warning", "Please select a product to update")
            return
        
        item_id, product_name, size, batch_val, stock, price_str = self.selected_item
        price = float(price_str.replace('₱', '').replace(',', ''))
        
        dialog = tk.Toplevel(self.parent)
        dialog.title("Update Product")
        dialog.geometry("450x400")
        dialog.resizable(False, False)
        dialog.configure(bg="white")
        
        # Center dialog
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Title
        tk.Label(
            dialog,
            text="Update Product",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#800000"  # Maroon
        ).pack(pady=15)
        
        # Form frame
        form_frame = tk.Frame(dialog, bg="white")
        form_frame.pack(pady=10)
        
        # Product Name
        tk.Label(
            form_frame,
            text="Product Name:",
            font=("Arial", 11, "bold"),
            bg="white"
        ).grid(row=0, column=0, sticky="w", pady=10, padx=10)
        
        product_entry = tk.Entry(form_frame, font=("Arial", 11), width=25)
        product_entry.grid(row=0, column=1, pady=10, padx=10)
        product_entry.insert(0, product_name)
        
        # Size
        tk.Label(
            form_frame,
            text="Size:",
            font=("Arial", 11, "bold"),
            bg="white"
        ).grid(row=1, column=0, sticky="w", pady=10, padx=10)
        
        size_entry = tk.Entry(form_frame, font=("Arial", 11), width=25)
        size_entry.grid(row=1, column=1, pady=10, padx=10)
        size_entry.insert(0, size)
        
        # Batch
        tk.Label(
            form_frame,
            text="Batch:",
            font=("Arial", 11, "bold"),
            bg="white"
        ).grid(row=2, column=0, sticky="w", pady=10, padx=10)
        batch_entry = tk.Entry(form_frame, font=("Arial", 11), width=25)
        batch_entry.grid(row=2, column=1, pady=10, padx=10)
        batch_entry.insert(0, batch_val)
        
        # Stock
        tk.Label(
            form_frame,
            text="Stock:",
            font=("Arial", 11, "bold"),
            bg="white"
        ).grid(row=3, column=0, sticky="w", pady=10, padx=10)
        
        stock_entry = tk.Entry(form_frame, font=("Arial", 11), width=25)
        stock_entry.grid(row=3, column=1, pady=10, padx=10)
        stock_entry.insert(0, str(stock))
        
        # Price
        tk.Label(
            form_frame,
            text="Price (₱):",
            font=("Arial", 11, "bold"),
            bg="white"
        ).grid(row=4, column=0, sticky="w", pady=10, padx=10)
        
        price_entry = tk.Entry(form_frame, font=("Arial", 11), width=25)
        price_entry.grid(row=4, column=1, pady=10, padx=10)
        price_entry.insert(0, str(price))
        
        # Button frame
        btn_frame = tk.Frame(dialog, bg="white")
        btn_frame.pack(pady=20)
        
        def update_product():
            """Validate and update product"""
            product = product_entry.get().strip()
            size_val = size_entry.get().strip()
            batch_val_new = batch_entry.get().strip()

            try:
                stock_val = int(stock_entry.get())
                price_val = float(price_entry.get())
                
                if not product or not size_val:
                    messagebox.showerror("Error", "Please fill all fields")
                    return
                
                if stock_val < 0 or price_val < 0:
                    messagebox.showerror("Error", "Stock and price must be positive")
                    return
                
                # Update in database
                if self.db.update_product(item_id, product, size_val, stock_val, price_val, batch_val_new):
                    messagebox.showinfo("Success", "Product updated successfully!")
                    dialog.destroy()
                    self.load_inventory()
                else:
                    messagebox.showerror("Error", "Failed to update product")
            
            except ValueError:
                messagebox.showerror("Error", "Invalid stock or price value")
        
        # Update button (Yellow)
        tk.Button(
            btn_frame,
            text="💾 Update",
            font=("Arial", 11, "bold"),
            bg="#FFC107",  # Yellow
            fg="black",    # Black
            padx=30,
            pady=10,
            cursor="hand2",
            command=update_product
        ).pack(side=tk.LEFT, padx=10)
        
        # Cancel button (Gray)
        tk.Button(
            btn_frame,
            text="❌ Cancel",
            font=("Arial", 11, "bold"),
            bg="#95a5a6",
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2",
            command=dialog.destroy
        ).pack(side=tk.LEFT, padx=10)
    
    def delete_product(self):
        """Delete selected product"""
        if not self.selected_item:
            messagebox.showwarning("Warning", "Please select a product to delete")
            return
        
        item_id = self.selected_item[0]
        product_name = self.selected_item[1]
        size = self.selected_item[2]
        
        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete:\n{product_name} ({size})?"
        )
        
        if confirm:
            if self.db.delete_product(item_id):
                messagebox.showinfo("Success", "Product deleted successfully!")
                self.load_inventory()
                self.selected_item = None
            else:
                messagebox.showerror("Error", "Failed to delete product")