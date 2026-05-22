# -*- coding: utf-8 -*-
"""Download real photos of Shanghai buildings from Baidu image search."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import requests, re, os, json, time, urllib.parse
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'photos')
os.makedirs(OUT, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://image.baidu.com/',
}

PHOTOS = [
    ('上海和平饭店', '01-peace-hotel.jpg'),
    ('上海东方明珠塔', '02-oriental-pearl.jpg'),
    ('上海金茂大厦', '03-jinmao.jpg'),
    ('上海环球金融中心', '04-swfc.jpg'),
    ('上海中华艺术宫', '05-china-art-museum.jpg'),
    ('上海中心大厦', '06-shanghai-tower.jpg'),
]

def get_baidu_img_urls(query, max_count=8):
    """Get image URLs from Baidu image search."""
    word = urllib.parse.quote(query)
    urls = []
    
    # Baidu acjson API
    api_url = f'https://image.baidu.com/search/acjson?tn=resultjson_com&word={word}&pn=0&rn=30'
    try:
        r = requests.get(api_url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            text = r.text
            # Extract thumbURL - these are direct image URLs
            found = re.findall(r'"thumbURL":"(https?://[^"]+)"', text)
            urls.extend(found)
            if not found:
                found = re.findall(r'"middleURL":"(https?://[^"]+)"', text)
                urls.extend(found)
    except Exception as e:
        print(f"  Search error: {e}")
    
    # Deduplicate
    seen = set()
    result = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            result.append(u)
    return result[:max_count]

def download_image(url, save_path):
    for attempt in range(2):
        try:
            r = requests.get(url, headers=HEADERS, timeout=20, stream=True)
            if r.status_code == 200:
                ct = r.headers.get('Content-Type', '')
                if 'image' not in ct:
                    print(f"  Not an image: {ct}")
                    return False
                with open(save_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                size = os.path.getsize(save_path)
                if size > 15000:
                    try:
                        img = Image.open(save_path)
                        img.load()
                        print(f"  [OK] {size//1024}KB {img.size[0]}x{img.size[1]}")
                        return True
                    except:
                        print(f"  Invalid image file")
                        return False
                else:
                    print(f"  Too small: {size} bytes")
                    return False
            else:
                print(f"  HTTP {r.status_code}")
        except Exception as e:
            print(f"  Attempt {attempt+1}: {e}")
            time.sleep(1)
    return False

def main():
    print("="*60)
    print("Downloading real photos from Baidu Image Search")
    print("="*60)
    
    # Delete old files
    for f in os.listdir(OUT):
        os.remove(os.path.join(OUT, f))
        print(f"Removed old: {f}")
    
    success = 0
    for idx, (query, filename) in enumerate(PHOTOS, 1):
        print(f"\n[{idx}/6] Searching: {query}")
        save_path = os.path.join(OUT, filename)
        
        urls = get_baidu_img_urls(query)
        if not urls:
            print(f"  No results, retrying with shorter name...")
            urls = get_baidu_img_urls(query[:4])
        
        if not urls:
            print(f"  [FAIL] No images found")
            continue
        
        print(f"  Got {len(urls)} URLs, trying to download...")
        ok = False
        for i, url in enumerate(urls):
            print(f"  URL {i+1}: {url[:60]}...")
            if download_image(url, save_path):
                ok = True
                success += 1
                break
        
        if not ok:
            print(f"  [FAIL] Could not download")
        time.sleep(1.5)
    
    print(f"\n{'='*60}")
    print(f"Result: {success}/6 photos downloaded successfully!")
    print(f"Location: {OUT}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()