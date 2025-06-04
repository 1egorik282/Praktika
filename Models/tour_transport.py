from basa_dannix import get_connection

class TourTransport:
    def __init__(self, id=None, tour_id=None, transport_type=None, cost=0):
        self.id = id
        self.tour_id = tour_id
        self.transport_type = transport_type
        self.cost = cost

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute("""
            INSERT INTO tour_transports (tour_id, transport_type, cost)
            VALUES (?, ?, ?)
            """, (self.tour_id, self.transport_type, self.cost))
            self.id = cursor.lastrowid
        else:
            cursor.execute("""
            UPDATE tour_transports SET tour_id=?, transport_type=?, cost=?
            WHERE id=?
            """, (self.tour_id, self.transport_type, self.cost, self.id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tour_transports")
        rows = cursor.fetchall()
        conn.close()
        return [TourTransport(*row) for row in rows]

    @staticmethod
    def get_by_tour(tour_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tour_transports WHERE tour_id=?", (tour_id,))
        rows = cursor.fetchall()
        conn.close()
        return [TourTransport(*row) for row in rows]