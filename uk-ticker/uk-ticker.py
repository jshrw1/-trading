# import required packages
import httplib2
import pandas as pd
from bs4 import BeautifulSoup


# function to obtain  excel links from london stock exchange website
def get_link(url: object):
    http = httplib2.Http()
    response, content = http.request(url)

    links = []

    for link in BeautifulSoup(content, features="html.parser").find_all('a', href=True):
        if '.xlsx' in link['href']:
            links.append(link['href'])

    return links[0]


# excel links
link1 = get_link('https://www.londonstockexchange.com/reports?tab=instruments')

# load london stock exchange instruments and ticker lists into dataframes
_df = pd.read_excel(link1, header=7, sheet_name='1.1 Shares', usecols="A:O")

# process and clean dataset
df = _df[['TIDM', 'Issuer Name', 'ICB Super-Sector Name', 'Trading Currency', 'Country of Incorporation',
          'Security Mkt Cap (in £m)', 'LSE Market']]

df = df.rename(columns={'TIDM': 'ticker', 'Issuer Name': 'name', 'ICB Super-Sector Name': 'industry',
                        'Trading Currency': 'currency', 'Country of Incorporation': 'country',
                        'LSE Market': 'code', 'Security Mkt Cap (in £m)': 'cap'})

df = df[df['currency'] == 'GBX']
df = df[df['code'] == 'MAIN MARKET']
df['cap'] = df['cap'].astype(float)
df = df.sort_values(by='cap', ascending=False)
df = df.dropna().reset_index(drop=True)

# final ticker list
ftse250 = df.iloc[100:350, :]
ftse250 = ftse250.sort_values(by='ticker', ascending=True)
ftse250 = ftse250[['ticker', 'name', 'industry']].reset_index(drop=True)
