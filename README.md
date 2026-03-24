# 📅 Scheduling Manager
A Python CLI program to manage appointments: schedule, cancel, conclude, view alerts, and check tables, using PostgreSQL for data storage.

--------------------------------------------------------------------------------------------------------------------------

# 🛠 Features

* Schedule appointments with optional notes.
* Cancel appointments with a reason.
* Register concluded appointments with optional notes.
* Alerts for upcoming appointments within 7 days.
* View detailed tables for scheduled, canceled, or concluded appointments.
* Clear and colorful CLI interface for easy usage.

--------------------------------------------------------------------------------------------------------------------------

# 📝 Technologies Used

* Python 3.x
* SQLAlchemy (ORM)
* PostgreSQL
* Colorama (for terminal colors)
* Tabulate (for pretty tables)
* Custom utility module (`fanymodules`) for input validation

--------------------------------------------------------------------------------------------------------------------------

# ⚙ Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/scheduling.git
cd scheduling
```

2. **Install dependencies**

```bash
pip install sqlalchemy psycopg2-binary colorama tabulate
```

3. **Configure PostgreSQL**
   Update the `DATABASE_URL` in `main.py`:

```python
DATABASE_URL = "postgresql+psycopg2://username:password@localhost:5432/database_name"
```

Make sure the PostgreSQL server is running.

4. **Run the program**

```bash
python main.py
```

--------------------------------------------------------------------------------------------------------------------------

# 🧭 How to Use

 Menu Options

1. **Schedule Appointment** – Enter appointment details, date, and optional note.
2. **Cancel Appointment** – Cancel a scheduled appointment with a reason.
3. **Register Concluded Appointment** – Mark an appointment as concluded and add optional note.
4. **Check Alerts** – View upcoming appointments within the next 7 days.
5. **View Tables** – Check scheduled, canceled, or concluded appointments in a specific date range.

- Exit Program

--------------------------------------------------------------------------------------------------------------------------

## 💡 Notes

* All inputs are validated using the custom `fanymodules` library.
* Dates must be entered in **DD/MM/YYYY** format.
* Notes are optional when scheduling or concluding appointments.
