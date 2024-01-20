import os
import mysql.connector


class Database:
    def _setup_connection(self):
        self.conn = mysql.connector.connect(host='localhost', user='root', 
                                            password=os.environ['password'], database='fb-images')
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('CREATE DATABASE IF NOT EXISTS fistbump')
        self.cursor.execute('USE fistbump')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                major VARCHAR(255) NOT NULL,
                year INT NOT NULL
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                image_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                path VARCHAR(255) NOT NULL,
                date_published DATETIME NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        self.conn.commit()

    def _close_connection(self):
        self.cursor.close()
        self.conn.close()
        
    def add_user(self, name: str, major: str, year: int) -> int:
        self._setup_connection()
        
        insert_query = 'INSERT INTO users (name, major, year) VALUES (%s, %s)'
        row = (name, major, year)
        self.cursor.execute(insert_query, row)
        user_id = self.cursor.lastrowid
        
        self._close_connection()
        return user_id
        
    def add_image(self, user_id: int, path: str) -> int:
        self._setup_connection()
        
        insert_query = 'INSERT INTO images (user_id, path, date_published) VALUES (%s, %s)'
        row = (user_id, path, 'CURRENT_TIMESTAMP')
        self.cursor.execute(insert_query, row)
        image_id = self.cursor.lastrowid
        
        self._close_connection()
        return image_id
    
    def get_images(self):
        self._setup_connection()
        
        self.cursor.execute('SELECT * FROM images')
        rows = self.cursor.fetchall()
        
        self._close_connection()
        return rows