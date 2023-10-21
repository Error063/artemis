# ARTEMiS
A network service emulator for games running SEGA'S ALL.NET service, and similar.

# Supported games
Games listed below have been tested and confirmed working. Only game versions older then the version currently active in arcades, or games versions that have not recieved a major update in over one year, are supported.

+ CHUNITHM
    + All versions up to SUN

+ crossbeats REV.
    + All versions + omnimix

+ maimai DX
    + All versions up to FESTiVAL

+ Hatsune Miku: Project DIVA Arcade
    + All versions

+ Card Maker
    + 1.30
    + 1.35

+ O.N.G.E.K.I.
    + All versions up to bright MEMORY

+ WACCA
    + Lily R
    + Reverse

+ POKKÉN TOURNAMENT
    + Final Online

+ Sword Art Online Arcade (partial support)
    + Final

## Requirements
- python 3 (tested working with 3.9 and 3.10, other versions YMMV)
- pip
- memcached (for non-windows platforms)
- mysql/mariadb server

## Setup guides
Follow the platform-specific guides for [windows](docs/INSTALL_WINDOWS.md), [ubuntu](docs/INSTALL_UBUNTU.md) or [docker](docs/INSTALL_DOCKER.md) to setup and run the server.

## Game specific information
Read [Games specific info](docs/game_specific_info.md) for all supported games, importer settings, configuration option and database upgrades.

## Production guide
See the [production guide](docs/prod.md) for running a production server.
