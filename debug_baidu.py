# -*- coding: utf-8 -*-
"""Debug script to understand Baidu API response format."""
import requests, re, json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://image.baidu.com/',
}

# Use correct GBK encoding URL for 上海和平饭店
word_bytes = '上海和平饭店'.encode('gbk')
word_encoded = requests.utils.quote(word_bytes)
print("Encoded word:", word_encoded)

url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&word=' + word_encoded + '&pn=0&rn=30'
print("URL:", url)
print()

r = requests.get(url, headers=headers, timeout=15)
print("Status:", r.status_code)
print("Content-Type:", r.headers.get('Content-Type'))
print("Content-Encoding:", r.headers.get('Content-Encoding'))
print()

# Try raw content
raw = r.content
print("Raw bytes length:", len(raw))
print()

# Try to detect encoding
if raw[:3] == b'\xef\xbb\xbf':
    print("Has UTF-8 BOM")
    text = raw[3:].decode('utf-8', errors='replace')
elif raw[:2] == b'\xff\xfe':
    print("Has UTF-16 LE BOM")
    text = raw.decode('utf-16-le', errors='replace')
else:
    text = r.text

# Save to file for inspection
with open('C:/Users/gjx68/Desktop/shanghai-evolution/debug_response.txt', 'w', encoding='utf-8') as f:
    f.write(text[:10000])

print("First 500 chars:")
print(text[:500])
print()
print("...")
print()

# Check for thumbURL
if 'thumbURL' in text:
    print("'thumbURL' found in text")
else:
    print("'thumbURL' NOT found in text")
    
# Check for middleURL
if 'middleURL' in text:
    print("'middleURL' found in text")
else:
    print("'middleURL' NOT found in text")

# Find URLs ending with image extensions
img_urls = re.findall(r'"(https?://[^"]+\.(?:jpg|jpeg|png|gif|webp)[^"]*)"', text)
print("\nDirect image URLs:", len(img_urls))
for u in img_urls[:5]:
    print(" ", u[:100])

# Check if there's a different key
print("\nSearching for URL-like patterns...")
all_url_patterns = re.findall(r'"(https?://[^"]+)"', text)
print("Total URL patterns:", len(all_url_patterns))
for u in all_url_patterns[:10]:
    print(" ", u[:100])

# Try to parse as JSON
try:
    data = json.loads(text)
    print(f"\nJSON parsed successfully. Top keys: {list(data.keys())}")
    items = data.get('data', [])
    print(f"Data items count: {len(items)}")
    if items and isinstance(items[0], dict):
        print(f"First item keys: {list(items[0].keys())[:15]}")
except Exception as e:
    print(f"\nJSON parse failed: {e}")