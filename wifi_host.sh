#!/bin/bash
read -p 'Enter new hostname: ' hostname
ansible-playbook -i hosts --ask-vault-pass -e host="$hostname" wifi_setup.yml
read -p 'Press enter and unplug pi' junk
ssh pi@"$hostname" sudo reboot now
