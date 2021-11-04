import yaml
import logging.config
import urllib.request
from pathlib import Path

FILE_URL = 'https://dnbradio.com/podcast/dl/livesets/' \
           'ritchey_LIVE_on_DNBRADIO.COM_20141205_0900_-_coffee_n_bass__120514__cup001.mp3'
SAVE_DIR = 'C:/Users/godin/Music'


def init_logging():
    with open('logger.yaml', 'r') as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)
    logging.config.dictConfig(config)


def extract_file_name(url):
    return url.split(sep='/')[-1]


def download_file_if_absent(url, save_dir):
    file_name = extract_file_name(url)
    logging.info(f"Checking {file_name}")
    full_path = Path(save_dir) / file_name
    if full_path.exists():
        logging.info(f"{file_name} already downloaded, skipping")
        return
    logging.info(f"Start downloading {file_name}")
    urllib.request.urlretrieve(url, full_path)
    logging.info(f"Finish downloading {file_name}")


def init_urllib():
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)


def main():
    init_logging()
    init_urllib()
    Path(SAVE_DIR).mkdir(parents=True, exist_ok=True)
    download_file_if_absent(FILE_URL, SAVE_DIR)


if __name__ == '__main__':
    main()
