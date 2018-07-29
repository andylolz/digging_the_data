from os.path import exists, join
import re

import requests
import scraperwiki


base_url = 'http://beta.charitycommission.gov.uk'

id_re = re.compile(r'regid=(\d+)&subid=(\d+)')
d_and_l_re = re.compile(r'\'Donations and legacies: ([^\']+)\'')
income_re = re.compile(r'Income</span><span class="big-money">([^<]+)</span>')
end_date_re = re.compile(r'Data for financial year ending <em>([^<]+)</em>')

charity_count = scraperwiki.sqlite.execute(
    'select count(*) from swdata')['data'][0][0]
for offset in range(charity_count):
    print(offset + 1)
    item = scraperwiki.sqlite.select(
        '* from swdata limit 1 offset {}'.format(offset))[0]
    id_ = '_'.join(id_re.search(item['url']).groups())
    fname = join('scraped', id_ + '.html')
    if exists(fname):
        continue
    url = base_url + item['url']
    print(url)
    r = requests.get(url)
    with open(fname, 'w') as f:
        _ = f.write(r.text)
    try:
        d_and_l = d_and_l_re.search(r.text)
        if d_and_l:
            item['donations_and_legacies'] = d_and_l.group(1)
        item['income'] = income_re.search(r.text).group(1)
        item['end_date'] = end_date_re.search(r.text).group(1)
        print(item)
        scraperwiki.sqlite.save(['url'], item)
    except AttributeError:
        print('something went wrong')
        continue
