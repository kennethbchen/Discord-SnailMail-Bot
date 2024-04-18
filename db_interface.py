import os
import sqlite3
import os.path as path

class SnailMailDBInterface:

    def __init__(self, db_path="database.db", reset_database=False):
        self.db_path = db_path

        if not path.exists(db_path):
            self.db_connection = sqlite3.connect(db_path)
            self.init_tables()
        elif reset_database and path.exists(db_path):
            os.remove(db_path)
            self.db_connection = sqlite3.connect(db_path)
            self.init_tables()

        self.db_connection = sqlite3.connect(db_path)



    def init_tables(self):

        cur = self.db_connection.cursor()

        cur.execute("CREATE TABLE users (id integer PRIMARY KEY NOT NULL, username string UNIQUE)")

        cur.close()

    def register_user(self, discord_username):

        cur = self.db_connection.cursor()

        cur.execute("INSERT INTO users values (NULL, ?)", [discord_username])

        cur.close()

        self.db_connection.commit()

    def is_user_registered(self, discord_username):

        pass

    def get_unread_messages(self, discord_username):
        pass

    def send_message(self, sender_id, receiver_id, send_time, delivery_time, body):
        pass

    def set_message_read(self, message_id):
        pass