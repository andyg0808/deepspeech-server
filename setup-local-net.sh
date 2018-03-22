#!/bin/bash
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
nmcli dev set enp0s25 managed no
ip addr add dev enp0s25 192.168.10.1/24
iptables -t nat -A POSTROUTING -o wlp3s0 -j MASQUERADE
iptables -A FORWARD -s 192.168.10.0/24 -i enp0s25 -o wlp3s0 -m conntrack --ctstate NEW -j ACCEPT
iptables -A FORWARD -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
sudo systemctl restart isc-dhcp-server.service
