import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import os

class DatabaseTool:
    def __init__(self, root):
        self.root = root
        self.root.title("EVSU-OC IGP Database Manager")
        self.root.geometry("1000x700")
        
        # Database Path
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database", "igp_sales.db")
        
        # UI Setup
        self.create_ui()
        self.load_tables()
        
    def get_connection(self):
        """Create database connection"""
        if not os.path.exists(self.db_path):
            messagebox.showerror("Error", f"Database not found at:\n{self.db_path}")
            return None
        return sqlite3.connect(self.db_path)

    def create_ui(self):
        # --- TOP TOOLBAR ---
        toolbar = tk.Frame(self.root, bg="#f0f0f0", padx=10, pady=10)
        toolbar.pack(fill=tk.X)
        
        tk.Label(toolbar, text="Select Table:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.table_combo = ttk.Combobox(toolbar, state="readonly", width=30)
        self.table_combo.pack(side=tk.LEFT, padx=5)
        self.table_combo.bind("<<ComboboxSelected>>", self.load_data)
        
        tk.Button(toolbar, text="🔄 Refresh Data", command=self.load_data, bg="#3498db", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="🗑️ Delete Selected Row", command=self.delete_selected_row, bg="#e74c3c", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="⚠️ Clear Entire Table", command=self.clear_table, bg="#c0392b", fg="white").pack(side=tk.LEFT, padx=5)

        # --- DATA VIEW (TREEVIEW) ---
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Scrollbars
        y_scroll = ttk.Scrollbar(tree_frame, orient="vertical")
        x_scroll = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        self.tree = ttk.Treeview(tree_frame, yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        y_scroll.config(command=self.tree.yview)
        x_scroll.config(command=self.tree.xview)
        
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # --- SQL QUERY SECTION ---
        sql_frame = tk.LabelFrame(self.root, text="Execute SQL Query (Advanced)", padx=10, pady=10)
        sql_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.sql_text = scrolledtext.ScrolledText(sql_frame, height=5, font=("Consolas", 10))
        self.sql_text.pack(fill=tk.X, pady=5)
        self.sql_text.insert(tk.END, "-- Type SQL query here (e.g., INSERT INTO inventory...)\n")
        
        btn_frame = tk.Frame(sql_frame)
        btn_frame.pack(fill=tk.X)
        
        tk.Button(btn_frame, text="▶️ Execute Query", command=self.execute_sql, bg="#27ae60", fg="white", font=("Arial", 10, "bold")).pack(side=tk.RIGHT)
        tk.Label(btn_frame, text="Use this area to manually ADD data or fix issues using SQL commands.", fg="#7f8c8d").pack(side=tk.LEFT)

    def load_tables(self):
        """Load list of tables from database"""
        conn = self.get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence'")
            tables = [row[0] for row in cursor.fetchall()]
            self.table_combo['values'] = tables
            if tables:
                self.table_combo.current(0)
                self.load_data()
            conn.close()

    def load_data(self, event=None):
        """Load data from selected table into Treeview"""
        table = self.table_combo.get()
        if not table: return
        
        # Clear existing view
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = ()
        
        conn = self.get_connection()
        if conn:
            cursor = conn.cursor()
            try:
                # Get column names
                cursor.execute(f"PRAGMA table_info({table})")
                columns = [col[1] for col in cursor.fetchall()]
                
                # Setup Treeview columns
                self.tree["columns"] = columns
                self.tree["show"] = "headings"
                
                for col in columns:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=150, anchor="w")
                
                # Fetch data
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()
                
                for row in rows:
                    self.tree.insert("", tk.END, values=row)
                    
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

    def delete_selected_row(self):
        """Delete the selected row from the database"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a row to delete.")
            return
            
        table = self.table_combo.get()
        # Assume first column is always the Primary Key (ID)
        item_values = self.tree.item(selected_item)['values']
        record_id = item_values[0]
        
        # Get primary key column name dynamically
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table})")
        pk_col = cursor.fetchone()[1] # First column name
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete record ID {record_id}?"):
            try:
                cursor.execute(f"DELETE FROM {table} WHERE {pk_col} = ?", (record_id,))
                conn.commit()
                messagebox.showinfo("Success", "Record deleted.")
                self.load_data()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

    def clear_table(self):
        """Clear all data from selected table"""
        table = self.table_combo.get()
        if messagebox.askyesno("DANGER", f"⚠️ Are you sure you want to delete ALL data in '{table}'?\nThis cannot be undone!"):
            conn = self.get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute(f"DELETE FROM {table}")
                # Reset auto-increment
                cursor.execute("DELETE FROM sqlite_sequence WHERE name=?", (table,))
                conn.commit()
                messagebox.showinfo("Success", f"Table '{table}' cleared.")
                self.load_data()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

    def execute_sql(self):
        """Execute raw SQL from text area"""
        query = self.sql_text.get("1.0", tk.END).strip()
        if not query or query.startswith("--"):
            messagebox.showwarning("Warning", "Please enter a SQL query.")
            return

        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            conn.commit()
            messagebox.showinfo("Success", "Query executed successfully!")
            self.load_data() # Refresh view
        except Exception as e:
            messagebox.showerror("SQL Error", str(e))
        finally:
            conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseTool(root)
    root.mainloop()