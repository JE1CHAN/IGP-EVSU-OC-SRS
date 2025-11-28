"""
Sales History Module
View and search all transaction history with filters
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class HistoryModule:
    """Sales history viewer with search and filter capabilities"""
    
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db = db_manager
        
        # Create main frame
        self.main_frame = tk.Frame(parent, bg="white")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.create_ui()
        self.load_all_transactions()
    
    def create_ui(self):
        """Create sales history interface"""
        # Title
        title_label = tk.Label(
            self.main_frame,
            text="📊 SALES HISTORY",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#800000"  # Maroon
        )
        title_label.pack(pady=(0, 20))
        
        # Search frame
        search_frame = tk.LabelFrame(
            self.main_frame,
            text="Search & Filter",
            font=("Arial", 11, "bold"),
            bg="white",
            padx=15,
            pady=15
        )
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # First row of filters
        row1 = tk.Frame(search_frame, bg="white")
        row1.pack(fill=tk.X, pady=5)
        
        # Buyer Name search
        tk.Label(
            row1,
            text="Buyer Name:",
            font=("Arial", 10),
            bg="white"
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.buyer_search = tk.Entry(row1, font=("Arial", 10), width=20)
        self.buyer_search.pack(side=tk.LEFT, padx=5)
        
        # Product Name search
        tk.Label(
            row1,
            text="Product:",
            font=("Arial", 10),
            bg="white"
        ).pack(side=tk.LEFT, padx=(15, 5))
        
        self.product_search = tk.Entry(row1, font=("Arial", 10), width=20)
        self.product_search.pack(side=tk.LEFT, padx=5)
        
        # OR Number search
        tk.Label(
            row1,
            text="OR Number:",
            font=("Arial", 10),
            bg="white"
        ).pack(side=tk.LEFT, padx=(15, 5))
        
        self.or_search = tk.Entry(row1, font=("Arial", 10), width=15)
        self.or_search.pack(side=tk.LEFT, padx=5)
        
        # Second row - date filters
        row2 = tk.Frame(search_frame, bg="white")
        row2.pack(fill=tk.X, pady=10)
        
        # Start Date
        tk.Label(
            row2,
            text="From Date:",
            font=("Arial", 10),
            bg="white"
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.start_date = tk.Entry(row2, font=("Arial", 10), width=12)
        self.start_date.pack(side=tk.LEFT, padx=5)
        
        # End Date
        tk.Label(
            row2,
            text="To Date:",
            font=("Arial", 10),
            bg="white"
        ).pack(side=tk.LEFT, padx=(15, 5))
        
        self.end_date = tk.Entry(row2, font=("Arial", 10), width=12)
        self.end_date.pack(side=tk.LEFT, padx=5)
        
        # Search button (Yellow)
        search_btn = tk.Button(
            row2,
            text="🔍 Search",
            font=("Arial", 10, "bold"),
            bg="#FFC107",  # Yellow
            fg="black",    # Black
            padx=20,
            pady=5,
            cursor="hand2",
            command=self.search_transactions
        )
        search_btn.pack(side=tk.LEFT, padx=15)
        
        # Clear button (Maroon)
        clear_btn = tk.Button(
            row2,
            text="🔄 Clear Filters",
            font=("Arial", 10, "bold"),
            bg="#800000",  # Maroon
            fg="white",    # White
            padx=20,
            pady=5,
            cursor="hand2",
            command=self.clear_filters
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Stats frame (Light Yellow for visibility)
        stats_frame = tk.Frame(self.main_frame, bg="#fdf2ce", relief=tk.RIDGE, bd=2)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.stats_label = tk.Label(
            stats_frame,
            text="Total Transactions: 0 | Total Revenue: ₱0.00",
            font=("Arial", 11, "bold"),
            bg="#fdf2ce",
            fg="#800000", # Maroon text
            pady=10
        )
        self.stats_label.pack()
        
        # Table frame
        table_frame = tk.Frame(self.main_frame, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create Treeview
        columns = ("ID", "Buyer", "Product", "Size", "Qty", "Amount", "OR#", "Date")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15
        )
        
        # Define column headings
        self.tree.heading("ID", text="ID")
        self.tree.heading("Buyer", text="Buyer Name")
        self.tree.heading("Product", text="Product")
        self.tree.heading("Size", text="Size")
        self.tree.heading("Qty", text="Qty")
        self.tree.heading("Amount", text="Amount (₱)")
        self.tree.heading("OR#", text="OR Number")
        self.tree.heading("Date", text="Date")
        
        # Define column widths
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Buyer", width=180, anchor="w")
        self.tree.column("Product", width=180, anchor="w")
        self.tree.column("Size", width=70, anchor="center")
        self.tree.column("Qty", width=60, anchor="center")
        self.tree.column("Amount", width=120, anchor="e")
        self.tree.column("OR#", width=120, anchor="center")
        self.tree.column("Date", width=100, anchor="center")
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Pack tree and scrollbars
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
    
    def load_all_transactions(self):
        """Load all transactions"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load from database
        transactions = self.db.get_all_transactions()
        
        total_revenue = 0
        
        for trans in transactions:
            trans_id, buyer, product, size, qty, amount, or_num, date = trans
            
            # Format amount
            amount_str = f"₱{amount:,.2f}"
            total_revenue += amount
            
            # Insert into tree
            self.tree.insert(
                "",
                tk.END,
                values=(trans_id, buyer, product, size, qty, amount_str, or_num, date)
            )
        
        # Update stats
        self.stats_label.config(
            text=f"Total Transactions: {len(transactions)} | Total Revenue: ₱{total_revenue:,.2f}"
        )
    
    def search_transactions(self):
        """Search transactions based on filters"""
        # Get filter values
        buyer = self.buyer_search.get().strip()
        product = self.product_search.get().strip()
        or_num = self.or_search.get().strip()
        start = self.start_date.get().strip()
        end = self.end_date.get().strip()
        
        # Validate dates
        if start:
            try:
                datetime.strptime(start, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror(
                    "Invalid Date",
                    "Start date must be in format: YYYY-MM-DD"
                )
                return
        
        if end:
            try:
                datetime.strptime(end, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror(
                    "Invalid Date",
                    "End date must be in format: YYYY-MM-DD"
                )
                return
        
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Search in database
        transactions = self.db.search_transactions(
            buyer_name=buyer if buyer else None,
            product_name=product if product else None,
            or_number=or_num if or_num else None,
            start_date=start if start else None,
            end_date=end if end else None
        )
        
        total_revenue = 0
        
        for trans in transactions:
            trans_id, buyer, product, size, qty, amount, or_num, date = trans
            
            # Format amount
            amount_str = f"₱{amount:,.2f}"
            total_revenue += amount
            
            # Insert into tree
            self.tree.insert(
                "",
                tk.END,
                values=(trans_id, buyer, product, size, qty, amount_str, or_num, date)
            )
        
        # Update stats
        self.stats_label.config(
            text=f"Total Transactions: {len(transactions)} | Total Revenue: ₱{total_revenue:,.2f}"
        )
        
        if len(transactions) == 0:
            messagebox.showinfo("No Results", "No transactions found matching your criteria")
    
    def clear_filters(self):
        """Clear all filters and reload all transactions"""
        self.buyer_search.delete(0, tk.END)
        self.product_search.delete(0, tk.END)
        self.or_search.delete(0, tk.END)
        self.start_date.delete(0, tk.END)
        self.end_date.delete(0, tk.END)
        self.load_all_transactions()