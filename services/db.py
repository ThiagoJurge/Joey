import mysql.connector

# Dados de conexão ao banco de dados
db_config = {
    'host': '187.16.255.97',
    'user': 'read_donovan',
    'password': 'D0D0,C@rl@',
    'database': 'admin_noc'
}

def connect_to_database():
    """Cria uma conexão com o banco de dados e retorna o objeto de conexão."""
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        return None

def execute_query(query):
    """Executa uma consulta SQL e retorna os resultados."""
    connection = connect_to_database()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            return None
        finally:
            connection.close()
