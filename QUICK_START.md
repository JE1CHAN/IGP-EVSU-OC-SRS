# EVSU-OC IGP Sales Record System - Quick Start Guide

## 🚀 Quick Start (First Time Users)

### Step 1: Initialize Database
1. Double-click **`SETUP_DATABASE.bat`**
2. Press any key when prompted
3. Wait for "SUCCESS" message
4. Press any key to close

### Step 2: Run the System
1. Double-click **`RUN_SYSTEM.bat`**
2. The application window will open
3. Start using the system!

---

## 📝 Quick Operations Guide

### Adding Your First Product
1. Click **"Inventory"** in the menu
2. Click **"➕ Add New Product"**
3. Fill in:
   - Product Name: e.g., "School T-Shirt"
   - Size: e.g., "M"
   - Initial Stock: e.g., 100
   - Price: e.g., 250.00
4. Click **"💾 Save"**

### Recording Your First Sale
1. Click **"Transaction Entry"** in the menu
2. Fill in:
   - Buyer Name: Customer's name
   - Product: Select from dropdown
   - Size: Select from dropdown
   - Quantity: Number of items
   - OR Number: Official receipt number
   - Date: Today's date (auto-filled)
3. Click **"💾 SAVE TRANSACTION"**

### Viewing Sales
1. Click **"Sales History"**
2. See all transactions
3. Use filters to search specific transactions

### Generating Reports
1. Click **"Reports"**
2. Choose:
   - **Monthly Report**: Select month & year
   - **Custom Report**: Enter date range
3. Click generate button
4. View and print report

---

## ⚠️ Important Tips

### Daily Backup
- Copy `database/igp_sales.db` to a safe location
- Do this at the end of each day
- Rename with date: `igp_sales_2024-11-27.db`

### Date Format
- Always use: **YYYY-MM-DD**
- Example: 2024-11-27

### Stock Warnings
- 🟢 Green numbers = Good stock
- 🔴 Red numbers = Low stock (less than 10)
- Red background = Out of stock

---

## 🆘 Common Issues

### "Python is not recognized"
- **Fix**: Install Python from https://www.python.org/downloads/
- Check "Add Python to PATH" during installation

### Database not found
- **Fix**: Run `SETUP_DATABASE.bat` first

### Cannot save transaction
- **Fix**: Check if product has available stock
- Check if all fields are filled correctly

---

## 📞 Need Help?

Contact EVSU-OC IT Department for assistance.

---

**Quick Reference Card**

| Task | Steps |
|------|-------|
| **Start System** | Double-click `RUN_SYSTEM.bat` |
| **Add Product** | Inventory → Add New Product |
| **Record Sale** | Transaction Entry → Fill Form → Save |
| **View History** | Sales History → Use Filters |
| **Generate Report** | Reports → Select Period → Generate |
| **Backup Data** | Copy `database/igp_sales.db` file |

---

✅ **System is ready to use!**
