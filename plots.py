import os
import pandas as pd
import matplotlib.pyplot as plt

# load in price data
df = pd.read_csv('~\\PycharmProjects\\-trading\\price-data\\price-data.csv')

# format date variable to datetime format and set as index
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# visualise the price data in separate plots (aggregate to weekly)
os.chdir('C:\\Users\\Joshua Rawlings\\PycharmProjects\\-trading\\plots')

ticker = df['id'].unique().tolist()

for x in ticker:
    _df = df[df['id'].str.contains(x)]
    _df = _df.groupby(pd.Grouper(freq='W')).price.mean()
    _df.plot(title=x)
    plt.savefig(x)
    plt.close()
    print(x)
