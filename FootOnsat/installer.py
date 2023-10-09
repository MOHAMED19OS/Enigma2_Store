# -*- coding: utf-8 -*-
# code BY: MOHAMED_OS

from __future__ import print_function

import ssl
from os import chdir, popen, remove, system
from os.path import isdir, isfile, join
from re import MULTILINE, S, findall
from shutil import move
from sys import version_info
from time import sleep

if version_info[0] == 3:
    from urllib.error import HTTPError, URLError
    from urllib.request import Request, urlopen, urlretrieve
else:
    from urllib import urlretrieve

    from urllib2 import HTTPError, Request, URLError, urlopen

# colors
C = "\033[0m"     # clear (end)
R = "\033[0;31m"  # red (error)
G = "\033[0;32m"  # green (process)
B = "\033[0;36m"  # blue (choice)
Y = "\033[0;33m"  # yellow (info)

ssl._create_default_https_context = ssl._create_unverified_context

class FootOnsat():
    URL = 'https://raw.githubusercontent.com/MOHAMED19OS/Enigma2_Store/main/FootOnsat/'
    page = "https://github.com/MOHAMED19OS/Enigma2_Store/tree/main/FootOnsat"

    def __init__(self):
        self.NamePkg = "enigma2-plugin-extensions-footonsat"
        self.package = ['python-sqlite3','python-six','alsa-utils-aplay']
        self.plugin_path='/usr/lib/enigma2/python/Plugins/Extensions/FootOnSat'

        if version_info[0] == 3:
            self.package = list(
                map(lambda x: x.replace('python', 'python3'), self.package))

    def Stb_Image(self):
        if isfile('/etc/opkg/opkg.conf'):
            self.status = '/var/lib/opkg/status'
            self.update = 'opkg update >/dev/null 2>&1'
            self.install = 'opkg install'
            self.list = 'opkg list'
            self.uninstall = 'opkg remove --force-depends'
        elif isfile('/etc/apt/apt.conf'):
            self.status = '/var/lib/dpkg/status'
            self.update = 'apt-get update >/dev/null 2>&1'
            self.install = 'apt-get install -y'
            self.list = 'apt-get list'
            self.uninstall = 'apt-get purge --auto-remove'
        return isfile('/etc/opkg/opkg.conf')


    def info(self):
        try:
            req = Request(self.page)
            req.add_header(
                'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0')
            response = urlopen(req)
            link = response.read().decode('utf-8')
            UrlData = findall('data-target.+?footonsat_(.+?)_',link,S)
            return UrlData[0]
        except HTTPError as e:
            print('{}HTTP Error code{}: '.format(Y,C), e.code)
        except URLError as e:
            print('{}URL Error{}: '.format(R,C), e.reason)

    def banner(self):
        system('clear')
        print(B, r'''
d88888b  .d88b.   .d88b.  d888888b  .d88b.  d8b   db .d8888.  .d8b.  d888888b
88'     .8P  Y8. .8P  Y8. `~~88~~' .8P  Y8. 888o  88 88'  YP d8' `8b `~~88~~'
88ooo   88    88 88    88    88    88    88 88V8o 88 `8bo.   88ooo88    88
88~~~   88    88 88    88    88    88    88 88 V8o88   `Y8b. 88~~~88    88
88      `8b  d8' `8b  d8'    88    `8b  d8' 88  V888 db   8D 88   88    88
YP       `Y88P'   `Y88P'     YP     `Y88P'  VP   V8P `8888Y' YP   YP    YP''', C)

    def check(self, pkg):
        with open(self.status) as file:
            for item in file.readlines():
                if item.startswith('Package:'):
                    if findall(pkg, item[item.index(' '):].strip(), MULTILINE):
                        return True
            file.close()

    def version(self, name):
        return popen("{} | grep {} | awk '{{print $3}}'".format(self.list,name)).read().strip()

    def main(self):
        self.Stb_Image()

        if self.Stb_Image():
            FileName_ = "{}_{}_all.ipk".format(self.NamePkg,self.info())
        else:
            FileName_ = "{}_{}_all.deb".format(self.NamePkg,self.info())

        for filename in self.package:
            if not self.check(filename):
                system(self.update)
                system('clear')
                print("   >>>>   {}Please Wait{} while we Install {}{}{} ...".format(
                    G, C, Y, filename, C))
                system(" ".join([self.install, filename]))
                sleep(1)

        system('clear')
        self.banner()
        sleep(2)


        if isfile(join('/tmp/', FileName_)):
            remove(join('/tmp/', FileName_))
            sleep(0.8)

        version_stb = self.version(self.NamePkg)

        if version_stb == self.info():
            system('clear')
            print('you are use the latest version: {}{}{}\n'.format(Y, self.info(), C).capitalize())
            sleep(0.8)
            print("\n   Written by {}MOHAMED_OS{} (͡๏̯͡๏)\n".format(R, C))
            exit()
        elif version_stb == '':
            pass
        elif version_stb > self.info():
            print("\n   Written by {}MOHAMED_OS{} (͡๏̯͡๏)\n".format(R, C))
            exit()
        else:
            if isfile(join(self.plugin_path,'db/footonsat.db')):
                print("Keep old db....")
                move('/usr/lib/enigma2/python/Plugins/Extensions/FootOnSat/db/footonsat.db','/tmp')
            system(" ".join([self.uninstall, self.NamePkg]))

        system('clear')
        print("{}Please Wait{} while we Download And Install {}FootOnsat{} ...".format(
            G, C, Y, C))

        chdir('/tmp')

        urlretrieve("".join([self.URL, FileName_]), filename=FileName_)
        sleep(0.8)

        system(" ".join([self.install, FileName_]))
        sleep(1)

        if isfile(join('/tmp/', FileName_)):
            remove(join('/tmp/', FileName_))
            sleep(0.8)

        if isdir(self.plugin_path):
            if isfile('/tmp/footonsat.db'):
                if isfile(join(self.plugin_path,'db/footonsat.db')):
                    remove(join(self.plugin_path,'db/footonsat.db'))
                    move('/tmp/footonsat.db',join(self.plugin_path,'db'))

        print('{}(?){} Device will restart now'.format(B, C))
        if self.Stb_Image():
            system('killall -9 enigma2')
        else:
            system('systemctl restart enigma2')


if __name__ == '__main__':
    build = FootOnsat()
    build.main()
    print("   Written by {}MOHAMED_OS{} (͡๏̯͡๏)".format(R, C))
