import urllib.request
from datetime import datetime
from pathlib import Path

FILE_URL = 'https://dnbradio.com/podcast/dl/livesets/' \
           'ritchey_LIVE_on_DNBRADIO.COM_20141205_0900_-_coffee_n_bass__120514__cup001.mp3'
SAVE_DIR = 'C:/Users/godin/Music'


def extract_file_name(url):
    return url.split(sep='/')[-1]


def download_file(url, save_dir):
    file_name = extract_file_name(url)
    print(f"{datetime.now()} Start downloading {file_name}")
    full_path = Path(save_dir) / file_name
    urllib.request.urlretrieve(url, full_path)
    print(f"{datetime.now()} Finish downloading {file_name}")


def init_urllib():
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)


def main():
    init_urllib()
    Path(SAVE_DIR).mkdir(parents=True, exist_ok=True)
    download_file(FILE_URL, SAVE_DIR)


if __name__ == '__main__':
    main()
