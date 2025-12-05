"""
Reports Module
Generate and print monthly or custom date range sales reports
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import calendar
import csv
from tkcalendar import DateEntry

class ReportsModule:
    """Sales reports generation with print capability"""
    
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db = db_manager
        
        # Create main frame
        self.main_frame = tk.Frame(parent, bg="white")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.create_ui()
    
    def create_ui(self):
        """Create reports interface"""
        # Title
        title_label = tk.Label(
            self.main_frame,
            text="📈 SALES REPORTS",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#800000"  # Maroon
        )
        title_label.pack(pady=(0, 20))
        
        # Report options frame
        options_frame = tk.LabelFrame(
            self.main_frame,
            text="Report Options",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=20,
            pady=20
        )
        options_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Monthly Report Section
        monthly_frame = tk.Frame(options_frame, bg="white")
        monthly_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            monthly_frame,
            text="Monthly Report:",
            font=("Arial", 12, "bold"),
            bg="white"
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        # Month selection
        tk.Label(
            monthly_frame,
            text="Month:",
            font=("Arial", 11),
            bg="white"
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.month_combo = ttk.Combobox(
            monthly_frame,
            font=("Arial", 11),
            width=12,
            state="readonly"
        )
        months = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"]
        self.month_combo['values'] = months
        self.month_combo.set(months[datetime.now().month - 1])
        self.month_combo.pack(side=tk.LEFT, padx=5)
        
        # Year selection
        tk.Label(
            monthly_frame,
            text="Year:",
            font=("Arial", 11),
            bg="white"
        ).pack(side=tk.LEFT, padx=(15, 5))
        
        self.year_entry = tk.Entry(monthly_frame, font=("Arial", 11), width=8)
        self.year_entry.insert(0, str(datetime.now().year))
        self.year_entry.pack(side=tk.LEFT, padx=5)
        
        # Generate Monthly Report button (Yellow)
        tk.Button(
            monthly_frame,
            text="📊 Generate Monthly Report",
            font=("Arial", 11, "bold"),
            bg="#FFC107",  # Yellow
            fg="black",    # Black
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.generate_monthly_report
        ).pack(side=tk.LEFT, padx=20)
        
        # Separator
        ttk.Separator(options_frame, orient="horizontal").pack(fill=tk.X, pady=15)
        
        # Custom Date Range Section
        custom_frame = tk.Frame(options_frame, bg="white")
        custom_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            custom_frame,
            text="Custom Date Range:",
            font=("Arial", 12, "bold"),
            bg="white"
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        # Start Date
        tk.Label(
            custom_frame,
            text="From:",
            font=("Arial", 11),
            bg="white"
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.custom_start_date = DateEntry(
            custom_frame,
            font=("Arial", 12),
            width=10,
            background="maroon",
            foreground="white",
            borderwidth=2,
            date_pattern="yyyy-mm-dd",
            showweeknumbers=False
        )
        self.custom_start_date.pack(side=tk.LEFT, padx=5)
        self.custom_start_date.delete(0, "end")
        
        # End Date
        tk.Label(
            custom_frame,
            text="To:",
            font=("Arial", 11),
            bg="white"
        ).pack(side=tk.LEFT, padx=(15, 5))
        
        self.custom_end_date = DateEntry(
            custom_frame,
            font=("Arial", 12),
            width=10,
            background="maroon",
            foreground="white",
            borderwidth=2,
            date_pattern="yyyy-mm-dd",
            showweeknumbers=False
        )
        self.custom_end_date.pack(side=tk.LEFT, padx=5)
        self.custom_end_date.delete(0, "end")
        
        
        tk.Label(
            custom_frame,
            text="(YYYY-MM-DD)",
            font=("Arial", 9, "italic"),
            bg="white",
            fg="#7f8c8d"
        ).pack(side=tk.LEFT, padx=5)
        
        # Generate Custom Report button (Yellow)
        tk.Button(
            custom_frame,
            text="📊 Generate Custom Report",
            font=("Arial", 11, "bold"),
            bg="#FFC107",  # Yellow
            fg="black",    # Black
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.generate_custom_report
        ).pack(side=tk.LEFT, padx=20)
        
        # Report display frame
        self.report_frame = tk.Frame(self.main_frame, bg="white")
        self.report_frame.pack(fill=tk.BOTH, expand=True)
    
    def generate_monthly_report(self):
        """Generate monthly sales report"""
        try:
            # Get selected month and year
            month_name = self.month_combo.get()
            year = int(self.year_entry.get())
            month = list(calendar.month_name).index(month_name)
            
            # Get report data
            report_data = self.db.get_monthly_report(year, month)
            
            # Display report
            self.display_report(
                f"{month_name} {year} Sales Report",
                report_data
            )
        
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid year")
    
    def generate_custom_report(self):
        """Generate custom date range report"""
        start_date = self.custom_start_date.get().strip()
        end_date = self.custom_end_date.get().strip()
        
        # Validate dates
        if not start_date or not end_date:
            messagebox.showerror("Error", "Please enter both start and end dates")
            return
        
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror(
                "Error",
                "Invalid date format. Please use YYYY-MM-DD"
            )
            return
        
        # Get report data
        report_data = self.db.get_date_range_report(start_date, end_date)
        
        # Display report
        self.display_report(
            f"Sales Report ({start_date} to {end_date})",
            report_data
        )
    
    def center_window(self, window):
        """Center a window on screen"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2) - 35
        window.geometry(f'{width}x{height}+{x}+{y}')
    
    def display_report(self, title, report_data):
        """Display report in a new window"""
        # Clear current report frame
        for widget in self.report_frame.winfo_children():
            widget.destroy()
        
        # Create report window
        report_window = tk.Toplevel(self.parent)
        report_window.title(title)
        report_window.geometry("900x700")
        report_window.configure(bg="white")
        
        # Center the window on screen
        self.center_window(report_window)
        
        # Create scrollable frame
        canvas = tk.Canvas(report_window, bg="white")
        scrollbar = ttk.Scrollbar(report_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind mouse wheel scroll to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        
        
        # Report Header (Maroon)
        header_frame = tk.Frame(scrollable_frame, bg="#800000", padx=20, pady=20)
        header_frame.pack(fill=tk.X)
        
        tk.Label(
            header_frame,
            text="EVSU-OC IGP SALES REPORT",
            font=("Arial", 16, "bold"),
            bg="#800000",
            fg="white"
        ).pack()
        
        tk.Label(
            header_frame,
            text=title,
            font=("Arial", 12),
            bg="#800000",
            fg="white"
        ).pack()
        
        tk.Label(
            header_frame,
            text=f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            font=("Arial", 10),
            bg="#800000",
            fg="white"
        ).pack()
        
        # Content frame
        content_frame = tk.Frame(scrollable_frame, bg="white", padx=30, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Summary section
        summary_frame = tk.LabelFrame(
            content_frame,
            text="SUMMARY",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=20,
            pady=15
        )
        summary_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            summary_frame,
            text=f"Total Transactions: {report_data['total_transactions']}",
            font=("Arial", 11),
            bg="white",
            anchor="w"
        ).pack(fill=tk.X, pady=3)
        
        tk.Label(
            summary_frame,
            text=f"Total Items Sold: {report_data['total_items_sold']}",
            font=("Arial", 11),
            bg="white",
            anchor="w"
        ).pack(fill=tk.X, pady=3)
        
        tk.Label(
            summary_frame,
            text=f"Total Revenue: ₱{report_data['total_revenue']:,.2f}",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#800000", # Maroon text
            anchor="w"
        ).pack(fill=tk.X, pady=3)
        
        # Product Summary section
        if report_data['product_summary']:
            product_summary_frame = tk.LabelFrame(
                content_frame,
                text="PRODUCT SUMMARY",
                font=("Arial", 12, "bold"),
                bg="white",
                padx=20,
                pady=15
            )
            product_summary_frame.pack(fill=tk.X, pady=(0, 20))
            
            # Create table for product summary
            columns = ("Product", "Size", "Quantity", "Revenue")
            product_tree = ttk.Treeview(
                product_summary_frame,
                columns=columns,
                show="headings",
                height=8
            )
            
            product_tree.heading("Product", text="Product")
            product_tree.heading("Size", text="Size")
            product_tree.heading("Quantity", text="Total Quantity")
            product_tree.heading("Revenue", text="Total Revenue")
            
            product_tree.column("Product", width=250, anchor="w")
            product_tree.column("Size", width=100, anchor="center")
            product_tree.column("Quantity", width=120, anchor="center")
            product_tree.column("Revenue", width=150, anchor="e")
            
            for item in report_data['product_summary']:
                product, size, qty, revenue = item
                product_tree.insert(
                    "",
                    tk.END,
                    values=(product, size, qty, f"₱{revenue:,.2f}")
                )
            
            product_tree.pack(fill=tk.X)
        
        # Detailed Transactions section
        if report_data['transactions']:
            transactions_frame = tk.LabelFrame(
                content_frame,
                text="DETAILED TRANSACTIONS",
                font=("Arial", 12, "bold"),
                bg="white",
                padx=20,
                pady=15
            )
            transactions_frame.pack(fill=tk.BOTH, expand=True)
            
            # Create table for transactions
            columns = ("ID", "Date", "Buyer", "Product", "Size", "Qty", "Amount", "OR#")
            trans_tree = ttk.Treeview(
                transactions_frame,
                columns=columns,
                show="headings",
                height=15
            )
            
            trans_tree.heading("ID", text="ID")
            trans_tree.heading("Date", text="Date")
            trans_tree.heading("Buyer", text="Buyer Name")
            trans_tree.heading("Product", text="Product")
            trans_tree.heading("Size", text="Size")
            trans_tree.heading("Qty", text="Qty")
            trans_tree.heading("Amount", text="Amount")
            trans_tree.heading("OR#", text="OR Number")
            
            trans_tree.column("ID", width=50, anchor="center")
            trans_tree.column("Date", width=90, anchor="center")
            trans_tree.column("Buyer", width=150, anchor="w")
            trans_tree.column("Product", width=150, anchor="w")
            trans_tree.column("Size", width=70, anchor="center")
            trans_tree.column("Qty", width=50, anchor="center")
            trans_tree.column("Amount", width=100, anchor="e")
            trans_tree.column("OR#", width=100, anchor="center")
            
            for trans in report_data['transactions']:
                # transaction tuple now: (id, buyer_name, program_course, product_name, size, quantity, amount, or_number, date)
                trans_id, buyer, course, product, size, qty, amount, or_num, date = trans
                trans_tree.insert(
                    "",
                    tk.END,
                    values=(trans_id, date, buyer, product, size, qty, f"₱{amount:,.2f}", or_num)
                )
            
            # Add scrollbar to transactions tree
            trans_scroll = ttk.Scrollbar(
                transactions_frame,
                orient="vertical",
                command=trans_tree.yview
            )
            trans_tree.configure(yscrollcommand=trans_scroll.set)
            
            trans_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            trans_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            tk.Label(
                content_frame,
                text="No transactions found for this period",
                font=("Arial", 12, "italic"),
                bg="white",
                fg="#95a5a6"
            ).pack(pady=30)
        
        # Button frame
        button_frame = tk.Frame(scrollable_frame, bg="white", pady=20, padx=20)
        button_frame.pack(fill=tk.X)
        
        # REMOVED PRINT BUTTON AS REQUESTED
        
        # Export CSV button (Green)
        tk.Button(
            button_frame,
            text="💾 Export to Excel",
            font=("Arial", 12, "bold"),
            bg="#27ae60",  # Green
            fg="white",    # White
            padx=30,
            pady=12,
            cursor="hand2",
            command=lambda: self.export_to_csv(report_data, title)
        ).pack(side=tk.LEFT, padx=10)
        
        # Close button (Maroon)
        tk.Button(
            button_frame,
            text="❌ Close",
            font=("Arial", 12, "bold"),
            bg="#800000",  # Maroon
            fg="white",    # White
            padx=30,
            pady=12,
            cursor="hand2",
            command=report_window.destroy
        ).pack(side=tk.LEFT, padx=10)
        
        # Pack canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
            
    def export_to_csv(self, report_data, title):
        """Export report data to CSV file"""
        try:
            # Generate default filename
            filename = f"{title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            # Ask user for save location
            filepath = filedialog.asksaveasfilename(
                initialfile=filename,
                defaultextension=".csv",
                filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
                title="Save Report As"
            )
            
            if not filepath:
                return

            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                     
                # Detailed Transactions Section - group by product and include batch
                if report_data['transactions']:
                    # Group transactions by product_name
                    products = {}
                    for tr in report_data['transactions']:
                        # tuple: (transaction_id, buyer_name, program_course, product_name, size, quantity, amount, or_number, date)
                        product_name = tr[3]
                        products.setdefault(product_name, []).append(tr)

                    # Helper to get batch for a product (try inventory table 'batch' column, else parse parentheses)
                    def _get_batch_for_product(prod_name):
                        batch_val = ''
                        try:
                            conn = self.db.get_connection()
                            cur = conn.cursor()
                            cur.execute("PRAGMA table_info(inventory)")
                            cols = [c[1] for c in cur.fetchall()]
                            if 'batch' in cols:
                                cur.execute("SELECT batch FROM inventory WHERE product_name = ? LIMIT 1", (prod_name,))
                                r = cur.fetchone()
                                if r and r[0] is not None:
                                    batch_val = str(r[0])
                            conn.close()
                        except Exception:
                            batch_val = ''

                        if not batch_val:
                            # Try to parse something like '(13th Batch)' from product name
                            import re
                            m = re.search(r"\(([^)]+Batch[^)]*)\)", prod_name, flags=re.IGNORECASE)
                            if m:
                                batch_val = m.group(1)
                        return batch_val

                    # Prefer a common size ordering if present
                    preferred = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
                    def _size_key(x):
                        return (preferred.index(x) if x in preferred else len(preferred), x)

                    # For each product, write its own header and table
                    for product_name, trs in products.items():
                        batch = _get_batch_for_product(product_name)
                        header_title = product_name
                        if batch:
                            header_title = f"{product_name} ({batch})"

                        writer.writerow([header_title])

                        # Collect sizes for this product
                        sizes_found = []
                        for tr in trs:
                            s = tr[4]
                            if s and s not in sizes_found:
                                sizes_found.append(s)

                        sizes_sorted = sorted(sizes_found, key=_size_key)

                        # Write column header for this product block
                        header = ["NAME", "COURSE", "OR #"] + sizes_sorted + ["DATE", "AMOUNT"]
                        writer.writerow(header)

                        for tr in trs:
                            buyer = tr[1]
                            course = (tr[2] if len(tr) > 2 else '') or ''
                            size = tr[4]
                            qty = tr[5]
                            amount = tr[6]
                            or_num = tr[7]
                            date = tr[8]

                            row = [buyer, course, or_num] + [''] * len(sizes_sorted) + [date, f"{amount:.2f}"]
                            if size in sizes_sorted:
                                idx = sizes_sorted.index(size)
                                row[3 + idx] = str(qty)

                            writer.writerow(row)
                        # blank line between product sections
                        writer.writerow([])
            
            messagebox.showinfo("Success", f"Report exported successfully to:\n{filepath}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export CSV: {str(e)}")