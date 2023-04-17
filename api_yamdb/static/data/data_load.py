"""
Приложение data_load.py - консольное приложение, предназначенное для
автоматизации загрузки в приложение Yamdb начальных данных из файлов CSV.
"""
import csv
import sqlite3

DEFAULT_CSV_PATH = ""
DEFAULT_SQL_PATH = "../../db.sqlite3"

tables_queue = {
    "users.csv": "reviews_customuser",
    "category.csv": "reviews_category",
    "genre.csv": "reviews_genre",
    "titles.csv": "reviews_title",
    "genre_title.csv": "reviews_genretitle",
    "review.csv": "reviews_review",
    "comments.csv": "reviews_comment"
}
conn = sqlite3.connect(DEFAULT_SQL_PATH)


def load_csv(filename):
    """Загрузка CSV файла"""
    data_head = []
    data_rows = []
    with open(filename, encoding='utf-8') as r_file:
        # Создаем объект reader, указываем символ-разделитель ","
        file_reader = csv.reader(r_file, delimiter=",")
        # Счетчик для подсчета количества строк и вывода заголовков столбцов
        count = 0
        # Считывание данных из CSV файла
        for row in file_reader:
            if count == 0:
                # Строки, содержащей заголовки для столбцов
                data_head = row
            else:
                # Строки данных
                row_revised = []
                for item in row:
                    if item == "":
                        item = "_"
                    row_revised.append(item)
                data_rows.append(row_revised)
            count += 1
    return {"head": data_head, "data": data_rows}


def clear_all_db():
    """Сброс ранее введенных данных"""
    for table in tables_queue.values():
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {table};")
        conn.commit()


def data_prepare(data, add_field_count):
    """Предварительная подготовка данных"""
    data_updated = []
    for row in data:
        empty_list = ['_'] * add_field_count
        row_list = row + empty_list
        row_tuple = tuple(row_list)
        data_updated.append(row_tuple)
    return data_updated


def data_save(table_name, csv_file_data):
    """Сохраняем данные из CSV файла в SQL таблицу table_name"""
    cur = conn.cursor()

    get_fields_names = cur.execute(f"select * from {table_name} limit 1")
    field_name = [i[0] for i in get_fields_names.description]

    difference_1 = set(csv_file_data['head']).difference(set(field_name))
    difference_2 = set(field_name).difference(set(csv_file_data['head']))
    difference_names = list(difference_1.union(difference_2))
    fields_names = csv_file_data['head'] + difference_names

    field_count = len(fields_names)
    add_data_count = field_count - len(csv_file_data['head'])
    fields_names_template = ', '.join(fields_names)
    values_template = ', '.join(['?'] * field_count)
    insert_data = data_prepare(csv_file_data['data'],
                               add_data_count)
    sql_insert = (f'INSERT INTO {table_name} ({fields_names_template}) '
                  f'VALUES({values_template});')
    cur.executemany(sql_insert, insert_data)
    conn.commit()


def main():
    """
        Скрипт выполняет загрузку данных из таблиц CSV в базу данных
        приложения API_YAMDB.
    """
    print('Скрипт data_load.py выполняет загрузку данных из таблиц CSV в базу данных приложения API_YAMDB.')
    data_clear = input('Выполнить очистку базы данных?(Y/N)')
    if data_clear == "Y":
        print("Очистка данных...", end=' ')
        clear_all_db()
        print("выполнена!")
    data_add = input('Начать процесс загрузки?(Y/N)')
    if data_add != "Y":
        return
    # Загрузить список таблиц для обработки
    try:
        print("Загрузка данных...", end=' ')
        csv_list = list(tables_queue.keys())
        for csv_file_name in csv_list:
            csv_file_data = load_csv(f"{DEFAULT_CSV_PATH}{csv_file_name}")
            try:
                data_save(tables_queue[csv_file_name], csv_file_data)
            except sqlite3.Error as err_msg:
                print()
                print(f"Выполнение скрипта прервано! Ошибка: {err_msg}")
                raise
        print("выполнена!")
    finally:
        # Закрыть соединение с базой данных
        conn.close()


if __name__ == '__main__':
    main()
