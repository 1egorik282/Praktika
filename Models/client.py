from basa_dannix import get_connection

class Client:
    def __init__(self, id=None, surname=None, name=None, patronymic=None, address=None, phone=None):
        self.id = id
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.address = address
        self.phone = phone

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            cursor.execute("""
            INSERT INTO clients (surname, name, patronymic, address, phone)
            VALUES (?, ?, ?, ?, ?)
            """, (self.surname, self.name, self.patronymic, self.address, self.phone))
            self.id = cursor.lastrowid
        else:
            cursor.execute("""
            UPDATE clients SET surname=?, name=?, patronymic=?, address=?, phone=?
            WHERE id=?
            """, (self.surname, self.name, self.patronymic, self.address, self.phone, self.id))
        
        conn.commit()
        conn.close()

    def delete(self):
        if self.id:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clients WHERE id=?", (self.id,))
            conn.commit()
            conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients")
        rows = cursor.fetchall()
        conn.close()
        return [Client(*row) for row in rows]

    @staticmethod
    def get_by_id(client_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE id=?", (client_id,))
        row = cursor.fetchone()
        conn.close()
        return Client(*row) if row else None