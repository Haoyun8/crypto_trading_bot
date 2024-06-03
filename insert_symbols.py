from database import Database

def insert_initial_symbols():
    db = Database()
    symbols = ["BTC/USDT", "ETH/USDT"]
    db.insert_symbols(symbols)
    print("Inserted symbols into the database.")

if __name__ == "__main__":
    insert_initial_symbols()
