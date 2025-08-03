# 🚗 Smart Parking Management System

A Python-based desktop application built with **PyQt5** for managing parking slots, vehicle entries/exits, and generating invoices automatically. It is designed for small to mid-sized parking lots and offers a user-friendly GUI with automated billing and history tracking.


## 💡 Features

- ✅ Visual parking slot tracking (up to 50 slots)
- 🚗 Add and manage vehicle entries and exits
- 🧾 Auto-generate invoices with duration & billing
- 🕑 Records entry/exit time with per-hour charges
- 📜 History of all vehicle visits
- 💾 Local storage with `SQLite` or `JSON` config
- 📷 Save invoices as image files

---

## 📂 Project Structure

SmartParkingSystem/
│
├── main.py # Main execution file
├── InstallWindow.py # Setup screen
├── LoginWindow.py # Login screen logic
├── Dashboard.py # Main dashboard with slot GUI
├── AddVehicleWindow.py # Form to add vehicles
├── ManageVehicleWindow.py # Entry/exit & billing
├── HistoryWindow.py # Complete log viewer
├── config.json # Generated after setup
├── database.db # SQLite database
└── images/ # Splash and UI images

### Prerequisites

- Python 3.7+
- `pip` package manager

### Install Dependencies

```bash
pip install -r requirements.txt

Note: If requirements.txt is not available, install manually:

bash
Copy
Edit
pip install PyQt5
🚀 Getting Started
Run the app:

bash
Copy
Edit
python main.py
If config.json is not found, you'll be redirected to a setup window.

Once set up, you'll be taken to the login screen.

💸 Billing Logic
Charges are calculated per hour.

Currently set to:

₹20/hour for 2-Wheelers

₹50/hour for 4-Wheelers

Invoices are generated with:

Entry time

Exit time

Duration

Total amount

Invoices can be saved as JPG.

📊 Database
Stores vehicle information, timestamps, and history.

Can be customized to use other databases (e.g., MySQL).

📦 Future Improvements
 Admin/User roles

 Search/filter in history

 Export to PDF/Excel

 Web version (Flask/Django backend)
