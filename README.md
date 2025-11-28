# EVSU-OC IGP Sales Record System

**Eastern Visayas State University - Ormoc Campus**  
**Income Generating Project Sales Record System**

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite3-orange.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

---

## 📌 System Overview

The **EVSU-OC IGP Sales Record System** is a complete, offline desktop application designed to replace the manual logbook and Excel-based encoding system currently used in EVSU-Ormoc Campus's Income Generating Project.

This system provides:
- ✅ **Automated transaction recording**
- ✅ **Real-time inventory tracking**
- ✅ **Comprehensive sales reports**
- ✅ **Searchable transaction history**
- ✅ **User-friendly interface**

---

## 🎯 Key Features

### 1. **Transaction Entry Module**
- Record sales transactions with buyer name, product, size, quantity, amount, and OR number
- Real-time stock validation
- Automatic amount calculation
- Date selection (manual or automatic)
- Input validation to prevent errors

### 2. **Inventory Management Module**
- Add, update, and delete products
- Track stock levels by product and size
- Visual indicators for low stock and out-of-stock items
- Real-time stock updates after each sale
- Prevent negative stock values

### 3. **Sales History Viewer**
- View all transaction history
- Search and filter by:
  - Buyer name
  - Product name
  - OR number
  - Date range
- Real-time statistics (total transactions and revenue)

### 4. **Monthly Reports Generator**
- Generate monthly sales reports
- Custom date range reports
- Detailed transaction listings
- Product summary with quantities and revenue
- Print/export capability
- Professional report formatting

---

## 🛠️ Technical Specifications

### Technologies Used
- **Python 3.7+** - Core programming language
- **Tkinter** - GUI framework (built-in with Python)
- **SQLite3** - Local database (built-in with Python)
- **ttk** - Enhanced Tkinter widgets

### Database Schema

#### Table: `inventory`
```sql
item_id INTEGER PRIMARY KEY
product_name TEXT
size TEXT
stock INTEGER
price REAL
created_at TEXT
updated_at TEXT
```

#### Table: `transactions`
```sql
transaction_id INTEGER PRIMARY KEY
buyer_name TEXT
product_name TEXT
size TEXT
quantity INTEGER
amount REAL
or_number TEXT
date TEXT
created_at TEXT
```

---

## 📁 Project Structure

```
EVSU-OC IGP SRS/
│
├── main.py                          # Main application entry point
│
├── database/
│   ├── __init__.py
│   ├── db_manager.py                # Database operations
│   └── igp_sales.db                 # SQLite database (auto-created)
│
├── modules/
│   ├── __init__.py
│   ├── transaction_module.py        # Transaction entry interface
│   ├── inventory_module.py          # Inventory management interface
│   ├── history_module.py            # Sales history viewer
│   └── reports_module.py            # Report generation
│
├── assets/                          # (Reserved for future use)
│
└── README.md                        # This file
```

---

## 🚀 Installation & Setup

