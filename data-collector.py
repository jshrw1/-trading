# import required packages
import pandas as pd
import yfinance as yf
from time import sleep
from random import randint
from datetime import datetime
from dateutil.relativedelta import relativedelta

# load in ftse250 ticker list
ftse250 = pd.read_csv('~\\PycharmProjects\\-trading\\uk-ticker\\ticker.csv')
ticker = ftse250['ticker'].tolist()

# data download loop
df = pd.DataFrame()
for x in list(ticker):
    ticker2 = (x + '.L')
    a = yf.Ticker(x + '.L')
    _df = a.history(period='max')
    _df = _df.rename_axis('date').reset_index()
    _df['date'] = _df['date'].dt.strftime('%Y%m%d')
    _df = _df[['date', 'Close']]
    _df['id'] = x
    _df = _df.rename(columns={'Close': 'price'})
    df = df.append(_df)
    sleep(randint(0, 1))
    print(x)

# set start and end date d1 and d2 & filter datasets
i = datetime.now()
d2 = i.strftime('%Y%m%d')
e = i - relativedelta(years=5)
d1 = e.strftime('%Y%m%d')
_filter = (df['date'] > d1) & (df['date'] <= d2)
df = df.loc[_filter]

# filter dataset to ensure full sample coverage
_df = df.groupby(df['id'], as_index=False).count()
_df = _df[_df['date'] == 1264]
df = df[df['id'].isin(_df['id'])]

df.to_csv('~\\PycharmProjects\\-trading\\ftse-250-price-data-5-year.csv', index=False)
