from enum import Enum
from dataclasses import dataclass
from BaseClasses import ItemClassification


class DS2Version(Enum):
    SOTFS = "sotfs"
    VANILLA = "vanilla"


class APLocationType(Enum):
    ItemLotParam2_Chr = 100_000_000
    ItemLotParam2_Other = 200_000_000
    ShopLineupParam = 300_000_000


class APItemType(Enum):
    ITEM = 1
    EVENT = 2
    TRAP = 3


class ItemCategory(Enum):
    MELEE_WEAPON = "Melee Weapons"
    RANGED_WEAPON = "Ranged Weapons"
    MISC_WEAPON = "Misc Weapons"
    STAFF = "Staves"
    CHIME = "Chimes"
    SHIELD = "Shields"
    HEAD_ARMOR = "Head Armor"
    CHEST_ARMOR = "Chest Armor"
    HANDS_ARMOR = "Hands Armor"
    LEGS_ARMOR = "Legs Armor"
    RING = "Rings"
    ARROW = "Arrows"
    GREAT_ARROW = "Great Arrows"
    BOLT = "Bolts"
    SPELL = "Spells"
    UNIQUE = "Unique Items"
    GOOD = "Goods"
    FLASK_UPGRADE = "Flask Upgrades"
    BOSS_SOUL = "Boss Souls"
    SOUL = "Souls"
    GESTURE = "Gestures"
    STATUE = "Statues"
    UPGRADE_MATERIAL = "Upgrade Materials"
    TRAP = "Trap"


class DLC(Enum):
    SUNKEN_KING = 1
    OLD_IRON_KING = 2
    IVORY_KING = 3
    ALL = 4

# moved ItemData into here to avoid circular import
# TrapData needs ItemData and items.py needs ItemData and the trap_list
@dataclass
class ItemData:
    code: int
    """The Archipelago code for this item."""

    name: str
    """The Archipelago name for this item."""

    category: ItemCategory
    """The category that this item is part of."""

    item_type: APItemType
    """TODO"""

    classification: ItemClassification = ItemClassification.filler
    """How important this item is to the game progression."""

    version: DS2Version | None = None
    """The version that this item is part of."""

    skip: bool = False
    """Whether to omit this item from randomization and replace it with other items."""

    exclude: bool = False
    """This item exists in the original game but is excluded from the multiworld item pool."""
    # TODO explain why this is needed instead of just removing the item aka cause the item is still in the location name

    bundle: bool = False
    """
    Whether this item comes in a quantity greater than one.
    
    The item's quantity is added to its code. For example, an item with 
    code 1000 and a quantity of 5 would be represented as 1005.
    """

    max_reinforcement: int = 0
    """The max reinforcement level for this item."""

    reinforcement: int = 0
    """The reinforcement level for this item."""

@dataclass
class TrapData(ItemData):
    category: ItemCategory = ItemCategory.TRAP
    """The category that this item is part of."""

    classification: ItemClassification = ItemClassification.trap
    """How important this item is to the game progression."""

    item_type: APItemType = APItemType.TRAP
    """Item type identifier."""
    
    max_count: int = 100
    """Maximum number of copies of this trap allowed in the pool."""