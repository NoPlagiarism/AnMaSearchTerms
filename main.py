import os
import re
import json

MALSYNC_PATH = os.path.join(os.path.dirname(__file__), "data", "MALSync")
PAGES_PATH = os.path.join(MALSYNC_PATH, "src", "pages")


def get_name_from_main_malsync(raw_text):
    match = re.findall(r"\s{2}name:\s+'(.*)'", raw_text)
    if not match:
        return
    return match[0]

def get_type_from_main_malsync(raw_text):
    match = re.findall(r"\s{2}type:\s+'(anime|manga)'", raw_text)
    if not match:
        return
    return match[0]

def get_sterm_from_malsync_page(page_path):
    meta_path = os.path.join(page_path, "meta.json")
    if not os.path.exists(meta_path):
        return
    with open(meta_path, mode="r", encoding="utf-8") as f:
        meta_data = json.load(f)
    if "search" not in meta_data:
        return
    meta_search = meta_data["search"]
    main_path = os.path.join(page_path, "main.ts")
    if not os.path.exists(main_path):
        name = os.path.dirname(page_path)
        media_type = "Both"
        return dict(url=meta_search, name=name, media_type=media_type)
    with open(main_path, mode="r", encoding="utf-8") as f:
        main_text = f.read()
    name = get_name_from_main_malsync(main_text)
    if name is None:
        name = os.path.dirname(page_path)
    media_type = get_type_from_main_malsync(main_text)
    if media_type is None:
        media_type = "both"
    return dict(url=meta_search, name=name, media_type=media_type)

def get_malsync_sterms():
    res = list()
    if not os.path.exists(PAGES_PATH):
        raise FileNotFoundError("PAGES_PATH not found")
    for page_path in tuple(filter(lambda x: os.path.isdir(os.path.join(PAGES_PATH, x)), os.listdir(PAGES_PATH))):
        page_sterm = get_sterm_from_malsync_page(os.path.join(PAGES_PATH, page_path))
        if not page_sterm:
            print(f"Skipping {page_path}")
            continue
        res.append(page_sterm)
    return res

def save_malsync_sterms():
    mal_data = get_malsync_sterms()
    if not mal_data:
        return
    print(f"MAL-Sync total count: {len(mal_data)}")
    with open("mal_sync.json", mode="w+", encoding="utf-8") as f:
        json.dump(mal_data, f, ensure_ascii=False, indent=4)

def save_all():
    all_ = list()
    for filename in ("mal_sync.json", "custom.json"):
        with open(filename, mode="r", encoding="utf-8") as f:
            all_.extend(json.load(f))
    all_.sort(key=lambda x: x['name'])
    print(f"All total count: {len(all_)}")
    with open("all.json", mode="w+", encoding="utf-8") as f:
        json.dump(all_, f, ensure_ascii=False, indent=4)
    with open("all.min.json", mode="w+", encoding="utf-8") as f:
        json.dump(all_, f, ensure_ascii=False)

def main():
    save_malsync_sterms()
    save_all()


if __name__ == "__main__":
    main()