### Prerequisites
- **Python 3.7 or higher** (Download from: https://www.python.org/downloads/)
- Windows operating system (tested on Windows 10/11)

### Step-by-Step Installation

#### 1. **Install Python**
   - Download Python from https://www.python.org/downloads/
   - During installation, **check "Add Python to PATH"**
   - Verify installation by opening Command Prompt and typing:
     ```bash
     python --version
     ```

#### 2. **Download/Extract the System**
   - Extract the provided ZIP file to your desired location
   - Example: `C:\Users\YourName\Desktop\EVSU-OC IGP SRS\`

#### 3. **Verify File Structure**
   Ensure you have the following structure:
   ```
   EVSU-OC IGP SRS/
   ├── main.py
   ├── database/
   └── modules/
   ```

#### 4. **Initialize the Database** (First Time Only)
   Open Command Prompt in the project directory and run:
   ```bash
   cd "C:\Users\YourName\Desktop\EVSU-OC IGP SRS"
   python database/db_manager.py
   ```
   
   This will:
   - Create the database file
   - Initialize tables
   - Add sample inventory data (optional)

---

## ▶️ Running the System

### Method 1: Command Line
1. Open Command Prompt
2. Navigate to project directory:
   ```bash
   cd "C:\Users\Laire Neil Villena\Desktop\EVSU-OC IGP SRS"
   ```
3. Run the application:
   ```bash
   python main.py
   ```

### Method 2: Double-Click (Windows)
1. Create a shortcut to `main.py`
2. Right-click the shortcut → Properties
3. Change "Target" to: `python "C:\Users\Laire Neil Villena\Desktop\EVSU-OC IGP SRS\main.py"`
4. Double-click the shortcut to run

### Method 3: Create a Batch File
Create a file named `run_system.bat` with this content:
```batch
@echo off
cd /d "C:\Users\Laire Neil Villena\Desktop\EVSU-OC IGP SRS"
python main.py
pause
```
Double-click this file to run the system.

---

## 📖 User Guide

### First-Time Setup

#### 1. **Add Products to Inventory**
   - Click **"Inventory"** in the left menu
   - Click **"➕ Add New Product"**
   - Enter product details:
     - Product Name (e.g., "T-Shirt")
     - Size (e.g., "M", "L", "XL")
     - Initial Stock (e.g., 50)
     - Price (e.g., 250.00)
   - Click **"💾 Save"**

#### 2. **Add Multiple Sizes**
   Repeat the process for each size:
   - T-Shirt - S
   - T-Shirt - M
   - T-Shirt - L
   - T-Shirt - XL

### Daily Operations

#### Recording a Sale Transaction
1. Click **"Transaction Entry"** in the menu
2. Fill in the form:
   - **Buyer Name**: Enter student/faculty/staff name
   - **Product**: Select from dropdown
   - **Size**: Select from dropdown
   - **Quantity**: Enter number of items
   - **OR Number**: Enter official receipt number
   - **Date**: Auto-filled (can be modified)
3. The system will:
   - Show available stock
   - Calculate total amount automatically
   - Validate all inputs
4. Click **"💾 SAVE TRANSACTION"**
5. Stock is automatically deducted

#### Viewing Sales History
1. Click **"Sales History"** in the menu
2. Use filters to search:
   - Buyer name
   - Product name
   - OR number
   - Date range (YYYY-MM-DD format)
3. Click **"🔍 Search"**
4. View total transactions and revenue at the top

#### Generating Reports
1. Click **"Reports"** in the menu

**For Monthly Report:**
- Select month and year
- Click **"📊 Generate Monthly Report"**

**For Custom Date Range:**
- Enter start date (YYYY-MM-DD)
- Enter end date (YYYY-MM-DD)
- Click **"📊 Generate Custom Report"**

The report shows:
- Total transactions
- Total items sold
- Total revenue
- Product summary
- Detailed transaction list

#### Managing Inventory
1. Click **"Inventory"** in the menu
2. View all products with current stock levels
3. Options:
   - **Add New Product**: Add new items
   - **Update Product**: Modify selected item
   - **Delete Product**: Remove selected item
   - **Refresh**: Reload inventory data

---

## ⚠️ Important Notes

### Data Safety
- The database file is stored in `database/igp_sales.db`
- **Backup this file regularly** to prevent data loss
- Create backups before system updates

### Backup Procedure
1. Close the application
2. Copy `database/igp_sales.db` to a safe location
3. Add date to filename: `igp_sales_2024-12-01.db`

### Date Format
- Always use **YYYY-MM-DD** format
- Examples: `2024-12-01`, `2024-11-15`

### Stock Management
- System prevents selling more than available stock
- Red text indicates low stock (< 10 items)
- Products with 0 stock cannot be sold

---

## 🔧 Troubleshooting

### Problem: "Python is not recognized"
**Solution:** Python is not in PATH
1. Reinstall Python and check "Add Python to PATH"
2. Or manually add Python to system PATH

### Problem: "Module not found" error
**Solution:** Missing Python installation
- Tkinter and SQLite3 are built-in with Python
- Ensure you're using Python 3.7+

### Problem: Database file not found
**Solution:** Initialize the database
```bash
python database/db_manager.py
```

### Problem: Application won't start
**Solution:** Check file structure
- Ensure all files are in correct directories
- Verify `__init__.py` files exist in `database/` and `modules/`

### Problem: Permission denied error
**Solution:** Run with appropriate permissions
- Right-click Command Prompt → Run as Administrator

---

## 📊 Sample Data

The system includes sample inventory data for testing:
- T-Shirt (S, M, L, XL) - ₱250.00 each
- Polo Shirt (M, L) - ₱350.00 each
- Cap (One Size) - ₱150.00

You can delete or modify these after installation.

---

## 🔄 System Updates

To update the system:
1. **Backup your database file**
2. Replace Python files with new versions
3. Keep the `database/igp_sales.db` file
4. Restart the application

---

## 📞 Support & Contact

For technical support or issues:
- Contact: EVSU-OC IT Department
- Email: [Your Email Here]
- Location: EVSU Ormoc Campus

---

## 📝 System Limitations

1. **Single Computer Operation**
   - System runs on one computer only
   - No network or cloud sync capabilities

2. **No Multi-User Login**
   - No user authentication system
   - No role-based access control

3. **Print Functionality**
   - Reports can be viewed and captured
   - Native printing requires additional setup

4. **Offline Only**
   - No internet connectivity required
   - No cloud backup

---

## 🎓 Developer Notes

### Code Structure
- **MVC-inspired architecture**
- **Modular design** for easy maintenance
- **Extensive comments** for beginners
- **Error handling** throughout

### Extending the System

#### Adding New Features
1. Create new module in `modules/` directory
2. Import in `main.py`
3. Add navigation button
4. Follow existing code patterns

#### Database Modifications
1. Update schema in `db_manager.py`
2. Add corresponding CRUD operations
3. Update UI components accordingly

---

## 📜 License

This system is developed for **Eastern Visayas State University - Ormoc Campus** for internal use in the Income Generating Project.

---

## ✅ System Checklist

Before deploying to production:

- [ ] Python 3.7+ installed
- [ ] Database initialized with sample data
- [ ] All modules tested
- [ ] Backup procedure documented
- [ ] Staff trained on system usage
- [ ] Emergency contact information available

---

## 🎉 Version History

**Version 1.0.0** (Initial Release)
- Transaction Entry Module
- Inventory Management Module
- Sales History Viewer
- Monthly Reports Generator
- SQLite Database Integration
- Complete User Interface

---

**Developed with ❤️ for EVSU-OC**

*This system replaces manual logbooks and Excel files, providing a modern, efficient solution for tracking IGP sales at Eastern Visayas State University - Ormoc Campus.*
