import requests
import bs4
from fake_headers import Headers

KEYWORDS = ['Python', 'Человек', 'web']
BASE_URL = 'https://habr.com'

headers = Headers(browser='chrome', os='win').generate()

response = requests.get(f'{BASE_URL}/ru/articles/', headers=headers)

soup = bs4.BeautifulSoup(response.text, features='lxml')

articles_block = soup.select('article[data-test-id="articles-list-item"]')

for article in articles_block:
    content = article.select_one('h2')
    title = content.select_one('span').text
    link = BASE_URL + content.select_one('a[data-article-link]')['href']
    time = article.select_one('div.meta-container time')['title']
    description_body = article.select_one('div.article-formatted-body')
    description = description_body.get_text()

    if any(keyword.lower() in description.lower() for keyword in KEYWORDS):
        print(f'{time} - {title} - {link}')
