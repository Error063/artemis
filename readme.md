# ARTEMiS
A network service emulator for games running SEGA'S ALL.NET service, and similar.

# Supported games
Games listed below have been tested and confirmed working. Only game versions older then the current one in active use in arcades (n-0) or current game versions older then a year (y-1) are supported.
+ Chunithm
    + All versions up to New!! Plus

+ Crossbeats Rev
    + All versions + omnimix

+ Maimai
    + All versions up to Universe Plus

+ Hatsune Miku Arcade
    + All versions

+ Ongeki
    + All versions up to Bright

+ Wacca
    + Lily R
    + Reverse


## Requirements
- python 3 (tested working with 3.9 and 3.10, other versions YMMV)
- pip
- memcached (for non-windows platforms)
- mysql/mariadb server

## Setup guides
Follow the platform-specific guides for [windows](docs/INSTALL_WINDOWS.md) and [ubuntu](docs/INSTALL_UBUNTU.md) to setup and run the server.

## Production guide
See the [production guide](docs/prod.md) for running a production server.
