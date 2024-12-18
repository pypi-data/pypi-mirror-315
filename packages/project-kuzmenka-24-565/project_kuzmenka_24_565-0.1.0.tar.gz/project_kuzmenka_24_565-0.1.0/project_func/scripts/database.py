# project_func/scripts/database.py

import sqlite3


def create_table(table_name, col_names):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    columns = ', '.join([f"{col.strip()} TEXT" for col in col_names.split(',')])
    cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({columns})')

    conn.commit()
    conn.close()
    return f"Таблица {table_name} успешно создана."


def check_table(table_name):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name=?;', (table_name,))
    exists = cursor.fetchone() is not None

    conn.close()
    return exists


def delete_table(table_name):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS {};'.format(table_name))

    conn.commit()
    conn.close()
    return f"Таблица {table_name} успешно удалена."


def database_main():
    print("***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create table_name col_names - создать таблицу table_name со следующими столбцами col_names")
    print("<command> check table_name - проверить на наличие такой таблицы table")
    print("<command> delete table_name - удалить таблицу table")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация")

    while True:
        command = input(">>>Введите команду: ").strip().split()

        if not command:
            continue

        cmd_type = command[0].lower()

        if cmd_type == "create":
            if len(command) < 3:
                print("Некорректное значение. Используйте: create table_name col_names.")
                continue
            table_name, col_names = command[1], ','.join(command[2:])
            print(create_table(table_name, col_names))

        elif cmd_type == "check":
            if len(command) != 2:
                print("Некорректное значение. Используйте: check table_name.")
                continue
            table_name = command[1]
            if check_table(table_name):
                print(f"Таблица с таким именем {table_name} существует.")
            else:
                print(f"Таблица с таким именем {table_name} НЕ существует.")

        elif cmd_type == "delete":
            if len(command) != 2:
                print("Некорректное значение. Используйте: delete table_name.")
                continue
            table_name = command[1]
            if check_table(table_name):
                print(delete_table(table_name))
            else:
                print(f"Таблица с таким именем {table_name} НЕ существует.")

        elif cmd_type == "exit":
            print("Выход из программы.")
            break

        elif cmd_type == "help":
            print("***Процесс работы с таблицей***")
            print("Функции:")
            print("<command> create table_name col_names - создать таблицу table_name со следующими столбцами col_names")
            print("<command> check table_name - проверить на наличие такой таблицы table")
            print("<command> delete table_name - удалить таблицу table")

        else:
            print(f"Функции {command[0]} нет. Попробуйте снова.")
