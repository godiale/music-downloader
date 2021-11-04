import re
import yaml
import logging.config
import urllib.request
from pathlib import Path
from bs4 import BeautifulSoup


DNBRADIO_SEARCH_URL = 'https://dnbradio.com/?isSearch=1&pc=LiveMixes&search=ritchey&frm_event=search'
SAVE_DIR = 'C:/Users/godin/Music'


def init_logging(filename):
    with open('logger.yaml', 'r') as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)
    config['handlers']['file']['filename'] = f'log/{filename}'
    Path('log').mkdir(exist_ok=True)
    logging.config.dictConfig(config)


def extract_file_name(url):
    return url.split(sep='/')[-1]


def download_file_if_absent(url, save_dir):
    file_name = extract_file_name(url)
    logger.info(f"Checking {file_name}")
    full_path = Path(save_dir) / file_name
    if full_path.exists():
        logger.info(f"{file_name} already downloaded, skipping")
        return
    logger.info(f"Start downloading {file_name}")
    urllib.request.urlretrieve(url, full_path)
    logger.info(f"Finish downloading {file_name}")


def init_urllib():
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)


def get_links(url):
    logger.info(f"Getting links from {url}")
    req = urllib.request.Request(url)
    html_page = urllib.request.urlopen(req)
    soup = BeautifulSoup(html_page, "html5lib")
    links = []
    for link in soup.findAll('a'):
        links.append(link.get('href'))
    logger.info(f"Collected {len(links)} links")
    return links


def main():
    init_urllib()
    Path(SAVE_DIR).mkdir(parents=True, exist_ok=True)
    download_links = get_links(DNBRADIO_SEARCH_URL)
    for link in download_links:
        if re.search('.mp3$', link, re.IGNORECASE) and re.search('coffee', link, re.IGNORECASE):
            download_file_if_absent(link, SAVE_DIR)


if __name__ == '__main__':
    init_logging(filename='dnbradio_ritchey_coffee.log')
    logger = logging.getLogger(__name__)
    main()
