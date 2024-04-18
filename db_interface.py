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

        cur.execute("CREATE TABLE messages (id integer PRIMARY KEY NOT NULL, sender_id integer NOT NULL, receiver_id integer NOT NULL, send_datetime integer NOT NULL, delivery_datetime integer NOT NULL, body TEXT NOT NULL, read integer default FALSE NOT NULL)")

        cur.close()

    def register_user(self, discord_username):

        if self.is_user_registered(discord_username):
            return

        cur = self.db_connection.cursor()

        cur.execute("INSERT INTO users values (NULL, ?)", [discord_username])

        cur.close()

        self.db_connection.commit()

    def is_user_registered(self, discord_username):

        cur = self.db_connection.cursor()

        cur.execute("SELECT COUNT(*) FROM users WHERE username = ?", [discord_username])

        count = cur.fetchone()[0]

        cur.close()

        return count > 0

    def get_user_id_from_username(self, discord_username):

        if not self.is_user_registered(discord_username):
            return -1

        cur = self.db_connection.cursor()

        cur.execute("SELECT id FROM users WHERE username = ?", [discord_username])

        result = cur.fetchone()[0]

        cur.close()

        return result


    def get_unread_messages(self, discord_username):

        if not self.is_user_registered(discord_username):
            return None

        receiver_id = self.get_user_id_from_username(discord_username)

        cur = self.db_connection.cursor()

        # Messages that are delivered have a delivery_datetime that is in the past
        cur.execute("SELECT username as sender, body FROM messages JOIN users ON sender_id=users.id WHERE receiver_id = ? AND delivery_datetime < strftime('%s') AND read = FALSE ORDER BY send_datetime ASC", [receiver_id])

        result = cur.fetchall()

        cur.close()

        return result


    def send_message(self, sender_id, receiver_id, send_time, delivery_time, body):

        cur = self.db_connection.cursor()

        cur.execute("INSERT INTO messages (id, sender_id, receiver_id, send_datetime, delivery_datetime, body, read) VALUES (NULL, ?, ?, ?, ?, ?, FALSE)", [sender_id, receiver_id, send_time, delivery_time, body])

        cur.close()

        self.db_connection.commit()

    def set_message_read(self, message_id):
        pass