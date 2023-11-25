from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re

def print_hacker_style(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def remove_non_ascii(text):
    return ''.join(char for char in text if char.isascii() or ord(char) > 127)

def analyze_seo_selenium(url):

    print(print_hacker_style("Analyzing the website...\n", "91"))

    if not re.match(r'https?://', url):
        url = 'http://' + url
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(5)

    page_source = driver.page_source

    driver.quit()

    soup = BeautifulSoup(page_source, 'html.parser')

    cms_tag = soup.find('meta', attrs={'name': 'generator'})
    cms = remove_non_ascii(cms_tag['content']) if cms_tag else 'Unknown CMS'

    title_tag = soup.find('title')
    title = remove_non_ascii(title_tag.text) if title_tag else 'No title'

    keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
    keywords = remove_non_ascii(keywords_tag['content']) if keywords_tag else 'No keywords'

    h1_tags = soup.find_all('h1')
    h1_list = [remove_non_ascii(h1.text) for h1 in h1_tags]

    images = soup.find_all('img')
    missing_alt_images = [img['src'] for img in images if 'alt' not in img.attrs]

    links = soup.find_all('a')
    invalid_links = [(remove_non_ascii(link.text), link.get('href', 'No href attribute')) for link in links if not link.get('href')]

    print(f'1. CMS: {cms}')
    print(f'2. Title: {title}')
    print(f'3. Keywords: {keywords}')
    print(f'4. Number of H1 headers: {len(h1_list)}')
    print(f'   List of H1 headers: {h1_list}')

    print(f'5. Number of images without alt attribute: {len(missing_alt_images)}')

    print(f'6. Invalid links:')
    if invalid_links:
        for link_text, link_href in invalid_links:
            print(f'      {link_text}: {link_href}')
    else:
        print('      No invalid links.')

while True:
    print(print_hacker_style("MENU", "97"))
    print("1. Analyze a website")
    print("2. Exit")

    choice = input("Choose an option (1/2): ")

    if choice == '1':
        url_to_analyze = input("Enter the URL to analyze: ")
        analyze_seo_selenium(url_to_analyze)
    elif choice == '2':
        break
    else:
        print("Invalid choice. Choose 1 or 2.")
