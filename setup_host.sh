#!/bin/bash
IP=192.168.1.222
read -p 'Enter new hostname: ' newname
ssh-copy-id pi@$IP
ansible-playbook -i hosts setup.yml
echo yorowCes0 | ssh pi@$IP passwd
ssh pi@$IP passwd -l pi
ssh pi@$IP sudo reboot now
