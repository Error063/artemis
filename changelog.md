# Changelog
Documenting updates to ARTEMiS, to be updated every time the master branch is pushed to.

## 20231001
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
