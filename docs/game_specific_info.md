# ARTEMiS Games Documentation

Below are all supported games with supported version ids in order to use
the corresponding importer and database upgrades.

**Important: The described database upgrades are only required if you are using an old database schema, f.e. still
using the megaime database. Clean installations always create the latest database structure!**

To upgrade the core database and the database for every game, execute:

```shell
python dbutils.py autoupgrade
```

# Table of content

- [Supported Games](#supported-games)
    - [CHUNITHM](#chunithm)
    - [crossbeats REV.](#crossbeats-rev)
    - [maimai DX](#maimai-dx)
    - [O.N.G.E.K.I.](#o-n-g-e-k-i)
    - [Card Maker](#card-maker)
    - [WACCA](#wacca)
    - [Sword Art Online Arcade](#sao)
	- [Initial D THE ARCADE](#initial-d-the-arcade)


# Supported Games

Games listed below have been tested and confirmed working.

## CHUNITHM

### SDBT

| Version ID | Version Name          |
| ---------- | --------------------- |
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
| ---------- | ------------------- |
| 11         | CHUNITHM NEW!!      |
| 12         | CHUNITHM NEW PLUS!! |
| 13         | CHUNITHM SUN        |
| 14         | CHUNITHM SUN PLUS   |


### Importer

In order to use the importer locate your game installation folder and execute:

```shell
python read.py --game SDBT --version <version ID> --binfolder /path/to/game/folder --optfolder /path/to/game/option/folder
```

The importer for Chunithm will import: Events, Music, Charge Items and Avatar Accesories.

### Config

Config file is located in `config/chuni.yaml`.

| Option           | Info                                                                                                           |
|------------------|----------------------------------------------------------------------------------------------------------------|
| `news_msg`       | If this is set, the news at the top of the main screen will be displayed (up to Chunithm Paradise Lost)        |
| `name`           | If this is set, all players that are not on a team will use this one by default.                               |
| `use_login_bonus`| This is used to enable the login bonuses                                                                       |
| `crypto`         | This option is used to enable the TLS Encryption                                                               |


**If you would like to use network encryption, the following will be required underneath but key, iv and hash are required:**

```yaml
crypto:
  encrypted_only: False
  keys:
    13: ["0000000000000000000000000000000000000000000000000000000000000000", "00000000000000000000000000000000", "0000000000000000"]
```

### Database upgrade

Always make sure your database (tables) are up-to-date:

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

### Rivals

You can configure up to 4 rivals in Chunithm on a per-user basis. There is no UI to do this currently, so in the database, you can do this:
```sql
INSERT INTO aime.chuni_item_favorite (user, version, favId, favKind) VALUES (<user1>, <version>, <user2>, 2);
INSERT INTO aime.chuni_item_favorite (user, version, favId, favKind) VALUES (<user2>, <version>, <user1>, 2);
```
Note that the version **must match**, otherwise song lookup may not work.

### Teams

You can also configure teams for users to be on. There is no UI to do this currently, so in the database, you can do this:
```sql
INSERT INTO aime.chuni_profile_team (teamName) VALUES (<teamName>);
```
Team names can be regular ASCII, and they will be displayed ingame.

### Favorite songs
You can set the songs that will be in a user's Favorite Songs category using the following SQL entries:
```sql
INSERT INTO aime.chuni_item_favorite (user, version, favId, favKind) VALUES (<user>, <version>, <songId>, 1);
```
The songId is based on the actual ID within your version of Chunithm.


## crossbeats REV.

### SDCA

| Version ID | Version Name                       |
| ---------- | ---------------------------------- |
| 0          | crossbeats REV.                    |
| 1          | crossbeats REV. SUNRISE            |
| 2          | crossbeats REV. SUNRISE S2         |
| 3          | crossbeats REV. SUNRISE S2 Omnimix |

### Importer

In order to use the importer you need to use the provided `Export.csv` file:

```shell
python read.py --game SDCA --version <version ID> --binfolder titles/cxb/data
```

The importer for crossbeats REV. will import Music.

### Config

Config file is located in `config/cxb.yaml`.

| Option                | Info                                                       |
| --------------------- | ---------------------------------------------------------- |
| `hostname`            | Requires a proper `hostname` (not localhost!) to run       |
| `ssl_enable`          | Enables/Disables the use of the `ssl_cert` and `ssl_key`   |
| `port`                | Set your unsecure port number                              |
| `port_secure`         | Set your secure/SSL port number                            |
| `ssl_cert`, `ssl_key` | Enter your SSL certificate (requires not self signed cert) |


## maimai DX

### Versions

| Game Code | Version ID | Version Name            |
| --------- | ---------- | ----------------------- |
| SBXL      | 0          | maimai                  |
| SBXL      | 1          | maimai PLUS             |
| SBZF      | 2          | maimai GreeN            |
| SBZF      | 3          | maimai GreeN PLUS       |
| SDBM      | 4          | maimai ORANGE           |
| SDBM      | 5          | maimai ORANGE PLUS      |
| SDCQ      | 6          | maimai PiNK             |
| SDCQ      | 7          | maimai PiNK PLUS        |
| SDDK      | 8          | maimai MURASAKi         |
| SDDK      | 9          | maimai MURASAKi PLUS    |
| SDDZ      | 10         | maimai MiLK             |
| SDDZ      | 11         | maimai MiLK PLUS        |
| SDEY      | 12         | maimai FiNALE           |
| SDEZ      | 13         | maimai DX               |
| SDEZ      | 14         | maimai DX PLUS          |
| SDEZ      | 15         | maimai DX Splash        |
| SDEZ      | 16         | maimai DX Splash PLUS   |
| SDEZ      | 17         | maimai DX UNiVERSE      |
| SDEZ      | 18         | maimai DX UNiVERSE PLUS |
| SDEZ      | 19         | maimai DX FESTiVAL      |
| SDEZ      | 20         | maimai DX FESTiVAL PLUS |

### Importer

In order to use the importer locate your game installation folder and execute:
DX:
```shell
python read.py --game <Game Code> --version <Version ID> --binfolder /path/to/StreamingAssets --optfolder /path/to/game/option/folder
```
Pre-DX:
```shell
python read.py --game <Game Code> --version <Version ID> --binfolder /path/to/data --optfolder /path/to/patch/data
```
The importer for maimai DX will import Events, Music and Tickets.

The importer for maimai Pre-DX will import Events and Music. Not all games will have patch data. Milk - Finale have file encryption, and need an AES key. That key is not provided by the developers. For games that do use encryption, provide the key, as a hex string, with the `--extra` flag. Ex `--extra 00112233445566778899AABBCCDDEEFF`

**Important: It is required to use the importer because some games may not function properly or even crash without Events!**

### Database upgrade

Always make sure your database (tables) are up-to-date:

```shell
python dbutils.py --game SDEZ upgrade
```

Pre-Dx uses the same database as DX, so only upgrade using the SDEZ game code!

## Hatsune Miku Project Diva

### SBZV

| Version ID | Version Name                    |
| ---------- | ------------------------------- |
| 0          | Project Diva Arcade             |
| 1          | Project Diva Arcade Future Tone |


### Importer

In order to use the importer locate your game installation folder and execute:

```shell
python read.py --game SBZV --version <version ID> --binfolder /path/to/game/data/diva --optfolder /path/to/game/data/diva/mdata
```

The importer for Project Diva Arcade will all required data in order to use
the Shop, Modules and Customizations.

### Config

Config file is located in `config/diva.yaml`.

| Option               | Info                                                                                            |
| -------------------- | ----------------------------------------------------------------------------------------------- |
| `unlock_all_modules` | Unlocks all modules (costumes) by default, if set to `False` all modules need to be purchased   |
| `unlock_all_items`   | Unlocks all items (customizations) by default, if set to `False` all items need to be purchased |

### Custom PV Lists (databanks)

In order to use custom PV Lists, simply drop in your .dat files inside of /titles/diva/data/ and make sure they are called PvList0.dat, PvList1.dat, PvList2.dat, PvList3.dat and PvList4.dat exactly.

### Database upgrade

Always make sure your database (tables) are up-to-date:

```shell
python dbutils.py --game SBZV upgrade
```

## O.N.G.E.K.I.

### SDDT

| Version ID | Version Name               |
| ---------- | -------------------------- |
| 0          | O.N.G.E.K.I.               |
| 1          | O.N.G.E.K.I. +             |
| 2          | O.N.G.E.K.I. SUMMER        |
| 3          | O.N.G.E.K.I. SUMMER +      |
| 4          | O.N.G.E.K.I. R.E.D.        |
| 5          | O.N.G.E.K.I. R.E.D. +      |
| 6          | O.N.G.E.K.I. bright        |
| 7          | O.N.G.E.K.I. bright MEMORY |


### Importer

In order to use the importer locate your game installation folder and execute:

```shell
python read.py --game SDDT --version <version ID> --binfolder /path/to/game/folder --optfolder /path/to/game/option/folder
```

The importer for O.N.G.E.K.I. will all all Cards, Music and Events.

**NOTE: The Importer is required for Card Maker.**

### Config

Config file is located in `config/ongeki.yaml`.

| Option           | Info                                                                                                           |
| ---------------- | -------------------------------------------------------------------------------------------------------------- |
| `enabled_gachas` | Enter all gacha IDs for Card Maker to work, other than default may not work due to missing cards added to them |
| `crypto`         | This option is used to enable the TLS Encryption                                                               |

Note: 1149 and higher are only for Card Maker 1.35 and higher and will be ignored on lower versions.

**If you would like to use network encryption, the following will be required underneath but key, iv and hash are required:**

```yaml
crypto:
  encrypted_only: False
  keys:
    7: ["0000000000000000000000000000000000000000000000000000000000000000", "00000000000000000000000000000000", "0000000000000000"]
```

### Database upgrade

Always make sure your database (tables) are up-to-date:

```shell
python dbutils.py --game SDDT upgrade
```

### Controlling Events (Ranking Event, Technical Challenge Event, Mission Event)

Events are controlled by 2 types of enabled events:
- RankingEvent (type 6), TechChallengeEvent (type 17)
- AcceptRankingEvent (type 7), AcceptTechChallengeEvent (type 18)

Both Ranking and Accept must be enabled for event to function properly

Event will run for the time specified in startDate and endDate

AcceptRankingEvent and AcceptTechChallengeEvent are reward period for events, which specify from what startDate until endDate you can collect the rewards for attending the event, so the reward period must start in the future, e.g. :

- RankingEvent startDate 2023-12-01 - endDate 2023-12-30 - period in which whole event is running
- AcceptRankingEvent startDate 2023-12-23 - endDate 2023-12-30 - period in which you can collect rewards for the event

If player misses the AcceptRankingEvent period - ranking will be invalidated and receive lowest reward from the event (typically 500x money)

Technical Challenge Song List:

Songs that are used for Technical Challenge are not stored anywhere in data files, so you need to fill the database table by yourself, you can gather all songs that should be in Technical Challenges from ONGEKI japanese wikis, or, you can create your own sets:

Database table : `ongeki_static_tech_music`

```
id: Id in table, just increment for each entry
version: version of the game you want the tech challenge to be in (from RED and up)
eventId: Id of the event in ongeki_static_events, insert the Id of the TechChallengeEvent (type 17) you want the song be assigned to
musicId: Id of the song you want to add, use songId from ongeki_static_music table
level: Difficulty of the song you want to track during the event, from 0(basic) to 3(master)

```

Current implementation of Ranking and Technical Challenge Events are updated on every profile save to the Network, and Ranked on each player login, in official specification, calculation for current rank on the network should be done in the maintenance window

Mission Event (type 13) is a monthly type of event, which is used when another event doesn't have it's own Ranking or Technical Challenge Event running, only one Mission Event should be running at a time, so enable only the specific Mission you want to run currently on the Network

If you're often trying fresh cards, registering new profiles etc., you can also consider disabling all Announcement Events (type 1), as it will disable all the banners that pop up on login (they show up only once though, so if you click through them once they won't show again)

Event type 2 in Database are Advertisement Movies, enable only 1 you want to currently play, and disable others


Present and Reward List - populate reward list using read.py

Create present for players by adding an entry in `ongeki_static_present_list`
```
id: unique for each entry
version: game version you want the present be in
presentId: id of the present - starts with 1001 and go up from that, must be unique for each reward(don't set multiple rewardIds with same presentId)
presentName: present name which will be shown on the bottom when received
rewardId: ID of item from ongeki_static_rewards
stock: how many you want to give (like 5 copies of same card, or 10000 money, etc.)
message: no idea, can be left empty
startDate: date when to start giving out
endDate: date when ends
```

After inserting present to the table, add the presentId into players `ongeki_static_item`, where itemKind is 9, itemId is the presentId, and stock set 1 and isValid to 1

After that, on next login the present should be received (or whenever it supposed to happen)



## Card Maker

### SDED

| Version ID | Version Name    |
| ---------- | --------------- |
| 0          | Card Maker 1.30 |
| 1          | Card Maker 1.35 |


### Support status

#### Card Maker 1.30:
* CHUNITHM NEW!!: Yes
* maimai DX UNiVERSE: Yes
* O.N.G.E.K.I. bright: Yes

#### Card Maker 1.35:
* CHUNITHM: 
  * NEW!!: Yes
  * NEW PLUS!!: Yes (added in A028)
  * SUN: Yes (added in A032)
* maimai DX:
  * UNiVERSE PLUS: Yes
  * FESTiVAL: Yes (added in A031)
  * FESTiVAL PLUS: Yes (added in A035)
* O.N.G.E.K.I. bright MEMORY: Yes


### Importer

In order to use the importer you need to use the provided `.csv` files (which are required for O.N.G.E.K.I.) and the
option folders:

```shell
python read.py --game SDED --version <version ID> --binfolder titles/cm/cm_data --optfolder /path/to/cardmaker/option/folder
```

**If you haven't already executed the O.N.G.E.K.I. importer, make sure you import all cards!**

```shell
python read.py --game SDDT --version <version ID> --binfolder /path/to/game/folder --optfolder /path/to/game/option/folder
```

Also make sure to import all maimai DX and CHUNITHM data as well:

```shell
python read.py --game SDED --version <version ID> --binfolder /path/to/cardmaker/CardMaker_Data
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

For now you also need to update your `config/ongeki.yaml` with the correct version number, for example:

```yaml
version:
  7: # O.N.G.E.K.I. bright MEMORY
    card_maker: 1.35.03
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
| ---------- | ------------- |
| 0          | WACCA         |
| 1          | WACCA S       |
| 2          | WACCA Lily    |
| 3          | WACCA Lily R  |
| 4          | WACCA Reverse |


### Importer

In order to use the importer locate your game installation folder and execute:

```shell
python read.py --game SDFE --version <version ID> --binfolder /path/to/game/WindowsNoEditor/Mercury/Content
```

The importer for WACCA will import all Music data.

### Config

Config file is located in `config/wacca.yaml`.

| Option             | Info                                                                        |
| ------------------ | --------------------------------------------------------------------------- |
| `always_vip`       | Enables/Disables VIP, if disabled it needs to be purchased manually in game |
| `infinite_tickets` | Always set the "unlock expert" tickets to 5                                 |
| `infinite_wp`      | Sets the user WP to `999999`                                                |
| `enabled_gates`    | Enter all gate IDs which should be enabled in game                          |


### Database upgrade

Always make sure your database (tables) are up-to-date:

```shell
python dbutils.py --game SDFE upgrade
```

### VIP Rewards
Below is a list of VIP rewards. Currently, VIP is not implemented, and thus these are not obtainable. These 23 rewards were distributed once per month for VIP users on the real network.

	Plates:
		211004 リッチ
		211018 特盛えりざべす
		211025 イースター
		211026 特盛りりぃ
		311004 ファンシー
		311005 インカンテーション
		311014 夜明け
		311015 ネイビー
		311016 特盛るーん
	
	Ring Colors:
		203002 Gold Rushイエロー
		203009 トロピカル
		303005 ネイチャー
	
	Icons:
		202020 どらみんぐ
		202063 ユニコーン
		202086 ゴリラ
		302014 ローズ
		302015 ファラオ
		302045 肉球
		302046 WACCA
		302047 WACCA Lily
		302048 WACCA Reverse
	
	Note Sound Effect:
		205002 テニス
		205008 シャワー
		305003 タンバリンMk-Ⅱ

## SAO

### SDEW

| Version ID | Version Name |
| ---------- | ------------ |
| 0          | SAO          |


### Importer

In order to use the importer locate your game installation folder and execute:

```shell
python read.py --game SDEW --version <version ID> --binfolder /path/to/game/extractedassets
```

The importer for SAO will import all items, heroes, support skills and titles data.

### Config

Config file is located in `config/sao.yaml`.

| Option          | Info                                                              |
| --------------- | ----------------------------------------------------------------- |
| `hostname`      | Changes the server listening address for Mucha                    |
| `port`          | Changes the listing port                                          |
| `auto_register` | Allows the game to handle the automatic registration of new cards |


### Database upgrade

Always make sure your database (tables) are up-to-date:

```shell
python dbutils.py --game SDEW upgrade
```

### Notes
- Defrag Match will crash at loading
- Co-Op Online is not supported
- Shop is not functionnal
- Player title is currently static and cannot be changed in-game
- QR Card Scanning currently only load a static hero

**Network hashing in GssSite.dll must be disabled**

### Credits for SAO support:

- Midorica - Limited Network Support
- Dniel97 - Helping with network base
- tungnotpunk - Source

## Initial D THE ARCADE

### SDGT

| Version ID | Version Name                  |
| ---------- | ----------------------------- |
| 0          | Initial D THE ARCADE Season 1 |
| 1          | Initial D THE ARCADE Season 2 |

**Important: Only version 1.50.00 (Season 2) is currently working and actively supported!**

### Profile Importer

In order to use the profile importer download the `idac_profile.json` file from the frontend
and either directly use the folder path with `idac_profile.json` in it or specify the complete
path to the `.json` file

```shell
python read.py --game SDGT --version <Version ID> --optfolder /path/to/game/download/folder
```

The importer for SDGT will import the complete profile data with personal high scores as well.

### Config

Config file is located in `config/idac.yaml`.

| Option                        | Info                                                                                                        |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `ssl`                         | Enables/Disables the use of the `ssl_cert` and `ssl_key` (currently unsuported)                             |
| `matching_host`               | IPv4 address of your PC for the Online Battle (currently unsupported)                                       |
| `port_matching`               | Port number for the Online Battle Matching                                                                  |
| `port_echo1/2`                | Port numbers for Echos                                                                                      |
| `port_matching_p2p`           | Port number for Online Battle (currently unsupported)                                                       |
| `stamp.enable`               | Enables/Disabled the play stamp events                                                                      |
| `stamp.enabled_stamps`        | Define up to 3 play stamp events (without `.json` extension, which are placed in `titles/idac/data/stamps`) |
| `timetrial.enable`           | Enables/Disables the time trial event                                                                       |
| `timetrial.enabled_timetrial` | Define one! trial event (without `.json` extension, which are placed in `titles/idac/data/timetrial`)       |


### Database upgrade

Always make sure your database (tables) are up-to-date:

```shell
python dbutils.py --game SDGT upgrade
```

### Notes
- Online Battle is not supported
- Online Battle Matching is not supported

### Item categories

| Category ID | Category Name            |
| ----------- | ------------------------ |
| 1           | D Coin                   |
| 3           | Car Dressup Token        |
| 5           | Avatar Dressup Token     |
| 6           | Tachometer               |
| 7           | Aura                     |
| 8           | Aura Color               |
| 9           | Avatar Face              |
| 10          | Avatar Eye               |
| 11          | Avatar Mouth             |
| 12          | Avatar Hair              |
| 13          | Avatar Glasses           |
| 14          | Avatar Face accessories  |
| 15          | Avatar Body              |
| 18          | Avatar Background        |
| 21          | Chat Stamp               |
| 22          | Keychain                 |
| 24          | Title                    |
| 25          | FullTune Ticket          |
| 26          | Paper Cup                |
| 27          | BGM                      |
| 28          | Drifting Text            |
| 31          | Start Menu BG            |
| 32          | Car Color/Paint          |
| 33          | Aura Level               |
| 34          | FullTune Ticket Fragment |
| 35          | Underneon Lights         |

### TimeRelease Chapter:

1. Story: 1, 2, 3, 4, 5, 6, 7, 8, 9, 19 (Chapter 10), (29 Chapter 11?)
2. MF Ghost: 10, 11, 12, 13, 14, 15
3. Bunta: 15, 16, 17, 18, 19, 20, (21, 21, 22?)
4. Special Event: 23, 24, 25, 26, 27, 28 (Touhou Project)

### TimeRelease Courses:


| Course ID | Course Name               | Direction                |
| --------- | ------------------------- | ------------------------ |
| 0         | Akina Lake(秋名湖)        | CounterClockwise(左周り) |
| 2         | Akina Lake(秋名湖)        | Clockwise(右周り)        |
| 52        | Hakone(箱根)              | Downhill(下り)           |
| 54        | Hakone(箱根)              | Hillclimb(上り)          |
| 36        | Usui(碓氷)                | CounterClockwise(左周り) |
| 38        | Usui(碓氷)                | Clockwise(右周り)        |
| 4         | Myogi(妙義)               | Downhill(下り)           |
| 6         | Myogi(妙義)               | Hillclimb(上り)          |
| 8         | Akagi(赤城)               | Downhill(下り)           |
| 10        | Akagi(赤城)               | Hillclimb(上り)          |
| 12        | Akina(秋名)               | Downhill(下り)           |
| 14        | Akina(秋名)               | Hillclimb(上り)          |
| 16        | Irohazaka(いろは坂)       | Downhill(下り)           |
| 18        | Irohazaka(いろは坂)       | Reverse(逆走)            |
| 56        | Momiji Line(もみじライン) | Downhill(下り)           |
| 58        | Momiji Line(もみじライン) | Hillclimb(上り)          |
| 20        | Tsukuba(筑波)             | Outbound(往路)           |
| 22        | Tsukuba(筑波)             | Inbound(復路)            |
| 24        | Happogahara(八方ヶ原)     | Outbound(往路)           |
| 26        | Happogahara(八方ヶ原)     | Inbound(復路)            |
| 40        | Sadamine(定峰)            | Downhill(下り)           |
| 42        | Sadamine(定峰)            | Hillclimb(上り)          |
| 44        | Tsuchisaka(土坂)          | Outbound(往路)           |
| 46        | Tsuchisaka(土坂)          | Inbound(復路)            |
| 48        | Akina Snow(秋名雪)        | Downhill(下り)           |
| 50        | Akina Snow(秋名雪)        | Hillclimb(上り)          |
| 68        | Odawara(小田原)           | Forward(順走)            |
| 70        | Odawara(小田原)           | Reverse(逆走)            |

### Credits
- Bottersnike: For the HUGE Reverse Engineering help
- Kinako: For helping with the timeRelease unlocking of courses and special mode

A huge thanks to all people who helped shaping this project to what it is now and don't want to be mentioned here.

