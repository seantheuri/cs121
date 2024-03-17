import mysql.connector
from mysql.connector import Error

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',        
            user='root',    
            password='password', 
            database='cs121'
        )
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_query(connection, query, params=None, return_id=False):
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        connection.commit()
        if return_id:
            return cursor.lastrowid 
    except Error as e:
        print(f"The error '{e}' occurred")
        return None

def execute_read_query(connection, query, params=None):
    cursor = connection.cursor(dictionary=True)  
    result = []
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall() 
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
    return result

def execute_stored_procedure(connection, procedure_name, args=()):
    with connection.cursor() as cursor:
        cursor.callproc(procedure_name, args)
        results = []
        for result in cursor.stored_results():
            results.extend(result.fetchall())
        return results
