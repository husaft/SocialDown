from bs4 import BeautifulSoup
import requests
import urllib.parse
from os.path import join, isfile
from core_inputs import clean_string, create_sub_dir
from core_imagehost import extract_imagevenue, extract_backbook, download_backbook, download_imagevenue


def extract_sxnarod(url):
    print(f" * Extracting '{url}'...")
    req = requests.get(url, allow_redirects=True)
    soup = BeautifulSoup(req.content, 'html.parser')
    lang = soup.find('html').get('lang')
    title = clean_string(soup.find('title').string)
    ass = soup.find_all('a')
    pages = dict()
    for one in ass:
        href = one.get('href')
        if href is None:
            continue
        if "sxnarod" in href and href.endswith('.html'):
            sub_nr = one.get_text()
            if len(sub_nr) == 0 or len(sub_nr) > 2:
                continue
            sub_id = int(sub_nr)
            pages[sub_id] = href
    return {'l': lang, 't': title, 'p': pages}


def extract_sxnarod_page(url):
    print(f" * Extracting page '{url}'...")
    req = requests.get(url, allow_redirects=True)
    html_text = req.content.decode("utf-8")
    html_text = html_text \
        .replace("<br></div><table", "<br><table") \
        .replace("<br> </div><table", "<br><table")
    soup = BeautifulSoup(html_text, 'html.parser')
    lang = soup.find('html').get('lang')
    title = clean_string(soup.find('title').string)
    entries = dict()
    trs = soup.find_all('tr')
    i = 0
    for one in trs:
        cells = one.find_all('td')
        meta = cells[0]
        meta_imgs = meta.find_all('img')
        if len(meta_imgs) == 0:
            continue
        meta_gender = meta_imgs[0].get('alt')
        user_strong = meta.find('strong')
        if user_strong is None:
            continue
        user_name = user_strong.get_text()
        user_name_add = meta.find('div').get_text()
        user_avatar = meta_imgs[1 if len(meta_imgs) >= 2 else 0].get('src')
        user_avatar = user_avatar.split('/')[-1].replace('.jpg', '') \
            .replace('.png', '').replace('.gif', '').replace('user_avatar_', '')
        content = cells[1]
        time_stamp = content.find('i').get_text().strip()
        img_list = set()
        imgs = content.find_all('a')
        for one_img in imgs:
            img_list.add(one_img.get('href'))
        img_list = sorted(img_list)
        content_txt = content.get_text().replace(time_stamp, '').strip()
        i += 1
        entries[i] = {'g': meta_gender, 'n': user_name, 'd': user_name_add,
                      'i': user_avatar, 't': time_stamp, 'l': img_list, 'c': content_txt}
    return {'l': lang, 't': title, 'e': entries}


def download_sxnarod(posts, page_item, img_dir, txt_dir, users, all_links):
    pages = page_item['p']
    for page_idx in pages:
        page_url = pages[page_idx]
        if page_url not in posts:
            posts[page_url] = extract_sxnarod_page(page_url)
        res = posts[page_url]
        lang = res['l']
        title = res['t']
        entries = res['e']
        page_id = page_url.split('/')[-1].replace('-t.html', '')

        full_txt_path = join(txt_dir, page_id + ".txt")
        if not isfile(full_txt_path):
            print(f"   - #{int(page_idx):02d} ({len(entries):02d} E) [{lang}] {title}")
            print(f"     --> {full_txt_path}")
            with open(full_txt_path, 'w') as text_file:
                text_file.write(page_url + '\n' + '\n')
                text_file.write(f"nr = {page_idx}" + '\n')
                text_file.write(f"lang = {lang}" + '\n')
                text_file.write(f"title = {title}" + '\n')
                text_file.write(f"entries = {len(entries)}" + '\n' + '\n' + '\n')
                for entry_idx in entries:
                    entry_val = entries[entry_idx]
                    gender = entry_val["g"]
                    name = entry_val["n"]
                    desc = entry_val["d"]
                    iter = entry_val["i"]
                    time = entry_val["t"]
                    link = entry_val["l"]
                    cont = entry_val["c"].strip()
                    text_file.write(f"[{entry_idx}]" + '\n')
                    text_file.write(f"({time})" + '\n')
                    text_file.write(f"{iter} | {gender} | {name} | {desc}" + '\n')
                    if len(link) >= 1:
                        text_file.write(f"{len(link)} link(s)" + '\n')
                    text_file.write('\n')
                    text_file.write("'" + cont + "'" + '\n')
                    text_file.write('\n')
                    text_file.write('\n')

        link_count = sum([len(entries[x]["l"]) for x in entries if entries[x]["n"] in users])
        link_idx = 0
        for entry_idx in entries:
            entry_val = entries[entry_idx]
            name = entry_val["n"]
            if name not in users:
                continue
            name_img_dir = create_sub_dir(img_dir, name.replace(' ', '_'))
            link = entry_val["l"]
            time_raw = entry_val["t"].split(' - ')[0].strip().split('-')
            time = time_raw[2] + "-" + time_raw[1] + "-" + time_raw[0]
            for one_link in link:
                link_idx += 1
                if link_idx == 1:
                    print(f"   - #{int(page_idx):02d} ({link_count:03d} L) [{lang}] {title}")
                if one_link.startswith('/'):
                    continue
                if '.sxnarod.com/away.php?' in one_link:
                    one_link = urllib.parse.unquote(one_link.split('?url=')[1])
                if '.sxnarod.com/' in one_link:
                    continue
                if 'sxn.today/' in one_link:
                    continue
                if 'hostingfailov.com' in one_link:
                    continue
                if '.kolgotki.net/' in one_link:
                    continue
                if 'webfile.ru/' in one_link:
                    continue
                if 'gigapeta.com/' in one_link:
                    continue
                if 'globalforum.ru/' in one_link:
                    continue
                if '.imagebam.com/' in one_link:
                    continue
                if 'imagetwist.com/' in one_link:
                    continue
                if 'pixroute.com/' in one_link:
                    continue
                if 'pimpandhost.com/' in one_link:
                    continue
                if 'imagenpic.com/' in one_link:
                    continue
                if ".backbook.me/" in one_link:
                    if one_link not in all_links:
                        all_links[one_link] = extract_backbook(one_link)
                    bb_item = all_links[one_link]
                    img_dl_dir = create_sub_dir(name_img_dir, page_id)
                    download_backbook(bb_item, img_dl_dir, overwrite_time=time)
                    continue
                if ".imagevenue.com/" in one_link:
                    if one_link not in all_links:
                        all_links[one_link] = extract_imagevenue(one_link)
                    iv_item = all_links[one_link]
                    img_dl_dir = create_sub_dir(name_img_dir, page_id)
                    download_imagevenue(iv_item, img_dl_dir, overwrite_time=time)
                    continue
