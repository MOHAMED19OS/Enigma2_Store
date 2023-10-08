# -*- coding: utf-8 -*-
# code BY: MOHAMED_OS

from __future__ import print_function

import ssl
from os import chdir, popen, remove, system
from os.path import isdir, isfile, join
from re import MULTILINE, findall
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
            data_deb = findall('<script type=.*?deb["\'],["\']path["\']:["\']FootOnsat/(.+?)["\']',link)[0]
            data_ipk = findall('<script type=.*?ipk["\'],["\']path["\']:["\']FootOnsat/(.+?)["\']',link)[0]
            return data_deb,data_ipk
        except HTTPError as e:
            print('HTTP Error code: ', e.code)
        except URLError as e:
            print('URL Error: ', e.reason)

    def banner(self):
        system('clear')
        print(B, r'''
  _______   ______      ______  ___________  ______    _____  ___    ________     __  ___________
 /"     "| /    " \    /    " \("     _   ")/    " \  (\"   \|"  \  /"       )   /""\("     _   ")
(: ______)// ____  \  // ____  \)__/  \\__/// ____  \ |.\\   \    |(:   \___/   /    \)__/  \\__/
 \/    | /  /    ) :)/  /    ) :)  \\_ /  /  /    ) :)|: \.   \\  | \___  \    /' /\  \  \\_ /
 // ___)(: (____/ //(: (____/ //   |.  | (: (____/ // |.  \    \. |  __/  \\  //  __'  \ |.  |
(:  (    \        /  \        /    \:  |  \        /  |    \    \ | /" \   :)/   /  \\  \\:  |
 \__/     \"_____/    \"_____/      \__|   \"_____/    \___|\____\)(_______/(___/    \___)\__|''', C)

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
            file = self.info()[1]
        else:
            file = self.info()[0]

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
        elif version_stb == '':
            pass
        elif version_stb > file.split('_')[1]:
            print("\n   Written by {}MOHAMED_OS{} (͡๏̯͡๏)\n".format(R, C))
            exit()
        else:
            if isfile(join(self.plugin_path,'db/footonsat.db')):
                print("Keep old db....")
                move('/usr/lib/enigma2/python/Plugins/Extensions/FootOnSat/db/footonsat.db','/tmp')
            system(" ".join([self.uninstall, file.split('_')[0]]))

        system('clear')
        print("{}Please Wait{} while we Download And Install {}FootOnsat{} ...".format(
            G, C, Y, C))

        chdir('/tmp')

        urlretrieve("".join([self.URL, file]), filename=file)
        sleep(0.8)

        system(" ".join([self.install, file]))
        sleep(1)

        if isfile(join('/tmp/', file)):
            remove(join('/tmp/', file))
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
