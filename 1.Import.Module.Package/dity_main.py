from app.salary import *
from app.db.people import *
import pandas

if __name__ == '__main__':
    from datetime import datetime

    print(f"Текущая дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    calculate_salary()
    get_employees()
