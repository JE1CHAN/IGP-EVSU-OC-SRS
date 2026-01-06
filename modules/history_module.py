"""
Sales History Module
View and search all transaction history with filters
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry


import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry


class HistoryModule:
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db = db_manager

        self.main_frame = tk.Frame(parent, bg="white")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.create_ui()
        self.load_all_transactions()

    def create_ui(self):
        title_label = tk.Label(
            self.main_frame,
            text="📊 SALES HISTORY",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#800000"
        )
        title_label.pack(pady=(0, 20))

        search_frame = tk.LabelFrame(
            self.main_frame,
            text="Search & Filter",
            font=("Arial", 11, "bold"),
            bg="white",
            padx=15,
            pady=15
        )
        search_frame.pack(fill=tk.X, pady=(0, 10))

        row1 = tk.Frame(search_frame, bg="white")
        row1.pack(fill=tk.X, pady=5)

        tk.Label(row1, text="Buyer Name:", font=("Arial", 10), bg="white").pack(side=tk.LEFT, padx=(0, 5))
        self.buyer_search = tk.Entry(row1, font=("Arial", 10), width=20)
        self.buyer_search.pack(side=tk.LEFT, padx=5)

        tk.Label(row1, text="Product:", font=("Arial", 10), bg="white").pack(side=tk.LEFT, padx=(15, 5))
        self.product_search = tk.Entry(row1, font=("Arial", 10), width=20)
        self.product_search.pack(side=tk.LEFT, padx=5)

        tk.Label(row1, text="OR Number:", font=("Arial", 10), bg="white").pack(side=tk.LEFT, padx=(15, 5))
        self.or_search = tk.Entry(row1, font=("Arial", 10), width=15)
        self.or_search.pack(side=tk.LEFT, padx=5)

        row2 = tk.Frame(search_frame, bg="white")
        row2.pack(fill=tk.X, pady=10)

        tk.Label(row2, text="From Date:", font=("Arial", 10), bg="white").pack(side=tk.LEFT, padx=(0, 5))
        self.start_date = tk.Entry(row2, font=("Arial", 10), width=12)
        self.start_date.pack(side=tk.LEFT, padx=5)

        tk.Label(row2, text="To Date:", font=("Arial", 10), bg="white").pack(side=tk.LEFT, padx=(15, 5))
        self.end_date = tk.Entry(row2, font=("Arial", 10), width=12)
        self.end_date.pack(side=tk.LEFT, padx=5)

        search_btn = tk.Button(
            row2,
            text="🔍 Search",
            font=("Arial", 10, "bold"),
            bg="#FFC107",
            fg="black",
            padx=20,
            pady=5,
            cursor="hand2",
            command=self.search_transactions
        )
        search_btn.pack(side=tk.LEFT, padx=15)

        clear_btn = tk.Button(
            row2,
            text="🔄 Clear Filters",
            font=("Arial", 10, "bold"),
            bg="#800000",
            fg="white",
            padx=20,
            pady=5,
            cursor="hand2",
            command=self.clear_filters
        )
        clear_btn.pack(side=tk.LEFT, padx=5)

        edit_btn = tk.Button(
            row2,
            text="✏️ Edit Transaction",
            font=("Arial", 10, "bold"),
            bg="#27ae60",
            fg="white",
            padx=20,
            pady=5,
            cursor="hand2",
            command=self.edit_transaction
        )
        edit_btn.pack(side=tk.LEFT, padx=5)

        stats_frame = tk.Frame(self.main_frame, bg="#fdf2ce", relief=tk.RIDGE, bd=2)
        stats_frame.pack(fill=tk.X, pady=(0, 10))

        self.stats_label = tk.Label(
            stats_frame,
            text="Total Transactions: 0 | Total Revenue: ₱0.00",
            font=("Arial", 11, "bold"),
            bg="#fdf2ce",
            fg="#800000",
            pady=10
        )
        self.stats_label.pack()

        table_frame = tk.Frame(self.main_frame, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("Buyer", "Product", "Batch", "Size", "Qty", "Amount", "OR#", "Date")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        self.tree.heading("Buyer", text="Buyer Name")
        self.tree.heading("Product", text="Product")
        self.tree.heading("Batch", text="Batch")
        self.tree.heading("Size", text="Size")
        self.tree.heading("Qty", text="Qty")
        self.tree.heading("Amount", text="Amount (₱)")
        self.tree.heading("OR#", text="OR Number")
        self.tree.heading("Date", text="Date")

        self.tree.column("Buyer", width=150, anchor="w")
        self.tree.column("Product", width=150, anchor="w")
        self.tree.column("Batch", width=100, anchor="center")
        self.tree.column("Size", width=70, anchor="center")
        self.tree.column("Qty", width=60, anchor="center")
        self.tree.column("Amount", width=100, anchor="e")
        self.tree.column("OR#", width=100, anchor="center")
        self.tree.column("Date", width=90, anchor="center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

    def load_all_transactions(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        transactions = self.db.get_all_transactions()

        total_revenue = 0

        for trans in transactions:
            trans_id, buyer, product, size, qty, amount, or_num, date = trans

            amount_str = f"₱{amount:,.2f}"
            total_revenue += amount

            prod_data = self.db.get_product_by_name_size(product, size)
            batch = prod_data[3] if prod_data and len(prod_data) > 3 else ''

            self.tree.insert("", tk.END, values=(buyer, product, batch, size, qty, amount_str, or_num, date))

        self.stats_label.config(text=f"Total Transactions: {len(transactions)} | Total Revenue: ₱{total_revenue:,.2f}")

    def search_transactions(self):
        buyer = self.buyer_search.get().strip()
        product = self.product_search.get().strip()
        or_num = self.or_search.get().strip()
        start = self.start_date.get().strip()
        end = self.end_date.get().strip()

        if start:
            try:
                datetime.strptime(start, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid Date", "Start date must be in format: YYYY-MM-DD")
                return

        if end:
            try:
                datetime.strptime(end, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid Date", "End date must be in format: YYYY-MM-DD")
                return

        for item in self.tree.get_children():
            self.tree.delete(item)

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

            amount_str = f"₱{amount:,.2f}"
            total_revenue += amount

            self.tree.insert("", tk.END, values=(trans_id, buyer, product, size, qty, amount_str, or_num, date))

        self.stats_label.config(text=f"Total Transactions: {len(transactions)} | Total Revenue: ₱{total_revenue:,.2f}")

        if len(transactions) == 0:
            messagebox.showinfo("No Results", "No transactions found matching your criteria")

    def clear_filters(self):
        self.buyer_search.delete(0, tk.END)
        self.product_search.delete(0, tk.END)
        self.or_search.delete(0, tk.END)
        self.start_date.delete(0, tk.END)
        self.end_date.delete(0, tk.END)
        self.load_all_transactions()

    def edit_transaction(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a transaction to edit.")
            return

        item_values = self.tree.item(selected_item)['values']
        trans_id = item_values[0]
        curr_buyer = item_values[1]
        curr_prod = item_values[2]
        curr_size = item_values[3]
        curr_qty = item_values[4]
        curr_amount_str = item_values[5]
        curr_or = item_values[6]
        curr_date = item_values[7]

        curr_amount = float(str(curr_amount_str).replace('₱', '').replace(',', ''))

        edit_window = tk.Toplevel(self.parent)
        edit_window.title(f"Edit Transaction #{trans_id}")
        edit_window.geometry("450x550")
        edit_window.configure(bg="white")
        edit_window.transient(self.parent)
        edit_window.grab_set()

        form_frame = tk.Frame(edit_window, bg="white", padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(form_frame, text="Edit Transaction Details", font=("Arial", 14, "bold"), bg="white", fg="#27ae60").pack(pady=(0, 20))

        tk.Label(form_frame, text="Buyer Name:", font=("Arial", 11), bg="white").pack(anchor="w")
        buyer_entry = tk.Entry(form_frame, font=("Arial", 11))
        buyer_entry.pack(fill=tk.X, pady=(0, 10))
        buyer_entry.insert(0, curr_buyer)

        tk.Label(form_frame, text="Product:", font=("Arial", 11), bg="white").pack(anchor="w")
        product_combo = ttk.Combobox(form_frame, font=("Arial", 11), state="readonly")
        product_combo.pack(fill=tk.X, pady=(0, 10))
        product_combo['values'] = self.db.get_unique_products()
        product_combo.set(curr_prod)

        tk.Label(form_frame, text="Size:", font=("Arial", 11), bg="white").pack(anchor="w")
        size_combo = ttk.Combobox(form_frame, font=("Arial", 11), state="readonly")
        size_combo.pack(fill=tk.X, pady=(0, 10))
        size_combo['values'] = self.db.get_sizes_for_product(curr_prod)
        size_combo.set(curr_size)

        def on_prod_change(event):
            p = product_combo.get()
            sizes = self.db.get_sizes_for_product(p)
            size_combo['values'] = sizes
            size_combo.set('')

        product_combo.bind("<<ComboboxSelected>>", on_prod_change)

        tk.Label(form_frame, text="Quantity:", font=("Arial", 11), bg="white").pack(anchor="w")
        qty_entry = tk.Entry(form_frame, font=("Arial", 11))
        qty_entry.pack(fill=tk.X, pady=(0, 10))
        qty_entry.insert(0, str(curr_qty))

        tk.Label(form_frame, text="Total Amount:", font=("Arial", 11), bg="white").pack(anchor="w")
        amount_entry = tk.Entry(form_frame, font=("Arial", 11))
        amount_entry.pack(fill=tk.X, pady=(0, 10))
        amount_entry.insert(0, str(curr_amount))

        def recalc_price():
            p = product_combo.get()
            s = size_combo.get()
            try:
                q = int(qty_entry.get())
                prod_data = self.db.get_product_by_name_size(p, s)
                if prod_data:
                    price = prod_data[5]
                    new_total = price * q
                    amount_entry.delete(0, tk.END)
                    amount_entry.insert(0, f"{new_total:.2f}")
            except:
                pass

        recalc_btn = tk.Button(form_frame, text="🔄 Recalculate Amount", command=recalc_price, bg="#eee", font=("Arial", 9))
        recalc_btn.pack(anchor="e", pady=(0, 10))

        tk.Label(form_frame, text="OR Number:", font=("Arial", 11), bg="white").pack(anchor="w")
        or_entry = tk.Entry(form_frame, font=("Arial", 11))
        or_entry.pack(fill=tk.X, pady=(0, 10))
        or_entry.insert(0, curr_or)

        tk.Label(form_frame, text="Date:", font=("Arial", 11), bg="white").pack(anchor="w")
        date_entry = DateEntry(form_frame, font=("Arial", 11), date_pattern="yyyy-mm-dd")
        date_entry.pack(fill=tk.X, pady=(0, 20))
        date_entry.set_date(curr_date)

        def save_changes():
            new_buyer = buyer_entry.get().strip()
            new_prod = product_combo.get()
            new_size = size_combo.get()
            new_or = or_entry.get().strip()
            new_date = date_entry.get()

            if not new_buyer or not new_prod or not new_size or not new_or:
                messagebox.showerror("Error", "All fields are required.")
                return

            try:
                new_qty = int(qty_entry.get())
                new_amount = float(amount_entry.get().replace(',', ''))
                if new_qty <= 0:
                    raise ValueError
            except:
                messagebox.showerror("Error", "Invalid Quantity or Amount.")
                return

            success, msg = self.db.update_transaction(
                trans_id, new_buyer, new_prod, new_size, new_qty, new_amount, new_or, new_date
            )

            if success:
                messagebox.showinfo("Success", msg)
                edit_window.destroy()
                self.load_all_transactions()
            else:
                messagebox.showerror("Error", msg)

        tk.Button(
            form_frame, text="💾 Save Changes", font=("Arial", 12, "bold"), bg="#27ae60", fg="white", pady=10, command=save_changes
        ).pack(fill=tk.X)