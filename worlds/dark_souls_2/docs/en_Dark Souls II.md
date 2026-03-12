# Dark Souls II

Game Page | [Items] | [Locations]
<!-- placeholder link -->
[Items]: /tutorial/Dark%20Souls%20II/items/en
[Locations]: /tutorial/Dark%20Souls%20II/locations/en

## Is this Archipelago world for Dark Souls II vanilla or SOTFS?

This APWorld currently supports both the vanilla and Scholar of the First Sin
versions of the game.

The mod is still in active development. Join the [Archipelago Discord server]
for technical support, development updates, or to contribute!
<!-- placeholder link -->
[Archipelago Discord Server]: /link/to/discord

## What do I need to do to randomize DS2?

See full instructions on [the setup page].
<!-- placeholder links -->
[the setup page]: /tutorial/Dark%20Souls%20II/setup/en

## Where is the options page?

The [player options page for this game][options] contains all the options you
need to configure and export a config file.
<!-- placeholder links -->
[options]: ../player-options

## What does randomization do to this game? WIP

1. Most item locations are randomized, including those in the overworld, in
   shops, and dropped by enemies. Randomized locations can contain games from other
   worlds, and any items from your world can appear in other players' worlds. Keep
   scrolling to find out exactly what is and isn't randomized.

2. Currently, enemies and bosses are <b>not natively randomized</b>, but external
   enemy randomisers are supported for SOTFS. See [the setup page] FAQ for instructions.

There are also options that can make playing the game more convenient or
bring a new experience, like removing equip loads, removing stat requirements, or
auto-equipping weapons as you pick them up. Check out [the options page][options] for more!

## What's the goal?

Your goal is to find the "Giant's Lordship" item randomized into the multiworld
and defeat Nashandra in the Throne of Want.
> <small>The trigger for Nashandra to spawn can also be acquired by killing
the Giant Lord in Memory of Jeigh.</small>


## Do I have to check every item in every area? WIP

Dark Souls II has about ### item locations, and Dark Souls II: Scholar of the First Sin has ###.

Not all locations must be checked. Some by default will never contain
any item required for any game to progress; these are missable locations such as
rewards from NPC quests, enemy and boss drops, and so on.

Additionally, the following location groups are set to not be required by default.
This list can be customised via the `exclude_locations` option.

## What if I don't want to do the whole game? WIP

If you want a shorter DS2 randomizer experience, you can exclude entire regions
from containing progression items. The locations of those regions will still
be included in the randomization pool (and appear on trackers), but none of them
will contain any item required to progress any game.

For example, the following configuration requires you to only [WIP] :

```yaml
Dark Souls II:
  # Exclude all DLCs
  sunken_king_dlc: false
  old_iron_king_dlc: false
  ivory_king_dlc: false

  TODO: MAKE EXAMPLE YAML
  exclude_locations:
    # Exclude late-game and DLC regions
    - Anor Londo
    - Lothric Castle
    - Consumed King's Garden
    - Untended Graves
    - Grand Archives
    - Archdragon Peak
    - Painted World of Ariandel
    - Dreg Heap
    - Ringed City

    # Default exclusions
    - Hidden
    - Small Crystal Lizards
    - Upgrade
    - Small Souls
    - Miscellaneous
```

## Are there items that aren't randomized? <!--probably move to item/location guide doc-->

Some groups of items are not randomized in any way and will always behave as
they do in vanilla Dark Souls II.

The following item groups are **not randomized**:

* **Boss soul trades:** Items traded for boss souls at Straid and Ornifex.

* **Dyna and Tillo trades:** Items obtained by trading with Dyna and Tillo.

* **NG+ items:** Items that are only available in later NG cycles, or by
burning a Bonfire Ascetic.
  > **Warning: Some locations contain different items in NG+ (which the randomizer
  > ignores). Burning a Bonfire Ascetic will trigger this replacement and override
  > the randomized NG item that was initially there with the non-randomized NG+ item.
  > This may result in losing an important item.**

The following groups of items are **shuffled within their own group**, rather
than being mixed into the main item pool:

* **NPC rewards:** Items given directly by NPCs.

The following groups of items are **excluded from the item pool**. You will never
find them:
* Items used to raise covenant ranks.
* Items related to online play and matchmaking (excluding `Token of Reprisal` and `Token of Spite`).
* Gestures, Carvings and the Rubbish item.

## How is Game Progression changed? <!--probably move to item/location guide doc-->

Dark Souls II contains various in-game events and key items required for main
story progression. Some of these progression elements behave differently in
this randomizer:

* **Direct-use items:** Items that are directly "used" behave normally once
  obtained. Examples include `Soldier's Key`, `Dull Ember`, and
  `Ashen Mist Heart`.

* **Giant's Kinship / Eye of the Priestess:** These behave identically to
  direct-use items, but can also be acquired by checking their original
  locations. This means defeating the Giant Lord or interacting with
  the altar in Eleum Loyce will still grant their effects. <!--TODO: VERIFY-->

* **Majula Rotunda:** The Majula Rotunda cannot be rotated by Licia. Instead,
  it requires the `Rotunda Lockstone` item.

* **Shrine of Winter:** The Shrine of Winter opens when the "Great Soul
  Embraced" events are triggered at their vanilla locations, **not** by
  obtaining the boss soul items. It will also open upon reaching
  1,000,000 Soul Memory, as in normal Dark Souls II.

* **Petrified statues:** The `Fragrant Branch of Yore` item is unobtainable.
  Instead, you may find statue-specific items that remove petrification from a
  particular statue. For example, `Unpetrify Rosabeth of Melfia`.

* **Pharros contraptions:** The `Pharros' Lockstone` item is unobtainable.
  Instead, the `Master Lockstone` item may be found, which functions as an
  infinitely reusable Pharros' Lockstone.

* **Consolidated items:** All `Smelter Wedge` and `Soul of a Giant` items are
  consolidated into single bundle items: `Smelter Wedge x11` and
  `Soul of a Giant x5`.


## Where can I learn more about Dark Souls II locations?

Location names have to pack a lot of information into very little space. To
better understand them, check out the [location guide], which explains all the
names used in locations and provides more detailed descriptions for each
individual location.

[location guide]: /tutorial/Dark%20Souls%20II/locations/en

## Where can I learn more about Dark Souls II items?

Check out the [item guide], which explains the named groups available for items.

[item guide]: /tutorial/Dark%20Souls%20II/items/en
