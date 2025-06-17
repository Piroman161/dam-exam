from db_module import fetch_all, execute_query

# Получение всех материалов
def list_materials():
    query = "SELECT * FROM materials;"
    return fetch_all(query)

# Получение всех поставщиков
def list_suppliers():
    query = "SELECT * FROM suppliers;"
    return fetch_all(query)

# Добавление нового материала
def add_material(m_name, quantity, unit):
    query = "INSERT INTO materials (m_name, quantity, unit) VALUES (%s, %s, %s);"
    execute_query(query, (m_name, quantity, unit))

# Обновление количества материала по ID
def update_material_quantity(material_id, quantity):
    query = "UPDATE materials SET quantity = %s WHERE id = %s;"
    execute_query(query, (quantity, material_id))

# Удаление материала по ID
def delete_material(material_id):
    query = "DELETE FROM materials WHERE id = %s;"
    execute_query(query, (material_id,))

# Добавление нового поставщика
def add_supplier(name, contact):
    query = "INSERT INTO suppliers (name, contact_info) VALUES (%s, %s);"
    execute_query(query, (name, contact))

# Запись новой поставки
def record_delivery(material_id, supplier_id, quantity):
    query = """
    INSERT INTO deliveries (material_id, supplier_id, quantity, delivery_date)
    VALUES (%s, %s, %s, NOW());  -- NOW() вставляет текущую дату и время
    """
    execute_query(query, (material_id, supplier_id, quantity))

    # После поставки — увеличиваем количество материала на складе
    update_quantity_query = """
    UPDATE materials SET quantity = quantity + %s WHERE id = %s;
    """
    execute_query(update_quantity_query, (quantity, material_id))