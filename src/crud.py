import sqlite3

connection = sqlite3.connect("src/user.db")

cursor = connection.cursor()


# C operation , create user , create request 

def create_submission(id:int):
    pass


def create_user(id:int):
    pass


# R , selection

def search_user(user_name : str , password : str):
    pass

def get_users():
    pass

def get_history():
    pass


# Delete submission 


def delete_submission(id:int):
    pass


connection.commit()
connection.close()