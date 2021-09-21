# import required packages
import pandas as pd

# download ticker data from lse website
df = pd.read_excel("https://bit.ly/39FLd6I", header=7, usecols="A:O")

# noinspection SpellCheckingInspection
tick_list = df[['TIDM', 'Issuer Name', 'Instrument Name', 'ICB Super-Sector Name', 'Trading Currency',
                'Country of Incorporation', 'Market Sector Code']]

df = pd.read_excel("https://bit.ly/2QLIy2z", header=5, usecols="B:J")
mrk_cap = df[['Company Name', 'Company Market Cap (£m)']]
mrk_cap = mrk_cap.rename(columns={'Company Name': 'Issuer Name'})

uk_list = pd.merge(tick_list, mrk_cap, how='left', on="Issuer Name")

uk_list = uk_list.rename(columns={'TIDM': 'ticker', 'Issuer Name': 'name', 'Instrument Name': 'instrument',
                                  'ICB Super-Sector Name': 'industry', 'Trading Currency': 'currency',
                                  'Country of Incorporation': 'country', 'Market Sector Code': 'code',
                                  'Company Market Cap (£m)': 'cap'})
# clean ticker data
uk_list = uk_list[uk_list['country'] == 'United Kingdom']
uk_list = uk_list[uk_list['currency'] == 'GBX']
uk_list = uk_list[uk_list['code'].str.contains('F')]

uk_list['cap'] = uk_list['cap'].replace(['-'], ['NaN'])
uk_list['cap'] = uk_list['cap'].astype(float)

uk_list = uk_list.sort_values(by='cap', ascending=False)
uk_list['ticker'] = uk_list['ticker'].str.replace('.', '')
uk_list = uk_list.dropna()

del mrk_cap
del tick_list
del df
