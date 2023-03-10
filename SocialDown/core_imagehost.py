from bs4 import BeautifulSoup
import shutil
import requests
from core_inputs import clean_string
from os.path import join, isfile


def download_backbook(item, img_dir, overwrite_time):
    title = item['t']
    images = item['i']
    index = 0
    for image in images:
        index += 1
        group = image['a'].split('-')[1].strip()
        imgurl = image['s']
        if overwrite_time is None:
            time_raw = [] if '//fu' in imgurl \
                else imgurl.split('/file/')[1].split('/')
            time = 't' if len(time_raw) == 0 \
                else f"{time_raw[0]}-{time_raw[1]}-{time_raw[2]}"
        else:
            time = overwrite_time
        imgname = imgurl.split('/')[-1].replace("full_", "")
        tgtname = f"{time}_{group}_{index:02d}_{imgname}"
        full_tgtname = join(img_dir, tgtname)
        if isfile(full_tgtname):
            continue
        print(f"   - {title}")
        req = requests.get(imgurl, stream=True, allow_redirects=False)
        with open(full_tgtname, 'wb') as out_file:
            shutil.copyfileobj(req.raw, out_file)
        print(f"     --> {full_tgtname}")


def download_imagevenue(item, img_dir, overwrite_time):
    title = item['t']
    images = item['i']
    index = 0
    for image in images:
        index += 1
        imgurl = image['s']
        group = imgurl.split('/upload')[1].split('/')[0]
        if overwrite_time is None:
            time = 't'
        else:
            time = overwrite_time
        imgname = imgurl.split('/')[-1]
        tgtname = f"{time}_{group}_{index:02d}_{imgname}"
        full_tgtname = join(img_dir, tgtname)
        if isfile(full_tgtname):
            continue
        print(f"   - {title}")
        req = requests.get(imgurl, stream=True, allow_redirects=False)
        with open(full_tgtname, 'wb') as out_file:
            shutil.copyfileobj(req.raw, out_file)
        print(f"     --> {full_tgtname}")


def extract_backbook(url):
    print(f" * Extracting '{url}'...")
    req = requests.get(url, allow_redirects=True)
    soup = BeautifulSoup(req.content, 'html.parser')
    title = clean_string(soup.find('title').string)
    imgs = soup.find_all('img')
    img_list = list()
    for img in imgs:
        alt = img.get('alt')
        if "Photo" not in alt:
            continue
        src = img.get('src')
        img_list.append({'a': alt, 's': src})
    return {'t': title, 'i': img_list}


def extract_imagevenue(url):
    print(f" * Extracting '{url}'...")
    req = requests.get(url, allow_redirects=True)
    soup = BeautifulSoup(req.content, 'html.parser')
    title = clean_string(soup.find('title').string)
    imgs = soup.find_all('img')
    img_list = list()
    for img in imgs:
        alt = img.get('alt')
        if alt is None:
            continue
        src = img.get('src')
        img_list.append({'a': alt, 's': src})
    return {'t': title, 'i': img_list}
