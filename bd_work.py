import sqlite3
from sqlite3 import Error


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
    except Error as er:
        print(f"The error '{er}' occurred")

    return connection


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as er:
        print(f"The error '{er}' occurred")

def showName(connection, id, category):
    cursor = connection.cursor()
    if(category == "laugh"):
        cursor.execute("SELECT title FROM party WHERE id = ?", (id, ))
    else:
        cursor.execute("SELECT title FROM think WHERE id = ?", (id,))
    result = cursor.fetchone()
    if result:
        return result[0]