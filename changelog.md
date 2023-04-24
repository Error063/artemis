# Changelog
Documenting updates to ARTEMiS, to be updated every time the master branch is pushed to.

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
