from basa_dannix import get_connection
from Models.client import Client
from Models.country import Country
from Models.hotel import Hotel
from Models.tour import Tour
from datetime import date

class Sale:
    def __init__(self, id=None, client_id=None, tour_id=None, sale_date=None, 
                 discount=0, total_price=0, departure_date=None):
        self.id = id
        self.client_id = client_id
        self.tour_id = tour_id
        self.sale_date = sale_date or date.today().strftime("%Y-%m-%d")
        self.discount = discount
        self.total_price = total_price
        self.departure_date = departure_date

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        # Рассчитываем цену с учетом скидок
        tour = Tour.get_by_id(self.tour_id)
        country = Country.get_by_id(Hotel.get_by_id(tour.hotel_id).country_id)
        
        # Базовая цена
        base_price = tour.base_price
        
        # Добавляем стоимость визы, если требуется
        visa_cost = 5000 if country.visa_required else 0
        
        # Применяем скидки (суммируются)
        total_discount = self.discount
        
        # Итоговая цена
        self.total_price = (base_price + visa_cost) * (1 - total_discount/100)

        if self.id is None:
            cursor.execute("""
            INSERT INTO sales (client_id, tour_id, sale_date, discount, total_price, departure_date)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (self.client_id, self.tour_id, self.sale_date, self.discount, 
                  self.total_price, self.departure_date))
            self.id = cursor.lastrowid
        else:
            cursor.execute("""
            UPDATE sales SET client_id=?, tour_id=?, sale_date=?, 
                            discount=?, total_price=?, departure_date=?
            WHERE id=?
            """, (self.client_id, self.tour_id, self.sale_date, self.discount, 
                  self.total_price, self.departure_date, self.id))
        
        conn.commit()
        conn.close()

    def delete(self):
        if self.id:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sales WHERE id=?", (self.id,))
            conn.commit()
            conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sales")
        rows = cursor.fetchall()
        conn.close()
        print("\n💰 Список продаж:")
        return [Sale(*row) for row in rows]

    @staticmethod
    def get_by_id(sale_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sales WHERE id=?", (sale_id,))
        row = cursor.fetchone()
        conn.close()
        return Sale(*row) if row else None

    @staticmethod
    def get_by_client(client_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sales WHERE client_id=?", (client_id,))
        rows = cursor.fetchall()
        conn.close()
        return [Sale(*row) for row in rows]