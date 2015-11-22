#!/usr/bin/env python3

"""
Colorize source-code blocks using pygments.
"""

import argparse
import glob
import os
import re
import sys

from itertools import chain
from lxml import html
from os import path


def fix_urls(tree, rexp, xpath, attr):
    for link in tree.xpath(xpath):
        url = link.get(attr)
        if url and rexp.search(url):
            # link_str = html.tostring(link).strip()
            link.set(attr, '../' + url)
            # print ('{} -> {}'.format(link_str, html.tostring(link).strip()))


def main(arguments):

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('output', help="Pelican output directory")

    args = parser.parse_args(arguments)

    subdirs = [d for d in os.listdir(args.output)
               if path.isdir(path.join(args.output, d))]

    rexp = re.compile(r'^({})'.format('|'.join(subdirs)))

    infiles = chain.from_iterable(glob.glob(path.join(args.output, f, '*.html'))
                                  for f in ['author', 'category', 'tag'])

    # There were problems with writing the page - it complained that
    # the type was BYTE not str so explicitly convert to and from
    for infile in infiles:
        with open(infile) as f:
            pageAsUTF8 = f.read()
            pageAsBytes = pageAsUTF8.encode(encoding='UTF-8')
            tree = html.fromstring(pageAsBytes)

        fix_urls(tree, rexp, '//img', 'src')
        fix_urls(tree, rexp, '//a', 'href')

        with open(infile, 'w') as f:
            pageAsUTF8 =html.tostring(tree).decode(encoding="UTF-8") 
            print("RESULT", type(pageAsUTF8), infile)
            f.write(pageAsUTF8)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
