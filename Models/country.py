from basa_dannix import get_connection

class Country:
    def __init__(self, id=None, name=None, climate=None, visa_required=False):
        self.id = id
        self.name = name
        self.climate = climate
        self.visa_required = visa_required

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            cursor.execute("""
            INSERT INTO countries (name, climate, visa_required)
            VALUES (?, ?, ?)
            """, (self.name, self.climate, self.visa_required))
            self.id = cursor.lastrowid
        else:
            cursor.execute("""
            UPDATE countries SET name=?, climate=?, visa_required=?
            WHERE id=?
            """, (self.name, self.climate, self.visa_required, self.id))
        
        conn.commit()
        conn.close()

    def delete(self):
        if self.id:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM countries WHERE id=?", (self.id,))
            conn.commit()
            conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM countries")
        rows = cursor.fetchall()
        conn.close()
        print("\n🌍 Список стран:")
        return [Country(*row) for row in rows]

    @staticmethod
    def get_by_id(country_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM countries WHERE id=?", (country_id,))
        row = cursor.fetchone()
        conn.close()
        return Country(*row) if row else None