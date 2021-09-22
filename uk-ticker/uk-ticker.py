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
link2 = get_link('https://www.londonstockexchange.com/reports?tab=equities')

# load london stock exchange instruments and ticker lists into dataframes
_df = pd.read_excel(link1, header=7, usecols="A:O")
_df2 = pd.read_excel(link2, header=7, usecols="B:O")

# TO COMPLETE

tick_list = _df[['TIDM', 'Issuer Name', 'Instrument Name', 'ICB Super-Sector Name', 'Trading Currency',
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
