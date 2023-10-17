import requests
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom

def main():
    output_file = "makeRSS_ZDNetJapan.xml"
  
    feed = {
        "url": "http://feed.japan.zdnet.com/rss/index.rdf",
        "includeWords": ["AI", "ChatGPT", "DX", "自動化", "RPA", "ノーコード", "ローコード"]
    }
    
    url = feed["url"]
    includeWords = feed["includeWords"]
    
    response = requests.get(url)
    rss_content = response.text
    
    results = []
    items = re.findall(r"<item[^>]*>([\s\S]*?)<\/item>", rss_content)
    
    for item in items:
        title = re.search(r"<title>(.*?)<\/title>", item).group(1)
        link = re.search(r"<link>(.*?)<\/link>", item).group(1)
        description = re.search(r"<description>([\s\S]*?)<\/description>", item).group(1)
        date = re.search(r"<dc:date>(.*?)<\/dc:date>", item).group(1)
        
        if any(word in title or word in description for word in includeWords):
            results.append({
                "date": date,
                "title": title,
                "link": link,
                "description": description
            })
            
    root = ET.Element("rss", version="2.0")
    channel = ET.SubElement(root, "channel")
    
    title = "ZDNet Japanの特定のキーワードを含むRSS" if url == "http://feed.japan.zdnet.com/rss/index.rdf" else "特定のキーワードを含むRSS"
    description = "ZDNet Japanから特定のキーワードを含む記事を提供します。" if url == "http://feed.japan.zdnet.com/rss/index.rdf" else "指定したキーワードを含む記事を提供します。"

    ET.SubElement(channel, "title").text = title
    ET.SubElement(channel, "description").text = description
    ET.SubElement(channel, "link").text = "https://example.com"
    
    for result in results:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = result["title"]
        ET.SubElement(item, "link").text = result["link"]
        ET.SubElement(item, "description").text = result["description"]
        ET.SubElement(item, "pubDate").text = result["date"]

    xml_str = ET.tostring(root)
    xml_pretty_str = minidom.parseString(xml_str).toprettyxml(indent="  ")

    with open(output_file, "w") as f:
        f.write(xml_pretty_str)

if __name__ == "__main__":
    main()
