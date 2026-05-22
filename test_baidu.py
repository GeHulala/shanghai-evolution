# -*- coding: utf-8 -*-
import requests, re
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

# Search for peace hotel
url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&word=%C9%CF%BA%A3%BA%CD%C6%BD%B7%B9%B5%EA&pn=0&rn=30'
r = requests.get(url, headers=headers, timeout=10)

# Decode as gbk
text = r.content.decode('gbk', errors='replace')

# Find thumbURL
urls = re.findall(r'"thumbURL":"([^"]+)"', text)
print("thumbURLs found:", len(urls))
for u in urls[:3]:
    print(" ", u[:80])

# Also middleURL
urls2 = re.findall(r'"middleURL":"([^"]+)"', text)
print("middleURLs found:", len(urls2))
for u in urls2[:3]:
    print(" ", u[:80])

# Also objURL
urls3 = re.findall(r'"objURL":"([^"]+)"', text)
print("objURLs found:", len(urls3))
for u in urls3[:3]:
    print(" ", u[:80])

# Print raw JSON keys around data area
import json
# Try json parse
try:
    data = json.loads(text)
    items = data.get('data', [])
    print("JSON items:", len(items))
    for item in items[:2]:
        if isinstance(item, dict):
            print(" keys:", list(item.keys())[:10])
            if 'thumbURL' in item:
                print(" thumbURL:", item['thumbURL'][:60])
            break
except:
    print("JSON parse failed, searching for image URLs...")
    # Just look for http URLs that look like images
    all_urls = re.findall(r'"(https?://[^"]+\.(?:jpg|jpeg|png|webp)[^"]*)"', text)
    print("Direct image URLs:", len(all_urls))
    for u in all_urls[:3]:
        print(" ", u[:80])