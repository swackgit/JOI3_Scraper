#! /usr/bin/python3
from email.utils import formatdate
from bs4 import BeautifulSoup
import requests
import re
from variables import *

rss_opening_tags = f'<?xml version="1.0" encoding="utf-8"?>\n<rss version="2.0"\n' \
                   f'xmlns:content="http://purl.org/rss/1.0/modules/content/"\n' \
                   f'xmlns:wfw="http://wellformedweb.org/CommentAPI/"\n' \
                   f'xmlns:dc="http://purl.org/dc/elements/1.1/"\n' \
                   f'xmlns:atom="http://www.w3.org/2005/Atom"\n' \
                   f'xmlns:sy="http://purl.org/rss/1.0/modules/syndication/"\n' \
                   f'xmlns:slash="http://purl.org/rss/1.0/modules/slash/"\n>\n<channel>' \
                   f'\n<title>JOI feed</title>\n' \
                   f'<atom:link href="https://swack.ddns.net/swack.rss" rel="self" type="application/rss+xml" />\n' \
                   f'<link>' \
                   f'http://www.planetsuzy.org/t1027914-planetsuzys-jerkoff-instruction-encouragement-videos-iii.html' \
                   f'</link>' \
                   f'\n<description> dunno stuff </description>\n' \
                   f'\n<lastBuildDate>{formatdate()}</lastBuildDate>'
item_link = f'http://www.planetsuzy.org/showpost.php?p='

usernames, post_numbers, post_counts, descriptions = ([] for i in range(4))
next_page = True

while next_page:
    for i in range(start_page, 1000):
        try:
            # with open(f"page{i}.txt", 'rb') as output:
            output = requests.get(f'http://www.planetsuzy.org/t1027914-p{i}-planetsuzys-jerkoff-instruction-encouragement-videos-iii.html')
            output.raise_for_status()
            soup = BeautifulSoup(output.text, 'html.parser')
#            print(i)
        except TypeError:
            break

        # get text of item
        post_messages = soup.find_all('div', id=re.compile(r"post_message_\d{8}"))
        for post_message in post_messages:
            parent2 = post_message.parent
            parent3 = parent2.find('div', id=re.compile(r"post_message_\d{8}"))
            parent3 = re.sub(r'<div.*?>|<font.*?>|<ol.*?>|</font>|</ol>|</div>|onload.*?this\)', "", str(parent3))
            parent3 = re.sub(r'<script type.*?/fieldset>', "", str(parent3), flags=re.S)
            descriptions.append(parent3)
            # print(parent3)
            # print('=' * 150)

        # get username to make author
        uns = soup.find_all(class_="bigusername")
        for username in uns:
            parent = username.parent.text.strip()
            usernames.append(parent)
            # print(parent)

        # get post number
        p_nums = soup.find_all(id=re.compile(r"postcount\d{8}"))
        for post_num in p_nums:
            rent = post_num.parent.text.strip()
            post_numbers.append(rent[1:])
            # print(rent[1:])

        # get exact post count
        p_counts = soup.find_all('a', class_="bigusername")
        for pc in p_counts:
            rent = pc.parent
            rent2 = rent.attrs['id']
            post_counts.append(rent2[9:])
            # print(rent2[9:])

        # find next page link
        npl = bool(soup.find(rel="next"))
        next_page = npl
        with open("/var/www/python/JOI3_scraper/variables.py", 'w') as w:
            w.write(f"start_page = {i}")
        if next_page is False:
            break


with open('/var/www/html/swack.rss', 'w', encoding="utf-8") as f:
    f.write(f"{rss_opening_tags}")
    for x in range(len(usernames)):
        f.write(f"<item>\n<title>{'{:0>4}'.format(post_numbers[x])} - {usernames[x]}</title>\n"
                f"<link>{item_link}{post_counts[x]}</link>\n"
                f"<dc:creator><![CDATA[{usernames[x]}]]></dc:creator>\n"
                f"<guid>{item_link}{post_counts[x]}</guid>\n"
                f"<description><![CDATA[{descriptions[x]}]]></description>\n"
                f"<pubDate>{formatdate()}</pubDate>\n</item>")
    f.write(f"\n</channel>\n</rss>")

