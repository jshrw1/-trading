# import required packages
import httplib2
import pandas as pd
from bs4 import BeautifulSoup


# function to obtain  excel links from london stock exchange website
def get_link(web_url):
    http = httplib2.Http()
    response, content = http.request(web_url)

    links = []

    for link in BeautifulSoup(content, features="html.parser").find_all('a', href=True):
        if '.xlsx' in link['href']:
            links.append(link['href'])

    return links[0]


# excel links
url = get_link('https://www.londonstockexchange.com/reports?tab=instruments')

# load london stock exchange instruments and ticker lists into dataframes
_df = pd.read_excel(url, header=7, sheet_name='1.1 Shares', usecols="A:O")

# process and clean dataset
df = _df[['TIDM', 'Issuer Name', 'ICB Super-Sector Name', 'LSE Market', 'Market Sector Code']]

df = df.rename(columns={'TIDM': 'ticker', 'Issuer Name': 'name', 'ICB Super-Sector Name': 'industry',
                        'LSE Market': 'code', 'Market Sector Code': 'market'})

df = df[df['code'] == 'MAIN MARKET']
df = df[df['market'].str.contains('F25')]
df = df.dropna().reset_index(drop=True)
df['ticker'] = df['ticker'].str.replace('.', '')

# final ticker list
ftse250 = df
ftse250 = ftse250.sort_values(by='ticker', ascending=True)
ftse250 = ftse250[['ticker', 'name', 'industry']].reset_index(drop=True)

# save in windows or macos
ftse250.to_csv('~\\PycharmProjects\\-trading\\uk-ticker\\ticker.csv', index=False)
