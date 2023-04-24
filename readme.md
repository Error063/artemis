# ARTEMiS
A network service emulator for games running SEGA'S ALL.NET service, and similar.

# Supported games
Games listed below have been tested and confirmed working. Only game versions older then the current one in active use in arcades (n-0) or current game versions older then a year (y-1) are supported.
+ Chunithm
    + All versions up to New!! Plus

+ Crossbeats Rev
    + All versions + omnimix

+ maimai DX
    + All versions up to Festival

+ Hatsune Miku Arcade
    + All versions

+ Card Maker
    + 1.34.xx
    + 1.35.xx

+ Ongeki
    + All versions up to Bright Memory

+ Wacca
    + Lily R
    + Reverse

+ Pokken
    + Final Online

## Requirements
- python 3 (tested working with 3.9 and 3.10, other versions YMMV)
- pip
- memcached (for non-windows platforms)
- mysql/mariadb server

## Setup guides
Follow the platform-specific guides for [windows](docs/INSTALL_WINDOWS.md) and [ubuntu](docs/INSTALL_UBUNTU.md) to setup and run the server.

## Game specific information
Read [Games specific info](docs/game_specific_info.md) for all supported games, importer settings, configuration option and database upgrades.

## Production guide
See the [production guide](docs/prod.md) for running a production server.
