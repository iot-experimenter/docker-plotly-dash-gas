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


In my case :

root@GOJODISK2:/volume1/docker/___FluviusGasDemo-V1# docker network ls
NETWORK ID          NAME                DRIVER              SCOPE
f5177f6053b3        VLAN_web            macvlan             local
6c768ceb0c54        bridge              bridge              local
44fce7e8be12        host                host                local
0cd87240d292        none                null                local


root@GOJODISK2:/volume1/docker/___FluviusGasDemo-V1# docker network inspect VLAN_web
[
    {
        "Name": "VLAN_web",
        "Id": "f5177f6053b3a3306bc6e8291ff5d397d7e82f482e42d50edf14c037d0ea0e30",
        "Created": "2020-06-21T08:58:26.458909036+02:00",
        "Scope": "local",
        "Driver": "macvlan",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "192.168.1.0/24",
                    "IPRange": "192.168.1.254/32",
                    "Gateway": "192.168.1.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "081f614d804a075e43a65d10fe916f2ec1c99332a24b58a45f2411b05ad90753": {
                "Name": "gasapp",
                "EndpointID": "c5c5ebf322a55fb6f85591f180460b0964eae7bbf186243c222974b986423a4a",
                "MacAddress": "02:43:d0:a8:01:d7",
                "IPv4Address": "192.168.1.254/24",
                "IPv6Address": ""
            }
        },
        "Options": {
            "parent": "eth0"
        },
        "Labels": {}
    }
]


