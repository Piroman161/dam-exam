import mysql.connector
import math

# Настройки подключения к базе данных
config = {
    'host': 'localhost',       
    'user': 'ваш_пользователь',
    'password': 'ваш_пароль',
    'database': 'ваша_база'
}

try:
    # Подключение к базе данных
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Получаем все материалы
    cursor.execute("SELECT material_id, name, price_per_unit, package_size FROM Material")
    materials = cursor.fetchall()

    print(f"{'Материал':15} {'Запас на складе':15} {'Минимальная партия':20} {'Стоимость закупки'}")
    
    for material in materials:
        material_id, name, price_per_unit, package_size = material
        
        # Получаем текущий запас по материалу
        cursor.execute("SELECT quantity FROM Warehouse_Stock WHERE material_id=%s", (material_id,))
        row = cursor.fetchone()
        current_stock = row[0] if row else 0
        
        # Минимальный запас — например, 0 или задайте свой
        min_required_stock = 0
        
        needed_qty = min_required_stock - current_stock
        if needed_qty <= 0:
            # Нет необходимости закупать
            continue
        
        # Расчет количества упаковок
        pack_size = package_size
        pack_count = math.ceil(needed_qty / pack_size)
        
        # Стоимость закупки
        total_cost = pack_count * price_per_unit * pack_size
        
        print(f"{name:15} {current_stock:15.2f} {needed_qty:20.2f} {total_cost:15.2f}")

except mysql.connector.Error as err:
    print(f"Ошибка: {err}")
finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()