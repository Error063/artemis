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

## Quick start guide
1) Clone this repository
2) Install requirements (see the platform-specific guides for instructions)
3) Install python libraries via `pip`
4) Copy the example configuration files into another folder (by default the server looks for the `config` directory)
5) Edit the newly copied configuration files to your liking, using [this](docs/config.md) doc as a guide.
6) Run the server by invoking `index.py` ex. `python3 index.py`