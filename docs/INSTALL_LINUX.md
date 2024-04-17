# Installing ARTEMiS on Linux
This guide assumes a fresh install of Debian 12 or Rasperry Pi OS. If you're using a different distrubution, your package manager commands and package names may be different then what's listed below. Please check with your repository's package manager for package names.

## Install prerequisits
### Python
Some installs may come with python already installed. You can verify this by trying the following commands:
- `python --version`
- `python3 --version`
- `python3.<minor version> --version` where `<minor version>` is a python 3 release (eg 11, 10)

If your python version is at least 3.7, you can move to the next step

### Libraries and other software
ARTEMiS depends on mysql and memcached. As stated above, package names may vary by distrubution, but this is generally what you should expect to install.
#### Rasperry Pi OS
`sudo apt install git mariadb-server python3-pip memcached libmemcached-dev `

#### Debian 12
`sudo apt install git mariadb-server python3-pip memcached libmemcached-dev default-libmysqlclient-dev pkg-config`

### Optional: Install proxy
If you intend to use a proxy (recomended for public-facing production setups), we recomend nginx
`sudo apt install nginx`

## Database setup
### mysql_secure_installation
If you already have your database installed and configured, and are able to log in, skip down to the [Creating the database](#creating-the-database) section below. Otherwise, setup your newly installed database.

`sudo mysql_secure_installation`

Leave the root password blank, do not switch to unix socket, do reset the root password to something secure, and answer yes to the rest of the prompts. You can then log into your database with `sudo mysql`

### Creating the database
Once you're logged in, run the following commands, as root, to set up our database. Make sure you note down whatever you decide to make the password for the aime account, as you will need it to configure artemis.

```sql
CREATE USER 'aime'@'localhost' IDENTIFIED BY '<password>';
CREATE DATABASE aime;
GRANT Alter,Create,Delete,Drop,Index,Insert,References,Select,Update ON aime.* TO 'aime'@'localhost';
quit
```
We have now set up our new user, `aime`, created a database called `aime` and given our user all the permissions it needs on every table of that database.

### Configure memcached
Under the file /etc/memcached.conf, please make sure the following parameters are set:

```
# Start with a cap of 64 megs of memory. It's reasonable, and the daemon default
# Note that the daemon will grow to this size, but does not start out holding this much
# memory

-I 128m
-m 1024
```

** This is mandatory to avoid memcached overload caused by Crossbeats or by massive profiles

Restart memcached using:  sudo systemctl restart memcached

## Getting ARTEMiS
### Clone from gitea
use `git clone https://gitea.tendokyu.moe/Hay1tsme/artemis.git` to pull down ARTEMiS into a folder called `artemis` created at wherever your current working directory is. `cd` into `artemis`.

### Optional: Create a venv
Python venvs are a way to install and manage packages on a per-project basis and are recomended on systems that will have multiple python scripts running on them to avoid dependancy issues. If this server will be running ARTEMiS and ONLY ARTEMiS, then it is possible to get away without creating one. If you do want to create one, you will have to install an additional package:

`sudo apt install python3-venv` (like above, package name may vary depending on distro and python version)

Now, simply run `python -m venv .venv` (may have to use python3 or python 3.11 instead of python) to create your virtual environment in the folder `.venv`. In order to install packages and run scripts in this environment, you have to 'activate' it by running `source .venv/bin/activate`. Your terminal should now have (venv) appended to it.

### Optional: Use the develop branch
By default, pulling down ARTEMiS from gitea will pull the `master` branch. This branch is updated less frequently, but is considered stable and ready for production use. If you'd rather have more updates, but a possibility for instability or bugs, you can switch to the develop branch by running `git checkout develop`. You can run `git checkout master` to switch back to stable.

## Install python libraries
Run `pip install -r requirements.txt` to install all of ARTEMiS' dependencies. If any installs fail, you may have missed a step in the [Install prerequisits](#install-prerequisits) section above. If you're absolutly sure you didn't, submit an issue on gitea.

## Configuration
### Copy example configs
From the `artemis` directory, run `cp -r example_config config` to copy the example configuration files to a new folder called `config`. All of the config changes you make will be done in the `config` folder.

### Optional: Generate AimeDB and Frontend JWT Secrets
AimeDB and the frontend utalize JSON Web Tokens (JWT) for card authentication and session cookies respectivly. While generating a secret for AimeDB is optional, if you intend to run the frontend, a secret is required. You can generate a secret easily by running:

`openssl rand --base64 64`

With 64 being the number of bytes. You shouldn't need to go higher then 64, but you can if desired. **NOTE: When pasting secrets into the config file, make sure you remove any newlines!**

### Edit `core.yaml`
Before editing `core.yaml`, you should familiarize yourself with the name and function of each of the config options. You can find a full list in [config.md](config.md)

Open `core.yaml` in the `config` folder in your prefered text editor. The only configuration option that it is absolutly mandatory to change is `aimedb`->`key`. This key must be set for the server to start, and the key must be correct, otherwise you will not be able to process aimedb requests. The correct key is floating around online, and finding it is left as an excersie to the reader. 

Another option that should be changed is `database`->`password` to be the password you set when you created your database user. You did write it down somewhere, right?

Since you are presumably not running the games on the same computer you're installing this server on, you're going to want to change `server`->`hostname` to be whatever hostname or IP address other PCs can reach this server by. Note that some games reject IPs and require hostnames, so setting a hostname is always recomended over an IP.

### Edit game configs
Every game has their own yaml file with settings that you may want to tweek. `InitialD Zero` and `Pokken` both have `hostname` fields in their config file that you should edit, and some games support encryption, if supplied with proper keys.

### A note about IDZ
InitialD Zero is currently the only game where it is required to specify encryption information (the AES key and at least one RSA key) for the game to start. These keys are, like the aimedb key, floating around online and will not be provided. If you don't have the keys, and don't plan on anybody connecting to your server playing InitialD Zero, it's best to set `enabled` to `False` in idz.yaml to disable the game.

## Create database tables
ARTEMiS uses alembic to manage datbase versioning. `dbutils.py` acts as a wrapper for alembic, and can execute some necessassary database functions. To create the database tables, run `python dbutils.py create`. Confirm that there are no errors, and you're good to go. If you intend to use the frontend, you may also want to run `python dbutils.py create-owner -a <your 20 digit access code here>` to create a superuser account to log in with.

## Run ARTEMiS
Once you have everything configured properly, simply run `python index.py` to start ARTEMiS. Verify that clients can connect to all services (allnet, billing, aimedb, and game servers) and setup is complete.