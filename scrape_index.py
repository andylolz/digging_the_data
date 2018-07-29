from bs4 import BeautifulSoup as bs
import requests
import scraperwiki


base_url = 'http://beta.charitycommission.gov.uk'

tmpl = base_url + '/charity-search/?q=&p={}&onlyShow=Up-to-date'

page = 1
while True:
    print(page)
    r = requests.get(tmpl.format(page))
    soup = bs(r.text, 'html.parser')
    charity_links = soup.find_all(class_='charity-link')
    if len(charity_links) == 0:
        break
    page_data = [{
        'url': x['href'],
        'name': x.text,
    } for x in charity_links]
    print(page_data)
    for item in page_data:
        scraperwiki.sqlite.save(['url'], item)
    page += 1
