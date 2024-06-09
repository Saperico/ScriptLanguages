import requests
import sqlite3

uri_currencies = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd'

class DatabaseIntegration:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
    
    def close(self):
        self.conn.close()
    
    def create_table(self, table_name, columns):
        self.cursor.execute(f"CREATE TABLE {table_name} {columns}")
        self.conn.commit()

    def add_currencies(self, data):
        for key in data:
            self.cursor.execute("INSERT INTO coingecko VALUES (?, ?)", (key, data[key]))
        self.conn.commit()

    def get_part_of_data(self,data):


    def get_all_currencies(self):
        self.cursor.execute("SELECT * FROM currencies")
        return self.cursor.fetchall()


class Download:
    def __init__(self, uri):
        self.uri = uri
        self.data = self.download_data()
    
    def download_data(self):
        response = requests.get(self.uri)
        return response.json()
    
    def get_data(self):
        return self.data
    
def main():
    download = Download(uri_currencies)
    data = download.get_data()
    print(data)
    print(data[0]['id'])
    db = DatabaseIntegration('lab13/currency.db')

    

def create_table(db: DatabaseIntegration):
    #db.create_table('currencies', '(id TEXT PRIMARY KEY, name TEXT)')
    db.create_table('coingecko', '(id TEXT PRIMARY KEY, symbol TEXT, image TEXT, current_price FLOAT, market_cap FLOAT, market_cap_rank INT, price_change_24h FLOAT, price_change_percentage_24h FLOAT)')
    
if __name__ == "__main__":
    main()