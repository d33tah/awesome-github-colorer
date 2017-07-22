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

s = open(sys.argv[1]).read()
links = set(re.findall('\[[^]]+\]\(https://github.com/[^/]+/[^\)]+\)', s))
for n, link in enumerate(links):
    sys.stderr.write('%d/%d\n' % (n + 1, len(links)))
    url = link.split('(')[1][:-1]
    tree = html.fromstring(requests.get(url).text)
    stars_xpath = '//a [contains(@class, "social-count") and contains(@href, "/stargazers")]'
    try:
        stars_text = tree.xpath(stars_xpath)[0].text
    except IndexError:
        sys.stderr.write('IndexError on %s\n' % url)
        continue
    stars = int(stars_text.replace(',', ''))
    s = s.replace(link, '%s%s' % (stars_to_emoji(stars), link))
sys.stdout.write(s)
