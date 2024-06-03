import sqlite3
from config import DB_NAME
from logger import log_error, log_info

class Database:
    def __init__(self, db_name=DB_NAME):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        query_trades = '''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            amount REAL NOT NULL,
            price REAL NOT NULL,
            side TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            strategy TEXT
        )
        '''
        query_symbols = '''
        CREATE TABLE IF NOT EXISTS symbols (
            symbol TEXT PRIMARY KEY
        )
        '''
        self.conn.execute(query_trades)
        self.conn.execute(query_symbols)
        self.conn.commit()

    def insert_trade(self, symbol, amount, price, side, strategy):
        query = 'INSERT INTO trades (symbol, amount, price, side, strategy) VALUES (?, ?, ?, ?, ?)'
        try:
            self.conn.execute(query, (symbol, amount, price, side, strategy))
            self.conn.commit()
            log_info(f"Inserted trade: {symbol}, {amount}, {price}, {side}, {strategy}")
        except sqlite3.Error as e:
            log_error(f"Database error: {e}")

    def fetch_trades(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM trades')
        return cursor.fetchall()

    def fetch_symbols(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT symbol FROM symbols')
        return [row[0] for row in cursor.fetchall()]

    def insert_symbols(self, symbols):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM symbols')  # Clear existing symbols
        for symbol in symbols:
            cursor.execute('INSERT INTO symbols (symbol) VALUES (?)', (symbol,))
        self.conn.commit()

    def fetch_daily_trade_count(self):
        cursor = self.conn.cursor()
        query = "SELECT COUNT(*) FROM trades WHERE DATE(timestamp) = DATE('now', 'localtime')"
        cursor.execute(query)
        return cursor.fetchone()[0]

    def backup_database(self, backup_path):
        try:
            with sqlite3.connect(backup_path) as backup_conn:
                self.conn.backup(backup_conn)
            log_info("Database backup successful")
        except sqlite3.Error as e:
            log_error(f"Database backup error: {e}")

# Usage example
# db = Database()
# db.backup_database('backup_trading_bot.db')


