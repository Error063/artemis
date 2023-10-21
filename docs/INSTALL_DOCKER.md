# ARTEMiS - Docker Installation Guide
This step-by-step guide will allow you to install a Contenerized Version of ARTEMiS inside Docker, some steps can be skipped assuming you already have pre-requisite components and modules installed.

This guide assumes using Debian 12(bookworm-stable) as a Host Operating System for most of packages and modules.

## Pre-Requisites:
- Linux-Based Operating System (e.g. Debian, Ubuntu)
- Docker (https://get.docker.com)
- Python 3.9+
- (optional) Git

## Install Python3.9+ and Docker
```
(if this is a fresh install of the system)
sudo apt update && sudo apt upgrade

(installs python3 and pip)
sudo apt install python3 python3-pip

(installs docker)
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

(optionally install git)
sudo apt install git
```

## Get ARTEMiS
If you installed git, clone into your choice of ARTEMiS git repository, e.g.:
```
git clone <ARTEMiS Repo> <folder>
```
If not, download the source package, and unpack it to the folder of your choice.

## Prepare development/home configuration
To build our Docker setup, first we need to create some folders and copy some files around
- Create 'aime', 'configs', 'AimeDB', and 'logs' folder in ARTEMiS root folder (where all source files exist)
- Inside configs folder, create 'config' folder, and copy all .yaml files from example_config to config (thats all files without nginx_example.conf)
- Edit .yaml files inside configs/config to suit your server needs
- Edit core.yaml inside configs/config:
```
set server.listen_address: to "0.0.0.0"
set title.hostname: to machine's IP address, e.g. "192.168.x.x", depending on your network, or actual hostname if your configuration is already set for dns resolve
set database.host: to "ma.db"
set database.memcached_host: to "ma.memcached"
set aimedb.key: to "<actual AIMEDB key>"
```

## Running Docker Compose
After configuring, go to ARTEMiS root folder, and execute:
```
docker compose up -d
("-d" argument means detached or daemon, meaning you will regain control of your terminal and Containers will run in background)
```
This will start pulling and building required images from network, after it's done, a development server should be running, with server accessible under machine's IP, frontend with port 8090, and PHPMyAdmin under port 9090.

To turn off the server, from ARTEMiS root folder, execute:
```
docker compose down
```

If you changed some files around, and don't see your changes applied, execute:
```
(turn off the server)
docker compose down
(rebuild)
docker compose build
(turn on)
docker compose up -d
```

If you need to see logs from containers running, execute:
```
docker compose logs
```
add '-f' to the end if you want to follow logs.

## Running commands
If you need to execute python scripts supplied with the application, use `docker compose exec app python3 <script> <command>`, for example `docker compose exec app python3 dbutils.py version`

## Persistent DB
By default, in development mode, ARTEMiS database is stored temporarily, if you wish to keep your database saved between restarts, we need to bind the database inside the container to actual storage/folder inside our server, to do this we need to make a few changes:
First off, edit docker-compose.yml, and uncomment 2 lines:
```
(uncomment these two)
#volumes:
#  - ./AimeDB:/var/lib/mysql
```
After that, start up the server, this time Database will be saved in AimeDB folder we created in our configuration steps.
If you wish to save it in another folder and/or storage device, change the "./AimeDB" target folder to folder/device of your choice

NOTE (NEEDS FIX): at the moment running development mode with persistent DB will always run database creation script at the start of application, while it doesn't break database outright, it might create some issues, a temporary fix can be applied:

- Start up containers with persistent DB already enabled, let application create database
- After startup, `docker compose down` the instance
- Edit entrypoint.sh and remove the `python3 dbutils.py create` line from Development mode statement
- Execute `docker compose build` and `docker compose up -d` to rebuild the app and start the containers back

## Adding importer data

To add data using importer, we can do that a few ways:

### Use importer locally on server
For that we need actual GameData and Options supplied somehow to the server system, be it wsl2 mounting layer, a pendrive with data, network share, or a direct copy to the server storage
With python3 installed on system, install requirements.txt directly to the system, or through python3 virtual-environment (python3-venv)
Default mysql/mariadb client development packages will also be required

In the system:
```
sudo apt install default-libmysqlclient-dev build-essential pkg-config libmemcached-dev
sudo apt install mysql-client
OR
sudo apt install libmariadb-dev
```

In the root ARTEMiS folder
```
python3 -m pip install -r requirements.txt
```

If we wish to layer that with python3 virtual-environment, install required system packages, then:
```
sudo apt install python3-venv
python3 -m venv /path/to/venv
cd /path/to/venv/bin
python3 -m pip install -r /path/to/artemis/requirements.txt
```

depending on how you installed, now you can run read.py using:
For direct installation, from root ARTEMiS folder:
```
python3 read.py <args>
```
Or from python3 virtual environment, from root ARTEMiS folder:
```
/path/to/python3-venv/bin/python3 /path/to/artemis/read.py <args>
```

We need to expose database container port, so that read.py can communicate with the database, inside docker-compose.yml, uncomment 2 lines in the database container declaration (db):
```
#ports:
#  - "3306:3306"
```
Now, `docker compose down && docker compose build && docker compose up -d` to restart containers

Now to insert the data, by default, docker doesn't expose container hostnames to root system, when trying to run read.py against a container, it will Error that hostname is not available, to fix that, we can add database hostname by hand to /etc/hosts:
```
sudo <editor of your choice> /etc/hosts
add '127.0.0.1  ma.db' to the table
save and close
```

You can remove the line in /etc/hosts and de-expose the database port after successful import (this assumes you're using Persistent DB, as restarting the container without it will clear imported data).

### Use importer on remote Linux system
Follow the system and python portion of the guide, installing required packages and python3 modules, Download the ARTEMiS source.
Edit core.yaml and insert it into config catalog:
```
database:
  host: "<hostname of target system>"
```
Expose port 3306 from database docker container to system, and allow port 3306 through system firewall to expose port to the system from which you will be importing data. (Remember to close down the database ports after finishing!)

Import data using read.py

### Use importer on remote Windows system
Follow the [windows](docs/INSTALL_WINDOWS.md) guide for installing python dependencies, download the ARTEMiS source.
Edit core.yaml and insert it into config catalog:
```
database:
  host: "<hostname of target system>"
```
Expose port 3306 from database docker container to system, and allow port 3306 through system firewall to expose port to the system from which you will be importing data.
For Windows, also allow port 3306 outside the system so that read.py can communicate with remote database. (Remember to close down the database ports after finishing!)

# Troubleshooting

## Game does not connect to ARTEMiS Allnet Server
Double check your core.yaml if all addresses are correct and ports are correctly set and/or opened.

## Game does not connect to Title Server
Title server hostname requires your actual system hostname, from which you set up the Containers, or it's IP address, you can get the IP by using command `ip a` which will list all interfaces, and one of them should be your system IP (typically under eth0).

## Unhandled command in AimeDB
Make sure you have a proper AimeDB Key added to configuration.

## Memcached Error in ARTEMiS application causes errors in loading data
Currently when running ARTEMiS from master branch, there is a small bug that causes app to always configure memcached service to 127.0.0.1, to fix that, locate cache.py file in core/data, and edit:
```
memcache = pylibmc.Client([hostname]), binary=True)
```
to:
```
memcache = pylibmc.Client(["ma.memcached"], binary=True)
```
And build the containers again.
This will fix errors loading data from server.
(This is fixed in development branch)

## read.py "Can't connect to local server through socket '/run/mysqld/mysqld.sock'"
sqlalchemy by default reads any ip based connection as socket, thus trying to connect locally, please use a hostname (such as ma.db as in guide, and do not localhost) to force it to use a network interface.

### TODO:
- Production environment
