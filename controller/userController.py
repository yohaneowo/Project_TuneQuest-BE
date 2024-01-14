import sqlite3
conn = sqlite3.connect('../temp_sqlite/TuneQuest.db')
def get_user(db, username:str):
    c = conn.cursor()
    c.execute("SELECT * FROM user WHERE username=?", (username,))
    user_data =  c.fetchone()
    user_exists = user_data is not None
    if user_exists:
        return user_data
    else:
        return None

if __name__ == "__main__":
    print(get_user(conn, 'test'))