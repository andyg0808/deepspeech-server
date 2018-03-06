#!/bin/bash
sudo umount /dev/sdf* || true
set -ex
while [ ! -b /dev/sdf ]
do
    sleep 1
    echo Waiting for card...
done
sudo dd status=progress bs=2M if=$HOME/OSs/RaPi/2017-11-29-raspbian-stretch-lite.img of=/dev/sdf oflag=dsync
sudo umount /dev/sdf* || true
echo 'Unplug and replug drive'
while [ ! -b /dev/sdf1 -o ! -e /media/andrew/boot ]
do
    sleep 1
    echo Waiting...
done
udisksctl mount -b /dev/sdf1 || test -d /media/andrew/boot
touch /media/andrew/boot/ssh
umount /dev/sdf* || true
