#/usr/bin/env python

# author: Hadi Cahyadi (cumulus13@gmail.com)
# purpose: buzzheavier link generator

import sys
import ctraceback
sys.excepthook = ctraceback.CTraceback
import requests
from bs4 import BeautifulSoup as bs
import argparse
from rich.console import Console
console = Console()
from configset import configset
from pathlib import Path
from parserheader import Parserheader
from pydebugger.debug import debug
import shutil
import clipboard
from urllib.parse import urlparse

class Buzz:
    CONFIGFILE = Path(__file__).parent / 'buzz.ini'
    CONFIG = configset(str(CONFIGFILE))
    SESS = requests.Session()
    SESS.headers.update(Parserheader()())

    @classmethod
    def get_name(self, url):
        if '/download' in url: url = url.split('/download')[0]
        a = self.SESS.get(url)
        content = a.content
        b = bs(content, 'lxml')
        name = b.find('span', {'class':'text-2xl'})
        debug(name = name)
        if name:
            return name.text
        return ''
    
    @classmethod
    def generate(self, url):
        '''
        @return: str: direct_url, bool: error_status
        '''
        if not "/download" in url:
            url += "/download"
        t_url = url.split("//")
        debug(t_url = t_url)
        if len(t_url) > 2: url = url.replace("//", "/", 1)
        url = url.strip()
        debug(url = url)
        self.SESS.headers.update({'referer':url.split("/download")[0]})
        self.SESS.headers.update({'hx-current-url':url.split("/download")[0]})
        self.SESS.headers.update({'hx-request':'true'})
        self.SESS.headers.update({'priority':'u=1, i'})
        debug(self_SESS_headers = self.SESS.headers)
        a = self.SESS.get(url.strip())
        headers = a.headers
        debug(headers = headers)
        d_url = headers.get('Hx-Redirect')
        if not d_url:
            return "", True
        p_url = urlparse(url)
        direct_url = p_url.scheme + "://" + p_url.netloc + d_url
        debug(direct_url = direct_url)
        name = self.get_name(p_url.scheme + "://" + p_url.netloc)
        return direct_url, name, False
    
    @classmethod
    def usage(self):
        parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument('URL', help = 'buzzheavier url', nargs = '*')
        parser.add_argument('-c', '--clip', help = 'copy direct link url to clipboard', action='store_true')
        if len(sys.argv) == 1:
            parser.print_help()
        else:
            args = parser.parse_args()
            for url in args.URL:
                direct_url, name, error = self.generate(url)
                console.print(f"[black on #FFFF00]Generated:[/]")
                console.print(f"  [bold #00FFFF]NAME  :[/] [bold #FFAA00]{name}[/]")
                console.print(f"  [bold #00FFFF]URL   :[/] [white on #5500FF]{direct_url}[/]")
                console.print(f"  [bold #00FFFF]ERROR :[/] [white on red]{'ERROR' if error else 'SUCCESS'}[/]")
                console.print(f"{'-'*shutil.get_terminal_size()[0]}")
                if args.clip:
                    clipboard.copy(direct_url)


if __name__ == '__main__':
    Buzz.usage()
                