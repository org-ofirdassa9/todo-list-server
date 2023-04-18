import os
import pyodbc
from datetime import datetime
import User

class Db_Commands:
    def __init__(self):
        self.conn = pyodbc.connect(f'DRIVER={os.environ["SQL_DRIVER"]};SERVER={os.environ["SQL_ADDR"]};DATABASE={os.environ["SQL_DB_NAME"]};UID={os.environ["SQL_USER"]};PWD={os.environ["SQL_PASS"]}')
        self.cursor = self.conn.cursor()
        
    def get_password(self, email):
        try:
            query = 'SELECT PasswordHash FROM dbo.Passwords WHERE UserID IN (SELECT UserID FROM dbo.Users WHERE Email = ?)'
            self.cursor.execute(query, email)
            return self.cursor.fetchone()[0]
        except Exception as e:
            print(e)

    def create_user(self, email, hashed_password, first_name, last_name):
        #check if this email already exists
        if self.get_user_by_email(email):
            return False
        query = 'INSERT INTO dbo.Users (Email, HasPassword, FirstName, LastName, CreatedAt) OUTPUT Inserted.UserID VALUES (?, 1, ?, ?, ?)'
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        params = email, first_name, last_name, date
        self.cursor.execute(query, params)
        inserted_user_id = self.cursor.fetchone()[0]
        query = 'INSERT INTO dbo.Passwords (UserId, PasswordHash) VALUES (?, ?)'
        params = inserted_user_id, hashed_password
        self.cursor.execute(query, params)
        self.cursor.commit()
        return self.get_user_by_email(email)

    def get_user_by_email(self, email):
        query = 'SELECT * FROM dbo.Users WHERE Email = ?'
        # Execute the SELECT query to fetch the user by id
        self.cursor.execute(query, email)
        row = self.cursor.fetchone()
        if row is None:
            return None
        # Create a new User object and return it
        return User.User(*row).__dict__

    def get_user_by_id(self, id):
        query = 'SELECT * FROM dbo.Users WHERE UserId = ?'
        # Execute the SELECT query to fetch the user by id
        self.cursor.execute(query, id)
        row = self.cursor.fetchone()
        if row is None:
            return None
        # Create a new User object and return it
        return User.User(*row).__dict__