from database.local_settings import database_settings
from psycopg2 import connect

def execute_query(query):
    connection = connect(**database_settings)
    connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute(query)
        try:
            result = cursor.fetchall()
        except:
            result = None
        connection.close()
        return result


if __name__ == '__main__':
    users = """
    CREATE TABLE IF NOT EXISTS users (
        user_id serial primary key,
        username varchar(255) not null,
        password varchar(255) not null
        );
    """
    messages = """
        CREATE TABLE IF NOT EXISTS messages (
            id serial primary key,
            from_id int not null,
            to_id int not null,
            message text,
            creation_date timestamp
        )
    """
    # execute_query(users)
    # execute_query(messages)
    