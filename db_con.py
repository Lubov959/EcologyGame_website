import psycopg2

# Параметры подключения
host = "127.0.0.1"
port = "5432"
database = "db_eco"  # Замените на имя вашей базы данных
admin_user = "postgres"    # Пользователь с полномочиями суперпользователя
admin_password = "lubov"  # Пароль администратора
app_user = "adm"      # Пользователь, под которым будет работать приложение
app_password = "adm"  # Пароль пользователя adm

def create_tables_and_grant_rights():
    connection = None
    try:
        # Подключение под администратором для создания таблиц и назначения прав
        connection = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=admin_user,
            password=admin_password
        )
        connection.autocommit = True  # Для выполнения DDL без явного commit
        cursor = connection.cursor()

        # # # Удаляем все записи из таблицы roles
        # # cursor.execute("DELETE FROM roles;")
        # # print("Все записи удалены из roles.")
        # # Добавляем роли по одной
        # roles = ['Теория', 'Интерактивный квиз', 'Сортировка']  # Добавьте нужные роли
        # for role_name in roles:
        #     cursor.execute("INSERT INTO types (name) VALUES (%s);", (role_name,))
        #     print(f"Роль '{role_name}' успешно добавлена.")

        # Выполняем запрос для получения id и username из таблицы users
        cursor.execute("SELECT * FROM users;")
        # Получаем все результаты
        users = cursor.fetchall()
        # Выводим записи пользователей
        for user in users:
            print(user)

    except Exception as e:
        print("Ошибка при выполнении операций с базой данных:", e)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с базой данных закрыто.")

if __name__ == "__main__":
    create_tables_and_grant_rights()
