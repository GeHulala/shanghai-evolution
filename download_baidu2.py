# -*- coding: utf-8 -*-
"""Download real photos using node.js script (more reliable)."""
import os, sys, json, time, subprocess

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'photos')
os.makedirs(OUT, exist_ok=True)

PHOTOS = [
    {'query': '上海和平饭店 外景', 'file': '01-peace-hotel.jpg'},
    {'query': '上海东方明珠塔 全景', 'file': '02-oriental-pearl.jpg'},
    {'query': '上海金茂大厦 建筑', 'file': '03-jinmao.jpg'},
    {'query': '上海环球金融中心 建筑', 'file': '04-swfc.jpg'},
    {'query': '上海中华艺术宫 外观', 'file': '05-china-art-museum.jpg'},
    {'query': '上海中心大厦 建筑', 'file': '06-shanghai-tower.jpg'},
]

# First, let's try a simpler approach - download directly from known photo sources
# using pre-made URLs from sites like pic.sogou.com
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.google.com/',
}

def download_img(url, save_path):
    try:
        r = requests.get(url, headers=headers, timeout=20, stream=True)
        if r.status_code == 200 and 'image' in r.headers.get('Content-Type', ''):
            with open(save_path, 'wb') as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
            size = os.path.getsize(save_path)
            if size > 10000:
                from PIL import Image
                img = Image.open(save_path)
                img.load()
                print(f"  [OK] {size//1024}KB {img.size}")
                return True
    except:
        pass
    return False

# Try using Sogou image search (usually more accessible)
def sogou_search_images(query):
    """Search images via Sogou."""
    import urllib.parse
    word = urllib.parse.quote(query)
    url = f'https://pic.sogou.com/pics?query={word}&mode=1&start=0&reqType=ajax&reqFrom=result'
    
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            data = r.json()
            items = data.get('items', [])
            urls = []
            for item in items:
                if isinstance(item, dict):
                    pic_url = item.get('pic_500') or item.get('pic_300') or item.get('thumb')
                    if pic_url:
                        urls.append(pic_url)
            return urls[:5]
    except:
        pass
    return []

# Also try Bing image search
def bing_search_images(query):
    """Search images via Bing."""
    import urllib.parse
    word = urllib.parse.quote(query)
    url = f'https://www.bing.com/images/search?q={word}&form=HDRSC2&first=1'
    
    import re
    try:
        r = requests.get(url, headers={**headers, 'Accept-Language': 'en-US,en;q=0.9'}, timeout=15)
        if r.status_code == 200:
            # Find image URLs in the page
            urls = re.findall(r'<img[^>]+src="(https?://[^"]+\.(?:jpg|jpeg|png)[^"]*)"', r.text)
            # Filter out small icons
            urls = [u for u in urls if 'th?id=' in u or 'bing' in u.lower() or 'media' in u.lower() or len(u) > 60]
            return urls[:5]
    except:
        pass
    return []

def main():
    print("="*60)
    print("Downloading real photos of Shanghai buildings")
    print("="*60)
    
    # Delete old files
    for f in os.listdir(OUT):
        os.remove(os.path.join(OUT, f))
        print(f"Removed old: {f}")
    
    success = 0
    for idx, photo in enumerate(PHOTOS, 1):
        query = photo['query']
        filename = photo['file']
        save_path = os.path.join(OUT, filename)
        
        print(f"\n[{idx}/6] Searching: {query}")
        
        # Try Sogou first
        print("  Trying Sogou...")
        urls = sogou_search_images(query)
        
        if not urls:
            # Try Bing
            print("  Sogou failed, trying Bing...")
            urls = bing_search_images(query)
        
        if not urls:
            print("  [FAIL] No image sources found")
            continue
        
        print(f"  Got {len(urls)} URLs")
        ok = False
        for i, url in enumerate(urls):
            print(f"  Download {i+1}: {url[:70]}...")
            if download_img(url, save_path):
                ok = True
                success += 1
                break
        
        if not ok:
            print(f"  [FAIL] All downloads failed")
        
        time.sleep(1)
    
    print(f"\n{'='*60}")
    print(f"Result: {success}/{len(PHOTOS)} photos downloaded!")
    print(f"Location: {OUT}")
    print(f"{'='*60}")
    
    if success == len(PHOTOS):
        print("\nAll photos downloaded successfully!")
    else:
        print(f"\nSome photos failed. Missing: {len(PHOTOS)-success}")
        for p in PHOTOS:
            p_path = os.path.join(OUT, p['file'])
            if not os.path.exists(p_path) or os.path.getsize(p_path) < 10000:
                print(f"  - {p['file']}")

if __name__ == '__main__':
    main()