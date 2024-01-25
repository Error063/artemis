# Installing ARTEMiS on Windows
This guide assumes a fresh install of Windows 10. Please be aware that due to the lack of memcached and the general woes of running a server on Windows, this is only recommended for local setups or small hosting-for-the-homies type servers.

## Install prerequisites
### Python
- Python versions from 3.8 to 3.11 work with ARTEMiS. We recommend 3.11.
    - https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe
- Install using whichever options best suit your environment, making sure that the Python executable is on path, such that you can open CMD, type `python --version` and see the version of Python you have installed.
- If you already have a working version of Python installed, skip this step.

### MariaDB
- It is always recommended to use MariaDB over MySQL because Oracle is a terrible company.
- While the latest release of v10 is recommended, as it is an LTS release, v11 should work fine.
    - https://ftp.osuosl.org/pub/mariadb//mariadb-10.11.6/winx64-packages/mariadb-10.11.6-winx64.msi
- REMEMBER YOUR ROOT PASSWORD SO YOU CAN LOG IN INF FUTURE STEPS.

### Git
- While technically optional, it is strongly recommended to obtain ARTEMiS via git clone instead of just downloading it.
    - https://git-scm.com/download/win
- It is recommended to use Notepad++ as the default editor (if you have it installed), other than that, the default settings should be fine.

### Optional: GUI database viewer
- Having a GUI database editor is recommended but not required.
- MariaDB will try to install HeidiSQL, but we recommend DBeaver.
    - https://dbeaver.io/download/

## Obtain ARTEMiS
### Via git (recommended)
- `git clone https://gitea.tendokyu.moe/Hay1tsme/artemis.git` via cmd in whatever folder you want to install ARTEMiS.
    - You can switch to the develop branch for latest changes via `git checkout develop`.

### Via http download
- Download [here](https://gitea.tendokyu.moe/Hay1tsme/artemis/archive/master.zip).
    - Develop branch can be found [here](https://gitea.tendokyu.moe/Hay1tsme/artemis/archive/develop.zip).
- Extract the zip file somewhere.

## Database setup
- Log into your server as root, either via GUI (recommended) or CMD
- Create the `aime` user, replace `<password>` with a password you choose. Remember it!
```
CREATE USER 'aime'@'localhost' IDENTIFIED BY '<password>';
CREATE DATABASE aime;
GRANT Alter,Create,Delete,Drop,Index,Insert,References,Select,Update ON aime.* TO 'aime'@'localhost';
```
- If you create the database via a GUI, make sure you grant all the above permissions.

## Create a venv
- Python virtual environments are a good way to manage packages and make dealing with python and pip easier.
- `python -m pip venv venv`
- `venv\Scripts\activate.bat` to activate the venv whenever you need to interact with ARTEMiS.
- All the rest of the steps assume your venv is activated.

## Install pip modules
- `pip install -r requirements.txt`

## Setup configuration
- Create a new `config` folder and copy the files in `example_config` over.
- edit `core.yaml`
    - Put the password you created for the aime user into the `database` section.
    - Put in the aimedb key (YOU DO NOT GENERATE THIS KEY, FIND IT SOMEWHERE).
    - Set your hostname to be whatever hostname or IP address games can reach your server at (many games reject localhost and 127.0.0.1).
    - Optional: generate base64-encoded secrets for aimedb and frontend.
    - See [config.md](docs/config.md) for a full list of options.
- edit `idz.yaml`
    - If you don't plan on anyone using your server to play Initial D Zero, it is best to disable it to cut down on console spam on boot.
- Edit other game yamls
    - Add keys, set hostnames, ports, etc. Specific settings will depend on the game. See [game_specific_info](docs/game_specific_info.md).

## Create Database Tables
- `python dbutils.py create`

## Firewall
- If you're planning on serving games not on your PC, open at least ports 80, 8443, and 22345 in windows firewall
    - Also set `listen_address` to either your local IP to serve on your LAN, or `0.0.0.0` for all interfaces, to accept connections from other places.

## Start ARTEMiS
- `python index.py`
