import csv
from dataclasses import fields
from prettytable import PrettyTable


class CsvManager:

    class Table:
        Headers: list = [] 
        Rows: list[dict] = []

        def PrintTable(self):

            table = PrettyTable()
            table.field_names = self.Headers

            for row in self.Rows:
                Row = []
                for value in row.values():
                    Row.append(value)
                table.add_row(Row)
            print(table)


    class Scenaries:

        @staticmethod
        def ReadInType(filepath: str, OutType: type) -> list:
            objects: list = []
            with open(filepath, "r") as file:
                reader = csv.DictReader(file)
                fieldnames = {field.name for field in fields(OutType)}

                for row in reader:
                    filtered_row = {key: row.get(key, None) for key in fieldnames}

                    obj = OutType(**filtered_row)
                    objects.append(obj)
            return objects
        

        @staticmethod
        def ReadInTable(filepath: str) -> 'CsvManager.Table':
            objects: list = []

            table: CsvManager.Table = CsvManager.Table()

            with open(filepath, "r") as file:
                reader = csv.DictReader(file)

                if(reader.fieldnames is not None):
                    for header in reader.fieldnames:
                        table.Headers.append(header)
         
                for row in reader:
                    table.Rows.append(row)
            return table


