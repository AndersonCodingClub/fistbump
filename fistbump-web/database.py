import os
import mysql.connector


class Database:
    def _setup_connection(self):
        self.conn = mysql.connector.connect(host='localhost', user='root', password=os.environ['password'])
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('CREATE DATABASE IF NOT EXISTS fistbump')
        self.cursor.execute('USE fistbump')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS waitlist (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL
            )
        ''')
        
        self.conn.commit()

    def _close_connection(self):
        self.cursor.close()
        self.conn.close()
        
    def add_waitlist_user(self, name: str, email: str):
        self._setup_connection()
        self.cursor.execute('INSERT INTO waitlist (name, email) VALUES (%s, %s)', (name, email))
        self.conn.commit()
        self._close_connection()