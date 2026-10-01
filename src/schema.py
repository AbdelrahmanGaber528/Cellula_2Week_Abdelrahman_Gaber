import sqlite3

connection = sqlite3.connect("src/users.db")

cursor = connection.cursor()



users_creation = """

        CREATE TABLE IF NOT EXISTS users(
                        
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL ,
            password_hashed TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'user')),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
"""

submissions_creation = """

        CREATE TABLE IF NOT EXISTS submissions(
         
         id INTEGER PRIMARY KEY AUtOINCREMENT,
         user_id INTEGER NOT NULL,
         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
         content_type TEXT NOT NULL CHECK(content_type IN ('text', 'image')),
         raw_text TEXT,
         file_path TEXT,
         prediction TEXT NOT NULL,
         FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
"""



cursor.execute(users_creation)
cursor.execute(submissions_creation)


connection.commit()
connection.close()
