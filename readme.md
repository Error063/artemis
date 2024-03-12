# ARTEMiS
A network service emulator for games running SEGA'S ALL.NET service, and similar.

# Supported games
Games listed below have been tested and confirmed working. Only game versions older then the version currently active in arcades, or games versions that have not recieved a major update in over one year, are supported.

+ Card Maker
    + 1.30
    + 1.35

+ CHUNITHM INTL
    + SUPERSTAR
    + NEW
    + NEW PLUS
    + SUN
    + SUN PLUS

+ CHUNITHM JP
    + AIR
    + AIR PLUS
    + AMAZON
    + AMAZON PLUS
    + CRYSTAL
    + CRYSTAL PLUS
    + PARADISE
    + PARADISE LOST
    + NEW
    + NEW PLUS
    + SUN
    + SUN PLUS

+ crossbeats REV.
    + Crossbeats REV.
    + Crossbeats REV. SUNRiSE S1
    + Crossbeats REV. SUNRiSE S2 + omnimix

+ Hatsune Miku: Project DIVA Arcade
    + Future Tone Arcade - All versions

+ Initial D THE ARCADE
    + Season 2

+ maimai DX
    + Splash
    + Splash Plus
    + UNiVERSE
    + UNiVERSE PLUS
    + FESTiVAL
    + FESTiVAL PLUS

+ O.N.G.E.K.I.
    + SUMMER
    + SUMMER PLUS
    + R.E.D.
    + R.E.D. PLUS
    + bright
    + bright MEMORY

+ POKKÉN TOURNAMENT
    + Final Online

+ Sword Art Online Arcade
    + Final (Single player only)

+ WACCA
    + Lily R
    + Reverse

## Requirements
- python 3 (tested working with 3.9 and 3.10, other versions YMMV)
- pip
- memcached (for non-windows platforms)
- mysql/mariadb server

## Setup guides
Follow the platform-specific guides for [windows](docs/INSTALL_WINDOWS.md), [linux (Debian 12 or Rasperry Pi OS recomended, but anything works)](docs/INSTALL_LINUX.md) or [docker](docs/INSTALL_DOCKER.md) to setup and run the server.

## Game specific information
Read [Games specific info](docs/game_specific_info.md) for all supported games, importer settings, configuration option and database upgrades.

## Production guide
See the [production guide](docs/prod.md) for running a production server.
