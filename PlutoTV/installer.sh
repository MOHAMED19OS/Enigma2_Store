#!/bin/bash

###########################################
# Configure where we can find things here #
TMPDIR='/tmp'
PACKAGE='enigma2-plugin-extensions-plutotv'
MY_URL='https://raw.githubusercontent.com/MOHAMED19OS/Enigma2_Store/main/PlutoTV'

#########################
if [ -f /etc/opkg/opkg.conf ]; then
    STATUS='/var/lib/opkg/status'
    OSTYPE='Opensource'
    OPKG='opkg update'
    OPKGINSTAL='opkg install'
    OPKGLIST='opkg list-installed'
    OPKGREMOV='opkg remove --force-depends'
    VERSION='20231021'
elif [ -f /etc/apt/apt.conf ]; then
    STATUS='/var/lib/dpkg/status'
    OSTYPE='DreamOS'
    OPKG='apt-get update'
    OPKGINSTAL='apt-get install'
    OPKGLIST='apt-get list-installed'
    OPKGREMOV='apt-get purge --auto-remove'
    DPKINSTALL='dpkg -i --force-overwrite'
    VERSION='1.0-r7'
fi

#########################
install() {
    if grep -qs "Package: $1" "$STATUS"; then
        echo
    else
        $OPKG >/dev/null 2>&1
        echo "   >>>>   Need to install $1   <<<<"
        echo
        if [ "$OSTYPE" = "Opensource" ]; then
            $OPKGINSTAL "$1"
            sleep 1
            clear
        elif [ "$OSTYPE" = "DreamOS" ]; then
            $OPKGINSTAL "$1" -y
            sleep 1
            clear
        fi
    fi
}

#########################
rm -rf $TMPDIR/"${PACKAGE:?}"* >/dev/null 2>&1

if [ "$($OPKGLIST $PACKAGE | awk '{ print $3 }')" = "$VERSION" ]; then
    echo " You are use the laste Version: $VERSION"
    exit 1
elif [ -z "$($OPKGLIST $PACKAGE | awk '{ print $3 }')" ]; then
    echo
    clear
else
    $OPKGREMOV $PACKAGE
fi

#########################
if [ "$OSTYPE" = "Opensource" ]; then
    install enigma2-plugin-systemplugins-serviceapp
elif [ "$OSTYPE" = "DreamOS" ]; then
    for i in gstreamer1.0-libav python-pytz; do
        install $i
    done
fi

#########################
echo "Insallling PlutoTV plugin Please Wait ......"
if [ "$OSTYPE" = "Opensource" ]; then
    wget $MY_URL/${PACKAGE}_"${VERSION}"_all.ipk -qP $TMPDIR
    $OPKGINSTAL $TMPDIR/${PACKAGE}_"${VERSION}"_all.ipk
else
    wget $MY_URL/${PACKAGE}_"${VERSION}"_all.deb -qP $TMPDIR
    $DPKINSTALL $TMPDIR/${PACKAGE}_"${VERSION}"_all.deb
    $OPKGINSTAL -f -y
fi

#########################
rm -rf $TMPDIR/"${PACKAGE:?}"*

sleep 1
clear
echo ""
echo "***********************************************************************"
echo "**                                                                    *"
echo "**                       PlutoTV    : $VERSION                        *"
echo "**                       Uploaded by: MOHAMED_OS                      *"
echo "**                       Develop by : Billy2011                       *"
echo "**  Support    : https://www.tunisia-sat.com/forums/threads/4226416/  *"
echo "**                                                                    *"
echo "***********************************************************************"
echo ""

if [ "$OSTYPE" = "Opensource" ]; then
    killall -9 enigma2
else
    systemctl restart enigma2
fi

exit 0
