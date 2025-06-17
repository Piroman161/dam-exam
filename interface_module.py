from logic_module import list_materials, list_suppliers, add_material, update_material_quantity, delete_material, add_supplier, record_delivery
from interface import *

# Функция для отображения меню
def show_menu():
    print("\n=== УЧЕТ МАТЕРИАЛОВ И ПОСТАВЩИКОВ ===")
    print("1. Просмотреть материалы")
    print("2. Добавить материал")
    print("3. Обновить количество материала")
    print("4. Удалить материал")
    print("5. Просмотреть поставщиков")
    print("6. Добавить поставщика")
    print("7. Записать поставку")
    print("8. interface")
    print("0. Выход")

# Главная функция интерфейса
def main():
    while True:
        show_menu()  # Показать доступные действия
        choice = input("Выберите действие: ")  # Ввод команды от пользователя
        
        if choice == "1":
            # Показать список всех материалов
            for row in list_materials():
                print(row)
        elif choice == "2":
            # Добавление нового материала
            name = input("Название: ")
            quantity = float(input("Количество: "))
            unit = input("Ед. измерения: ")
            add_material(name, quantity, unit)
            print("Материал добавлен.")
        elif choice == "3":
            # Обновление количества
            material_id = int(input("ID материала: "))
            quantity = float(input("Новое количество: "))
            update_material_quantity(material_id, quantity)
            print("Количество обновлено.")
        elif choice == "4":
            # Удаление материала
            material_id = int(input("ID материала: "))
            delete_material(material_id)
            print("Материал удалён.")
        elif choice == "5":
            # Показать список поставщиков
            for row in list_suppliers():
                print(row)
        elif choice == "6":
            # Добавление поставщика
            name = input("Название поставщика: ")
            contact = input("Контактная информация: ")
            add_supplier(name, contact)
            print("Поставщик добавлен.")
        elif choice == "7":
            # Запись новой поставки
            material_id = int(input("ID материала: "))
            supplier_id = int(input("ID поставщика: "))
            quantity = float(input("Количество: "))
            record_delivery(material_id, supplier_id, quantity)
            print("Поставка записана.")
        elif choice == "8":
            show_materials()
        elif choice == "0":
            print("Выход.")
            break
        else:
            print("Неверный выбор.")