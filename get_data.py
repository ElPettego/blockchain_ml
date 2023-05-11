import requests as r
import datetime as dt
import pandas as pd


"""
y -> market-price
x -> rest of data
"""

EP = [
    'n-unique-addresses',
    'miners-revenue',
    # 'market-cap', # SISTEMARE LA FREQUENZA
    'difficulty',
    'cost-per-transaction',
    'avg-block-size',
    'n-transactions-per-block',
    'market-price',
    'trade-volume',
    # 'utxo-count', # SAME AS market-cap
    'n-transactions-excluding-popular',
    'n-transactions',
    'hash-rate',
    'output-volume',
]

def main():
    df = None
    for ep in EP:
        # ep = 'utxo-count'
        res = r.get(
            f'https://api.blockchain.info/charts/{ep}?'
            'timespan=10years&format=json&sampled=false'
        ).json()
        _time = []
        _values = []
        for el in res['values']:
            tstamp = dt.datetime.utcfromtimestamp(float(el['x']))
            print(tstamp, el['y'])    
            _time.append(tstamp)
            _values.append(round(el['y'], 2))
        _df = pd.DataFrame(list(zip(_time, _values)), columns=['date', ep])
        if df is None:
            df = _df
        else:
            df = pd.merge(df, _df, on='date')
    df.to_csv('bc_data.csv')

if __name__ == '__main__':
    main()