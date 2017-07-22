#!/usr/bin/env python

import re
import math
import sys

import requests
from lxml import html

def stars_to_emoji(stars):
    if stars < 10:
        return ':broken_heart:'
    elif stars < 50:
        return ':purple_heart:'
    elif stars < 100:
        return ':blue_heart:'
    elif stars < 200:
        return ':green_heart:'
    elif stars < 500:
        return ':yellow_heart:'
    elif stars < 1000:
        return ':red_heart:'
    elif stars < 2000:
        return ':sparkling_heart:'
    elif stars < 3000:
        return ':heartbeat:'
    elif stars < 5000:
        return ':heartpulse:'
    else:
        return ':revolving_hearts:'

s = open('README.md').read()
links = set(re.findall('\[[^]]+\]\(https://github.com/[^/]+/[^\)]+\)', s))
for n, link in enumerate(links):
    sys.stderr.write('%d/%d\n' % (n, len(links)))
    url = link.split('(')[1][:-1]
    tree = html.fromstring(requests.get(url).text)
    stars_text = tree.xpath('//a [contains(@class, "social-count")]')[0].text
    stars = int(stars_text.replace(',', ''))
    s = s.replace(link, '%s%s' % (stars_to_emoji(stars), link))
    if n > 3:
        break
sys.stdout.write(s)
