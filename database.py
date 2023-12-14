import sqlite3


class DatabaseManager:
    def __init__(self, file):
        self.connection = sqlite3.connect(file)

    def _execute(self, sql, values=None):
        with self.connection as connect:
            cursor = connect.cursor()
            cursor.execute(sql, values or [])
            return cursor

    def create_table(self, table_name, columns):
        columns_with_type = [f"{name} {data_type}" for name, data_type in columns.items()]
        self._execute(
            f'''
            CREATE TABLE IF NOT EXISTS {table_name}
            ({', '.join(columns_with_type)});
            '''
        )

    def add(self, table_name, data: dict):
        column_names = ', '.join(data.keys())
        column_values = tuple(data.values())
        placeholders = ', '.join('?' * len(data))

        self._execute(
            f'''
            INSERT INTO {table_name}
            ({column_names})
            VALUES ({placeholders});
            ''',
            column_values
        )

    def delete(self, table_name, criteria):
        placeholders = [f'{column} = ?' for column in criteria.keys()]
        delete_criteria = ' AND '.join(placeholders)
        self._execute(
            f"""
            DELETE FROM {table_name}
            WHERE {delete_criteria}
            """,
            tuple(criteria.values())
        )

    def select(self, table_name, criteria=None, order_by=None):
        criteria = criteria or {}

        sql = f'SELECT * FROM {table_name}'

        if criteria:
            placeholders = [f'{column} = ?' for column in criteria.keys()]
            print(placeholders)
            select_criteria = ' AND '.join(placeholders)
            sql += f' WHERE {select_criteria}'

        if order_by:
            sql += f' ORDER BY {order_by}'

        return self._execute(sql, tuple(criteria.values()))

    def update(self, table_name, data_and_id):
        sql = f'''UPDATE {table_name} '''
        changes = ', '.join([f"{column} = '{value}'" for column, value in data_and_id[0].items()])
        sql += f'SET {changes} '
        sql += f'Where id = {data_and_id[1]}'

        self._execute(sql)

    def __del__(self):
        self.connection.close()



