# -*- coding: utf-8 -*-
# code BY: MOHAMED_OS

from __future__ import print_function

from os import chdir, popen, remove, system
from os.path import isfile, join
from re import MULTILINE, findall
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


class RakutenTV():
    URL = 'https://raw.githubusercontent.com/MOHAMED19OS/Enigma2_Store/main/RakutenTV/'
    page = "https://github.com/MOHAMED19OS/Enigma2_Store/tree/main/RakutenTV"

    def __init__(self):
        self.package = ['python-requests','enigma2-plugin-systemplugins-serviceapp', 'exteplayer3', 'gstplayer']

        if version_info[0] == 3:
            self.package = list(
                map(lambda x: x.replace('python', 'python3'), self.package))

    def Stb_Image(self):
        if isfile('/etc/opkg/opkg.conf'):
            self.status = '/var/lib/opkg/status'
            self.update = 'opkg update >/dev/null 2>&1'
            self.install = 'opkg install'
            self.list = 'opkg list-installed'
            self.uninstall = 'opkg remove --force-depends'

    def info(self):
        try:
            req = Request(self.page)
            req.add_header(
                'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0')
            response = urlopen(req)
            link = response.read().decode('utf-8')
            data_ = findall('<script type=.*?ipk","path":"RakutenTV/(.+?)"',link)[0]
            return data_
        except HTTPError as e:
            print('HTTP Error code: ', e.code)
        except URLError as e:
            print('URL Error: ', e.reason)

    def banner(self):
        system('clear')
        print(B, r'''
88""Yb    db    88  dP 88   88 888888 888888 88b 88 888888 Yb    dP
88__dP   dPYb   88odP  88   88   88   88__   88Yb88   88    Yb  dP
88"Yb   dP__Yb  88"Yb  Y8   8P   88   88""   88 Y88   88     YbdP
88  Yb dP""""Yb 88  Yb `YbodP'   88   888888 88  Y8   88      YP ''', C)

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

        file = self.info()

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


        if isfile(join('/tmp/', file)):
            remove(join('/tmp/', file))
            sleep(0.8)

        version_stb = self.version(file.split('_')[0])

        if version_stb == file.split('_')[1]:
            system('clear')
            print('you are use the latest version: {}{}{}\n'.format(
                Y, file.split('_')[1], C).capitalize())
            sleep(0.8)
            print("\n   Written by {}MOHAMED_OS{} (͡๏̯͡๏)\n".format(R, C))
            exit()
        elif version_stb > file.split('_')[1]:
            print("\n   Written by {}MOHAMED_OS{} (͡๏̯͡๏)\n".format(R, C))
            exit()
        else:
            system(" ".join([self.uninstall, file.split('_')[0]]))

        system('clear')
        print("{}Please Wait{} while we Download And Install {}RakutenTV{} ...".format(
            G, C, Y, C))

        chdir('/tmp')

        urlretrieve("".join([self.URL, file]), filename=file)
        sleep(0.8)

        system(" ".join([self.install, file]))
        sleep(1)

        if isfile(join('/tmp/', file)):
            remove(join('/tmp/', file))
            sleep(0.8)

        if self.Stb_Image():
            print('{}(?){} Device will restart now'.format(B, C))
            system('killall -9 enigma2')


if __name__ == '__main__':
    build = RakutenTV()
    build.main()
    print("   Written by {}MOHAMED_OS{} (͡๏̯͡๏)".format(R, C))
