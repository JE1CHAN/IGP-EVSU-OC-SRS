"""
Database Manager for EVSU-OC IGP Sales Record System
Handles all SQLite3 database operations including initialization and CRUD operations
"""

import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    """Manages SQLite database operations for the IGP Sales Record System"""
    
    def __init__(self, db_path="database/igp_sales.db"):
        """
        Initialize database manager and create tables if they don't exist
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        self.ensure_database_directory()
        self.initialize_database()
        self.check_and_update_schema()
    
    def ensure_database_directory(self):
        """Create database directory if it doesn't exist"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
    
    def get_connection(self):
        """
        Create and return a database connection
        
        Returns:
            sqlite3.Connection: Database connection object
        """
        return sqlite3.connect(self.db_path)
    
    def initialize_database(self):
        """Create database tables if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create inventory table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                size TEXT NOT NULL,
                batch TEXT DEFAULT '',
                stock INTEGER NOT NULL DEFAULT 0,
                price REAL NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                buyer_name TEXT NOT NULL,
                program_course TEXT,
                product_name TEXT NOT NULL,
                size TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                amount REAL NOT NULL,
                or_number TEXT NOT NULL,
                date TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indexes
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_transactions_date 
            ON transactions(date)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_transactions_buyer 
            ON transactions(buyer_name)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_inventory_product 
            ON inventory(product_name, size)
        ''')
        
        conn.commit()
        conn.close()

    def check_and_update_schema(self):
        """Check for missing columns and update schema if necessary (Migration)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Check if program_course exists in transactions
            cursor.execute("PRAGMA table_info(transactions)")
            columns = [info[1] for info in cursor.fetchall()]
            
            if "program_course" not in columns:
                print("Migrating database: Adding program_course column...")
                cursor.execute("ALTER TABLE transactions ADD COLUMN program_course TEXT")
                conn.commit()
                print("Migration successful.")
            
            # Check if batch exists in inventory
            cursor.execute("PRAGMA table_info(inventory)")
            inv_cols = [info[1] for info in cursor.fetchall()]
            if 'batch' not in inv_cols:
                print("Migrating database: Adding batch column to inventory...")
                cursor.execute("ALTER TABLE inventory ADD COLUMN batch TEXT DEFAULT ''")
                conn.commit()
                print("Inventory migration successful.")
                
            conn.close()
        except Exception as e:
            print(f"Schema update error: {e}")
    
    # ========== INVENTORY OPERATIONS ==========
    
    def add_product(self, product_name, size, stock, price, batch=''):
        """Add a new product to inventory"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO inventory (product_name, size, batch, stock, price)
                VALUES (?, ?, ?, ?, ?)
            ''', (product_name, size, batch, stock, price))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding product: {e}")
            return False
    
    def update_product(self, item_id, product_name, size, stock, price, batch=''):
        """Update an existing product in inventory"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE inventory 
                SET product_name = ?, size = ?, batch = ?, stock = ?, price = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE item_id = ?
            ''', (product_name, size, batch, stock, price, item_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating product: {e}")
            return False
    
    def update_stock(self, product_name=None, size=None, quantity_change=0, item_id=None):
        """Update stock quantity for a product or specific item (batch).

        If `item_id` is provided, update that specific inventory row.
        Otherwise, operate on the first matching inventory row for the given product_name and size.
        This ensures we only modify a single batch row and avoid affecting other batches.
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # If item_id is provided, target that row
            if item_id is not None:
                cursor.execute('SELECT stock FROM inventory WHERE item_id = ?', (item_id,))
                row = cursor.fetchone()
                if not row:
                    print(f"Item not found: item_id={item_id}")
                    conn.close()
                    return False

                new_stock = row[0] + quantity_change
                if new_stock < 0:
                    print(f"Error: Insufficient stock for item {item_id}. Current: {row[0]}, Requested: {abs(quantity_change)}")
                    conn.close()
                    return False

                cursor.execute('''
                    UPDATE inventory
                    SET stock = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE item_id = ?
                ''', (new_stock, item_id))

                conn.commit()
                conn.close()
                return True

            # No item_id: find the first matching row for product_name & size
            cursor.execute('''
                SELECT item_id, stock FROM inventory
                WHERE product_name = ? AND size = ?
                ORDER BY batch ASC, item_id ASC
                LIMIT 1
            ''', (product_name, size))

            result = cursor.fetchone()
            if not result:
                print(f"Product not found: {product_name} ({size})")
                conn.close()
                return False

            target_item_id, current_stock = result
            new_stock = current_stock + quantity_change

            if new_stock < 0:
                print(f"Error: Insufficient stock. Current: {current_stock}, Requested: {abs(quantity_change)}")
                conn.close()
                return False

            cursor.execute('''
                UPDATE inventory
                SET stock = ?, updated_at = CURRENT_TIMESTAMP
                WHERE item_id = ?
            ''', (new_stock, target_item_id))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating stock: {e}")
            return False
    
    def delete_product(self, item_id):
        """Delete a product from inventory"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM inventory WHERE item_id = ?', (item_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting product: {e}")
            return False
    
    def get_all_inventory(self):
        """Get all products from inventory"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT item_id, product_name, size, batch, stock, price 
                FROM inventory 
                ORDER BY product_name, size
            ''')
            results = cursor.fetchall()
            conn.close()
            return results
        except Exception as e:
            print(f"Error fetching inventory: {e}")
            return []
    
    def get_product_by_name_size(self, product_name, size):
        """Get product details by name and size"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT item_id, product_name, size, batch, stock, price 
                FROM inventory 
                WHERE product_name = ? AND size = ?
            ''', (product_name, size))
            result = cursor.fetchone()
            conn.close()
            return result
        except Exception as e:
            print(f"Error fetching product: {e}")
            return None
    
    def get_available_stock(self, product_name, size):
        """Get available stock for a specific product and size"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT SUM(stock) FROM inventory 
                WHERE product_name = ? AND size = ?
            ''', (product_name, size))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result and result[0] is not None else 0
        except Exception as e:
            print(f"Error checking stock: {e}")
            return 0
    
    def get_unique_products(self):
        """Get list of unique product names"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT product_name FROM inventory ORDER BY product_name')
            results = [row[0] for row in cursor.fetchall()]
            conn.close()
            return results
        except Exception as e:
            print(f"Error fetching products: {e}")
            return []
    
    def get_sizes_for_product(self, product_name):
        """Get available sizes for a specific product"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT DISTINCT size FROM inventory 
                WHERE product_name = ? 
                ORDER BY size
            ''', (product_name,))
            results = [row[0] for row in cursor.fetchall()]
            conn.close()
            return results
        except Exception as e:
            print(f"Error fetching sizes: {e}")
            return []
    
    def get_first_available_batch_for_size(self, product_name, size):
        """Get the first batch with available stock for a product/size combination"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT item_id, product_name, size, batch, stock, price
                FROM inventory 
                WHERE product_name = ? AND size = ? AND stock > 0
                ORDER BY batch ASC
                LIMIT 1
            ''', (product_name, size))
            result = cursor.fetchone()
            conn.close()
            return result
        except Exception as e:
            print(f"Error fetching first available batch: {e}")
            return None
    
    # ========== TRANSACTION OPERATIONS ==========
    
    def add_transaction(self, buyer_name, product_name, size, quantity, amount, or_number, date=None, program_course=None, item_id=None):
        """Add a new sales transaction"""
        try:
            if date is None:
                date = datetime.now().strftime("%Y-%m-%d")
            
            # Check and update stock
            if not self.update_stock(product_name, size, -quantity, item_id=item_id):
                return False
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO transactions (buyer_name, program_course, product_name, size, quantity, amount, or_number, date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (buyer_name, program_course, product_name, size, quantity, amount, or_number, date))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding transaction: {e}")
            return False

    def update_transaction(self, transaction_id, buyer_name, product_name, size, quantity, amount, or_number, date):
        """
        Update a transaction and adjust inventory if product/qty changed
        Returns: (success: bool, message: str)
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 1. Get old transaction details
            cursor.execute("SELECT product_name, size, quantity FROM transactions WHERE transaction_id = ?", (transaction_id,))
            old_data = cursor.fetchone()
            
            if not old_data:
                conn.close()
                return False, "Transaction not found"
            
            old_prod, old_size, old_qty = old_data
            
            # 2. Handle Inventory Updates
            # Revert old stock (Add back) on the specific batch (first matching batch for old transaction)
            cursor.execute("SELECT item_id, stock FROM inventory WHERE product_name = ? AND size = ? ORDER BY batch ASC, item_id ASC LIMIT 1", (old_prod, old_size))
            old_stock_row = cursor.fetchone()
            old_item_id = None
            old_stock = 0
            if old_stock_row:
                old_item_id, old_stock = old_stock_row
                cursor.execute("UPDATE inventory SET stock = ? WHERE item_id = ?", (old_stock + old_qty, old_item_id))

            # Deduct new stock on the specific batch (first matching batch for new selection)
            cursor.execute("SELECT item_id, stock FROM inventory WHERE product_name = ? AND size = ? ORDER BY batch ASC, item_id ASC LIMIT 1", (product_name, size))
            new_stock_row = cursor.fetchone()
            if not new_stock_row:
                conn.rollback() # Undo revert
                conn.close()
                return False, f"Product {product_name} ({size}) not found in inventory"

            new_item_id, new_stock = new_stock_row

            # Determine current available stock for deduction
            if product_name == old_prod and size == old_size and old_stock_row:
                current_stock = old_stock + old_qty
            else:
                current_stock = new_stock

            if current_stock < quantity:
                conn.rollback() # Undo revert
                conn.close()
                return False, f"Insufficient stock for {product_name} ({size}). Available: {current_stock}"

            # Deduct from the selected/new batch item
            cursor.execute("UPDATE inventory SET stock = ? WHERE item_id = ?", (current_stock - quantity, new_item_id))
            
            # 3. Update Transaction Record
            cursor.execute("""
                UPDATE transactions 
                SET buyer_name=?, product_name=?, size=?, quantity=?, amount=?, or_number=?, date=?
                WHERE transaction_id=?
            """, (buyer_name, product_name, size, quantity, amount, or_number, date, transaction_id))
            
            conn.commit()
            conn.close()
            return True, "Transaction updated successfully"
            
        except Exception as e:
            print(f"Error updating transaction: {e}")
            return False, str(e)
    
    def get_all_transactions(self):
        """Get all transactions"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            # Note: We keep original column selection for compatibility with history module
            cursor.execute('''
                SELECT transaction_id, buyer_name, product_name, size, quantity, amount, or_number, date
                FROM transactions
                ORDER BY date DESC, transaction_id DESC
            ''')
            results = cursor.fetchall()
            conn.close()
            return results
        except Exception as e:
            print(f"Error fetching transactions: {e}")
            return []
    
    def search_transactions(self, buyer_name=None, product_name=None, or_number=None, start_date=None, end_date=None):
        """Search transactions with multiple filters"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = '''
                SELECT transaction_id, buyer_name, product_name, size, quantity, amount, or_number, date
                FROM transactions
                WHERE 1=1
            '''
            params = []
            
            if buyer_name:
                query += ' AND buyer_name LIKE ?'
                params.append(f'%{buyer_name}%')
            
            if product_name:
                query += ' AND product_name LIKE ?'
                params.append(f'%{product_name}%')
            
            if or_number:
                query += ' AND or_number LIKE ?'
                params.append(f'%{or_number}%')
            
            if start_date:
                query += ' AND date >= ?'
                params.append(start_date)
            
            if end_date:
                query += ' AND date <= ?'
                params.append(end_date)
            
            query += ' ORDER BY date DESC, transaction_id DESC'
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            conn.close()
            return results
        except Exception as e:
            print(f"Error searching transactions: {e}")
            return []
    
    def get_monthly_report(self, year, month):
        """Get monthly sales report"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            start_date = f"{year}-{month:02d}-01"
            if month == 12:
                end_date = f"{year + 1}-01-01"
            else:
                end_date = f"{year}-{month + 1:02d}-01"
            
            cursor.execute('''
                SELECT COUNT(*), SUM(quantity), SUM(amount)
                FROM transactions
                WHERE date >= ? AND date < ?
            ''', (start_date, end_date))
            totals = cursor.fetchone()
            
            cursor.execute('''
                SELECT transaction_id, buyer_name, program_course, product_name, size, quantity, amount, or_number, date
                FROM transactions
                WHERE date >= ? AND date < ?
                ORDER BY date, transaction_id
            ''', (start_date, end_date))
            transactions = cursor.fetchall()
            
            cursor.execute('''
                SELECT product_name, size, SUM(quantity) as total_qty, SUM(amount) as total_amount
                FROM transactions
                WHERE date >= ? AND date < ?
                GROUP BY product_name, size
                ORDER BY product_name, size
            ''', (start_date, end_date))
            product_summary = cursor.fetchall()
            
            conn.close()
            
            return {
                'total_transactions': totals[0] or 0,
                'total_items_sold': totals[1] or 0,
                'total_revenue': totals[2] or 0.0,
                'transactions': transactions,
                'product_summary': product_summary
            }
        except Exception as e:
            print(f"Error generating monthly report: {e}")
            return {'total_transactions': 0, 'total_items_sold': 0, 'total_revenue': 0.0, 'transactions': [], 'product_summary': []}
    
    def get_date_range_report(self, start_date, end_date):
        """Get sales report for custom date range"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT COUNT(*), SUM(quantity), SUM(amount)
                FROM transactions
                WHERE date >= ? AND date <= ?
            ''', (start_date, end_date))
            totals = cursor.fetchone()
            
            cursor.execute('''
                SELECT transaction_id, buyer_name, program_course, product_name, size, quantity, amount, or_number, date
                FROM transactions
                WHERE date >= ? AND date <= ?
                ORDER BY date, transaction_id
            ''', (start_date, end_date))
            transactions = cursor.fetchall()
            
            cursor.execute('''
                SELECT product_name, size, SUM(quantity) as total_qty, SUM(amount) as total_amount
                FROM transactions
                WHERE date >= ? AND date <= ?
                GROUP BY product_name, size
                ORDER BY product_name, size
            ''', (start_date, end_date))
            product_summary = cursor.fetchall()
            
            conn.close()
            
            return {
                'total_transactions': totals[0] or 0,
                'total_items_sold': totals[1] or 0,
                'total_revenue': totals[2] or 0.0,
                'transactions': transactions,
                'product_summary': product_summary
            }
        except Exception as e:
            print(f"Error generating date range report: {e}")
            return {'total_transactions': 0, 'total_items_sold': 0, 'total_revenue': 0.0, 'transactions': [], 'product_summary': []}