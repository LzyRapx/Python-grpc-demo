import sqlite3
def create(conn):
    """
    create sqlite database
    """
    sql_create = '''
    CREATE TABLE `users` (
      `username`  TEXT NOT NULL PRIMARY KEY UNIQUE,
      `password`  TEXT NOT NULL
    )
    '''
    #  execute a sql 
    conn.execute(sql_create)
    print('Create Successful')

def main():

    db_path = 'chatroom.db'
    conn = sqlite3.connect(db_path)
    print("Opened database")

    create(conn)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()