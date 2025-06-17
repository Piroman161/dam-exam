import psycopg2

# Подключение к базе данных PostgreSQL
def get_connection():
    return psycopg2.connect(
        dbname="de",     # Имя базы данных
        user="postgres",        # Имя пользователя PostgreSQL
        password="123",  # Пароль (замени на свой)
        host="localhost",       # Хост (обычно localhost)
        port="5432"             # Порт PostgreSQL по умолчанию
    )

def fetch_materials():
    """
    Получает материалы с полями: тип, название, мин. кол-во, запас, цена, единица, упаковка.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    p.name AS type,
                    m.m_name AS name,
                    m.min_qty,
                    m.stock_qty,
                    m.price,
                    m.unit,
                    m.pack_qty
                FROM materials m
                JOIN postavki pv ON m.id = pv.post_id
                JOIN post p ON p.id = pv.m_id;
            """)
            return cur.fetchall()
        
# Выполнить SELECT-запрос и вернуть все строки
def fetch_all(query, params=None):
    with get_connection() as conn:  # Открытие соединения
        with conn.cursor() as cur:  # Открытие курсора
            cur.execute(query, params or ())  # Выполнение запроса с параметрами
            return cur.fetchall()  # Получение всех результатов

# Выполнить запрос INSERT, UPDATE или DELETE
def execute_query(query, params=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            conn.commit()  # Сохраняем изменения в базе данных