import sqlite3

class MessageStorage:
    def __init__(self, db_file='messages.db'):
        self.db_file = db_file
        self._create_table()

    def _create_table(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT,
                recipient TEXT,
                content TEXT,
                timestamp TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def store_message(self, message):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO messages (sender, recipient, content, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (message.sender, message.recipient, message.content, message.timestamp.isoformat()))
        conn.commit()
        conn.close()

    def get_messages(self, sender=None, recipient=None):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        query = 'SELECT * FROM messages'
        conditions = []
        params = []
        if sender:
            conditions.append('sender = ?')
            params.append(sender)
        if recipient:
            conditions.append('recipient = ?')
            params.append(recipient)
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
        cursor.execute(query, params)
        messages = cursor.fetchall()
        conn.close()
        return messages
