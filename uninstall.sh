#!/bin/bash
if [ "$UID" -ne 0 ]
then
    echo -e 'must be \E[34m\033[1mroot\033[0m to run this script.'
    echo -ne '\E[0m'
    exit 67
fi

if [ ! -f /usr/bin/uninstall ]
then
   echo "building file..."
   scripts="$(cat $0)"
   declare -i index=1
   cat $0 | while read line
   do
       if (( index == 19 ))
       then
          echo 'echo -e "must be \E[34m\033[1mroot\033[0m to run this script."'>>/usr/bin/uninstall
          echo 'echo -ne "\E[0m"'>>/usr/bin/uninstall
       elif (( index == 23 ))
       then
          echo 'stips="searching packages for \"$1\":"'>>/usr/bin/uninstall
      echo 'usage="usage: $0 \"package name\""'>>/usr/bin/uninstall
       elif (( index != 19 && index != 20 && (index<23 || index>52) ))
       then
          echo $line>>/usr/bin/uninstall
       fi
       index+=1;
   done
   chmod +x /usr/bin/uninstall
   echo "try \"uninstall [package name]\" again."
   exit
fi

stips="searching packages for \"$1\":"
usage="usage: $0 \"rpm package name\""

if [ $# -eq 0 ]
then
    echo "$0: no rpm packages given for uninstall."
    echo $usage
elif [ $# -gt 1 ]
then   
    echo $usage
else
    echo $stips
    rpms="$(rpm -qa | grep $1)"
    declare -i count=0
    for rpmk in $rpms
    do
       count+=1
       echo "package: $rpmk"
    done
    if (( count == 0 ))
    then
       echo "no packages"
       exit
    fi
    echo "packages: $count"
    echo
    read -p "are you sure you want to uninstall all above packages?(y/n)"
    if [[ $REPLY == [Yy] ]]
    then
         echo "starting to uninstall packages..."
         for rpmk in $rpms
     do
         count+=1
         echo "uninstalling package: $rpmk"
             rpm -e --nodeps $rpmk
             if [ $? -eq 0 ]
             then
             echo "done"
             else
                 echo "faild to uninstall $rpmk"
             fi
      done
    fi
fi
