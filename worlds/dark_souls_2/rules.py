from dataclasses import dataclass
from typing import List, Union

from worlds.generic.Rules import CollectionRule

from .enums import DS2Version

RuleInput = Union[
    CollectionRule,
    str,
    List[str],
]


@dataclass
class RuleData:
    spot: str
    """TODO"""

    rule: RuleInput
    """TODO"""

    version: DS2Version = None
    """TODO"""

    def to_collection_rule(self, player: int) -> CollectionRule:
        # must be (state, player)
        if callable(self.rule):
            return lambda state, f=self.rule: f(state, player)

        # single item
        if isinstance(self.rule, str):
            return lambda state: state.has(self.rule, player)

        # list of items (OR logic)
        if isinstance(self.rule, List):
            return lambda state: any(state.has(item, player) for item in self.rule)

        assert False, f"RuleData rule is invalid type {type(self.rule)}"

# TODO explain


connection_rules: List[RuleData] = [
    RuleData("Majula -> Huntsman's Copse", "Rotate the Majula Rotunda"),
    RuleData("Majula -> The Pit", ["Silvercat Ring", "Flying Feline Boots"]),
    RuleData("Majula -> Shaded Woods", "Unpetrify Rosabeth of Melfia"),

    RuleData("Forest of Fallen Giants -> Forest of Fallen Giants - Salamander Pit", "Iron Key"),
    RuleData("Forest of Fallen Giants -> Forest of Fallen Giants - Soldier Key", "Soldier Key"),
    RuleData("Forest of Fallen Giants -> Memory of Vammar", "Ashen Mist Heart"),

    RuleData("Forest of Fallen Giants - Soldier Key -> Memory of Orro", "Ashen Mist Heart"),
    RuleData("Forest of Fallen Giants - Soldier Key -> Memory of Jeigh", "Ashen Mist Heart"),
    RuleData("Forest of Fallen Giants - Soldier Key -> Memory of Jeigh", "King's Ring"),

    RuleData("The Lost Bastille - Wharf -> The Lost Bastille - After Key", "Antiquated Key"),
    RuleData("The Lost Bastille - After Statue -> Belfry Luna", "Master Lockstone"),
    RuleData("The Lost Bastille - After Key -> The Lost Bastille - Late", "Master Lockstone", version=DS2Version.VANILLA),
    RuleData("The Lost Bastille - Early -> The Lost Bastille - After Statue", "Unpetrify Statue in Lost Bastille", version=DS2Version.SOTFS),

    RuleData("Iron Keep -> Belfry Sol",  "Master Lockstone"),
    RuleData("Iron Keep -> Brume Tower", "Heavy Iron Key", version=DS2Version.SOTFS),

    RuleData("Black Gulch -> Shulva, Sanctum City", "Dragon Talon", version=DS2Version.SOTFS),

    RuleData("Shaded Woods -> Aldia's Keep", "King's Ring"),
    RuleData("Shaded Woods -> Drangleic Castle", "Open Shrine of Winter"),

    RuleData("Drangleic Castle -> Shrine of Amana", "Key to King's Passage"),
    RuleData("Drangleic Castle -> Throne of Want", "King's Ring"),
    RuleData("Drangleic Castle -> Frozen Eleum Loyce", "Frozen Flower", version=DS2Version.SOTFS),

    RuleData("Shulva, Sanctum City -> Cave of The Dead", "Eternal Sanctum Key"),
    RuleData("Dragon's Sanctum -> Dragon's Sanctum - Dragon Stone", "Dragon Stone"),

    RuleData("Brume Tower -> Brume Tower - Scepter", "Scorching Iron Scepter"),
    RuleData("Brume Tower - Scepter -> Iron Passage", "Tower Key"),
    RuleData("Brume Tower - Scepter -> Memory of the Old Iron King", "Tower Key"),
    RuleData("Brume Tower - Scepter -> Memory of the Old Iron King", "Ashen Mist Heart"),
]

