from psycopg2 import connect, OperationalError

sql = "create database message_server;"

try:
    cnx = connect(user="postgres", password="coderslab", host="localhost")
    cnx.autocommit = True
    cursor = cnx.cursor()
    cursor.execute(sql)
    print("Database created successfully")
except OperationalError:
    print("Error while connecting to database")
else:
    cursor.close()
    cnx.close()
    
    