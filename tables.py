from docx import Document
import re
import os


def parse_tables(file):

    doc = Document(file)
    table1 = doc.tables[0]

    data = []

    keys = None
    for i, row in enumerate(table1.rows):
        text = (cell.text for cell in row.cells)

        if i == 0:
            keys = tuple(text)
            continue

        row_data = dict(zip(keys, text))
        data.append(row_data)

    return data


def table_analyses(file):

    data = parse_tables(file)  # получаем содержимое таблицы компетенций

    codes = {"УК": [], "ПКП": [], "ОПК": []}

    keys = list(data[0].keys())  # названия столбцов

    first = keys[0]  # первый столбец
    last = keys[4]  # пятый столбец

    for row in data:

        if row[first] != '':

            c = re.match(r'[А-Я]* *-*[\d](\.[\d])*', row[last])  # ищем код компетенции
            code = c.group(0)

            # добавляем код в словарь
            if code[0:2] == "УК":
                if not (code in codes["УК"]):
                    codes["УК"].append(code)
            if code[0:3] == "ОПК":
                if not (code in codes["ОПК"]):
                    codes["ОПК"].append(code)
            if code[0:2] == "ПК":
                if not (code in codes["ПКП"]):
                    codes["ПКП"].append(code)

    # количество компетенций
    k1 = len(codes["ОПК"])
    k2 = len(codes["ПКП"])
    k3 = len(codes["УК"])
    sum = k1 + k2 + k3

    # вывод
    print("РПД: " + file)
    print(codes)
    print("Всего компетенций:    ", k1 + k2 + k3)
    print("Общепрофессиональные: ", k1, " | ", (k1 / sum) * 100, " %")
    print("Профессиональные:     ", k2, " | ", (k2 / sum) * 100, " %")
    print("Универсальные:        ", k3, " | ", (k3 / sum) * 100, " %")
    print()

    return [k1, k2, k3]


def analyses_all(dir):

    for f in os.listdir(dir):
        table_analyses(dir + f)


if __name__ == '__main__':

    analyses_all('Программы дисциплин/')
