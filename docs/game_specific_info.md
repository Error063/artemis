# ARTEMiS Games Documentation

Below are all supported games with supported version ids in order to use
the corresponding importer and database upgrades.

**Important: The described database upgrades are only required if you are using an old database schema, f.e. still
using the megaime database. Clean installations always create the latest database structure!**

# Table of content

- [Supported Games](#supported-games)
    - [Chunithm](#chunithm)
    - [crossbeats REV.](#crossbeats-rev)
    - [maimai DX](#maimai-dx)
    - [O.N.G.E.K.I.](#o-n-g-e-k-i)
    - [Card Maker](#card-maker)
    - [WACCA](#wacca)


# Supported Games

Games listed below have been tested and confirmed working.

## Chunithm

### SDBT

| Version ID | Version Name       |
|------------|--------------------|
| 0          | Chunithm           |
| 1          | Chunithm+          |
| 2          | Chunithm Air       |
| 3          | Chunithm Air +     |
| 4          | Chunithm Star      |
| 5          | Chunithm Star +    |
| 6          | Chunithm Amazon    |
| 7          | Chunithm Amazon +  |
| 8          | Chunithm Crystal   |
| 9          | Chunithm Crystal + |
| 10         | Chunithm Paradise  |

### SDHD/SDBT

| Version ID | Version Name    |
|------------|-----------------|
| 11         | Chunithm New!!  |
| 12         | Chunithm New!!+ |


### Importer

In order to use the importer locate your game installation folder and execute:

```shell
python read.py --series SDBT --version <version ID> --binfolder /path/to/game/folder --optfolder /path/to/game/option/folder
```

The importer for Chunithm will import: Events, Music, Charge Items and Avatar Accesories.

### Database upgrade

Always make sure your database (tables) are up-to-date, to do so go to the `core/data/schema/versions` folder and see
which version is the latest, f.e. `SDBT_3_upgrade.sql`. In order to upgrade to version 3 in this case you need to
perform all previous updates as well:

```shell
python dbutils.py --game SDBT upgrade
```

## crossbeats REV.

### SDCA

| Version ID | Version Name                       |
|------------|------------------------------------|
| 0          | crossbeats REV.                    |
| 1          | crossbeats REV. SUNRISE            |
| 2          | crossbeats REV. SUNRISE S2         |
| 3          | crossbeats REV. SUNRISE S2 Omnimix |

### Importer

In order to use the importer you need to use the provided `Export.csv` file:

```shell
python read.py --series SDCA --version <version ID> --binfolder titles/cxb/data
```

The importer for crossbeats REV. will import Music.

### Config

Config file is located in `config/cxb.yaml`.

| Option                 | Info                                                       |
|------------------------|------------------------------------------------------------|
| `hostname`             | Requires a proper `hostname` (not localhost!) to run       |
| `ssl_enable`           | Enables/Disables the use of the `ssl_cert` and `ssl_key`   |
| `port`                 | Set your unsecure port number                              |
| `port_secure`          | Set your secure/SSL port number                            |
| `ssl_cert`, `ssl_key`  | Enter your SSL certificate (requires not self signed cert) |


## maimai DX

### SDEZ

| Version ID | Version Name            |
|------------|-------------------------|
| 0          | maimai DX               |
| 1          | maimai DX PLUS          |
| 2          | maimai DX Splash        |
| 3          | maimai DX Splash PLUS   |
| 4          | maimai DX Universe      |
| 5          | maimai DX Universe PLUS |
| 6          | maimai DX Festival      |

### Importer

In order to use the importer locate your game installation folder and execute:

```shell
python read.py --series SDEZ --version <version ID> --binfolder /path/to/game/folder --optfolder /path/to/game/option/folder
```

The importer for maimai DX will import Events, Music and Tickets.

**NOTE: It is required to use the importer because the game will
crash without Events!**

### Database upgrade

Always make sure your database (tables) are up-to-date, to do so go to the `core/data/schema/versions` folder and see which version is the latest, f.e. `SDEZ_2_upgrade.sql`. In order to upgrade to version 2 in this case you need to perform all previous updates as well:

```shell
python dbutils.py --game SDEZ upgrade
```

## Hatsune Miku Project Diva

### SBZV

| Version ID | Version Name                    |
|------------|---------------------------------|
| 0          | Project Diva Arcade             |
| 1          | Project Diva Arcade Future Tone |


### Importer

In order to use the importer locate your game installation folder and execute:

```shell
python read.py --series SBZV --version <version ID> --binfolder /path/to/game/data/diva --optfolder /path/to/game/data/diva/mdata
```

The importer for Project Diva Arcade will all required data in order to use
the Shop, Modules and Customizations.

### Config

Config file is located in `config/diva.yaml`.

| Option               | Info                                                                                            |
|----------------------|-------------------------------------------------------------------------------------------------|
| `unlock_all_modules` | Unlocks all modules (costumes) by default, if set to `False` all modules need to be purchased   |
| `unlock_all_items`   | Unlocks all items (customizations) by default, if set to `False` all items need to be purchased |


### Database upgrade

Always make sure your database (tables) are up-to-date, to do so go to the `core/data/schema/versions` folder and see
which version is the latest, f.e. `SBZV_4_upgrade.sql`. In order to upgrade to version 4 in this case you need to
perform all previous updates as well:

```shell
python dbutils.py --game SBZV upgrade
```

## O.N.G.E.K.I.

### SDDT

| Version ID | Version Name               |
|------------|----------------------------|
| 0          | O.N.G.E.K.I.               |
| 1          | O.N.G.E.K.I. +             |
| 2          | O.N.G.E.K.I. Summer        |
| 3          | O.N.G.E.K.I. Summer +      |
| 4          | O.N.G.E.K.I. Red           |
| 5          | O.N.G.E.K.I. Red +         |
| 6          | O.N.G.E.K.I. Bright        |
| 7          | O.N.G.E.K.I. Bright Memory |


### Importer

In order to use the importer locate your game installation folder and execute:

```shell
python read.py --series SDDT --version <version ID> --binfolder /path/to/game/folder --optfolder /path/to/game/option/folder
```

The importer for O.N.G.E.K.I. will all all Cards, Music and Events.

**NOTE: The Importer is required for Card Maker.**

### Config

Config file is located in `config/ongeki.yaml`.

| Option           | Info                                                                                                           |
|------------------|----------------------------------------------------------------------------------------------------------------|
| `enabled_gachas` | Enter all gacha IDs for Card Maker to work, other than default may not work due to missing cards added to them |

Note: 1149 and higher are only for Card Maker 1.35 and higher and will be ignored on lower versions.

### Database upgrade

Always make sure your database (tables) are up-to-date, to do so go to the `core/data/schema/versions` folder and see
which version is the latest, f.e. `SDDT_4_upgrade.sql`. In order to upgrade to version 4 in this case you need to
perform all previous updates as well:

```shell
python dbutils.py --game SDDT upgrade
```

## Card Maker

### SDED

| Version ID | Version Name    |
|------------|-----------------|
| 0          | Card Maker 1.34 |
| 1          | Card Maker 1.35 |


### Support status

* Card Maker 1.34:
  * Chunithm New!!: Yes
  * maimai DX Universe: Yes
  * O.N.G.E.K.I. Bright: Yes

* Card Maker 1.35:
  * Chunithm New!!+: Yes
  * maimai DX Universe PLUS: Yes
  * O.N.G.E.K.I. Bright Memory: Yes


### Importer

In order to use the importer you need to use the provided `.csv` files (which are required for O.N.G.E.K.I.) and the
option folders:

```shell
python read.py --series SDED --version <version ID> --binfolder titles/cm/cm_data --optfolder /path/to/cardmaker/option/folder
```

**If you haven't already executed the O.N.G.E.K.I. importer, make sure you import all cards!**

```shell
python read.py --series SDDT --version <version ID> --binfolder /path/to/game/folder --optfolder /path/to/game/option/folder
```

Also make sure to import all maimai and Chunithm data as well:

```shell
python read.py --series SDED --version <version ID> --binfolder /path/to/cardmaker/CardMaker_Data
```

The importer for Card Maker will import all required Gachas (Banners) and cards (for maimai/Chunithm) and the hardcoded
Cards for each Gacha (O.N.G.E.K.I. only).

**NOTE: Without executing the importer Card Maker WILL NOT work!**


### O.N.G.E.K.I. Gachas

Gacha "無料ガチャ" can only pull from the free cards with the following probabilities: 94%: R, 5% SR and 1% chance of
getting an SSR card

Gacha "無料ガチャ（SR確定）" can only pull from free SR cards with prob: 92% SR and 8% chance of getting an SSR card

Gacha "レギュラーガチャ" can pull from every card added to ongeki_static_cards with the following prob: 77% R, 20% SR
and 3% chance of getting an SSR card

All other (limited) gachas can pull from every card added to ongeki_static_cards but with the promoted cards
(click on the green button under the banner) having a 10 times higher chance to get pulled

### Chunithm Gachas

All cards in Chunithm (basically just the characters) have the same rarity to it just pulls randomly from all cards
from a given gacha but made sure you cannot pull the same card twice in the same 5 times gacha roll.

### Notes

Card Maker 1.34 will only load an O.N.G.E.K.I. Bright profile (1.30). Card Maker 1.35 will only load an O.N.G.E.K.I.
Bright Memory profile (1.35).
The gachas inside the `ongeki.yaml` will make sure only the right gacha ids for the right CM version will be loaded.
Gacha IDs up to 1140 will be loaded for CM 1.34 and all gachas will be loaded for CM 1.35.

**NOTE: There is currently no way to load/use the (printed) maimai DX cards!**

## WACCA

### SDFE

| Version ID | Version Name  |
|------------|---------------|
| 0          | WACCA         |
| 1          | WACCA S       |
| 2          | WACCA Lily    |
| 3          | WACCA Lily R  |
| 4          | WACCA Reverse |


### Importer

In order to use the importer locate your game installation folder and execute:

```shell
python read.py --series SDFE --version <version ID> --binfolder /path/to/game/WindowsNoEditor/Mercury/Content
```

The importer for WACCA will import all Music data.

### Config

Config file is located in `config/wacca.yaml`.

| Option             | Info                                                                        |
|--------------------|-----------------------------------------------------------------------------|
| `always_vip`       | Enables/Disables VIP, if disabled it needs to be purchased manually in game |
| `infinite_tickets` | Always set the "unlock expert" tickets to 5                                 |
| `infinite_wp`      | Sets the user WP to `999999`                                                |
| `enabled_gates`    | Enter all gate IDs which should be enabled in game                          |


### Database upgrade

Always make sure your database (tables) are up-to-date, to do so go to the `core/data/schema/versions` folder and see which version is the latest, f.e. `SDFE_3_upgrade.sql`. In order to upgrade to version 3 in this case you need to perform all previous updates as well:

```shell
python dbutils.py --game SDFE upgrade
```
