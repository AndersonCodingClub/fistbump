import os
import hashlib
import random as rd
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
                year INT,
                streak INT NOT NULL DEFAULT 0
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS followers (
                follower_id INT NOT NULL,
                following_id INT NOT NULL,
                PRIMARY KEY (follower_id, following_id),
                FOREIGN KEY (follower_id) REFERENCES users(user_id),
                FOREIGN KEY (following_id) REFERENCES users(user_id)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                image_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                match_user_id INT NOT NULL,
                path VARCHAR(255) NOT NULL,
                date_published DATETIME NOT NULL
            )
        ''')
        
        self.conn.commit()

    def _close_connection(self):
        self.cursor.close()
        self.conn.close()
    
    # User creation, retrieval, and querying methods
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
        self._setup_connection()
        self.cursor.execute('SELECT * FROM users WHERE username=%s', (username,))
        row = self.cursor.fetchone()
        self._close_connection()
        if row:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if password_hash == row[3]:
                return row[0]
            
    def get_user_row(self, user_id: int):
        self._setup_connection()
        
        self.cursor.execute('SELECT * FROM users WHERE user_id=%s', (user_id,))
        row = self.cursor.fetchone()
        
        self._close_connection()
        return row
            
    def get_random_user(self, user_id: int) -> int:
        self._setup_connection()
        
        self.cursor.execute('SELECT user_id FROM users')
        user_ids = [row[0] for row in self.cursor.fetchall() if row[0] != user_id]
        
        self._close_connection()
        return rd.choice(user_ids)
    
    def get_streak(self, user_id: int) -> int:
        self._setup_connection()
        
        self.cursor.execute('SELECT streak FROM users WHERE user_id=%s', (user_id,))
        row = self.cursor.fetchone()
        
        self._close_connection()
        return row[0]
    
    def increment_streak(self, user_id: int) -> int:
        self._setup_connection()
        self.cursor.execute('UPDATE users SET streak=streak+1 WHERE user_id=%s', (user_id,))
        self.conn.commit()
        self._close_connection()
        
        return self.get_streak(user_id)
    
    def set_streak(self, user_id: int, value: int) -> int:
        self._setup_connection()
        self.cursor.execute('UPDATE users SET streak=%s WHERE user_id=%s', (value, user_id))
        self.conn.commit()
        self._close_connection()
        
        return value
    
    # Follow methods
    def add_follower(self, follower_id: int, following_id: int):
        self._setup_connection()
        insert_query = 'INSERT INTO followers (follower_id, following_id) VALUES (%s, %s)'
        self.cursor.execute(insert_query, (follower_id, following_id))
        self.conn.commit()
        self._close_connection()

    def remove_follower(self, follower_id: int, following_id: int):
        self._setup_connection()
        delete_query = 'DELETE FROM followers WHERE follower_id=%s AND following_id=%s'
        self.cursor.execute(delete_query, (follower_id, following_id))
        self.conn.commit()
        self._close_connection()
        
    def get_followers(self, user_id: int):
        self._setup_connection()
        self.cursor.execute('SELECT follower_id FROM followers WHERE following_id=%s', (user_id,))
        followers = [row[0] for row in self.cursor.fetchall()]
        self._close_connection()
        return followers
        
    def get_following(self, user_id: int):
        self._setup_connection()
        self.cursor.execute('SELECT following_id FROM followers WHERE follower_id=%s', (user_id,))
        following = [row[0] for row in self.cursor.fetchall()]
        self._close_connection()
        return following
        
    # Image methods
    def add_image(self, user_id: int, path: str, match_user_id: int) -> int:
        self._setup_connection()
        
        insert_query = 'INSERT INTO images (user_id, match_user_id, path, date_published) VALUES (%s, %s, %s, CURRENT_TIMESTAMP)'
        row = (user_id, match_user_id, path)
        self.cursor.execute(insert_query, row)
        self.conn.commit()
        image_id = self.cursor.lastrowid
        
        self._close_connection()
        return image_id
    
    def get_images(self, user_id: int=None):
        self._setup_connection()
        
        if user_id:
            self.cursor.execute('SELECT * FROM images WHERE user_id=%s', (user_id,))
        else:
            self.cursor.execute('SELECT * FROM images')
        rows = self.cursor.fetchall()
        
        self._close_connection()
        return rows
    
    def drop_image_table(self):
        self._setup_connection()
        self.cursor.execute('DROP TABLE images')
        self.conn.commit()
        self._close_connection()
        
    def drop_followers_table(self):
        self._setup_connection()
        self.cursor.execute('DROP TABLE followers')
        self.conn.commit()
        self._close_connection()
        
    def temp(self, num):
        self._setup_connection()
        self.cursor.execute(f'DELETE FROM images WHERE image_id={num}')
        self.conn.commit()
        self._close_connection()