# ARTEMiS Production mode
Production mode is a configuration option that changes how the server listens to be more friendly to a production environment. This mode assumes that a proxy (for this guide, nginx) is standing in front of the server to handle port mapping and TLS. In order to activate production mode, simply change `is_develop` to `False` in `core.yaml`. Next time you start the server, you should see "Starting server in production mode".

## Nginx Configuration
### Port forwarding
Artemis requires that the following ports be forwarded to allow internet traffic to access the server. This will not change regardless of what you set in the config, as many of these ports are hard-coded in the games.
`tcp:80` all.net, non-ssl titles
`tcp:8443` billing
`tcp:22345` aimedb
`tcp:443` frontend, SSL titles

### A note about external proxy services (cloudflare, etc)
Due to the way that artemis functions, it is currently not possible to put the server behind something like Cloudflare. Cloudflare only proxies web traffic on the standard ports (80, 443) and, as shown above, this does not work with artemis. Server administrators should seek other means to protect their network (VPS hosting, VPN, etc)

### SSL Certificates
You will need to generate SSL certificates for some games. The certificates vary in security and validity requirements. Please see the general guide below
- General Title: The certificate for the general title server should be valid, not self-signed and match the CN that the game will be reaching out to (e.i if your games are reaching out to titles.hostname.here, your ssl certificate should be valid for titles.hostname.here, or *.hostname.here)
- CXB: Same requires as the title server. It must not be self-signed, and CN must match. Recomended to get a wildcard cert if possible, and use it for both Title and CXB
- Pokken: Pokken can be self-signed, and the CN doesn't have to match, but it MUST use 2048-bit RSA. Due to the games age, andthing stronger then that will be rejected.

### Port mappings
An example config is provided in the `config` folder called `nginx_example.conf`. It is set up for the following:
`naominet.jp:tcp:80` -> `localhost:tcp:8000` for allnet
`ib.naominet.jp:ssl:8443` -> `localhost:tcp:8444` for the billing server
`your.hostname.here:ssl:443` -> `localhost:tcp:8080` for the SSL title server
`your.hostname.here:tcp:80` -> `localhost:tcp:8080` for the non-SSL title server
`cxb.hostname.here:ssl:443` -> `localhost:tcp:8080` for crossbeats (appends /SDCA/104/ to the request)
`pokken.hostname.here:ssl:443` -> `localhost:tcp:8080` for pokken
`frontend.hostname.here:ssl:443` -> `localhost:tcp:8090` for the frontend, includes https redirection

If you're using this as a guide, be sure to replace your.hostname.here with the hostname you specified in core.yaml under `titles->hostname`. Do *not* change naominet.jp, or allnet/billing will fail. Also remember to specifiy certificate paths correctly, as in the example they are simply placeholders.

### Multi-service ports
It is possible to use nginx to redirect billing and title server requests to the same port that all.net uses. By setting `port` to 0 under billing and title server, you can change the nginx config to serve the following (entries not shown here should be the same)
`ib.naominet.jp:ssl:8443` -> `localhost:tcp:8000` for the billing server
`your.hostname.here:ssl:443` -> `localhost:tcp:8000` for the SSL title server
`your.hostname.here:tcp:80` -> `localhost:tcp:8000` for the non-SSL title server
`cxb.hostname.here:ssl:443` -> `localhost:tcp:8000` for crossbeats (appends /SDCA/104/ to the request)
`pokken.hostname.here:ssl:443` -> `localhost:tcp:8000` for pokken

This will allow you to only use 3 ports locally, but you will still need to forward the same internet-facing ports as before.