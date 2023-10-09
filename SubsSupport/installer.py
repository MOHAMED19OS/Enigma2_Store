# -*- coding: utf-8 -*-
# _^ code BY: MOHAMED_OS _^


from os import chdir, popen, remove, system
from os.path import isfile
from re import MULTILINE, findall
from sys import version_info
from time import sleep

if version_info[0] == 3:
    from urllib.request import urlretrieve
else:
    from urllib import urlretrieve

C = "\033[0m"     # clear (end)
R = "\033[0;31m"  # red (error)
G = "\033[0;32m"  # green (process)
Y = "\033[0;33m"  # yellow (info)


class SubsSupport():
    url = "https://raw.githubusercontent.com/MOHAMED19OS/Enigma2_Store/main/SubsSupport/"

    def __init__(self):
        self.package = "enigma2-plugin-extensions-subssupport"
        self.depends = [
            "python-codecs", "python-compression", "python-difflib",
            "python-requests", "python-xmlrpc", "python-zlib", "unrar"]

        if version_info[0] == 3:
            self.depends = list(
                map(lambda x: x.replace('python-zlib', '').replace('python', 'python3'), self.depends))

    def Stb_Image(self):
        if isfile('/etc/opkg/opkg.conf'):
            self.status = '/var/lib/opkg/status'
            self.update = 'opkg update >/dev/null 2>&1'
            self.install = 'opkg install'
            self.list = 'opkg list'
            self.extension = 'ipk'
        else:
            self.status = '/var/lib/dpkg/status'
            self.update = 'apt-get update >/dev/null 2>&1'
            self.install = 'apt-get install'
            self.list = 'apt-get list'
            self.extension = 'deb'
        return isfile('/etc/opkg/opkg.conf')

    def package_check(self, name):
        with open(self.status) as file:
            for item in file.readlines():
                if item.startswith('Package:'):
                    if findall(name, item[item.index(' '):].strip(), MULTILINE):
                        return True
            file.close()

    def check(self):
        return popen(" ".join([self.list, self.package])).read().split(' - ')[0]

    def main(self):
        self.Stb_Image()

        print("\n{}(!){} Please Wait Check Package ...".format(R, C))
        system(self.update)
        sleep(1)

        for pkg_name in self.depends:
            if not self.package_check(pkg_name):
                system('clear')
                print("     Need To InsTall : {}{}{}\n".format(Y, pkg_name, C))
                system(" ".join([self.install, pkg_name]))
                sleep(1)

        system('clear')
        sleep(1)


        file = "".join([self.package, '_1.5.8_all.', self.extension])

        if self.package_check(self.package):
            print('The plugin is installed: {}{}{}\n'.format(
                Y, self.package, C).capitalize())
        else:
            print("   >>>>   {}Please Wait{} while we Install {}{}{} ...".format(
                G, C, Y, self.package, C))
            if self.check() == self.package:
                system(" ".join([self.install, self.package]))
            else:
                chdir('/tmp')

                if isfile(file):
                    remove(file)
                    sleep(0.8)

                urlretrieve("".join([self.url, file]), filename=file)
                sleep(0.8)

                system(" ".join([self.install, file]))

            if isfile(file):
                remove(file)
                sleep(0.8)

            if self.Stb_Image():
                system('killall -9 enigma2')
            else:
                system('systemctl restart enigma2')


if __name__ == '__main__':
    build = SubsSupport()
    build.main()
    print("\n   Written by {}MOHAMED_OS{} (͡๏̯͡๏)\n".format(R, C))
