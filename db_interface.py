import sqlite3


class SnailMailDBInterface:

    def __init__(self, db_path="database.db"):
        self.db_path = db_path

        self.db_connection = sqlite3.connect(db_path)

    def __init_tables(self):
        pass

    def register_user(self, discord_username):
        pass

    def is_user_registered(self, discord_username):
        pass

    def get_unread_messages(self, discord_username):
        pass

    def send_message(self, sender_id, receiver_id, send_time, delivery_time, body):
        pass

    def set_message_read(self, message_id):
        pass