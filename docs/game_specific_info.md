# ARTEMiS Games Documentation

Below are all supported games with supported version ids in order to use
the corresponding importer and database upgrades.

**Important: The described database upgrades are only required if you are using an old database schema, f.e. still
using the megaime database. Clean installations always create the latest database structure!**

# Table of content

- [Supported Games](#supported-games)
    - [CHUNITHM](#chunithm)
    - [crossbeats REV.](#crossbeats-rev)
    - [maimai DX](#maimai-dx)
    - [O.N.G.E.K.I.](#o-n-g-e-k-i)
    - [Card Maker](#card-maker)
    - [WACCA](#wacca)
    - [Sword Art Online Arcade](#sao)


# Supported Games

Games listed below have been tested and confirmed working.

## CHUNITHM

### SDBT

| Version ID | Version Name          |
|------------|-----------------------|
| 0          | CHUNITHM              |
| 1          | CHUNITHM PLUS         |
| 2          | CHUNITHM AIR          |
| 3          | CHUNITHM AIR PLUS     |
| 4          | CHUNITHM STAR         |
| 5          | CHUNITHM STAR PLUS    |
| 6          | CHUNITHM AMAZON       |
| 7          | CHUNITHM AMAZON PLUS  |
| 8          | CHUNITHM CRYSTAL      |
| 9          | CHUNITHM CRYSTAL PLUS |
| 10         | CHUNITHM PARADISE     |

### SDHD/SDBT

| Version ID | Version Name        |
|------------|---------------------|
| 11         | CHUNITHM NEW!!      |
| 12         | CHUNITHM NEW PLUS!! |
| 13         | CHUNITHM SUN        |


### Importer

In order to use the importer locate your game installation folder and execute:

```shell
python read.py --series SDBT --version <version ID> --binfolder /path/to/game/folder --optfolder /path/to/game/option/folder
```

The importer for Chunithm will import: Events, Music, Charge Items and Avatar Accesories.

### Database upgrade

Always make sure your database (tables) are up-to-date, to do so go to the `core/data/schema/versions` folder and see
which version is the latest, f.e. `SDBT_4_upgrade.sql`. In order to upgrade to version 4 in this case you need to
perform all previous updates as well:

```shell
python dbutils.py --game SDBT upgrade
```

### Online Battle

**Only matchmaking (with your imaginary friends) is supported! Online Battle does not (yet?) work!**

The first person to start the Online Battle (now called host) will create a "matching room" with a given `roomId`, after that max 3 other people can join the created room.
Non used slots during the matchmaking will be filled with CPUs after the timer runs out.
As soon as a new member will join the room the timer will jump back to 60 secs again.
Sending those 4 messages to all other users is also working properly.
In order to use the Online Battle every user needs the same ICF, same rom version and same data version!
If a room is full a new room will be created if another user starts an Online Battle.
After a failed Online Battle the room will be deleted. The host is used for the timer countdown, so if the connection failes to the host the timer will stop and could create a "frozen" state.

#### Information/Problems:

- Online Battle uses UDP hole punching and opens port 50201?
- `reflectorUri` seems related to that?
- Timer countdown should be handled globally and not by one user
- Game can freeze or can crash if someone (especially the host) leaves the matchmaking


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

| Game Code | Version ID | Version Name            |
|-----------|------------|-------------------------|
| SDEZ      | 0          | maimai DX               |
| SDEZ      | 1          | maimai DX PLUS          |
| SDEZ      | 2          | maimai DX Splash        |
| SDEZ      | 3          | maimai DX Splash PLUS   |
| SDEZ      | 4          | maimai DX Universe      |
| SDEZ      | 5          | maimai DX Universe PLUS |
| SDEZ      | 6          | maimai DX Festival      |

For versions pre-dx
| Game Code | Version ID | Version Name         |
|-----------|------------|----------------------|
| SBXL      | 1000       | maimai               |
| SBXL      | 1001       | maimai PLUS          |
| SBZF      | 1002       | maimai GreeN         |
| SBZF      | 1003       | maimai GreeN PLUS    |
| SDBM      | 1004       | maimai ORANGE        |
| SDBM      | 1005       | maimai ORANGE PLUS   |
| SDCQ      | 1006       | maimai PiNK          |
| SDCQ      | 1007       | maimai PiNK PLUS     |
| SDDK      | 1008       | maimai MURASAKI      |
| SDDK      | 1009       | maimai MURASAKI PLUS |
| SDDZ      | 1010       | maimai MILK          |
| SDDZ      | 1011       | maimai MILK PLUS     |
| SDEY      | 1012       | maimai FiNALE        |

### Importer

In order to use the importer locate your game installation folder and execute:
DX:
```shell
python read.py --series <Game Code> --version <Version ID> --binfolder /path/to/StreamingAssets --optfolder /path/to/game/option/folder
```
Pre-DX:
```shell
python read.py --series <Game Code> --version <Version ID> --binfolder /path/to/data --optfolder /path/to/patch/data
```
The importer for maimai DX will import Events, Music and Tickets.

The importer for maimai Pre-DX will import Events and Music. Not all games will have patch data. Milk - Finale have file encryption, and need an AES key. That key is not provided by the developers. For games that do use encryption, provide the key, as a hex string, with the `--extra` flag. Ex `--extra 00112233445566778899AABBCCDDEEFF`

**Important: It is required to use the importer because some games may not function properly or even crash without Events!**

### Database upgrade

Always make sure your database (tables) are up-to-date, to do so go to the `core/data/schema/versions` folder and see which version is the latest, f.e. `SDEZ_2_upgrade.sql`. In order to upgrade to version 2 in this case you need to perform all previous updates as well:

```shell
python dbutils.py --game SDEZ upgrade
```
Pre-Dx uses the same database as DX, so only upgrade using the SDEZ game code!

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
| 0          | Card Maker 1.30 |
| 1          | Card Maker 1.35 |


### Support status

* Card Maker 1.30:
  * CHUNITHM NEW!!: Yes
  * maimai DX UNiVERSE: Yes
  * O.N.G.E.K.I. Bright: Yes

* Card Maker 1.35:
  * CHUNITHM SUN: Yes (NEW PLUS!! up to A032)
  * maimai DX FESTiVAL: Yes (up to A035) (UNiVERSE PLUS up to A031)
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

Also make sure to import all maimai DX and CHUNITHM data as well:

```shell
python read.py --series SDED --version <version ID> --binfolder /path/to/cardmaker/CardMaker_Data
```

The importer for Card Maker will import all required Gachas (Banners) and cards (for maimai DX/CHUNITHM) and the hardcoded
Cards for each Gacha (O.N.G.E.K.I. only).

**NOTE: Without executing the importer Card Maker WILL NOT work!**


### Config setup

Make sure to update your `config/cardmaker.yaml` with the correct version for each game. To get the current version required to run a specific game, open every opt (Axxx) folder descending until you find all three folders:

- `MU3`: O.N.G.E.K.I.
- `MAI`: maimai DX
- `CHU`: CHUNITHM

Inside each folder is a `DataConfig.xml` file, for example:

`MU3/DataConfig.xml`:
```xml
  <cardMakerVersion>
    <major>1</major>
    <minor>35</minor>
    <release>3</release>
  </cardMakerVersion>
```

Now update your `config/cardmaker.yaml` with the correct version number, for example:

```yaml
version:
  1: # Card Maker 1.35
    ongeki: 1.35.03
```	 

### O.N.G.E.K.I.

Gacha "無料ガチャ" can only pull from the free cards with the following probabilities: 94%: R, 5% SR and 1% chance of
getting an SSR card

Gacha "無料ガチャ（SR確定）" can only pull from free SR cards with prob: 92% SR and 8% chance of getting an SSR card

Gacha "レギュラーガチャ" can pull from every card added to ongeki_static_cards with the following prob: 77% R, 20% SR
and 3% chance of getting an SSR card

All other (limited) gachas can pull from every card added to ongeki_static_cards but with the promoted cards
(click on the green button under the banner) having a 10 times higher chance to get pulled

### CHUNITHM

All cards in CHUNITHM (basically just the characters) have the same rarity to it just pulls randomly from all cards
from a given gacha but made sure you cannot pull the same card twice in the same 5 times gacha roll.

### maimai DX

Printed maimai DX cards: Freedom (`cardTypeId=6`) or Gold Pass (`cardTypeId=4`) can now be selected during the login process. You can only have ONE Freedom and ONE Gold Pass active at a given time. The cards will expire after 15 days.

Thanks GetzeAvenue for the `selectedCardList` rarity hint!

### Notes

Card Maker 1.30-1.34 will only load an O.N.G.E.K.I. Bright profile (1.30). Card Maker 1.35+ will only load an O.N.G.E.K.I.
Bright Memory profile (1.35).
The gachas inside the `config/ongeki.yaml` will make sure only the right gacha ids for the right CM version will be loaded.
Gacha IDs up to 1140 will be loaded for CM 1.34 and all gachas will be loaded for CM 1.35.

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

## SAO

### SDEW

| Version ID | Version Name  |
|------------|---------------|
| 0          | SAO           |


### Importer

In order to use the importer locate your game installation folder and execute:

```shell
python read.py --series SDEW --version <version ID> --binfolder /path/to/game/extractedassets
```

The importer for SAO will import all items, heroes, support skills and titles data.

### Config

Config file is located in `config/sao.yaml`.

| Option             | Info                                                                        |
|--------------------|-----------------------------------------------------------------------------|
| `hostname`         | Changes the server listening address for Mucha                              |
| `port`             | Changes the listing port                                                    |
| `auto_register`    | Allows the game to handle the automatic registration of new cards           |


### Database upgrade

Always make sure your database (tables) are up-to-date, to do so go to the `core/data/schema/versions` folder and see which version is the latest, f.e. `SDEW_1_upgrade.sql`. In order to upgrade to version 3 in this case you need to perform all previous updates as well:

```shell
python dbutils.py --game SDEW upgrade
```

### Notes
- Co-Op (matching) is not supported
- Shop is not functionnal
- Player title is currently static and cannot be changed in-game

### Credits for SAO support:

- Midorica - Limited Network Support
- Dniel97 - Helping with network base
- tungnotpunk - Source