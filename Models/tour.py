from basa_dannix import get_connection
from Models.hotel import Hotel

class Tour:
    def __init__(self, id=None, duration=7, base_price=0, hotel_id=None):
        self.id = id
        self.duration = duration
        self.base_price = base_price
        self.hotel_id = hotel_id

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            cursor.execute("""
            INSERT INTO tours (duration, base_price, hotel_id)
            VALUES (?, ?, ?)
            """, (self.duration, self.base_price, self.hotel_id))
            self.id = cursor.lastrowid
        else:
            cursor.execute("""
            UPDATE tours SET duration=?, base_price=?, hotel_id=?
            WHERE id=?
            """, (self.duration, self.base_price, self.hotel_id, self.id))
        
        conn.commit()
        conn.close()

    def delete(self):
        if self.id:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tours WHERE id=?", (self.id,))
            conn.commit()
            conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tours")
        rows = cursor.fetchall()
        conn.close()
        print("\n🧳 Список туров:")
        return [Tour(*row) for row in rows]

    @staticmethod
    def get_by_id(tour_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tours WHERE id=?", (tour_id,))
        row = cursor.fetchone()
        conn.close()
        return Tour(*row) if row else None

    @staticmethod
    def get_by_hotel(hotel_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tours WHERE hotel_id=?", (hotel_id,))
        rows = cursor.fetchall()
        conn.close()
        return [Tour(*row) for row in rows]