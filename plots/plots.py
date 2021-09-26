import os
import pandas as pd
import matplotlib.pyplot as plt

# load in ftse250 ticker list
ftse250 = pd.read_csv('~\\PycharmProjects\\-trading\\uk-ticker\\ticker.csv')
ticker = ftse250['ticker'].tolist()

# ftse250 data
df = pd.read_csv('~\\PycharmProjects\\-trading\\ftse-250-price-data-5-year.csv')

# visualise the data & identify outliers.
os.chdir('C:\\Users\\Joshua Rawlings\\PycharmProjects\\-trading\\plots')

for x in ticker:
    _df = df[df['id'].str.contains(x)]
    _df['price'].plot(title=x)
    plt.savefig(x)
    plt.close()
