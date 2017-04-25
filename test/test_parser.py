FIELDS = ('area','population','iso','country','captial','continent','tld','currency_code','currency_name','phone','postal_code_format','postal_code_regex','languages','neighbours')

import re
def re_scraper(html):
    results = {}
    for field in FIELDS:
        results[field] = re.search(r'<tr id="places_%s_row">.*?<td class="w2p_fw">(.*?)</td>' % field,html).groups()[0]
    return results

from bs4 import BeautifulSoup
def bs_scraper(html):
    soup = BeautifulSoup(html,'html.parser')
    results = {}
    for field in FIELDS:
        results[field] = soup.find('table').find('tr',id = 'places_%s__row'%field).find('td',class_='w2p_fw').text
    return results

import lxml.html
def lxml_scraper(html):
    tree = lxml.html.fromstring(html)
    results = {}
    for field in FIELDS:
        results[field] = tree.cssselect('table > tr#places_%s__row > td.w2p_fw'% field).text_content()
    return results
