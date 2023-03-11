from core_glue import handle_url
from core_inputs import load_json, load_lines, save_json, create_dir


def run_tool():
    hashes = load_json('hashes.json')
    links = load_json('links.json')
    posts = load_json('posts.json')
    urls = load_lines('urls.txt')
    print(f"Unique input URLs = {len(urls)}")
    users = load_lines('users.txt')
    print(f"Unique user names = {len(users)}")
    img_dir = create_dir('images')
    txt_dir = create_dir('texts')
    print(f"Image destination = {img_dir}")
    print(f"Text destination = {txt_dir}")
    for url in urls:
        before_nr_h = len(hashes)
        before_nr_l = len(links)
        before_nr_p = len(posts)
        handle_url(links, posts, users, hashes, url, img_dir, txt_dir)
        after_nr_h = len(hashes)
        after_nr_l = len(links)
        after_nr_p = len(posts)
        if before_nr_h != after_nr_h:
            save_json(hashes, 'hashes.json')
        if before_nr_l != after_nr_l:
            save_json(links, 'links.json')
        if before_nr_p != after_nr_p:
            save_json(posts, 'posts.json')
    print("Done.")


if __name__ == '__main__':
    run_tool()
