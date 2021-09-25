# import required packages
import pandas as pd
from time import sleep
from random import randint
from datetime import datetime
from dateutil.relativedelta import relativedelta

# load in ftse250 ticker list
ftse250 = pd.read_csv('~\\PycharmProjects\\-trading\\uk-ticker\\ticker.csv')
ticker = ftse250['ticker'].tolist()

# set start and end date d1 and d2
i = datetime.now()
d2 = i.strftime('%Y%m%d')
e = i - relativedelta(years=5)
d1 = e.strftime('%Y%m%d')

# data download loop
df = pd.DataFrame()
for x in ticker:
    url = "https://stooq.com/q/d/l/?s=" + x + ".uk&d1" + d1 + "&d2=" + d2 + "&i=d&o=0000001"
    _df = pd.read_csv(url)
    _df = _df[['Date', 'Close']]
    _df['id'] = x
    _df = _df.rename(columns={'Close': 'price', 'Date': 'date'})
    df = df.append(_df)
    sleep(randint(0, 1))
    print(x)
