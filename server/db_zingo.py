import pyodbc

'''
Anslutningen till DB
database_name global fär att kunna användas i funktionerna
'''

# global_variables
server_host = "localhost"
database_name = "Zingo_DB"

try:
    conn = pyodbc.connect('driver={ODBC Driver 17 for SQL Server};'
                        f'server={server_host};'  
                        f'database={database_name};'
                        'trusted_connection=yes;')

    cursor = conn.cursor()
    print("Connected")
    
except:
    print("Could't find database")

'''
Funktion för att läsa från db, behöver tabellnamn och select argument som parametrar
'''

def read_from_db(table_name, select_query, arguments):
    cursor.execute(
        f"select {select_query} from {database_name}.dbo.{table_name} {arguments}")

    row = cursor.fetchone()
    if row:
        return row

'''
Funktion för att skriva till db.
Parametrar = {
    table_name = namn på tabellen
    table_content = lista med värden som ska läggas till på den nya raden
    keys = namn på kolumner som påverkas
}
'''

def write_to_db(table_name, table_content, keys):
    '''
    fields_param och values_param gör det möjligt att skicka in en lista i SQL queryn då vi kommer skicka in olika mängd keys och values baserat på vilken tabell som ska skrivas
    '''
    # stringify the fields and values.
    fields_param = ','.join(keys)
    values_param = ','.join(['?']*len(table_content))
   
    cursor.execute(
    f"insert into {database_name}.dbo.{table_name} ({fields_param}) values ({values_param})", table_content)
    conn.commit()

def update_db(table_name, params):
    try:
        cursor.execute(
            f"update {database_name}.dbo.{table_name} {params}")
        conn.commit()
        print(f"\nUpdated! \n")
    except:
        print("\nSomething went wrong \n")

def delete_from_db(table_name, user_id):
    try:
        cursor.execute(
            f"delete from {database_name}.dbo.{table_name} where [user_id] = {user_id}")
        conn.commit()
        print(f"\n{user_id} is deleted! \n")
    except:
        print("\nCould not find user")

def execute_procedure(string): 
    # string behöver procedure namn + parametrar
    try:
        sql = f"exec [{database_name}].[dbo].{string};"
        print(sql)

        cursor.execute(sql)
        try:
            rows = cursor.fetchall()
            if rows:
                return rows
        except:
            print("Nothing to report back!")

        conn.commit()

    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        if sqlstate == '28000':
            print("LDAP Connection failed: check password")