import os
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

BASE_URL = "https://fastnow.github.io/"
OUTPUT_FILE = "sitemap.xml"
IGNORE_DIRS = {".git", ".github", "assets"}
IGNORE_FILES = {"sitemap_generator.py", "README.md", "404.html"}

def get_last_modified(filepath):
    timestamp = os.path.getmtime(filepath)
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')

def generate_sitemap():
    urlset = Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in files:
            if file in IGNORE_FILES:
                continue
            if file.endswith('.html') or file.endswith('.htm'):
                filepath = os.path.join(root, file)
                url_path = filepath.lstrip('./').replace('\\', '/')
                if url_path.endswith('index.html'):
                    url_path = url_path[:-10]
                elif url_path.endswith('.html'):
                    url_path = url_path[:-5]
                else:
                    continue
                loc = f"{BASE_URL.rstrip('/')}/{url_path}"
                lastmod = get_last_modified(filepath)

                url = SubElement(urlset, 'url')
                SubElement(url, 'loc').text = loc
                SubElement(url, 'lastmod').text = lastmod

    rough_string = tostring(urlset, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)

    print(f"sitemap.xml 已生成，共 {len(urlset)} 条记录。")

if __name__ == "__main__":
    generate_sitemap()
