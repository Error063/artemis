# Changelog
Documenting updates to ARTEMiS, to be updated every time the master branch is pushed to.

## 20240109
### System
+ Removed `ADD config config` from dockerfile [#83](https://gitea.tendokyu.moe/Hay1tsme/artemis/pulls/83) (Thanks zaphkito!)

### Aimedb
+ Fixed an error that resulted from trying to scan a banned or locked card

## 20240108
### System
+ Change how the underlying system handles URLs
  + This can now allow for things like version-specific, or even keychip-specific URLs
  + Specific changes to games are noted below
+ Fix docker files [#60](https://gitea.tendokyu.moe/Hay1tsme/artemis/pulls/60) (Thanks Rylie!)
+ Fix support for python 3.8 - 3.10

### Aimedb
+ Add support for SegaAuth key in games that support it (for now only Chunithm)
  + This is a JWT that is sent to games, by Aimedb, that the games send to their game server, to verify that the access code the game is sending to the server was obtained via aimedb.
  + Requires a base64-encoded secret to be set in the `core.yaml`

### Chunithm
+ Fix Air support
+ Add saving for userRecentPlayerList
+ Add support for SegaAuthKey
+ Fix a bug arising if a user set their name to be 'true' or 'false'
+ Add support for Sun+ [#78](https://gitea.tendokyu.moe/Hay1tsme/artemis/pulls/78) (Thanks EmmyHeart!)
+ Add `matching` section to `chuni.yaml`
+ ~~Change `udpHolePunchUri` and `reflectorUri` to be STUN and TURN servers~~ Reverted
+ Imrpove `GetGameSetting` request handling for different versions
+ Fix issue where songs would not always return all scores [#92](https://gitea.tendokyu.moe/Hay1tsme/artemis/pulls/92) (Thanks Kumubou!)

### maimai DX
+ Fix user charges failing to save

### maimai
+ Made it functional

### CXB
+ Improvements to request dispatching
+ Add support for non-omnimix music lists


### IDZ
+ Fix news urls in accordance with the system change to URLs

### Initial D THE ARCADE
+ Added support for Initial D THE ARCADE S2
  + Story mode progress added
  + Bunta Challenge/Touhou Project modes added
  + Time Trials added
  + Leaderboards added, but doesn't refresh sometimes
  + Theory of Street mode added (with CPUs)
  + Play Stamp/Timetrial events added
  + Frontend to download profile added
  + Importer to import profiles added

### ONGEKI
+ Now supports HTTPS on a per-version basis
+ Merg PR [#61](https://gitea.tendokyu.moe/Hay1tsme/artemis/pulls/61) (Thanks phantomlan!)
  + Add Ranking Event Support
  + Add reward list support
  + Add version segregation to Event Ranking, Tech Challenge, and Music Ranking
  + Now stores ClientTestmode and ClientSetting data
+ Fix mission points not adding correctly [#68](https://gitea.tendokyu.moe/Hay1tsme/artemis/pulls/68) (Thanks phantomlan!)
+ Fix tech challenge [#70](https://gitea.tendokyu.moe/Hay1tsme/artemis/pulls/70) (Thanks phantomlan!)

### SAO
+ Change endpoint in accordance with the system change to URLs
+ Update request header class to be more accurate
+ Encrypted requests are now supported
+ Change to using handler classes instead of raw structs for simplicity

### Wacca
+ Fix a server error causing a seperate error that casued issues
+ Add better error printing
+ Add better request validation
+ Fix HousingStartV2
+ Fix Lily's housing/get handler

## 20231107
### CXB
+  Hotfix `render_POST` sometimes failing to read the request body on large requests

## 20231106
### CXB
+ Hotfix `render_POST` function signature signature
+ Hotfix `handle_action_addenergy_request` hard failing if `get_energy` returns None

## 20231015
### maimai DX
+ Added support for FESTiVAL PLUS

### Card Maker
+ Added support for maimai DX FESTiVAL PLUS

## 20230716
### General
+ Docker files added (#19)
+ Added support for threading
  + This comes with the caviat that enabling it will not allow you to use Ctrl + C to stop the server.

### Webui
+ Small improvements
+ Add card display

### Allnet
+ Billing format validation
+ Fix naomitest.html endpoint
+ Add event logging for auths and billing
+ LoaderStateRecorder endpoint handler added

### Mucha
+ Fixed log level always being "Info"
+ Add stub handler for DownloadState

### Sword Art Online
+ Support added

### Crossbeats
+ Added threading to profile loading
  + This should cause a noticeable speed-up

### Card Maker
+ DX Passes fixed
+ Various improvements

### Diva
+ Added clear status calculation
+ Various minor fixes and improvements

### Maimai
+ Added support for memorial photo uploads
+ Added support for the following versions
  + Festival
  + FiNALE
+ Various bug fixes and improvements

### Wacca
+ Fixed an error that sometimes occoured when trying to unlock songs (#22)

### Pokken
+ Profile saving added (loading TBA)
+ Use external STUN server for matching by default
  + Matching still not working

## 2023042300
### Wacca
+ Time free now works properly
+ Fix reverse gate mission causing a fatal error
+ Other misc. fixes
+ Latest DB: 5

### Pokken
+ Added preliminary support
    + Nothing saves currently, but the game will boot and function properly.

### Initial D Zero
+ Added preliminary support
    + Nothing saves currently, but the game will boot and function for the most part.

### Mai2
+ Added support for Festival
+ Lasted DB Version: 4

### Ongeki
+ Misc fixes
+ Lasted DB Version: 4

### Diva
+ Misc fixes
+ Lasted DB Version: 4

### Chuni
+ Fix network encryption
+ Add `handle_remove_token_api_request` for event mode

### Allnet
+ Added download order support
    + It is up to the sysop to provide the INI file, and host the files.
    + ONLY for use with cabs. It's not checked currently, which it's why it's default disabled
    + YMMV, use at your own risk
+ When running develop mode, games that are not recognised will still be able to authenticate.

### Database
+ Add autoupgrade command
    + Invoke to automatically upgrade all schemas to their latest versions

+ `version` arg no longer required, leave it blank to update the game schema to latest if it isn't already

### Misc
+ Update example nginx config file
