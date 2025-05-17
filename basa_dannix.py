import sqlite3
from config import DB_NAME

def get_connection():
    return sqlite3.connect(DB_NAME)

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Страны
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS countries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        climate TEXT,
        visa_required BOOLEAN
    )
    ''')
    
    # Отели
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hotels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category INTEGER,
        address TEXT,
        country_id INTEGER,
        FOREIGN KEY (country_id) REFERENCES countries(id)
    )
    ''')
    
    # Клиенты
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        surname TEXT,
        name TEXT,
        patronymic TEXT,
        address TEXT,
        phone TEXT
    )
    ''')
    
    # Туры
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tours (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        duration INTEGER,
        base_price REAL,
        hotel_id INTEGER,
        FOREIGN KEY (hotel_id) REFERENCES hotels(id)
    )
    ''')
    
    # Продажи
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        tour_id INTEGER,
        sale_date DATE,
        discount REAL DEFAULT 0,
        total_price REAL,
        departure_date DATE,
        FOREIGN KEY (client_id) REFERENCES clients(id),
        FOREIGN KEY (tour_id) REFERENCES tours(id)
    )
    ''')
    
    conn.commit()
    conn.close()