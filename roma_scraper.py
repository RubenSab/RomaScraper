from selenium import webdriver
from bs4 import BeautifulSoup

class RomaScraper():
    def __init__(self):
        self.URL = "https://forzaroma.info"
        self.parsed_news = []

    def get_html(self) -> str:
        driver = webdriver.Chrome()
        driver.get(self.URL)
        html = driver.page_source
        return html


    def get_titles(self, html: str) -> list[dict[str, str]]:
        soup = BeautifulSoup(html, 'html.parser')
        raw_news = soup.find_all('div', class_='bck-gn-media-news')

        parsed_news = []
        for news in raw_news:
            # Titolo
            title_tag = news.find('h4', class_='title')
            title = title_tag.get_text(strip=True) if title_tag else None
            if title:
                # Link
                link_tag = title_tag.find('a') if title_tag else None
                link = link_tag['href'] if link_tag and link_tag.has_attr('href') else 'N/A'
                # Data e ora
                time_tag = news.find('time')
                date = time_tag.get('datetime') if time_tag else 'N/A'
                #text_date = time_tag.get_text(strip=True) if time_tag else 'N/A'
                # Abstract
                abstract_tag = news.find('div', class_='gzn_home_abstract')
                abstract = abstract_tag.get_text(strip=True) if abstract_tag else 'N/A'

                # Output
                parsed_news.append({
                    'title': title,
                    'link': link,
                    'date': date,
                    'abstract': abstract
                })
        self.parsed_news = parsed_news
        return parsed_news


    def export_csv(self, filename: str) -> None:
        with open(filename, 'w') as f:
            f.write(','.join(self.parsed_news[0].keys())+'\n')
            for article in self.parsed_news:
                f.write(', '.join([f'"{field}"' for field in article.values()])+'\n')


    def export_html(self, filename) -> None:
        with open(filename, 'w') as f:
            f.write('<!DOCTYPE html>\n<html>\n<head>\n')
            f.write('<meta charset="UTF-8">\n')
            f.write('<title>Notizie da forzaroma.info</title>\n')
            f.write('<link rel="stylesheet" href="style.css">\n')
            f.write('</head>\n<body>\n')
            f.write('<h1>Notizie da forzaroma.info</h1>\n')
            f.write('<ul>\n')
            for article in self.parsed_news:
                link = article['link']
                text = f"{article['title']} ({article['date']})"
                f.write(f'\t<li><a href={link}>{text}</a></li>\n')
            f.write('</ul>\n')
            f.write('</body>\n</html>')


if __name__ == '__main__':

    scraper = RomaScraper()
    html = scraper.get_html()
    scraper.get_titles(html)
    scraper.export_csv('news.csv')
    scraper.export_html('website/news.html')
