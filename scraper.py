import scraperwiki, BeautifulSoup, re, urlparse

# Get the Indian Members of Parliament (Rajya Sabha)
mplist_url = 'http://india.gov.in/govt/rajyasabha.php?alpha=all'
html = scraperwiki.scrape(mplist_url)

soup = BeautifulSoup.BeautifulSoup(html)

# Find all URLs that match this pattern
mp_re = re.compile(r'.*rajyasabhampdetail.php\?mpcode=(\d+)')
key_re = re.compile(r'[^a-zA-Z0-9_\- ]+')

# For each of those URLs, parse the page
for link in soup.findAll('a', href=mp_re):
    mp_url = urlparse.urljoin(mplist_url, link.get('href'))
    # Get the full biodata page
    mp_url = mp_url.replace('rajyasabhampdetail', 'rajyasabhampbiodata')
    print mp_url
    html = scraperwiki.scrape(mp_url)
    soup = BeautifulSoup.BeautifulSoup(html)

    # Get the only table, and get the key:value pairs.
    # The first cell is the key, second is value
    table = soup.find('table')
    data = { 'url': mp_url }
    for row in table.findAll('tr'):
        cells = row.findAll('td')
        key = re.sub(key_re, '', cells[0].text)
        if key: data[key] = cells[1].text

    # Save it with the URL as the key
    scraperwiki.sqlite.save(unique_keys=['url'], data=data)
