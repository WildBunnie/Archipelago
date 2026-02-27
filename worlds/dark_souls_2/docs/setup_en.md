# Dark Souls II Randomizer Setup Guide

## Required Software

- The PC version of [Dark Souls II](https://store.steampowered.com/app/236430/DARK_SOULS_II/) or [Dark Souls II: Scholar of the First Sin](https://store.steampowered.com/app/335300/DARK_SOULS_II_Scholar_of_the_First_Sin/)
- [Dark Souls II Archipelago Mod](https://github.com/WildBunnie/DarkSoulsII-Archipelago/releases/latest)

## Optional Software

- [Map Tracker](https://github.com/AkagiCritMagnet/Dark-Souls-2-poptracker-for-Archipelago)

## Setting Up

In the release page for the mod presented above you will find three files, one for the apworld, and two zip files with each one being the mod for each version of the game.

### Installing the Mod

- Download the correct zip for your version of the game (`SOTFS` for Scholar of the First Sin and `VANILLA` for the original version)
- Unzip the file and move all it's contents to the game folder, inside the folder named `GAME`, where the game's exe is found.
- (OPTIONAL) You can edit the ds2modengine.ini file that comes with the mod if you wish to change any of it's configurations. It is very much not advised to use your default save file (sl2) or to play online though.
- (OPTIONAL) If you wish to download other mods, any dll mod placed in the archipelago folder that comes in the zip, will be loaded by the game. We don't guarantee that all other mods will work properly but simpler ones like the `bbj_mod` ([vanilla version](https://github.com/pseudostripy/bbj_mod), [sotfs version](https://github.com/pseudostripy/bbj_mod_sotfs)) will work.
<!-- TODO linux instructions -->

### Running and Connecting to the Game

- After the previous steps you can open the game and an overlay should popup
- Before creating a save file you should connect to the archipelago server. You can do this by filling in the server uri (e.g. `archipelago.gg:123456`), your slot name that you chose in the YAML file (e.g. `JohnDarkSoulsII`) and optionally you can fill in the password if the server has one. You can then press connect and wait for the overlay to say that you are `Connected`
- After you are connected you can create a new save and enjoy the game. Make sure to always connect in the menu before loading your save.

## Frequently Asked Questions

## Troubleshooting

### Game Crashes

This can happen for many different reasons, but below are some common reasons:

- Make sure you are on the latest Steam version of the game, no other versions are supported
- ...