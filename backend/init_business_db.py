import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = "data/business.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create sales table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        amount REAL,
        region TEXT,
        product TEXT,
        customer_type TEXT
    )
    ''')
    
    # Clear existing data just in case
    cursor.execute('DELETE FROM sales')

    # Generate some mock data for Q3 and Q4 2023
    regions = ['North', 'South', 'East', 'West']
    products = ['Laptop', 'Smartphone', 'Tablet', 'Monitor']
    customer_types = ['Retail', 'Enterprise', 'SMB']
    
    start_date = datetime(2023, 7, 1)
    end_date = datetime(2023, 12, 31)
    
    delta = end_date - start_date
    
    for _ in range(200):
        random_days = random.randrange(delta.days)
        sale_date = start_date + timedelta(days=random_days)
        date_str = sale_date.strftime('%Y-%m-%d')
        
        amount = round(random.uniform(100.0, 5000.0), 2)
        region = random.choice(regions)
        product = random.choice(products)
        customer_type = random.choice(customer_types)
        
        cursor.execute('''
        INSERT INTO sales (date, amount, region, product, customer_type)
        VALUES (?, ?, ?, ?, ?)
        ''', (date_str, amount, region, product, customer_type))

    conn.commit()
    print(f"Successfully populated {DB_PATH} with 200 mock sales records.")
    
    # Verify
    cursor.execute('SELECT COUNT(*) FROM sales')
    count = cursor.fetchone()[0]
    print(f"Total rows in sales table: {count}")
    
    conn.close()

if __name__ == '__main__':
    init_db()
