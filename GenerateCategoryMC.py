from bs4 import BeautifulSoup, SoupStrainer
from MarkovMaker import TrainAndSaveString
import urllib, os

"""
This gets links to wikipedia pages from a category page.
Returns a list.
"""

def scrape_category_page(url):
    links = []
    soup = BeautifulSoup(urllib.request.urlopen(url), 'lxml')

      ### accounts for categories with over 200 pages
    link = soup.find('a', href=True, text='next page')
    if (link != None):
        links += scrape_category_page('https://en.wikipedia.org' + link['href'])

      ### sends links of wikipedia articles in the category to be scraped
    pages_in_category = soup.find('div', {'id':'mw-pages'}).find('div',{'class':'mw-category'})
    for obj in pages_in_category.findAll('a'):
        links.append('https://en.wikipedia.org' + obj['href'])
    return links


"""
This gets the texts in the paragraphs of a webpage.
Returns a string
"""
def scrape(url):
      ### opens url so it's like a file
    link = urllib.request.urlopen(url)
    soup = BeautifulSoup(link.read().decode('utf-8'), 'lxml', parse_only=SoupStrainer('p'))

    alltxt = ''
      ### iterate thru the <p> tags
    for para in soup.find_all('p'):
        alltxt = alltxt + para.get_text() + ' '

    return alltxt

"""
Scripty script
"""


CATEGORIES = set()
while (len(CATEGORIES) < 1):
    link = urllib.request.urlopen('https://en.wikipedia.org/wiki/AdolfHitler')
    soup = BeautifulSoup(link, 'lxml')

    for cat in soup.find('div', {'id': 'catlinks'}).find('ul').findAll('li'):
        if cat.string not in CATEGORIES:
            cattext = ''
            for link in scrape_category_page('https://en.wikipedia.org' + cat.find('a')['href']):
                cattext = cattext + "\n" + scrape(link)
            print (cat.string)
            TrainAndSaveString(cattext, './Categories/' + cat.string + '.mc')
            
            #filename = './Categories/' + cat.string + '.txt'
            #os.makedirs(os.path.dirname(filename), exist_ok=True)
            #with open(filename, 'w') as file:
            #    file.write(cattext)
            
            CATEGORIES.add(cat.string)
            
print (CATEGORIES)
