# ARTEMiS - Ubuntu 20.04 LTS Guide
This step-by-step guide assumes that you are using a fresh install of Ubuntu 20.04 LTS, some of the steps can be skipped if you already have an installation with MySQL 5.7 or even some of the modules already present on your environment

# Setup
## Install memcached module
1. sudo apt-get install memcached
2. Under the file /etc/memcached.conf, please make sure the following parameters are set:

```
# Start with a cap of 64 megs of memory. It's reasonable, and the daemon default
# Note that the daemon will grow to this size, but does not start out holding this much
# memory

-I 128m
-m 1024
```

** This is mandatory to avoid memcached overload caused by Crossbeats or by massive profiles

3. Restart memcached using:  sudo systemctl restart memcached

## Install MySQL 5.7
```
sudo apt update
sudo apt install wget -y
wget https://dev.mysql.com/get/mysql-apt-config_0.8.12-1_all.deb
sudo dpkg -i mysql-apt-config_0.8.12-1_all.deb
```
    1. During the first prompt, select Ubuntu Bionic
    2. Select the default option
    3. Select MySQL 5.7
    4. Select the last option
```
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 467B942D3A79BD29
sudo apt-get update
sudo apt-cache policy mysql-server
sudo apt install -f mysql-client=5.7* mysql-community-server=5.7* mysql-server=5.7*
```

## Default Configuration for MySQL Server
1. sudo mysql_secure_installation
> Make sure to follow the steps that will be prompted such as changing the mysql root password and such

2. Test your MySQL Server login by doing the following command :
> mysql -u root -p

## Create the default ARTEMiS database and user
1. mysql -u root -p
2. Please change the password indicated in the next line for a custom secure one and continue with the next commands

```
CREATE USER 'aime'@'localhost' IDENTIFIED BY 'MyStrongPass.';
CREATE DATABASE aime;
GRANT Alter,Create,Delete,Drop,Insert,References,Select,Update ON aime.* TO 'aime'@'localhost';
FLUSH PRIVILEGES;
exit;
```

3. sudo systemctl restart mysql

## Install Python modules
```
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential mysql-client libmysqlclient-dev libmemcached-dev
sudo apt install libpython3.8-dev
sudo apt-get install python3-software-properties
sudo apt install python3-pip
sudo pip3 install --upgrade pip testresources
sudo pip3 install --upgrade pip setuptools
sudo apt-get install python3-tk
```
7. Change your work path to the ARTEMiS root folder using 'cd' and install the requirements:
> sudo python3 -m pip install -r requirements.txt

## Copy/Rename the folder example_config to config

## Adjust /config/core.yaml
1. Make sure to change the server listen_address to be set to your local machine IP (ex.: 192.168.1.xxx) 
2. Adjust the proper MySQL information you created earlier
3. Add the AimeDB key at the bottom of the file

## Create the database tables for ARTEMiS
1. sudo python3 dbutils.py create

2. If you get "No module named Crypto", run the following command:
```
sudo pip uninstall crypto
sudo pip uninstall pycrypto
sudo pip install pycrypto
```

## Firewall Adjustements 
```
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 8443
sudo ufw allow 22345
sudo ufw allow 8090
sudo ufw allow 8444
sudo ufw allow 9000
```

## Running the ARTEMiS instance
1. sudo python3 index.py

# Troubleshooting

## Game does not connect to ARTEMiS Allnet server
1. Double-check your core.yaml, the listen_address is most likely either not binded to the proper IP or the port is not opened

## Game does not connect to Title Server
1. Verify that your core.yaml is setup properly for both the server listen_address and title hostname
2. Boot your game and verify that an AllNet response does show and if it does, attempt to open the URI that is shown under a browser such as Edge, Chrome & Firefox.
3. If a page is shown, the server is working properly and if it doesn't, double check your port forwarding and also that you have entered the proper local IP under the Title hostname in core.yaml.

## Unhandled command under AimeDB
1. Double check your AimeDB key under core.yaml, it is incorrect.

## Memcache failed, error 3
1. Make sure memcached is properly installed and running. You can check the status of the service using the following command:
> sudo systemctl status memcached
2. If it is failing, double check the /etc/memcached.conf file, it may have duplicated arguments like the -I and -m
3. If it is still not working afterward, you can proceed with a workaround by manually editing the /core/data/cache.py file.
```
# Make memcache optional
try:
    has_mc = False
except ModuleNotFoundError:
    has_mc = False
```
