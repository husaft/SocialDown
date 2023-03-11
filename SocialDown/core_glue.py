from core_inputs import create_sub_dir
from core_forum import extract_sxnarod, download_sxnarod
from core_imagehost import extract_imagevenue, extract_backbook, download_backbook, download_imagevenue


def handle_url(links, posts, users, hashes, url, img_root_dir, txt_root_dir):
    if ".backbook.me/" in url:
        if url not in links:
            links[url] = extract_backbook(url)
        item = links[url]
        img_dir = create_sub_dir(img_root_dir, 'backbook')
        download_backbook(item, img_dir, hashes, overwrite_time=None)
        return

    if ".imagevenue.com/" in url:
        if url not in links:
            links[url] = extract_imagevenue(url)
        item = links[url]
        img_dir = create_sub_dir(img_root_dir, 'imagevenue')
        download_imagevenue(item, img_dir, hashes, overwrite_time=None)
        return

    if ".sxnarod.com/" in url:
        if url not in links:
            links[url] = extract_sxnarod(url)
        item = links[url]
        img_dir = create_sub_dir(img_root_dir, 'sxnarod')
        txt_dir = create_sub_dir(txt_root_dir, 'sxnarod')
        download_sxnarod(posts, item, img_dir, txt_dir, users, links, hashes)
        return
