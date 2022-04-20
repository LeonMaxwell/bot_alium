import psycopg2
from psycopg2 import Error
from data import config

def create_table(connection):
    cursor = connection.cursor()
    create_table_character = '''
    CREATE TABLE "user_telegram" (id SERIAL PRIMARY KEY, id_telegram VARCHAR(255) NOT NULL);
    CREATE TABLE "character" (id SERIAL PRIMARY KEY, id_account VARCHAR(255) NOT NULL , 
    login VARCHAR(255) NOT NULL UNIQUE, rang INTEGER NOT NULL DEFAULT 0, 
    type_of_weapon VARCHAR(3) NOT NULL DEFAULT 'NON', rating INTEGER NOT NULL DEFAULT 1, 
    win INTEGER NOT NULL DEFAULT 0, blessing_alium INTEGER NOT NULL DEFAULT 0, 
    finished_quest INTEGER NOT NULL DEFAULT 0, count_lore INTEGER NOT NULL DEFAULT 0, 
    max_cells_ability INTEGER NOT NULL DEFAULT 5, max_cells_inventory INTEGER NOT NULL DEFAULT 50, 
    gold INTEGER NOT NULL DEFAULT 100, diamond INTEGER NOT NULL DEFAULT 0, 
    aliamination INTEGER NOT NULL DEFAULT 10, level INTEGER NOT NULL DEFAULT 0, 
    health INTEGER NOT NULL DEFAULT 100, damage INTEGER NOT NULL DEFAULT 50, 
    magic_damage INTEGER NOT NULL DEFAULT 0, alium_power INTEGER NOT NULL DEFAULT 10, 
    power INTEGER NOT NULL DEFAULT 10, agility INTEGER NOT NULL DEFAULT 10, 
    stamina INTEGER NOT NULL DEFAULT 50, insight INTEGER NOT NULL DEFAULT 10, 
    lucky INTEGER NOT NULL DEFAULT 5, mind INTEGER NOT NULL DEFAULT 10, 
    armour INTEGER NOT NULL DEFAULT 50, magic_armour INTEGER NOT NULL DEFAULT 0, 
    critical_chance REAL NOT NULL DEFAULT 0.0, critical_damage REAL NOT NULL DEFAULT 0.0);
    '''
    # Выполнение команды на создание таблиц в БД
    cursor.execute(create_table_character)
    connection.commit()
    print("Таблицы успешно созданы в БД")


def add_id(id):
    connection = psycopg2.connect(user=config.USER,
                                  password=config.PASSWORD,
                                  host=config.HOST,
                                  port=config.PORT,
                                  database=config.DATABASE)

    # Создание курсора для выполнения операций с базой данных
    cursor = connection.cursor()
    insert_query = "INSERT INTO user_telegram (id_telegram) VALUES (%s)"
    cursor.execute(insert_query,  (id, ))
    connection.commit()


def check_id(id):
    connection = psycopg2.connect(user=config.USER,
                                  password=config.PASSWORD,
                                  host=config.HOST,
                                  port=config.PORT,
                                  database=config.DATABASE)

    # Создание курсора для выполнения операций с базой данных
    cursor = connection.cursor()
    cursor.execute("SELECT * from user_telegram where id_telegram=%s", (str(id), ))
    record = cursor.fetchall()
    if record:
        return True
    else:
        return False


def create_characters(login, id):
    connection = psycopg2.connect(user=config.USER,
                                  password=config.PASSWORD,
                                  host=config.HOST,
                                  port=config.PORT,
                                  database=config.DATABASE)
    cursor = connection.cursor()
    insert_query = "INSERT INTO character (id_account, login) VALUES (%s, %s)"
    cursor.execute(insert_query,  (str(id), login))
    connection.commit()
    cursor.close()


def get_info_character(id):
    connection = psycopg2.connect(user=config.USER,
                                  password=config.PASSWORD,
                                  host=config.HOST,
                                  port=config.PORT,
                                  database=config.DATABASE)
    cursor = connection.cursor()
    insert_query = "SELECT * from character WHERE id_account=%s"
    cursor.execute(insert_query, (str(id), ))
    data_character = cursor.fetchall()
    return data_character

def main():
    """
    Данная функция подключается к БД и выполняет запрос на создании таблицы.
    """
    try:
        # Подключение к базе данных
        connection = psycopg2.connect(user=config.USER,
                                      password=config.PASSWORD,
                                      host=config.HOST,
                                      port=config.PORT,
                                      database=config.DATABASE)

        # Создание курсора для выполнения операций с базой данных
        cursor = connection.cursor()
        create_table(connection)
    except (Exception, Error) as error:
        print("Ошибка при подключении к БД", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL подключение закрыто.")


if __name__ == '__main__':
    main()