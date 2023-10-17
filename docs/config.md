# ARTEMiS Configuration
## Server
- `listen_address`: IP Address or hostname that the server will listen for connections on. Set to 127.0.0.1 for local only, or 0.0.0.0 for all interfaces. Default `127.0.0.1`
- `allow_user_registration`: Allows users to register in-game via the AimeDB `register` function. Disable to be able to control who can use cards on your server. Default `True`
- `allow_unregistered_serials`: Allows games that do not have registered keychips to connect and authenticate. Disable to restrict who can connect to your server. Recomended to disable for production setups. Default `True`
- `name`: Name for the server, used by some games in their default MOTDs. Default `ARTEMiS`
- `is_develop`: Flags that the server is a development instance without a proxy standing in front of it. Setting to `False` tells the server not to listen for SSL, because the proxy should be handling all SSL-related things, among other things. Default `True`
- `threading`: Flags that `reactor.run` should be called via the `Thread` standard library. May provide a speed boost, but removes the ability to kill the server via `Ctrl + C`. Default: `False`
- `check_arcade_ip`: Checks IPs against the `arcade` table in the database, if one is defined. Default `False`
- `strict_ip_checking`: Rejects clients if there is no IP in the `arcade` table for the respective arcade
- `log_dir`: Directory to store logs. Server MUST have read and write permissions to this directory or you will have issues. Default `logs`
## Title
- `loglevel`: Logging level for the title server. Default `info`
- `hostname`: Hostname that gets sent to clients to tell them where to connect. Games must be able to connect to your server via the hostname or IP you spcify here. Note that most games will reject `localhost` or `127.0.0.1`. Default `localhost`
- `port`: Port that the title server will listen for connections on. Set to 0 to use the Allnet handler to reduce the port footprint. Default `8080`
- `reboot_start_time`: 24 hour JST time that clients will see as the start of maintenance period. Leave blank for no maintenance time. Default: ""
- `reboot_end_time`: 24 hour JST time that clients will see as the end of maintenance period. Leave blank for no maintenance time. Default: ""
## Database
- `host`: Host of the database. Default `localhost`
- `username`: Username of the account the server should connect to the database with. Default `aime`
- `password`: Password of the account the server should connect to the database with. Default `aime`
- `name`: Name of the database the server should expect. Default `aime`
- `port`: Port the database server is listening on. Default `3306`
- `protocol`: Protocol used in the connection string, e.i `mysql` would result in `mysql://...`. Default `mysql`
- `sha2_password`: Weather or not the password in the connection string should be hashed via SHA2. Default `False`
- `loglevel`: Logging level for the database. Default `warn`
- `user_table_autoincrement_start`: What the `aime_user` table ID autoincrememnt should start with. Default `10000`
- `memcached_host`: Host of the memcached server. Default `localhost`
## Frontend
- `enable`: Weather or not the frontend should be enabled. Default `False`
- `port`: Port the frontend should listen for connections on. Default `8090`
- `loglevel`: Logging level for the frontend server. Default `info`
## Allnet
- `loglevel`: Logging level for the allnet server. Default `info`
- `port`: Port the allnet server should listen for connections on. Games are hardcoded to ask for port `80` so only change if you have a proxy redirecting properly. Default `80`
- `allow_online_updates`: Allow allnet to distribute online updates via DownloadOrders. This system is currently non-functional, so leave it disabled. Default `False`
## Billing
- `port`: Port the billing server should listen for connections on. Games are hardcoded to ask for port `8443` so only change if you have a proxy redirecting properly. Set to 0 to use the allnet handler to reduce the number of ports the server eats up. Default `8443`
- `ssl_key`: Location of the ssl server key for the billing server. Ignored if `port` is set to `0` or `is_develop` set to `False`. Default `cert/server.key`
- `ssl_cert`: Location of the ssl server certificate for the billing server. Must match the CA distributed to users or the billing server will not connect. Ignored if `port` is set to `0` or `is_develop` is set to `False`. Default `cert/server.pem`
- `signing_key`: Location of the RSA Private key used to sign billing requests. Must match the public key distributed to users or the billing server will not connect. Default `cert/billing.key`
## Aimedb
- `loglevel`: Logging level for the aimedb server. Default `info`
- `port`: Port the aimedb server should listen for connections on. Games are hardcoded to ask for port `22345` so only change if you have a proxy redirecting properly. Default `22345`
- `key`: Key to encrypt/decrypt aimedb requests and responses. MUST be set or the server will not start. If set incorrectly, your server will not properly handle aimedb requests. Default `""`