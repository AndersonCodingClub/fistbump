import os
import hashlib
import mysql.connector


class Database:
    def _setup_connection(self):
        self.conn = mysql.connector.connect(host='localhost', user='root', password=os.environ['password'])
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('CREATE DATABASE IF NOT EXISTS fistbump')
        self.cursor.execute('USE fistbump')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                username VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                major VARCHAR(255),
                year INT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                image_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                path VARCHAR(255) NOT NULL,
                date_published DATETIME NOT NULL
            )
        ''')
        
        self.conn.commit()

    def _close_connection(self):
        self.cursor.close()
        self.conn.close()
        
    def add_user(self, name: str, username: str, password: str, major: str, year: int) -> int:
        self._setup_connection()
        
        insert_query = 'INSERT INTO users (name, username, password, major, year) VALUES (%s, %s, %s, %s, %s)'
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        row = (name, username, password_hash, major, year)
        self.cursor.execute(insert_query, row)
        self.conn.commit()
        user_id = self.cursor.lastrowid
        
        self._close_connection()
        return user_id
    
    def validate_user(self, username: str, password: str) -> int:
        """Validate whether entered user credentials match database entry

        Args:
            username (str): Entered username
            password (str): Entered password

        Returns:
            int: User ID of user if valid login. If not, returns None.
        """
        self._setup_connection()
        self.cursor.execute('SELECT * FROM users WHERE username=%s', (username,))
        row = self.cursor.fetchone()
        self._close_connection()
        if row:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if password_hash == row[2]:
                return row[0]
        
    def add_image(self, user_id: int, path: str) -> int:
        self._setup_connection()
        
        insert_query = 'INSERT INTO images (user_id, path, date_published) VALUES (%s, %s, CURRENT_TIMESTAMP)'
        row = (user_id, path)
        self.cursor.execute(insert_query, row)
        self.conn.commit()
        image_id = self.cursor.lastrowid
        
        self._close_connection()
        return image_id
    
    def get_images(self):
        self._setup_connection()
        
        self.cursor.execute('SELECT * FROM images')
        rows = self.cursor.fetchall()
        
        self._close_connection()
        return rows
    
    def drop_all_tables(self):
        self._setup_connection()
        self.cursor.execute('DROP TABLE users, images')
        self.conn.commit()
        self._close_connection()