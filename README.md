# *****           docker-plotly-dash-gas             *******
# deploy plotly dash example dashboard container

# build the container with :

docker build -t gasapp . && docker run --rm -p 8050:8050 gasapp
# Build a MAC-VLAN network so we can assign a ip-adres from local network to container
ip route |grep default

# In my case it returns :
# default via 192.168.1.1 dev eth0  src 192.168.1.201
# subnet 255.255.255.0   => 192.168.1.0/24
# for ip-range choose a not occupied ip-adress with /32 for mac-vlan network with only 1 ip-adres

# We need eth0 in next command :
docker network create --driver=macvlan --gateway=192.168.1.1 --subnet=192.168.1.0/24 --ip-range=192.168.1.254/32 -o parent=eth0 VLAN_web

docker run --detach 
--name gasapp 
-p 8050:8050 
--restart always 
--cap-add NET_ADMIN 
--dns=1.0.0.1 
--dns=1.1.1.1 
--env "DNS1=1.1.1.1" 
--env "DNS2=1.0.0.1" 
--env "serverIP=192.168.1.254" 
--env "DNSMASQ_LISTENING=local" //////local vervangen door 'all' dan is toegang buiten eigen netwerk mogelijk
--network VLAN_web 
--ip "192.168.1.254" 
--mac-address "02:43:d0:a8:01:d7" 
gasapp


