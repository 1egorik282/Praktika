from basa_dannix import get_connection
from Models.country import Country

class Hotel:
    def __init__(self, id=None, name=None, category=3, address=None, country_id=None):
        self.id = id
        self.name = name
        self.category = category
        self.address = address
        self.country_id = country_id

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            cursor.execute("""
            INSERT INTO hotels (name, category, address, country_id)
            VALUES (?, ?, ?, ?)
            """, (self.name, self.category, self.address, self.country_id))
            self.id = cursor.lastrowid
        else:
            cursor.execute("""
            UPDATE hotels SET name=?, category=?, address=?, country_id=?
            WHERE id=?
            """, (self.name, self.category, self.address, self.country_id, self.id))
        
        conn.commit()
        conn.close()

    def delete(self):
        if self.id:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM hotels WHERE id=?", (self.id,))
            conn.commit()
            conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hotels")
        rows = cursor.fetchall()
        conn.close()
        print("\n🏨 Список отелей:")
        return [Hotel(*row) for row in rows]

    @staticmethod
    def get_by_id(hotel_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hotels WHERE id=?", (hotel_id,))
        row = cursor.fetchone()
        conn.close()
        return Hotel(*row) if row else None

    @staticmethod
    def get_by_country(country_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hotels WHERE country_id=?", (country_id,))
        rows = cursor.fetchall()
        conn.close()
        return [Hotel(*row) for row in rows]