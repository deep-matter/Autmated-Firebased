#!/bin/bash
# Colors
white="\033[1;37m"
grey="\033[0;37m"
purple="\033[0;35m"
red="\033[1;31m"
green="\033[1;32m"
yellow="\033[1;33m"
Purple="\033[0;35m"
Cyan="\033[0;36m"
Cafe="\033[0;33m"
Fiuscha="\033[0;35m"
blue="\033[1;34m"
nc="\e[0m"

echo -e "$red by deep-matter.$nc"

# Installation
sleep 1
echo -e "Checking Installation $nc"
#bash install.sh
echo -e "Checking Completed [$green✓$nc] $nc "
sleep 1
clear

# Startup
echo -e "$green"
echo "        .▄▄ ·        ▄▄· ▪   ▄▄▄· ▄▄▌      ▄▄▄▄·       ▐▄• ▄ "
echo "        ▐█ ▀. ▪     ▐█ ▌▪██ ▐█ ▀█ ██•      ▐█ ▀█▪▪      █▌█▌▪"
echo "        ▄▀▀▀█▄ ▄█▀▄ ██ ▄▄▐█·▄█▀▀█ ██▪      ▐█▀▀█▄ ▄█▀▄  ·██· "
echo "        ▐█▄▪▐█▐█▌.▐▌▐███▌▐█▌▐█ ▪▐▌▐█▌▐▌    ██▄▪▐█▐█▌.▐▌▪▐█·█▌"
echo -e "         ▀▀▀▀  ▀█▄▀▪·▀▀▀ ▀▀▀ ▀  ▀ .▀▀▀     ·▀▀▀▀  ▀█▄▀▪•▀▀ ▀▀$nc $blue v1.beta$nc"
echo -e "[+]              $red Coded By Deep-matter$nc             		   [+]"
echo -e "[+] 		 $red FireSender $nc 		   [+]"
echo -e "[+] 		 $red Version To All$nc          		   [+]"
echo -e "[+]$red Special Thanks To$nc :$green {Douae , Badr}$nc [+]"
echo ""
echo -e "$yellow Select From Menu : $nc"
echo ""
echo -e "        $Cyan 1 : Sender With Reset Password$nc"
echo -e "        $Cyan 99: Exit$nc"
read -p "Choice >  " ch

if [ $ch = 1 ]; then
    echo -e "            $Cyan Send Firebase With Reset Password$nc"
    echo -e "$green"
    python main.py
    echo -e "$nc"
    sleep 1
    echo -e "        [+]$yellow Send is  Completed $nc[$green✓$nc] $nc[+]"
    echo -e "$red"
    read -p "Wanna Back To Main Menu [ Y / n ] : " check
    echo -e "$nc"
    if [ $check = "Y" ] || [ $check = "y" ] || [ $check = "Yes" ] || [ $check = "yes" ] || [ $check = "YES" ]; then
        bash run.sh
    else
        exit 1
    fi
elif [ $ch == 99 ]; then
    echo -e "$red Program Exit ...$nc"
    sleep 0.25
    exit 1
else
    echo "Not Found 404 , Exit"
    exit 1
fi
