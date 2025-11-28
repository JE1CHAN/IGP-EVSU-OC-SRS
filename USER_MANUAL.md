# EVSU-OC IGP Sales Record System - User Manual

## Table of Contents
1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
4. [Getting Started](#getting-started)
5. [Module Guides](#module-guides)
6. [Troubleshooting](#troubleshooting)
7. [Maintenance](#maintenance)

---

## 1. Introduction

### What is the EVSU-OC IGP Sales Record System?

The EVSU-OC IGP Sales Record System is a desktop application designed specifically for the Eastern Visayas State University - Ormoc Campus Income Generating Project. It replaces the traditional paper logbook and Excel spreadsheet method of recording sales transactions.

### Key Benefits
- ✅ Eliminates manual data entry errors
- ✅ Automatic stock tracking
- ✅ Instant sales reports
- ✅ Searchable transaction history
- ✅ Professional report generation
- ✅ No internet connection required

### Who Should Use This System?
- IGP staff recording daily sales
- Administrators reviewing sales data
- Inventory managers tracking stock levels
- Finance officers generating monthly reports

---

## 2. System Requirements

### Minimum Requirements
- **Operating System**: Windows 7 or higher
- **Processor**: Intel Core i3 or equivalent
- **RAM**: 4 GB
- **Hard Drive Space**: 100 MB
- **Display**: 1024x768 resolution
- **Software**: Python 3.7 or higher

### Recommended Requirements
- **Operating System**: Windows 10/11
- **Processor**: Intel Core i5 or higher
- **RAM**: 8 GB
- **Hard Drive Space**: 500 MB (for long-term data storage)
- **Display**: 1366x768 or higher resolution

---

## 3. Installation

### 3.1 Installing Python

1. **Download Python**
   - Visit: https://www.python.org/downloads/
   - Download Python 3.7 or higher
   - Choose Windows installer (64-bit recommended)

2. **Install Python**
   - Run the downloaded installer
   - ✅ **IMPORTANT**: Check "Add Python to PATH"
   - Click "Install Now"
   - Wait for installation to complete
   - Click "Close"

3. **Verify Installation**
   - Open Command Prompt (Win + R, type `cmd`, press Enter)
   - Type: `python --version`
   - You should see: `Python 3.x.x`

### 3.2 Setting Up the System

1. **Extract Files**
   - Extract the system ZIP file
   - Place in a permanent location (e.g., `C:\IGP-System\`)
   - **Do not** place on Desktop if multiple users will access it

2. **Initialize Database**
   - Navigate to the system folder
   - Double-click `SETUP_DATABASE.bat`
   - Press any key when prompted
   - Wait for success message
   - Database is now ready

3. **Test Run**
   - Double-click `RUN_SYSTEM.bat`
   - Application window should open
   - If successful, installation is complete!

---

## 4. Getting Started

### 4.1 First Launch

When you first run the system:
1. Main window opens with blue header
2. Left sidebar shows menu options
3. Transaction Entry module is displayed by default
4. Sample products are available (if database was initialized)

### 4.2 Navigation

The system has 5 main sections:

| Menu Item | Purpose |
|-----------|---------|
| 📝 Transaction Entry | Record daily sales |
| 📦 Inventory | Manage products and stock |
| 📊 Sales History | View and search transactions |
| 📈 Reports | Generate sales reports |
| ❌ Exit | Close the application |

**Navigation**: Click any menu button to switch between modules

### 4.3 Understanding the Interface

#### Header Section
- Displays system name and university
- Always visible at the top
- Blue background with white text

#### Left Sidebar (Menu)
- Dark gray background
- Large, easy-to-read buttons
- Active module highlighted in teal/green

#### Main Content Area
- White background
- Changes based on selected module
- Scrollable for long content

---

## 5. Module Guides

### 5.1 Transaction Entry Module

**Purpose**: Record daily sales transactions

#### Step-by-Step Process:

1. **Enter Buyer Information**
   - Click in "Buyer Name" field
   - Type customer's full name
   - Example: "Juan Dela Cruz" or "Maria Santos"

2. **Select Product**
   - Click "Product" dropdown
   - Select desired product
   - Available products load from inventory

3. **Select Size**
   - Click "Size" dropdown
   - Select appropriate size
   - Available sizes depend on selected product
   - Stock information appears in red text

4. **Enter Quantity**
   - Click "Quantity" field
   - Type number of items
   - Must be a positive whole number
   - Cannot exceed available stock
   - Total amount calculates automatically

5. **Review Total Amount**
   - Displayed in green bold text
   - Format: ₱XXX.XX
   - Calculated automatically from quantity × price

6. **Enter OR Number**
   - Click "OR Number" field
   - Type the official receipt number
   - Required for each transaction

7. **Check Date**
   - Date field shows today's date
   - Format: YYYY-MM-DD
   - Can be modified if needed

8. **Save Transaction**
   - Click "💾 SAVE TRANSACTION" button
   - System validates all fields
   - If valid:
     - Transaction saved to database
     - Stock automatically deducted
     - Success message appears
     - Form clears for next transaction
   - If invalid:
     - Error message shows which field needs correction

9. **Clear Form** (if needed)
   - Click "🔄 CLEAR FORM" button
   - All fields reset
   - No data is saved

#### Common Validations:
- ❌ Empty buyer name → "Please enter buyer name"
- ❌ No product selected → "Please select a product"
- ❌ Invalid quantity → "Please enter a valid quantity"
- ❌ Insufficient stock → "Only X items available"
- ❌ Empty OR number → "Please enter OR number"
- ❌ Invalid date format → "Please enter valid date (YYYY-MM-DD)"

---

### 5.2 Inventory Management Module

**Purpose**: Manage products, sizes, and stock levels

#### Viewing Inventory:
- Table shows all products with columns:
  - ID: Unique identifier
  - Product Name: Name of item
  - Size: Size designation
  - Available Stock: Current quantity
  - Price: Unit price in pesos

#### Stock Level Indicators:
- **White background**: Normal stock (10+ items)
- **Light red background**: Low stock (1-9 items)
- **Dark red background**: Out of stock (0 items)

#### Adding New Products:

1. Click "➕ Add New Product" button
2. Dialog window opens
3. Fill in fields:
   - **Product Name**: Enter descriptive name
     - Example: "EVSU T-Shirt", "School Cap"
   - **Size**: Enter size designation
     - Examples: "S", "M", "L", "XL", "One Size"
   - **Initial Stock**: Enter starting quantity
     - Must be 0 or greater
   - **Price**: Enter price per unit
     - Format: XXX.XX (no peso sign)
     - Example: 250.00
4. Click "💾 Save"
5. Product appears in inventory table

**Important Notes:**
- Each product + size combination is unique
- You can have same product in multiple sizes
- Each size is tracked separately

#### Updating Products:

1. Click on product row to select it
2. Click "✏️ Update Product" button
3. Dialog opens with current values
4. Modify fields as needed:
   - Product name
   - Size
   - Stock quantity
   - Price
5. Click "💾 Update"
6. Changes saved immediately

**Use Cases for Updates:**
- Correcting typos
- Adjusting prices
- Adding stock (restocking)
- Modifying product names

#### Deleting Products:

1. Click on product row to select it
2. Click "🗑️ Delete Product" button
3. Confirmation dialog appears
4. Click "Yes" to confirm deletion
5. Product removed from inventory

**Warning**: Deleting a product does NOT delete its transaction history. Past sales remain in the system.

#### Refreshing Display:
- Click "🔄 Refresh" button
- Reloads all data from database
- Use after another user makes changes

---

### 5.3 Sales History Module

**Purpose**: View and search all transaction records

#### Viewing All Transactions:

When you open this module:
- Table shows all transactions (newest first)
- Summary shows: Total Transactions | Total Revenue
- Columns display:
  - ID: Transaction number
  - Buyer Name: Customer name
  - Product: Item purchased
  - Size: Size purchased
  - Qty: Quantity sold
  - Amount: Total price
  - OR Number: Official receipt
  - Date: Transaction date

#### Searching Transactions:

**Search by Buyer Name:**
1. Type name in "Buyer Name" field
2. Partial match supported
3. Example: "Juan" finds "Juan Dela Cruz"

**Search by Product:**
1. Type product name in "Product" field
2. Partial match supported
3. Example: "Shirt" finds "T-Shirt" and "Polo Shirt"

**Search by OR Number:**
1. Type OR number in "OR Number" field
2. Exact or partial match
3. Useful for receipt verification

**Search by Date Range:**
1. Enter "From Date" in format: YYYY-MM-DD
2. Enter "To Date" in format: YYYY-MM-DD
3. Finds all transactions between dates (inclusive)

**Execute Search:**
- Click "🔍 Search" button
- Results display in table
- Summary updates with filtered totals

**Clear Filters:**
- Click "🔄 Clear Filters" button
- All filters reset
- Shows all transactions again

#### Search Examples:

**Example 1**: Find all purchases by specific person
- Buyer Name: "Maria Santos"
- Leave other fields empty
- Click Search

**Example 2**: Find all T-Shirt sales in November
- Product: "T-Shirt"
- From Date: 2024-11-01
- To Date: 2024-11-30
- Click Search

**Example 3**: Find specific OR number
- OR Number: "12345"
- Leave other fields empty
- Click Search

---

### 5.4 Reports Module

**Purpose**: Generate formatted sales reports for specific periods

#### Generating Monthly Reports:

1. **Select Month**
   - Click "Month" dropdown
   - Choose from January to December
   - Default: Current month

2. **Enter Year**
   - Type year in "Year" field
   - Example: 2024
   - Default: Current year

3. **Generate Report**
   - Click "📊 Generate Monthly Report"
   - Report window opens
   - Shows data for entire month

#### Generating Custom Date Range Reports:

1. **Enter Start Date**
   - Type in "From" field
   - Format: YYYY-MM-DD
   - Example: 2024-11-01

2. **Enter End Date**
   - Type in "To" field
   - Format: YYYY-MM-DD
   - Example: 2024-11-30

3. **Generate Report**
   - Click "📊 Generate Custom Report"
   - Report window opens
   - Shows data for specified range

#### Understanding Report Contents:

**Header Section:**
- System name
- Report title
- Generation date and time

**Summary Section:**
- **Total Transactions**: Number of sales recorded
- **Total Items Sold**: Sum of all quantities
- **Total Revenue**: Sum of all amounts (in green)

**Product Summary Section:**
- Lists each product sold
- Shows size breakdown
- Total quantity per product+size
- Total revenue per product+size
- Useful for inventory planning

**Detailed Transactions Section:**
- Complete list of all transactions
- Chronologically ordered
- All transaction details included
- Useful for auditing

#### Report Actions:

**Print Report:**
- Click "🖨️ Print Report" button
- Instructions appear for manual printing
- Take screenshot or use print screen
- Alternative: Export to PDF (future feature)

**Close Report:**
- Click "❌ Close" button
- Returns to Reports module
- Report data still accessible by regenerating

---

## 6. Troubleshooting

### Problem: Application won't start

**Symptoms:**
- Double-clicking RUN_SYSTEM.bat does nothing
- Error message appears
- Window closes immediately

**Solutions:**

1. **Check Python Installation**
   ```
   Open Command Prompt
   Type: python --version
   Should show: Python 3.x.x
   If not: Reinstall Python (see Installation section)
   ```

2. **Verify File Structure**
   ```
   Ensure these exist:
   - main.py
   - database/ folder
   - modules/ folder
   ```

3. **Run from Command Prompt**
   ```
   cd "C:\path\to\system"
   python main.py
   ```
   Check error messages for clues

### Problem: Database not found

**Symptoms:**
- Error: "No such table"
- Empty inventory
- Cannot save transactions

**Solutions:**

1. **Initialize Database**
   ```
   Run SETUP_DATABASE.bat
   Wait for success message
   ```

2. **Check Database File**
   ```
   Look in database/ folder
   Should have: igp_sales.db
   If missing, run setup again
   ```

### Problem: Cannot save transaction

**Symptoms:**
- Error message when saving
- "Failed to save transaction"

**Solutions:**

1. **Check Stock Availability**
   - Go to Inventory module
   - Verify product has sufficient stock
   - If stock is 0, cannot sell

2. **Verify All Fields**
   - Buyer name filled
   - Product selected
   - Size selected
   - Quantity > 0
   - OR number entered
   - Date in correct format

3. **Check Database Permissions**
   - Database file not read-only
   - Folder has write permissions
   - No other program accessing database

### Problem: Products not appearing

**Symptoms:**
- Empty dropdowns in Transaction Entry
- No products in Inventory

**Solutions:**

1. **Add Products First**
   - Go to Inventory module
   - Click Add New Product
   - Add at least one product

2. **Refresh Display**
   - Click Refresh button
   - Reload module

### Problem: Incorrect calculations

**Symptoms:**
- Total amount wrong
- Stock not deducting

**Solutions:**

1. **Verify Quantity**
   - Ensure you entered correct number
   - No decimals allowed

2. **Check Price**
   - Go to Inventory
   - Verify product price is correct
   - Update if needed

3. **Refresh Transaction Entry**
   - Exit and return to module
   - Select product again

### Problem: Report shows no data

**Symptoms:**
- Empty report
- "No transactions found"

**Solutions:**

1. **Verify Date Range**
   - Check start and end dates
   - Ensure transactions exist in that period
   - Try wider date range

2. **Check Transaction History**
   - Go to Sales History module
   - Verify transactions were recorded
   - If empty, no data to report

### Problem: Slow performance

**Symptoms:**
- Application lagging
- Long load times

**Solutions:**

1. **Close Other Programs**
   - Free up system resources
   - Especially other database programs

2. **Database Optimization**
   - Backup current database
   - Create new database
   - Import essential data only

3. **System Resources**
   - Check RAM usage
   - Ensure adequate disk space
   - Scan for viruses

---

## 7. Maintenance

### 7.1 Daily Maintenance

**End of Day Procedure:**

1. **Close All Transactions**
   - Ensure all sales recorded
   - Verify last OR number

2. **Backup Database**
   ```
   Steps:
   1. Close the application
   2. Go to database/ folder
   3. Copy igp_sales.db
   4. Paste to backup location
   5. Rename: igp_sales_YYYY-MM-DD.db
   6. Example: igp_sales_2024-11-27.db
   ```

3. **Quick Inventory Check**
   - Review low stock items
   - Note items needing restock
   - Report to procurement

### 7.2 Weekly Maintenance

**Every Week:**

1. **Verify Backups**
   - Check backup folder
   - Should have 7 daily backups
   - Delete backups older than 30 days

2. **Review Sales Data**
   - Generate weekly report
   - Check for unusual transactions
   - Verify data accuracy

3. **Clean Workspace**
   - Close unnecessary windows
   - Organize desktop
   - Update OR number log

### 7.3 Monthly Maintenance

**End of Month:**

1. **Generate Monthly Report**
   - Create official monthly report
   - Print for records
   - File in appropriate folder

2. **Inventory Reconciliation**
   - Physical count of actual stock
   - Compare with system stock
   - Adjust if needed

3. **Monthly Backup**
   - Create special monthly backup
   - Archive to external drive
   - Label: MONTHLY_YYYY_MM.db
   - Store securely

4. **System Health Check**
   - Review error logs
   - Check disk space
   - Update if needed

### 7.4 Database Backup Locations

**Recommended Backup Strategy:**

**Primary Backup** (Daily)
- Location: External USB drive
- Frequency: Daily
- Retention: 30 days

**Secondary Backup** (Weekly)
- Location: Network drive or cloud storage
- Frequency: Weekly
- Retention: 3 months

**Archive Backup** (Monthly)
- Location: External hard drive (off-site)
- Frequency: Monthly
- Retention: Permanent

### 7.5 Data Recovery

**If Database is Corrupted:**

1. **Stop Using System Immediately**
   - Don't try to save new transactions
   - Close the application

2. **Restore from Backup**
   ```
   Steps:
   1. Locate latest backup file
   2. Close application
   3. Go to database/ folder
   4. Rename corrupted: igp_sales_BAD.db
   5. Copy backup file
   6. Rename to: igp_sales.db
   7. Restart application
   ```

3. **Verify Restoration**
   - Check recent transactions
   - Verify inventory counts
   - Generate test report

4. **Resume Operations**
   - Re-enter missing transactions (if any)
   - Continue normal use
   - Document incident

### 7.6 System Updates

**When Updates are Available:**

1. **Backup Current System**
   - Backup database
   - Copy entire system folder

2. **Download Update**
   - Get update files
   - Verify source

3. **Apply Update**
   - Close application
   - Replace Python files only
   - Keep database file
   - Keep configuration

4. **Test Update**
   - Run system
   - Test all modules
   - Verify data intact

5. **Resume Operations**
   - If successful, continue use
   - If problems, restore backup

---

## 8. Best Practices

### Data Entry Best Practices

1. **Double-Check Before Saving**
   - Verify customer name spelling
   - Confirm quantity
   - Check OR number accuracy

2. **Use Consistent Naming**
   - Standardize product names
   - Consistent size labels
   - Uniform naming conventions

3. **Record Immediately**
   - Enter transactions as they occur
   - Don't batch at end of day
   - Reduces errors

### Inventory Management Best Practices

1. **Regular Stock Checks**
   - Weekly physical counts
   - Compare with system
   - Adjust discrepancies promptly

2. **Reorder Points**
   - Set minimum stock levels
   - Reorder when reaching threshold
   - Prevent stockouts

3. **Product Organization**
   - Group related products
   - Consistent size orders (S, M, L, XL)
   - Clear naming

### Report Generation Best Practices

1. **Regular Reporting**
   - Weekly summaries
   - Monthly detailed reports
   - Quarterly reviews

2. **Archive Reports**
   - Print important reports
   - File chronologically
   - Digital backup copies

3. **Data Analysis**
   - Identify best sellers
   - Spot trends
   - Plan inventory accordingly

---

## 9. Frequently Asked Questions (FAQ)

**Q: Can multiple users use the system simultaneously?**
A: No, this version is designed for single-computer use only.

**Q: Can I access the system from different computers?**
A: The database can be moved to a network location, but this requires additional configuration and is not officially supported.

**Q: What if I make a mistake in a transaction?**
A: Currently, there is no edit feature. Contact your supervisor for manual correction in the database.

**Q: Can I delete a transaction?**
A: No, for audit purposes, transactions cannot be deleted from the interface. Contact your IT administrator if absolutely necessary.

**Q: How far back can I search transactions?**
A: All transactions since system installation are searchable indefinitely.

**Q: What format should dates be in?**
A: Always use YYYY-MM-DD format (e.g., 2024-11-27).

**Q: Can I export reports to Excel?**
A: Not in the current version. Reports can be printed or captured as screenshots.

**Q: What happens if the power goes out?**
A: Only unsaved transactions are lost. Saved transactions are immediately written to the database.

**Q: Can I change prices after adding products?**
A: Yes, use the Update Product function in Inventory module.

**Q: How do I know if a backup is needed?**
A: Backup daily at minimum. More frequent backups recommended during busy periods.

---

## 10. Contact Information

**For Technical Support:**
- EVSU-OC IT Department
- Location: [Building/Office]
- Email: [Email Address]
- Phone: [Phone Number]

**For System Issues:**
- Report immediately to IT
- Provide error message if any
- Describe what you were doing
- Note time of error

**For Training:**
- New staff training available
- Refresher courses offered
- One-on-one assistance available

---

## 11. Appendices

### Appendix A: Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Tab | Move to next field |
| Shift + Tab | Move to previous field |
| Enter | (In buttons) Activate button |
| Escape | Close dialog windows |

### Appendix B: Error Messages

| Error Message | Meaning | Solution |
|---------------|---------|----------|
| "Please enter buyer name" | Buyer field empty | Enter customer name |
| "Please select a product" | No product chosen | Select from dropdown |
| "Insufficient stock" | Not enough items | Check inventory, reduce quantity |
| "Invalid quantity" | Wrong number format | Enter positive whole number |
| "Invalid date format" | Wrong date format | Use YYYY-MM-DD |
| "Failed to save transaction" | Database error | Check database permissions |

### Appendix C: File Locations

| File/Folder | Purpose | Location |
|-------------|---------|----------|
| main.py | Application entry | Root folder |
| database/ | Database folder | Root folder |
| igp_sales.db | Main database | database/ folder |
| modules/ | Program modules | Root folder |
| RUN_SYSTEM.bat | System launcher | Root folder |

---

**End of User Manual**

**Document Version**: 1.0  
**Last Updated**: November 27, 2024  
**System Version**: 1.0.0

---

*This manual is provided for EVSU-OC IGP staff use. For updates or corrections, contact the IT Department.*