location_rules: List[RuleData] = [
    # events
    RuleData("Rotate the Majula Rotunda", "Rotunda Lockstone"),
    RuleData("Open Shrine of Winter", "Defeat the Rotten"),
    RuleData("Open Shrine of Winter", "Defeat the Lost Sinner"),
    RuleData("Open Shrine of Winter", "Defeat the Old Iron King"),
    RuleData("Open Shrine of Winter", "Defeat the Duke's Dear Freja"),

    # Aldias Keep
    RuleData("Aldias: Large Soul of a Brave Warrior - locked side room, behind barrel", "Aldia Key"),
    RuleData("Aldias: Soul of a Proud Knight - locked side room, on table", "Aldia Key"),
    # Belfry Luna
    # Belfry Sol
    # Black Gulch
    RuleData("Gulch: Pharros' Lockstone - by second bonfire", "Unpetrify Statue in Black Gulch"),
    # Brume Tower
    RuleData("BrumeTower: Old Radiant Lifegem x3 - cursed area, chest on left", "Tower Key"),
    RuleData("BrumeTower: Fire Snake - cursed area, chest on right", "Tower Key"),
    RuleData("BrumeTower: Large Titanite Shard x5 - cursed area, on altar", "Tower Key"),
    RuleData("BrumeTower: Soul of Nadalia, Bride of Ash - second Ashen Idol", "Smelter Wedge x11"),
    RuleData("BrumeTower: Soul of Nadalia, Bride of Ash - lever room, Ashen Idol", "Smelter Wedge x11"),
    RuleData("BrumeTower: Soul of Nadalia, Bride of Ash - cursed area, Ashen Idol", "Smelter Wedge x11"),
    RuleData("BrumeTower: Soul of Nadalia, Bride of Ash - cursed area, Ashen Idol", "Tower Key"),
    RuleData("BrumeTower: Soul of Nadalia, Bride of Ash - first side tower, Ashen Idol", "Smelter Wedge x11"),
    RuleData("BrumeTower: Soul of Nadalia, Bride of Ash - by first bonfire, Ashen Idol", "Smelter Wedge x11"),
    # Brume Tower - Scepter
    RuleData("BrumeTower: Soul of the Fume Knight", "Smelter Wedge x11"),
    RuleData("BrumeTower: Soul of Nadalia, Bride of Ash - end boss drop", "Smelter Wedge x11"),
    RuleData("BrumeTower: Soul of Nadalia, Bride of Ash - left side before end boss, Ashen Idol", "Smelter Wedge x11"),
    RuleData("BrumeTower: Soul of Nadalia, Bride of Ash - left side before end boss, Ashen Idol", "Smelter Wedge x11"),
    RuleData("BrumeTower: Soul of Nadalia, Bride of Ash - right side before end boss, Ashen Idol", "Smelter Wedge x11"),
    RuleData("BrumeTower: Soul of Nadalia, Bride of Ash - right side before end boss, Ashen Idol", "Smelter Wedge x11"),
    RuleData("BrumeTower: Soul of Nadalia, Bride of Ash - towards Alonne, Ashen Idol", "Smelter Wedge x11"),
    RuleData("BrumeTower: Soul of Nadalia, Bride of Ash - towards Alonne, Ashen Idol", "Tower Key"),
    RuleData("BrumeTower: Soul of Nadalia, Bride of Ash - doors room, Ashen Idol", "Smelter Wedge x11"),
    # Cathedral of Blue
    # Cave of The Dead
    # Doors of Pharros
    RuleData("Pharros: Faintstone - room behind ladder after using lockstone above, chest", "Master Lockstone"),
    RuleData("Pharros: Twinkling Titanite - room behind ladder after using lockstone above, chest", "Master Lockstone"),
    RuleData("Pharros: Magic Arrow x15 - upper level, chest behind contraption", "Master Lockstone"),
    RuleData("Pharros: Santier's Spear - first big hall, three-part contraption", "Master Lockstone"),
    RuleData("Pharros: Soul of a Brave Warrior - upper level, three-part contraption", "Master Lockstone"),
    # Dragon Aerie
    # Dragon Shrine
    # Dragons Sanctum
    RuleData("DragonsSanctum: Dried Root - room behind Eternal Sanctum key door , Metal chest", "Eternal Sanctum Key"),
    RuleData("DragonsSanctum: Dried Root x2 - room behind Eternal Sanctum key door , Metal chest", "Eternal Sanctum Key"),
    RuleData("DragonsSanctum: Dried Root x5 - room behind Eternal Sanctum key door , Metal chest", "Eternal Sanctum Key"),
    RuleData("DragonsSanctum: Lightning Clutch Ring - room behind Eternal Sanctum key door , Metal chest", "Eternal Sanctum Key"),
    RuleData("DragonsSanctum: Dried Root x2 - room behind Eternal Sanctum key door , Metal chest", "Eternal Sanctum Key", version=DS2Version.VANILLA),
    RuleData("DragonsSanctum: Bonfire Ascetic x2 - room behind Eternal Sanctum key door , Metal chest", "Eternal Sanctum Key", version=DS2Version.SOTFS),
    RuleData("DragonsSanctum: Sanctum Shield - room atop tower opposite Priestess' Chamber bonfire, metal chest", "Eternal Sanctum Key"),
    # Drangleic Castle
    RuleData("Drangleic: Ring of the Dead - release locked Milfanito", "Key to the Embedded"),
    RuleData("Drangleic: Soul Bolt - after second boss, chest", "Key to King's Passage"),
    RuleData("Drangleic: Spell Quartz Ring+2 - after second boss, chest", "Key to King's Passage"),
    RuleData("Drangleic: Bonfire Ascetic x3 - after second boss, chest", "Key to King's Passage"),
    RuleData("Drangleic: Lifegem - before second boss", "Key to King's Passage"),
    RuleData("Drangleic: Soul of a Proud Knight - before second boss", "Key to King's Passage"),
    RuleData("Drangleic: Twinkling Titanite - before second boss", "Key to King's Passage"),
    RuleData("Drangleic: Alluring Skull x3 - before second boss", "Key to King's Passage"),
    RuleData("Drangleic: Petrified Something - before second boss", "Key to King's Passage", version=DS2Version.SOTFS),
    # Earthen Peak
    # Forest of Fallen Giants
    # Forest of Fallen Giants - Salamander Pit
    # Forest of Fallen Giants - Soldier Key
    # Frigid Outskirts
    # Frozen Eleum Loyce
    # Grave of Saints
    RuleData("GraveOfSaints: Whisper of Despair - after bridge, second floor", "Master Lockstone"),
    RuleData("GraveOfSaints: Torch - after bridge, second floor", "Master Lockstone"),
    RuleData("GraveOfSaints: Poison Moss x2 - after bridge, first floor", "Master Lockstone"),
    # Harvest Valley
    # Heides Tower of Flame
    RuleData("Heides: Knight Helm - behind statue before Wharf, metal chest", "Unpetrify Statue in Heide's Tower of Flame", version=DS2Version.SOTFS),
    RuleData("Heides: Knight Armor - behind statue before Wharf, metal chest", "Unpetrify Statue in Heide's Tower of Flame", version=DS2Version.SOTFS),
    RuleData("Heides: Knight Gauntlets - behind statue before Wharf, metal chest", "Unpetrify Statue in Heide's Tower of Flame", version=DS2Version.SOTFS),
    RuleData("Heides: Knight Leggings - behind statue before Wharf, metal chest", "Unpetrify Statue in Heide's Tower of Flame", version=DS2Version.SOTFS),
    RuleData("Heides: Estus Flask Shard - railing behind statue before Wharf", "Unpetrify Statue in Heide's Tower of Flame", version=DS2Version.SOTFS),
    # Huntsmans Copse
    RuleData("Chariot: Bone Crown - Gren shop after killing Copse boss", "Token of Spite"),
    RuleData("Chariot: Bone King Robe - Gren shop after killing Copse boss", "Token of Spite"),
    RuleData("Chariot: Bone King Cuffs - Gren shop after killing Copse boss", "Token of Spite"),
    RuleData("Chariot: Bone King Skirt - Gren shop after killing Copse boss", "Token of Spite"),
    # Iron Keep
    RuleData("IronKeep: Ancient Dragon Seal - join Dragon Remnants", "Petrified Egg"),
    RuleData("IronKeep: Dragon Eye - join Dragon Remnants", "Petrified Egg"),
    # Iron Passage 
    # Majula
    RuleData("Majula: Prism Stone - Rosabeth after unpetrifying her", "Unpetrify Rosabeth of Melfia"),
    RuleData("Majula: Titanite Shard x3 - mansion attic", "House Key"),
    RuleData("Majula: Torch x3 - mansion attic", "House Key"),
    RuleData("Majula: Short Bow - Lenigrast workshop", "Lenigrast's Key"),
    RuleData("Majula: Soul Vessel - mansion basement", "House Key"),
    RuleData("Majula: Estus Flask Shard - mansion basement", "House Key"),
    RuleData("Majula: Pharros' Lockstone - mansion library", "House Key"),
    RuleData("Majula: Fireball - Rosabeth shop", "Unpetrify Rosabeth of Melfia"),
    RuleData("Majula: Fire Orb - Rosabeth shop", "Unpetrify Rosabeth of Melfia"),
    RuleData("Majula: Combustion - Rosabeth shop", "Unpetrify Rosabeth of Melfia"),
    RuleData("Majula: Poison Mist - Rosabeth shop", "Unpetrify Rosabeth of Melfia"),
    RuleData("Majula: Flash Sweat - Rosabeth shop", "Unpetrify Rosabeth of Melfia"),
    RuleData("Majula: Iron Flesh - Rosabeth shop", "Unpetrify Rosabeth of Melfia"),
    RuleData("Majula: Flame Quartz Ring - Rosabeth shop", "Unpetrify Rosabeth of Melfia"),
    RuleData("Majula: Thunder Quartz Ring - Rosabeth shop", "Unpetrify Rosabeth of Melfia"),
    RuleData("Majula: Dark Quartz Ring - Rosabeth shop", "Unpetrify Rosabeth of Melfia"),
    RuleData("Majula: Longsword - Lenigrast shop", "Lenigrast's Key"),
    RuleData("Majula: Broadsword - Lenigrast shop", "Lenigrast's Key"),
    RuleData("Majula: Estoc - Lenigrast shop", "Lenigrast's Key"),
    RuleData("Majula: Rapier - Lenigrast shop", "Lenigrast's Key"),
    RuleData("Majula: Falchion - Lenigrast shop", "Lenigrast's Key"),
    RuleData("Majula: Battle Axe - Lenigrast shop", "Lenigrast's Key"),
    RuleData("Majula: Mace - Lenigrast shop", "Lenigrast's Key"),
    RuleData("Majula: Spear - Lenigrast shop", "Lenigrast's Key"),
    RuleData("Majula: Repair Powder - Lenigrast shop", "Lenigrast's Key"),
    RuleData("Majula: Flying Feline Boots - Shalquoir shop after killing Pharros and GraveOfSaints bosses", "Defeat Royal Rat Authority"),
    RuleData("Majula: Flying Feline Boots - Shalquoir shop after killing Pharros and GraveOfSaints bosses", "Defeat Royal Rat Vanguard"),
    # Memory of Jeigh
    # Memory of Orro
    RuleData("Orro: Soul of a Hero x3 - behind contraption", "Master Lockstone"),
    RuleData("Orro: Fire Seed - behind contraption, illusory wall", "Master Lockstone"),
    RuleData("Orro: Steel Helm - behind contraption, illusory wall", "Master Lockstone"),
    RuleData("Orro: Steel Armor - behind contraption, illusory wall", "Master Lockstone"),
    RuleData("Orro: Steel Gauntlets - behind contraption, illusory wall", "Master Lockstone"),
    RuleData("Orro: Steel Leggings - behind contraption, illusory wall", "Master Lockstone"),
    # Memory of The Old Iron King
    # Memory of Vammar
    RuleData("Vammar: Drangleic Helm - Drummond after defeating Giant Lord", "Giant's Kinship"),
    # No Mans Wharf
    # Quantum
    # Shaded Woods
    RuleData("ShadedWoods: Fragrant Branch of Yore - Tark after killing zone boss", "Ring of Whispers"),
    RuleData("ShadedWoods: Fragrant Branch of Yore - metal chest blocked by statue near boss path", "Unpetrify Lion Mage Set Statue in Shaded Ruins"),
    RuleData("ShadedWoods: Lion Mage Robe - metal chest blocked by statue near boss path", "Unpetrify Lion Mage Set Statue in Shaded Ruins"),
    RuleData("ShadedWoods: Lion Mage Cuffs - metal chest blocked by statue near boss path", "Unpetrify Lion Mage Set Statue in Shaded Ruins"),
    RuleData("ShadedWoods: Lion Mage Skirt - metal chest blocked by statue near boss path", "Unpetrify Lion Mage Set Statue in Shaded Ruins"),
    RuleData("ShadedWoods: Human Effigy x3 - statue-blocked metal chest, left from bonfire bridge", "Unpetrify Statue Blocking the Chest in Shaded Ruins", version=DS2Version.SOTFS),
    RuleData("ShadedWoods: Bleeding Serum x3 - statue-blocked metal chest, left from bonfire bridge", "Unpetrify Statue Blocking the Chest in Shaded Ruins", version=DS2Version.SOTFS),
    # Shaded Woods 
    # Shrine of Amana
    RuleData("Amana: King's Crown - behind door, opens after defeating Vendrick, metal chest", "Soul of a Giant x5"),
    RuleData("Amana: King's Armor - behind door, opens after defeating Vendrick, metal chest", "Soul of a Giant x5"),
    RuleData("Amana: King's Gauntlets - behind door, opens after defeating Vendrick, metal chest", "Soul of a Giant x5"),
    RuleData("Amana: King's Leggings - behind door, opens after defeating Vendrick, metal chest", "Soul of a Giant x5"),
    RuleData("Amana: Soul of the King - throne behind door, opens after defeating Vendrick", "Soul of a Giant x5"),
    # Shulva Sanctum City
    # Sinners Rise
    RuleData("SinnersRise: Fire Seed - locked upper left cell", "Bastille Key"),
    RuleData("SinnersRise: Smooth & Silky Stone - before boss, right side locked room", "Bastille Key"),
    # The Gutter
    # The Lost Bastille
    RuleData("Bastille: Soul Vessel - behind Pharros' contraption, Pharros/elevator room, chest", "Master Lockstone"),
    RuleData("Bastille: Petrified Dragon Bone - Straid's neighboring cell", "Bastille Key"),
    RuleData("Bastille: Firebomb x3 - Straid's neighboring cell", "Bastille Key"),
    RuleData("Bastille: Uchigatana - McDuff shop", "Dull Ember"),
    RuleData("Bastille: Bastard Sword - McDuff shop", "Dull Ember"),
    RuleData("Bastille: Greataxe - McDuff shop", "Dull Ember"),
    RuleData("Bastille: Winged Spear - McDuff shop", "Dull Ember"),
    RuleData("Bastille: Scythe - McDuff shop", "Dull Ember"),
    RuleData("Bastille: Long Bow - McDuff shop", "Dull Ember"),
    RuleData("Bastille: Light Crossbow - McDuff shop", "Dull Ember"),
    RuleData("Bastille: Royal Kite Shield - McDuff shop", "Dull Ember"),
    RuleData("Bastille: Repair Powder - McDuff shop", "Dull Ember"),
    RuleData("Bastille: Homing Soul Arrow - Straid shop", "Unpetrify Straid of Olaphis"),
    RuleData("Bastille: Resplendent Life - Straid shop", "Unpetrify Straid of Olaphis"),
    RuleData("Bastille: Great Lightning Spear - Straid of Olaphis after Crypt boss", "Unpetrify Straid of Olaphis"),
    RuleData("Bastille: Unveil - Straid shop", "Unpetrify Straid of Olaphis"),
    RuleData("Bastille: Sunlight Blade - Straid of Olaphis after Crypt boss", "Unpetrify Straid of Olaphis"),
    RuleData("Bastille: Lingering Flame - Straid shop", "Unpetrify Straid of Olaphis"),
    RuleData("Bastille: Flame Swathe - Straid shop", "Unpetrify Straid of Olaphis"),
    RuleData("Bastille: Dark Orb - Straid shop", "Unpetrify Straid of Olaphis"),
    RuleData("Bastille: Dark Hail - Straid shop", "Unpetrify Straid of Olaphis"),
    RuleData("Bastille: Dark Fog - Straid shop", "Unpetrify Straid of Olaphis"),
    RuleData("Bastille: Affinity - Straid shop", "Unpetrify Straid of Olaphis"),
    RuleData("Bastille: Strong Magic Shield - Straid shop", "Unpetrify Straid of Olaphis"),
    RuleData("Bastille: Cast Light - Straid shop", "Unpetrify Straid of Olaphis"),
    RuleData("Bastille: Ring of Knowledge - Straid shop", "Unpetrify Straid of Olaphis"),
    RuleData("Bastille: Lingering Dragoncrest Ring - Straid shop", "Unpetrify Straid of Olaphis"),
    RuleData("Bastille: Agape Ring - Straid shop", "Unpetrify Straid of Olaphis"),
    # The Pit
    # Things Betwixt
    RuleData("Betwixt: Estus Flask Shard - pit behind petrified statue", "Unpetrify Statue in Things Betwixt", version=DS2Version.SOTFS),
    RuleData("Betwixt: Twinkling Titanite - by coffin, enemy drop", "Unpetrify Statue in Things Betwixt", version=DS2Version.SOTFS),
    # Throne of Want
    RuleData("ThroneOfWant: Soul of Nashandra", "Giant's Kinship"),
    # Tseldora
    RuleData("ShadedWoods: Second Dragon Ring - Tark after killing last Tseldora boss", "Ring of Whispers"),
    RuleData("ShadedWoods: Black Scorpion Stinger - Tark after killing last Tseldora boss", "Ring of Whispers", version=DS2Version.SOTFS),
    RuleData("Tseldora: Rusted Coin x10 - Tseldora Den, trapped chest", "Tseldora Den Key"),
    RuleData("Tseldora: Engraved Gauntlets - Tseldora Den, metal chest", "Tseldora Den Key"),
    RuleData("Tseldora: Black Knight Ultra Greatsword - behind locked door, spider temple, metal chest", "Brightstone Key"),
    RuleData("Tseldora: Great Fireball - behind locked door, spider temple, metal chest", "Brightstone Key"),
    RuleData("Tseldora: Fire Seed - behind locked door, spider temple, metal chest", "Brightstone Key"),
    RuleData("Tseldora: Murakumo - Ornifex shop", "Fang Key"),
    RuleData("Tseldora: Twinblade - Ornifex shop", "Fang Key"),
    RuleData("Tseldora: Partizan - Ornifex shop", "Fang Key"),
    RuleData("Tseldora: Composite Bow - Ornifex shop", "Fang Key"),
    RuleData("Tseldora: Heavy Crossbow - Ornifex shop", "Fang Key"),
    RuleData("Tseldora: Homing Soul Arrow - Ornifex shop", "Fang Key"),
    RuleData("Tseldora: Homing Soulmass - Ornifex shop", "Fang Key"),
    RuleData("Tseldora: Fall Control - Ornifex shop", "Fang Key"),
    # Undead Crypt
    RuleData("Crypt: Darkdrift - Agdayne after King's Ring", "King's Ring"),
    RuleData("Crypt: Agdayne's Black Robe - Agdayne after King's Ring", "King's Ring"),
    RuleData("Crypt: Agdayne's Cuffs - Agdayne after King's Ring", "King's Ring"),
    RuleData("Crypt: Agdayne's Kilt - Agdayne after King's Ring", "King's Ring"),
    RuleData("Crypt: Olenford's Staff - Pharros contraption behind illusory wall, third graveyard room, metal chest", "Master Lockstone"),
    RuleData("Crypt: Great Lightning Spear - Pharros contraption behind illusory wall, third graveyard room, metal chest", "Master Lockstone"),
    # Undead Purgatory
    RuleData("Chariot: Crest of Blood - join Brotherhood of Blood", "Token of Spite"),
    RuleData("Chariot: Great Scythe - Gren shop", "Token of Spite"),
    RuleData("Chariot: Priest's Chime - Gren shop", "Token of Spite"),
    RuleData("Chariot: Executioner Helm - Gren shop after Shrine of Winter", "Token of Spite"),
    RuleData("Chariot: Executioner Helm - Gren shop after Shrine of Winter", "Open Shrine of Winter"),
    RuleData("Chariot: Executioner Armor - Gren shop after Shrine of Winter", "Token of Spite"),
    RuleData("Chariot: Executioner Armor - Gren shop after Shrine of Winter", "Open Shrine of Winter"),
    RuleData("Chariot: Executioner Gauntlets - Gren shop after Shrine of Winter", "Token of Spite"),
    RuleData("Chariot: Executioner Gauntlets - Gren shop after Shrine of Winter", "Open Shrine of Winter"),
    RuleData("Chariot: Executioner Leggings - Gren shop after Shrine of Winter", "Token of Spite"),
    RuleData("Chariot: Executioner Leggings - Gren shop after Shrine of Winter", "Open Shrine of Winter"),
    RuleData("Chariot: Firestorm - Gren shop", "Token of Spite"),
    RuleData("Chariot: Great Combustion - Gren shop", "Token of Spite"),
    RuleData("Chariot: Fire Whip - Gren shop", "Token of Spite"),
    RuleData("Chariot: Delicate String - Gren shop", "Token of Spite"),
    RuleData("Chariot: Red Sign Soapstone - Gren shop", "Token of Spite"),
    # Undefined
]
