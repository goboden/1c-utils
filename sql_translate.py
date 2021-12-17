import argparse
import re
from typing import Dict
from pprint import pprint


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, required=True)
    parser.add_argument('-o', type=str, required=False)
    parser.add_argument('-d', type=str, required=False)
    return parser.parse_args()


def read_conf(filename: str) -> str:
    return ''


def read_sql(filename: str) -> str:
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()
    return ''


def find_tables(sql: str) -> Dict:
    result = re.findall(r'(dbo\..\S+)\s(.\S+)', sql)
    tables = {table: {'name': name} for name, table in result}
    return tables


def find_fields(table_name: str, sql: str) -> Dict:
    result = re.findall(r'(' + table_name + r'\.).([^\s,\)]+)', sql)
    fields = {field: '' for _, field in result}
    return fields


def read_structure(sql: str) -> Dict:
    tables = find_tables(sql)
    for table in sorted(tables):
        fields = find_fields(table, sql)
        tables[table]['fields'] = fields
    return tables


def main():
    args = parse_args()

    sql = read_sql(args.i)
    structure = read_structure(sql)

    pprint(structure)


if __name__ == '__main__':
    main()
