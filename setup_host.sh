#!/bin/bash
read -p 'Enter new hostname: ' hostname
ansible-playbook -i ${HOSTSFILE:-teamhosts} --ask-vault-pass -e host="$hostname" setup.yml
