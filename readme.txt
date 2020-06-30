https://github.com/piwi3910/techtalk/... 



docker build -t gasapp . && docker run --rm -p 8050:8050 gasapp

docker build -t gasapp .

docker run --detach --name gasapp -p 8050:8050 --restart always --cap-add NET_ADMIN --dns=1.0.0.1 --dns=1.1.1.1 --env "DNS1=1.1.1.1" --env "DNS2=1.0.0.1" --env "serverIP=192.168.1.254" --env "DNSMASQ_LISTENING=local" --network VLAN_web --ip "192.168.1.254" --mac-address "02:43:d0:a8:01:d7" gasapp


root@GOJODISK2:/volume1/docker/___FluviusGasDemo-V1# docker info
Containers: 5
 Running: 1
 Paused: 0
 Stopped: 4
Images: 17
Server Version: 18.09.8
Storage Driver: btrfs
Logging Driver: db
Cgroup Driver: cgroupfs
Plugins:
 Volume: local
 Network: bridge host macvlan null overlay
 Log: awslogs db fluentd gcplogs gelf journald json-file local logentries splunk syslog
Swarm: inactive
Runtimes: runc
Default Runtime: runc
Init Binary: docker-init
containerd version: 0cf16177dbb234350dc27dd2bbd1d7cebd098108
runc version: 6cc9d3f2cd512eeb3d548e2f6b75bcdebc779d4d
init version: e01de58 (expected: fec3683)
Security Options:
 apparmor
Kernel Version: 4.4.59+
OSType: linux
Architecture: x86_64
CPUs: 4
Total Memory: 31.32GiB
Name: GOJODISK2
ID: 7AL3:4APP:5WTF:NP47:NQG4:7OKF:VN25:SJEE:KGD5:CVYA:RL4H:MEV7
Docker Root Dir: /volume1/@docker
Debug Mode (client): false
Debug Mode (server): false
Registry: https://index.docker.io/v1/
Labels:
Experimental: false
Insecure Registries:
 127.0.0.0/8
Live Restore Enabled: false

WARNING: No kernel memory limit support
WARNING: No cpu cfs quota support
WARNING: No cpu cfs period support




root@GOJODISK2:/volume1/docker/___FluviusGasDemo-V1# ip route |grep default
default via 192.168.1.1 dev eth0  src 192.168.1.201

eth0 hebben we als parent in volgende commando nodig om een mac-VLAN te bouwen die toelaat om een nieuw ip-adres aan docker container toe te kennen in je eigen netwerk; geen port re-mappings nodig etc...
Creeer macvlan netwerk
gateway van netwerk
subnet 255.255.255.0 dus 192.168.1.0/24
iprange kies een vrij ip-adres met /32 erachter wil zeggen dat we een macvlan netwerk met enkel 1 ip-adres

root@GOJODISK2:/volume1/docker/___FluviusGasDemo-V1# docker network create --driver=macvlan --gateway=192.168.1.1 --subnet=192.168.1.0/24 --ip-range=192.168.1.254/32 -o parent=eth0 VLAN_web
f5177f6053b3a3306bc6e8291ff5d397d7e82f482e42d50edf14c037d0ea0e30

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

