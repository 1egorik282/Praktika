from Models.client import Client
from basa_dannix import initialize_db
from Models.sale import Sale
from Models.tour import Tour
from Models.country import Country
from Models.hotel import Hotel
from Models.tour_transport import TourTransport

def show_main_menu():
    while True:
        print("\n✈️ === Туристическая фирма ===")
        print("1. 👤 Работа с клиентами")
        print("2. 🌍 Работа с турами")
        print("3. 💳 Продажи")
        print("0. 🛑 Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            client_menu()
        elif choice == "2":
            tour_menu()
        elif choice == "3":
            sale_menu()
        elif choice == "4":
            transport_menu()
        elif choice == "0":
            break
        else:
            print("❌ Неверный выбор")

def client_menu():
    while True:
        print("\n👤 === Работа с клиентами ===")
        print("1. ➕ Добавить клиента")
        print("2. 📋 Просмотреть клиентов")
        print("0. ◀️ Назад")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            surname = input("Фамилия: ")
            name = input("Имя: ")
            patronymic = input("Отчество: ")
            address = input("Адрес: ")
            phone = input("Телефон: ")
            
            client = Client(surname=surname, name=name, patronymic=patronymic, address=address, phone=phone)
            client.save()
            print("✅ Клиент сохранен!")
            
        elif choice == "2":
            clients = Client.get_all()
            print("\nСписок клиентов:")
            for c in clients:
                print(f"👤 {c.id}. {c.surname} {c.name} {c.patronymic}")
        elif choice == "0":
            break

def tour_menu():
    while True:
        print("\n🌍 === Работа с турами ===")
        print("1. 🌏 Добавить страну")
        print("2. 🏨 Добавить отель")
        print("3. ✈️ Добавить тур")
        print("4. 🗺️ Просмотреть все туры")
        print("5. ➕ Добавить транспорт к туру")
        print("6. 🚗 Просмотреть транспорт для тура")
        print("0. ◀️ Назад")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            name = input("Название страны: ")
            climate = input("Климат: ")
            visa = input("Нужна ли виза? (1-да, 0-нет): ")
            
            country = Country(name=name, climate=climate, visa_required=int(visa))
            country.save()
            print("Страна добавлена!")
            
        elif choice == "2":
            name = input("Название отеля: ")
            category = int(input("Категория (звёзд): "))
            address = input("Адрес: ")
            
            # Выбор страны
            countries = Country.get_all()
            for c in countries:
                print(f"{c.id}. {c.name}")
            country_id = int(input("ID страны: "))
            
            hotel = Hotel(name=name, category=category, address=address, country_id=country_id)
            hotel.save()
            print("Отель добавлен!")
            
        elif choice == "3":
            duration = int(input("Длительность (дни): "))
            price = float(input("Базовая цена: "))
            
            # Выбор отеля
            hotels = Hotel.get_all()
            for h in hotels:
                print(f"{h.id}. {h.name} ({h.category} звезд)")
            hotel_id = int(input("ID отеля: "))
            
            tour = Tour(duration=duration, base_price=price, hotel_id=hotel_id)
            tour.save()
            print("Тур добавлен!")
            
        elif choice == "4":
            tours = Tour.get_all()
            print("\nСписок туров:")
            for t in tours:
                hotel = Hotel.get_by_id(t.hotel_id)
                country = Country.get_by_id(hotel.country_id)
                transports = TourTransport.get_by_tour(t.id)
                transports_info = ", ".join([f"{tr.transport_type} ({tr.cost} руб.)" for tr in transports]) if transports else "Не указано"
                print(f"{t.id}. {country.name} - {hotel.name} ({t.duration} дней, {t.base_price} руб.) | Транспорт: {transports_info}")
        
        elif choice == "5":  # Добавление транспорта к туру
            tours = Tour.get_all()
            print("\nСписок туров:")
            for t in tours:
                hotel = Hotel.get_by_id(t.hotel_id)
                country = Country.get_by_id(hotel.country_id)
                print(f"{t.id}. {country.name} - {hotel.name} ({t.duration} дней)")
            tour_id = int(input("Введите ID тура: "))
            transport_type = input("Тип транспорта (самолет/поезд/автобус): ")
            cost = float(input("Стоимость транспорта: "))
            transport = TourTransport(tour_id=tour_id, transport_type=transport_type, cost=cost)
            transport.save()
            print("✅ Транспорт добавлен!")
        
        elif choice == "6":  # Просмотр транспорта для тура
            tour_id = int(input("Введите ID тура: "))
            transports = TourTransport.get_by_tour(tour_id)
            if transports:
                print(f"\nТранспорт для тура {tour_id}:")
                for tr in transports:
                    print(f"- {tr.transport_type} ({tr.cost} руб.)")
            else:
                print("⚠️ Для этого тура транспорт не указан.")
                        
        elif choice == "0":
            break

def transport_menu():
    while True:
        print("\n🚗 === Транспорт для туров ===")
        print("1. ➕ Добавить транспорт")
        print("2. 📋 Просмотреть транспорт для всех туров")
        print("3. 🔍 Просмотреть транспорт для конкретного тура")
        print("0. ◀️ Назад")
        choice = input("Выберите действие: ")
        
        if choice == "1":  # Добавление транспорта
            # Вывод списка туров
            tours = Tour.get_all()
            for t in tours:
                hotel = Hotel.get_by_id(t.hotel_id)
                country = Country.get_by_id(hotel.country_id)
                print(f"{t.id}. {country.name} - {hotel.name} ({t.duration} дней)")
            tour_id = int(input("Введите ID тура: "))
            
            # Ввод данных о транспорте
            transport_type = input("Тип транспорта (самолет/поезд/автобус): ")
            cost = float(input("Стоимость транспорта: "))
            
            # Сохранение в БД
            transport = TourTransport(tour_id=tour_id, transport_type=transport_type, cost=cost)
            transport.save()
            print("✅ Транспорт добавлен!")
        
        elif choice == "2":  # Просмотр всех транспортных опций
            transports = TourTransport.get_all()
            print("\nСписок транспортных опций:")
            for tr in transports:
                tour = Tour.get_by_id(tr.tour_id)
                hotel = Hotel.get_by_id(tour.hotel_id)
                country = Country.get_by_id(hotel.country_id)
                print(f"Тур: {country.name} - {hotel.name} | {tr.transport_type} ({tr.cost} руб.)")
        
        elif choice == "3":  # Просмотр транспорта по ID тура
            tour_id = int(input("Введите ID тура: "))
            transports = TourTransport.get_by_tour(tour_id)
            if transports:
                print(f"\nТранспорт для тура {tour_id}:")
                for tr in transports:
                    print(f"- {tr.transport_type} ({tr.cost} руб.)")
            else:
                print("⚠️ Для этого тура транспорт не указан.")
        
        elif choice == "0":
            break

def sale_menu():
    while True:
        print("\n💳 === Продажи ===")
        print("1. 📦 Оформить продажу")
        print("2. 📊 Просмотреть продажи")
        print("0. ◀️ Назад")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            # Выбор клиента
            clients = Client.get_all()
            for c in clients:
                print(f"{c.id}. {c.surname} {c.name} {c.patronymic}")
            client_id = int(input("ID клиента: "))
            
            # Выбор тура
            tours = Tour.get_all()
            for t in tours:
                hotel = Hotel.get_by_id(t.hotel_id)
                country = Country.get_by_id(hotel.country_id)
                print(f"{t.id}. {country.name} - {hotel.name} ({t.duration} дней, {t.base_price} руб.)")
            tour_id = int(input("ID тура: "))
            
            # Скидки
            print("Доступные скидки:")
            print("- 5% за раннее бронирование")
            print("- 3% за повторную покупку")
            print("- 2% за группу от 3 человек")
            discount = float(input("Общий процент скидки: "))
            
            departure = input("Дата выезда (ГГГГ-ММ-ДД): ")
            
            sale = Sale(
                client_id=client_id,
                tour_id=tour_id,
                discount=discount,
                departure_date=departure
            )
            sale.save()
            print(f"Продажа оформлена! Итоговая цена: {sale.total_price} руб.")
            
        elif choice == "2":
            sales = Sale.get_all()
            for s in sales:
                client = Client.get_by_id(s.client_id)
                tour = Tour.get_by_id(s.tour_id)
                hotel = Hotel.get_by_id(tour.hotel_id)
                country = Country.get_by_id(hotel.country_id)
                print(f"{s.id}. {client.surname} {client.name} - {country.name} ({tour.duration} дней), {s.total_price} руб.")
                
        elif choice == "0":
            break


if __name__ == '__main__':
    initialize_db()
    show_main_menu()
