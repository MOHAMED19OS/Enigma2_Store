# -*- coding: utf-8 -*-
# code BY: MOHAMED_OS

from __future__ import print_function

import ssl
from os import chmod, popen, remove, system
from os.path import exists, isfile, join
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

ssl._create_default_https_context = ssl._create_unverified_context


if hasattr(__builtins__, 'raw_input'):
    input = raw_input


class Emulator():
    URL = 'https://raw.githubusercontent.com/MOHAMED19OS/Enigma2_Store/main/Cam_Emulator/'
    page = "https://github.com/MOHAMED19OS/Enigma2_Store/tree/main/Cam_Emulator"

    def __init__(self):
        self.package = "enigma2-plugin-softcams-"

    def Stb_Image(self):
        if isfile("/etc/opkg/opkg.conf"):
            self.status = "/var/lib/opkg/status"
            self.update = "opkg update >/dev/null 2>&1"
            self.install = "opkg install"
            self.list = "opkg list"
            self.uninstall = "opkg remove --force-depends"
            self.extension = "ipk"
            return "OpenSource"
        else:
            self.status = "/var/lib/dpkg/status"
            self.update = "apt-get update >/dev/null 2>&1"
            self.install = "apt-get install --fix-broken --yes --assume-yes"
            self.list = "apt-get list"
            self.uninstall = "apt-get purge --auto-remove"
            self.extension = "deb"
            return "DreamOS"

    def info(self, name):
        try:
            req = Request(self.page)
            req.add_header(
                'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0')
            response = urlopen(req)
            link = response.read().decode('utf-8')
            return findall(r"".join(['Cam_Emulator/.+?-', name, '_(.*?)_']), link)[0]
        except HTTPError as e:
            print('HTTP Error code: ', e.code)
        except URLError as e:
            print('URL Error: ', e.reason)

    def banner(self):
        system('clear')
        print(B,r"""
            d88888b .88b  d88. db    db db       .d8b.  d888888b  .d88b.  d8888b.
            88'     88'YbdP`88 88    88 88      d8' `8b `~~88~~' .8P  Y8. 88  `8D
            88ooooo 88  88  88 88    88 88      88ooo88    88    88    88 88oobY'
            88~~~~~ 88  88  88 88    88 88      88~~~88    88    88    88 88`8b
            88.     88  88  88 88b  d88 88booo. 88   88    88    `8b  d8' 88 `88.
            Y88888P YP  YP  YP ~Y8888P' Y88888P YP   YP    YP     `Y88P'  88   YD""", C)
        print("".join(["\t\t\t{}Oscam Version{}: ".format(Y, C), self.info('oscam')]))
        print("".join(["\t\t\t{}Ncam Version{}: ".format(Y, C), self.info('ncam')]))

    def check(self, pkg):
        with open(self.status) as file:
            for item in file.readlines():
                if item.startswith('Package:'):
                    if findall(pkg, item[item.index(' '):].strip(), MULTILINE):
                        return True
            file.close()

    def prompt(self, choices):

        options = list(choices)
        options.sort(key=int)

        while True:
            print("{}(?){} Choose an option [{}-{}] : ".format(B, C, options[0], options[-1]), end='')
            choice = [str(x) for x in input().split()]

            for name in choice:
                if name not in options:
                    print("\n{}(!){} Select one of the available options !!\n".format(R, C))
                    continue
            return choice

    def FixEmu(self):
        for name in ["RELOAD.sh", "SUPAUTO.sh"]:
            if exists(join("/etc/", name)):
                remove(join("/etc/", name))
            if exists('/etc/cron/crontabs/root'):
                self.RootPath = '/etc/cron/crontabs/root'
            else:
                self.RootPath = '/var/spool/cron/crontabs/root'
            with open(self.RootPath, "r+") as f:
                line = f.readline()
                f.seek(0)
                if name not in line:
                    f.write(line)
                f.truncate()
        with open('/etc/init.d/fixemu.sh', "w") as file:
            file.writelines("""#!/bin/bash\n
STB_IMAGE=$(cut /etc/opkg/all-feed.conf -d'-' -f1 | awk '{{ print $2 }}')

if [ $STB_IMAGE = 'egami' ] || [ $STB_IMAGE = 'openbh' ]; then
    update-rc.d -f softcam remove
    sleep 1
    unlink /etc/init.d/softcam

    sleep 1

    ln -sf /etc/init.d/softcam.None /etc/init.d/softcam
    update-rc.d softcam defaults

    if [ -e /etc/init.d/softcam.SupCam ]; then
        rm -rf /etc/init.d/softcam.SupCam
    fi

fi

if [ -e /etc/RELOAD.sh ]; then
    rm -rf /etc/RELOAD.sh
fi

if [ -e /etc/SUPAUTO.sh ]; then
    rm -rf /etc/SUPAUTO.sh
fi
sed -i '/RELOAD/d' {}
sed -i '/SUPAUTO/d' {}\n""".format(self.RootPath, self.RootPath))
            file.close()

        chmod('/etc/init.d/fixemu.sh', 0o755)
        system("update-rc.d fixemu.sh defaults >/dev/null 2>&1")

    def main(self):

        self.Stb_Image()

        if not self.check('libcurl4'):
            system('clear')
            print("   >>>>   {}Please Wait{} while we Install {}libcurl4{} ...".format(G, C, Y, C))
            system('{};{} libcurl4'.format(self.update, self.install))

        if self.Stb_Image() == "OpenSource":
            cam = {
                "1": "".join([self.package, "oscam"]),
                "2": "".join([self.package, "ncam"]),
                "3": "".join([self.package, "powercam"]),
                "4": "".join([self.package, "gosatplus"]),
                "5": "".join([self.package, "ultracam"]),
                "6": "".join([self.package, "gosatplus-oscam"]),
                "7": "".join([self.package, "powercam-oscam"]),
                "8": "".join([self.package, "ultracam-oscam"]),
                "9": "".join([self.package, "supcam-oscam"]),
                "10": "".join([self.package, "gosatplus-ncam"]),
                "11": "".join([self.package, "powercam-ncam"]),
                "12": "".join([self.package, "ultracam-ncam"]),
                "13": "".join([self.package, "supcam-ncam"])
            }
            menu = """
                        (00) Exit

            (1) Oscam               (8)  UltraCam_Oscam
            (2) Ncam                (9)  SupTV_Oscam
            (3) PowerCam            (10) GosatPlus_Ncam
            (4) GosatPlus           (11) PowerCam_Ncam
            (5) UltraCam            (12) UltraCam_Oscam
            (6) GosatPlus_Oscam     (13) SupTV_Ncam
            (7) PowerCam_Oscam
            """
        else:
            cam = {
                "1": "".join([self.package, "oscam"]),
                "2": "".join([self.package, "ncam"]),
                "3": "".join([self.package, "powercam"]),
                "4": "".join([self.package, "gosatplus"])
            }
            menu = """
                            (00) Exit

            (1) Oscam       (3) PowerCam
            (2) Ncam        (4) GosatPlus
            """
        self.banner()

        print(menu)
        choice = self.prompt(cam.keys())

        for number in choice:
            if number == '00':
                system('clear')
                self.banner()
                print("\nGoodBye ...!\n", "   Written by {}MOHAMED_OS{}(͡๏̯͡๏) \n".format(
                    B, C, R, C))
                exit()
            else:
                value = cam.get(number)
                self.file = "{}_{}_all.{}".format(value, self.info(value.split('-')[-1]), self.extension)

                if self.check(value):
                    system('{} {} '.format(self.uninstall, value))

                if isfile(self.file):
                    remove(self.file)
                    sleep(0.8)

                if "powercam" in value or "ultracam" in value:
                    CheckLib = popen(" ".join([self.list, 'libcrypto-compat-1.0.0'])).read().split(' - ')[0]
                    if CheckLib == 'libcrypto-compat-1.0.0':
                        if not self.check('libcrypto-compat-1.0.0'):
                            system('clear')
                            print("   >>>>   {}Please Wait{} while we Install {}libcrypto-compat-1.0.0{} ...".format(G, C, Y, C))
                            system('{};{} libcrypto-compat-1.0.0'.format(self.update, self.install))
                    else:
                        if not self.check('libcrypto-compat'):
                            print("   >>>>   {}Please Wait{} while we Install {}libcrypto-compat{} ...".format(G, C, Y, C))
                            system(" ".join([self.install, "libcrypto-compat"]))

                try:
                    system('clear')
                    print(">>> {}Downloading{} >>> {}{}{} ...".format(G, C, Y, value, C))

                    FullFileName = join('/tmp/', self.file)
                    urlretrieve("".join([self.URL, self.file]), FullFileName)
                    sleep(1)
                except HTTPError as e:
                    print('·{}HTTP Error{} code: '.format(R,C), e.code)
                    exit()

                if exists(join("/tmp/", self.file)):
                    system('clear')
                    print(">>> {}Installing{} >>> {}{}{} ...".format(G, C, Y, value, C))
                    system(" ".join([self.install, '/tmp/' + self.file]))
                    sleep(1)

                    if "supcam" in value:
                        self.FixEmu()

                    if self.Stb_Image() == "OpenSource":
                        CheckImage = popen("cut /etc/opkg/all-feed.conf -d'-' -f1 | awk '{ print $2 }'").read().replace("\n","")
                        if CheckImage == "openpli":
                            if not self.check('softcam-support'):
                                system('clear')
                                system(" ".join([self.install, "softcam-support"]))
                                sleep(1)
                else:
                    print("Sorry {} Not Download ..!\n   Written by {}MOHAMED_OS{} (͡๏̯͡๏)".format(Y, value, C,R, C))
                    exit()



if __name__ == '__main__':
    build = Emulator()
    build.main()
    print("   Written by {}MOHAMED_OS{} (͡๏̯͡๏)".format(R, C))
