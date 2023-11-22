#!/bin/bash
# ###########################################
# SCRIPT : DOWNLOAD AND INSTALL IPtoSAT
# ###########################################
#
# Command: wget https://raw.githubusercontent.com/MOHAMED19OS/Enigma2_Store/main/IPtoSAT/installer.sh -qO - | /bin/sh
#
# ###########################################

# Colors
Color_Off='\e[0m'
Red='\e[0;31m'
Green='\e[0;32m'
Yellow='\e[0;33m'

###########################################
# Configure where we can find things here #
TMPDIR='/tmp'
MY_URL='https://raw.githubusercontent.com/MOHAMED19OS/Enigma2_Store/main/IPtoSAT'

#########################
Develop='ZAKARIYA KHA'
VERSION='1.8'
PACKAGE='enigma2-plugin-extensions-iptosat'

#########################
if [ -f /etc/opkg/opkg.conf ]; then
    STATUS='/var/lib/opkg/status'
    OSTYPE='Opensource'
    OPKG='opkg update'
    OPKGINSTAL='opkg install'
    OPKGLIST='opkg list-installed'
    OPKGREMOV='opkg remove --force-depends'
elif [ -f /etc/apt/apt.conf ]; then
    STATUS='/var/lib/dpkg/status'
    OSTYPE='DreamOS'
    OPKG='apt-get update'
    OPKGINSTAL='apt-get install'
    OPKGLIST='apt-get list-installed'
    OPKGREMOV='apt-get purge --auto-remove'
    DPKINSTALL='dpkg -i --force-overwrite'
fi

#########################
install() {
    if grep -qs "Package: $1" "${STATUS}"; then
        echo
    else
        $OPKG >/dev/null 2>&1
        echo "   >>>>   Need to install $1   <<<<"
        echo
        if [ "${OSTYPE}" = "Opensource" ]; then
            $OPKGINSTAL "$1"
            sleep 1
            clear
        elif [ "${OSTYPE}" = "DreamOS" ]; then
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

if [ "${OSTYPE}" = "Opensource" ]; then
    for i in exteplayer3 gstplayer; do
        install $i
    done
elif [ "${OSTYPE}" = "DreamOS" ]; then
    install gstreamer1.0-plugins-base-apps
fi

#########################
clear
echo -e "${Yellow}" "Downloading IPToSAT plugin Please Wait ......" "${Color_Off}"
if [ "${OSTYPE}" = "Opensource" ]; then
    wget $MY_URL/${PACKAGE}_"${VERSION}"_all.ipk -qP $TMPDIR
else
    wget $MY_URL/${PACKAGE}_"${VERSION}".deb -qP $TMPDIR
fi
if [ $? -gt 0 ]; then
    echo -e "${Red}" "error downloading file, end" "${Color_Off}"
    exit 1
else
    echo -e "${Green}" "File downloaded" "${Color_Off}"
fi

if [ "${OSTYPE}" = "Opensource" ]; then
    $OPKGINSTAL $TMPDIR/${PACKAGE}_"${VERSION}"_all.ipk
else
    $DPKINSTALL $TMPDIR/${PACKAGE}_"${VERSION}".deb
    $OPKGINSTAL -f -y
fi

if [ $? -gt 0 ]; then
    echo -e "${Red}" "error install plugin IPToSat, end" "${Color_Off}"
else
    echo -e "${Green}" "install plugin IPToSat" "${Color_Off}"
    for dir in python2 python3; do
        rm -rf "${TMPDIR}"/"${dir:?}"
        sleep 1
    done
fi

#########################
rm -rf $TMPDIR/"${PACKAGE:?}"*

sleep 1
clear
echo ""
echo "***********************************************************************"
echo "**                                                                    *"
echo "**                       IPtoSAT    : $VERSION                             *"
echo "**                       Uploaded by: MOHAMED_OS                      *"
echo "**                       Develop by : $Develop                    *"
echo "**  Support    : https://www.tunisia-sat.com/forums/threads/4171372/  *"
echo "**                                                                    *"
echo "***********************************************************************"
echo ""

if [ "${OSTYPE}" = "Opensource" ]; then
    init 4
    init 3
else
    systemctl restart enigma2
fi

exit 0
