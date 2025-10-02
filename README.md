# Financial Data Visualization
ull stack finance dashboard: Upload Excel files, store data in MySQL, display in table & chart

# Finance Dashboard

## Description
This is a **full stack web application** that allows users to upload Excel files containing monthly financial data. The data is stored in a MySQL database and visualized on a dashboard as a table and bar chart.  

---

## Features
- Upload Excel files (`.xlsx`) for specific users and years.
- Store data in MySQL tables: `users` and `financial_records`.
- Display uploaded data in a table.
- Visualize data in a bar chart using Chart.js.

---

## Technology Stack
- **Backend:** Python with Flask  
- **Database:** MySQL  
- **Frontend:** HTML, JavaScript, Chart.js  

---

## How to Run
1. Make sure **MySQL** is running and your database is set up (`finance_db`).  
2. Start the **Flask backend**:  
   ```bash
   python finance_api.py
