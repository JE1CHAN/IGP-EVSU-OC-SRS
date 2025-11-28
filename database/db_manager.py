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
                product_name TEXT NOT NULL,
                size TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                amount REAL NOT NULL,
                or_number TEXT NOT NULL,
                date TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create index for faster searches
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
        print("✓ Database initialized successfully")
    
    # ========== INVENTORY OPERATIONS ==========
    
    def add_product(self, product_name, size, stock, price):
        """
        Add a new product to inventory
        
        Args:
            product_name (str): Name of the product
            size (str): Size of the product
            stock (int): Initial stock quantity
            price (float): Price per unit
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO inventory (product_name, size, stock, price)
                VALUES (?, ?, ?, ?)
            ''', (product_name, size, stock, price))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding product: {e}")
            return False
    
    def update_product(self, item_id, product_name, size, stock, price):
        """
        Update an existing product in inventory
        
        Args:
            item_id (int): ID of the product to update
            product_name (str): Updated product name
            size (str): Updated size
            stock (int): Updated stock quantity
            price (float): Updated price
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE inventory 
                SET product_name = ?, size = ?, stock = ?, price = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE item_id = ?
            ''', (product_name, size, stock, price, item_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating product: {e}")
            return False
    
    def update_stock(self, product_name, size, quantity_change):
        """
        Update stock quantity for a product (increase or decrease)
        
        Args:
            product_name (str): Name of the product
            size (str): Size of the product
            quantity_change (int): Amount to change stock by (negative to decrease)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Check current stock
            cursor.execute('''
                SELECT stock FROM inventory 
                WHERE product_name = ? AND size = ?
            ''', (product_name, size))
            
            result = cursor.fetchone()
            if not result:
                print(f"Product not found: {product_name} ({size})")
                conn.close()
                return False
            
            new_stock = result[0] + quantity_change
            
            if new_stock < 0:
                print(f"Error: Insufficient stock. Current: {result[0]}, Requested: {abs(quantity_change)}")
                conn.close()
                return False
            
            cursor.execute('''
                UPDATE inventory 
                SET stock = ?, updated_at = CURRENT_TIMESTAMP
                WHERE product_name = ? AND size = ?
            ''', (new_stock, product_name, size))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating stock: {e}")
            return False
    
    def delete_product(self, item_id):
        """
        Delete a product from inventory
        
        Args:
            item_id (int): ID of the product to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
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
        """
        Get all products from inventory
        
        Returns:
            list: List of tuples containing inventory data
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT item_id, product_name, size, stock, price 
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
        """
        Get product details by name and size
        
        Args:
            product_name (str): Name of the product
            size (str): Size of the product
            
        Returns:
            tuple: Product data or None if not found
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT item_id, product_name, size, stock, price 
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
        """
        Get available stock for a specific product and size
        
        Args:
            product_name (str): Name of the product
            size (str): Size of the product
            
        Returns:
            int: Available stock quantity or 0 if not found
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT stock FROM inventory 
                WHERE product_name = ? AND size = ?
            ''', (product_name, size))
            
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else 0
        except Exception as e:
            print(f"Error checking stock: {e}")
            return 0
    
    def get_unique_products(self):
        """
        Get list of unique product names
        
        Returns:
            list: List of unique product names
        """
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
        """
        Get available sizes for a specific product
        
        Args:
            product_name (str): Name of the product
            
        Returns:
            list: List of available sizes
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT size FROM inventory 
                WHERE product_name = ? 
                ORDER BY size
            ''', (product_name,))
            
            results = [row[0] for row in cursor.fetchall()]
            conn.close()
            return results
        except Exception as e:
            print(f"Error fetching sizes: {e}")
            return []
    
    # ========== TRANSACTION OPERATIONS ==========
    
    def add_transaction(self, buyer_name, product_name, size, quantity, amount, or_number, date=None):
        """
        Add a new sales transaction
        
        Args:
            buyer_name (str): Name of the buyer
            product_name (str): Name of the product
            size (str): Size of the product
            quantity (int): Quantity purchased
            amount (float): Total amount
            or_number (str): Official Receipt number
            date (str): Transaction date (defaults to today)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if date is None:
                date = datetime.now().strftime("%Y-%m-%d")
            
            # Check and update stock
            if not self.update_stock(product_name, size, -quantity):
                return False
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO transactions (buyer_name, product_name, size, quantity, amount, or_number, date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (buyer_name, product_name, size, quantity, amount, or_number, date))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding transaction: {e}")
            return False
    
    def get_all_transactions(self):
        """
        Get all transactions
        
        Returns:
            list: List of all transactions
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
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
    
    def search_transactions(self, buyer_name=None, product_name=None, or_number=None, 
                           start_date=None, end_date=None):
        """
        Search transactions with multiple filters
        
        Args:
            buyer_name (str): Filter by buyer name (partial match)
            product_name (str): Filter by product name (partial match)
            or_number (str): Filter by OR number (partial match)
            start_date (str): Start date for date range
            end_date (str): End date for date range
            
        Returns:
            list: Filtered list of transactions
        """
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
        """
        Get monthly sales report
        
        Args:
            year (int): Year
            month (int): Month (1-12)
            
        Returns:
            dict: Dictionary containing report data
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            start_date = f"{year}-{month:02d}-01"
            if month == 12:
                end_date = f"{year + 1}-01-01"
            else:
                end_date = f"{year}-{month + 1:02d}-01"
            
            # Get total sales
            cursor.execute('''
                SELECT COUNT(*), SUM(quantity), SUM(amount)
                FROM transactions
                WHERE date >= ? AND date < ?
            ''', (start_date, end_date))
            
            totals = cursor.fetchone()
            
            # Get detailed transactions
            cursor.execute('''
                SELECT transaction_id, buyer_name, product_name, size, quantity, amount, or_number, date
                FROM transactions
                WHERE date >= ? AND date < ?
                ORDER BY date, transaction_id
            ''', (start_date, end_date))
            
            transactions = cursor.fetchall()
            
            # Get product summary
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
            return {
                'total_transactions': 0,
                'total_items_sold': 0,
                'total_revenue': 0.0,
                'transactions': [],
                'product_summary': []
            }
    
    def get_date_range_report(self, start_date, end_date):
        """
        Get sales report for custom date range
        
        Args:
            start_date (str): Start date (YYYY-MM-DD)
            end_date (str): End date (YYYY-MM-DD)
            
        Returns:
            dict: Dictionary containing report data
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get total sales
            cursor.execute('''
                SELECT COUNT(*), SUM(quantity), SUM(amount)
                FROM transactions
                WHERE date >= ? AND date <= ?
            ''', (start_date, end_date))
            
            totals = cursor.fetchone()
            
            # Get detailed transactions
            cursor.execute('''
                SELECT transaction_id, buyer_name, product_name, size, quantity, amount, or_number, date
                FROM transactions
                WHERE date >= ? AND date <= ?
                ORDER BY date, transaction_id
            ''', (start_date, end_date))
            
            transactions = cursor.fetchall()
            
            # Get product summary
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
            return {
                'total_transactions': 0,
                'total_items_sold': 0,
                'total_revenue': 0.0,
                'transactions': [],
                'product_summary': []
            }


# Test database initialization
if __name__ == "__main__":
    db = DatabaseManager()
    print("Database manager initialized successfully!")
    
    # Add sample data for testing
    print("\nAdding sample inventory...")
    db.add_product("T-Shirt", "S", 50, 250.00)
    db.add_product("T-Shirt", "M", 75, 250.00)
    db.add_product("T-Shirt", "L", 60, 250.00)
    db.add_product("T-Shirt", "XL", 40, 250.00)
    db.add_product("Polo Shirt", "M", 30, 350.00)
    db.add_product("Polo Shirt", "L", 25, 350.00)
    db.add_product("Cap", "One Size", 100, 150.00)
    
    print("Sample data added successfully!")
