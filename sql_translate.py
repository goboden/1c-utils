import argparse
import json
import re
from typing import Dict
from pathlib import WindowsPath


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, required=False)
    # parser.add_argument('-o', type=str, required=False)
    parser.add_argument('-d', type=str, required=False)
    return parser.parse_args()


def read_input(filename: str) -> str:
    if not filename:
        filename = WindowsPath('./sel.sql')
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()


def read_dictionary(filename: str) -> dict:
    if not filename:
        filename = WindowsPath('./dict.str')
    with open(filename, 'r', encoding='utf-8') as f:
        js = json.loads(f.read())
        return js


def find_tables(sql: str) -> Dict:
    result = re.findall(r'(dbo\..\S+)\s(.\S+)', sql)
    tables = {table: {'name': name, 'translation': ''} for name, table in result}
    return tables


def add_fields(table_name: str, tables: Dict, sql: str):
    result = re.findall(r'(' + table_name + r'\.)(.[^\s,)]+)', sql)
    fields = {field: '' for _, field in result}
    tables[table_name]['fields'] = fields


def make_table_translation(table: Dict, dictionary: Dict):
    search_key = table['name'].replace('dbo.', '')
    table_dict = dictionary[search_key]
    table['translation'] = table_dict['name']
    fields = table['fields']
    for field_name in fields:
        fields[field_name] = table_dict[field_name]


def make_translation(sql: str, dictionary: Dict) -> Dict:
    tables = find_tables(sql)
    for table in sorted(tables):
        add_fields(table, tables, sql)
        make_table_translation(tables[table], dictionary)
    return tables


def translate_table(output_sql, translation, table) -> (str, str):
    table_name = translation[table]['name']
    table_translation = translation[table]['translation']
    table_translation_repr = table_translation.replace('.', '_')
    table_repr = f'{table}_{table_translation_repr}'
    table_from = f'{table_name} {table}'
    table_to = f'{table_translation} AS {table_repr}'
    return output_sql.replace(table_from, table_to), table_repr


def translate_field(output_sql, fields, field, table, table_repr):
    field_translation = fields[field]
    field_from = f'{table}.{field}'
    field_to = f'{table_repr}.{field_translation}'
    return output_sql.replace(field_from, field_to)


def translate(input_sql: str, dictionary: Dict):
    translation = make_translation(input_sql, dictionary)
    output_sql = input_sql
    for table in translation:
        output_sql, table_repr = translate_table(output_sql, translation, table)
        fields = translation[table]['fields']
        for field in fields:
            output_sql = translate_field(output_sql, fields, field, table, table_repr)
    return output_sql


def main():
    args = parse_args()

    input_sql = read_input(args.i)
    dictionary = read_dictionary(args.d)
    output_sql = translate(input_sql, dictionary)
    print(output_sql)


if __name__ == '__main__':
    main()
