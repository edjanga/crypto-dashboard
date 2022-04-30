import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import sqlite3
import time
from config import Config

class Data:

    dummy_conn_obj = sqlite3.connect('tech-stock-dashboard.db',check_same_thread=False)
    ts = TimeSeries(Config.API_KEY, output_format='pandas')

    def __init__(self):
        pass

    def wait_between_5calls(func):
        """
        Function to be used as a decorator.
        Forces the argument function to sleep 60 sec before next call if it has reached the 5 calls/min limit
        """
        def wrapper(stock):
            try:
                func(stock)
            except ValueError:
                print('Waiting 1 Min..................')
                time.sleep(60)
            return True
        return wrapper

    @staticmethod
    @wait_between_5calls
    def query(stock):
        df, metadata_df = Data.ts.get_intraday(symbol=stock, interval='10min', outputsize='compact')
        df = df.transpose()
        features_ls = ['1. open', '2. high', '3. low', '4. close', '5. volume']
        df.rename(index={var: var.split(' ')[-1] for var in features_ls}, inplace=True)
        df = df.reset_index().rename(columns={'index': 'indicator'})
        df = pd.melt(df, id_vars=['indicator'], var_name='date', value_name='price')
        df = df[df['indicator'] != 'volume']
        df.loc[:, 'ticker'] = stock
        df.to_sql(name='dummy_data', con=Data.dummy_conn_obj, if_exists='append')
        return True

    def live_query(self,universe_ls):
        while True:
            for num, stock in enumerate(universe_ls):
                print('%s: Fetching data for %s:.................' % (num+1, stock))
                self.query(stock)

    def close(self):
        self.dummy_conn_obj.close()


if __name__ == '__main__':
    from app import universe_ls
    dummy_obj = Data()
    dummy_obj.live_query(universe_ls=universe_ls)