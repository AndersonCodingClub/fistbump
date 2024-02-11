import os
import redis
import mysql.connector


class Waitlist:
    def _setup_connection(self):
        self.conn = mysql.connector.connect(host='localhost', user='root', password=os.environ['password'])
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('CREATE DATABASE IF NOT EXISTS fistbump')
        self.cursor.execute('USE fistbump')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS waitlist (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                is_added TINYINT(1) NOT NULL DEFAULT 0
            )
        ''')
        
        self.conn.commit()

    def _close_connection(self):
        self.cursor.close()
        self.conn.close()
        
    def is_waitlist_user(self, email: str) -> bool:
        self._setup_connection()
        
        self.cursor.execute('SELECT id FROM waitlist WHERE email=%s', (email,))
        row = self.cursor.fetchone()
        
        self._close_connection()
        return row is not None
        
    def add_waitlist_user(self, name: str, email: str) -> int:
        self._setup_connection()
        
        self.cursor.execute('INSERT INTO waitlist (name, email) VALUES (%s, %s)', (name, email))
        self.conn.commit()
        waitlist_id = self.cursor.lastrowid
        
        self._close_connection()
        return waitlist_id
        
class Verification:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def get_user(self, email: str):
        return self.r.get(email)
    
    def add_user(self, email: str, verification_code: str):
        self.r.set(email, verification_code)
        
    def remove_user(self, email: str):
        self.r.delete(email)