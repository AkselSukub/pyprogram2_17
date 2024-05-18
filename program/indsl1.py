#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import date
import json
import click
import os.path
from jsonschema import validate, ValidationError
import sys


def display_workers(staff):
    """
    Отобразить список рейсов.
    """
    # Проверить, что список рейсов не пуст.
    if staff:
        # Заголовок таблицы.
        line = "+-{}-+-{}-+-{}-+-{}-+".format(
            "-" * 4, "-" * 30, "-" * 10, "-" * 20
        )
        print(line)
        print(
            "| {:^4} | {:^30} | {:^10} | {:^20} |".format(
                "No", "Пункт назначения", "No рейса", "Тип самолета"
            )
        )
        print(line)
        # Вывести данные о всех рейсах.
        for idx, worker in enumerate(staff, 1):
            print(
                "| {:>4} | {:<30} | {:<10} | {:>20} |".format(
                    idx,
                    worker.get("point", ""),
                    worker.get("number", 0),
                    worker.get("type", ""),
                )
            )
        print(line)
    else:
        print("Список рейсов пуст.")


def select_workers(staff, period):
    """
    Выбрать работников с заданным стажем.
    """
    # Получить текущую дату.
    today = date.today()
    # Сформировать список рейсов.
    result = []
    for employee in staff:
        if today.year - employee.get("year", today.year) >= period:
            result.append(employee)
    # Возвратить список выбранных рейсов.
    return result


def save_workers(file_name, staff):
    """
    Сохранить все рейсы в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_workers(file_name):
    """
    Загрузить все рейсы из файла JSON.
    """
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "point": {"type": "string"},
                "number": {"type": "integer"},
                "type": {"type": "string"},
            },
            "required": [
                "point",
                "number",
                "type",
            ],
        },
    }
    # Проверить, существует ли файл
    if os.path.exists(file_name):
        # Открыть файл с заданным именем для чтения.
        with open(file_name, "r", encoding="utf-8") as fin:
            data = json.load(fin)
        
        try:
            # Валидация
            validate(instance=data, schema=schema)
            print("JSON валиден по схеме.")
        except ValidationError as e:
            print(f"Ошибка валидации: {e.message}")
        return data
    else:
        print(f"Файл {file_name} не найден.")
        sys.exit(1)

@click.group()
def commands():
    pass


@commands.command("add")
@click.argument("filename")
@click.option("--point", help="point")
@click.option("--number", help="number")
@click.option("--type", help="type")
def add(filename, point, number, type):
    """
    Добавить данные о маршруте
    """
    staff = load_workers(filename)
    route = {
        "point": point,
        "number": number,
        "type": type,
    }
    staff.append(route)
    save_workers(filename, staff)


@commands.command("display")
@click.argument("filename")
def display(filename):
    """
    Отобразить список маршрутов
    """
    staff = load_workers(filename)
    display_workers(staff)


@commands.command("select")
@click.argument("number")
@click.argument("filename")
def select(filename, number):
    """
    Выбрать маршрут с заданным номером
    """
    staff = load_workers(filename)
    result = []
    for staff in staff:
        if staff.get("number") == number:
            result.append(staff)

    display_workers(result)


def main():
    commands()


if __name__ == "__main__":
    main()