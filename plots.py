import os
import pandas as pd
import matplotlib.pyplot as plt

# ftse250 data and id
df = pd.read_csv('~\\PycharmProjects\\-trading\\ftse-250-price-data-5-year.csv')
ticker = df['id'].unique().tolist()

# visualise the data & identify outliers.
os.chdir('/plots')

for x in ticker:
    _df = df[df['id'].str.contains(x)]
    _df['price'].plot(title=x)
    plt.savefig(x)
    print(x)
    plt.close()
