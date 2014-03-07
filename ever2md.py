#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import argparse
import html2text
import sys
import codecs
import re
import os
import time
from datetime import datetime
parser = argparse.ArgumentParser(description="Process html files" , usage='%(prog)s [options]' , add_help=True)
parser.add_argument('-f', '--filename', required=True)
args = parser.parse_args()
filename = args.filename
print("Converting: " + filename)
content = codecs.open(filename, mode="r", encoding="utf-8")
soup = BeautifulSoup(content)
invalid_tags = ['strong', 'span', 'style', 'i', 'u', 'b']
for tag in invalid_tags:
    for match in soup.findAll(tag):
        match.unwrap()
title = soup.title.string
for tag in soup():
    for attribute in ["class", "id", "name", "style"]:
        del tag[attribute]
texto = soup.prettify()
h = html2text.HTML2Text()
h.ignore_images = True
h.body_width = 0
textof = h.handle(texto)
s = re.sub("[\W]+", '_', title, flags = re.U)
def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)
s = removeNonAscii(s)
newname = s + ".md"
path = os.path.abspath(os.path.join(os.path.dirname(filename)))

if os.path.exists(newname):
    suffix = str(datetime.now().strftime("_%H_%M_%S.%f"))
    newname = s + suffix + ".md"
    path = os.path.join(path, newname)
    print("File exists, renaming to: %s" % newname)
    output_file = codecs.open(path, "w", encoding="utf-8")
    output_file.write(textof)
else:
    print("Writing to: %s" % newname)
    path = os.path.join(path, newname)
    output_file = codecs.open(path, "w", encoding="utf-8")
    output_file.write(textof)
