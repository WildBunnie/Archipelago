from BaseClasses import ItemClassification
from .enums import APItemType, ItemCategory, TrapData

trap_list: list[TrapData] = [
    TrapData(90000000, "Poison Trap", item_type=APItemType.TRAP, classification=ItemClassification.trap, category=ItemCategory.TRAP), # 900100
    TrapData(90000100, "Bleeding Trap" , item_type=APItemType.TRAP, classification=ItemClassification.trap, category=ItemCategory.TRAP), # 900200, 900210
    TrapData(90000200, "Curse Trap" , item_type=APItemType.TRAP, classification=ItemClassification.trap, category=ItemCategory.TRAP), # 900400
    TrapData(90000300, "Fire & Knockdown Trap" , item_type=APItemType.TRAP, classification=ItemClassification.trap, category=ItemCategory.TRAP), # 900500
    TrapData(90000400, "Toxic Trap" , item_type=APItemType.TRAP, classification=ItemClassification.trap, category=ItemCategory.TRAP), # 900600
    TrapData(90000500, "Petrification Trap" , item_type=APItemType.TRAP, classification=ItemClassification.trap, category=ItemCategory.TRAP), # 901100, 901110
    TrapData(90000600, "Slight Corrosion Trap" , item_type=APItemType.TRAP, classification=ItemClassification.trap, category=ItemCategory.TRAP), # 120000310, 140001000, 140001010
    TrapData(90000700, "Medium Corrosion Trap" , item_type=APItemType.TRAP, classification=ItemClassification.trap, category=ItemCategory.TRAP), # 120000310, 140001000, 140001010
    TrapData(90000800, "Heavy Corrosion Trap" , item_type=APItemType.TRAP, classification=ItemClassification.trap, category=ItemCategory.TRAP), # 120000310, 140001000, 140001010
    TrapData(90000900, "Hello Carving Trap" , item_type=APItemType.TRAP, classification=ItemClassification.trap, category=ItemCategory.TRAP), # 60470000
    TrapData(90001000, "Thank You Carving Trap" , item_type=APItemType.TRAP, classification=ItemClassification.trap, category=ItemCategory.TRAP), # 60480000
    TrapData(90001100, "Sorry Carving Trap" , item_type=APItemType.TRAP, classification=ItemClassification.trap, category=ItemCategory.TRAP), # 60490000
    TrapData(90001200, "Very Good Carving Trap" , item_type=APItemType.TRAP, classification=ItemClassification.trap, category=ItemCategory.TRAP), # 60500000
    TrapData(90001300, "Immolation Trap" , item_type=APItemType.TRAP, classification=ItemClassification.trap, category=ItemCategory.TRAP), # 33210000, 33210005, 33210010
    TrapData(90001400, "Firebomb Trap" , item_type=APItemType.TRAP, classification=ItemClassification.trap, category=ItemCategory.TRAP), # 60570000
    TrapData(90001500, "Black Firebomb Trap" , item_type=APItemType.TRAP, classification=ItemClassification.trap, category=ItemCategory.TRAP), # 60575000
]

TRAP_PRESETS = {
    "none": {
        "Poison Trap": 0,
        "Bleeding Trap": 0,
        "Curse Trap": 0,
        "Fire & Knockdown Trap": 0,
        "Toxic Trap": 0,
        "Petrification Trap": 0,
        "Slight Corrosion Trap": 0,
        "Medium Corrosion Trap": 0,
        "Heavy Corrosion Trap": 0,
        "Hello Carving Trap": 0,
        "Thank You Carving Trap": 0,
        "Sorry Carving Trap": 0,
        "Very Good Carving Trap": 0,
        "Immolation Trap": 0,
        "Firebomb Trap": 0,
        "Black Firebomb Trap": 0,
    },
    "easy": {
        "Poison Trap": 1,
        "Bleeding Trap": 2,
        "Curse Trap": 2,
        "Fire & Knockdown Trap": 1,
        "Toxic Trap": 0,
        "Petrification Trap": 0,
        "Slight Corrosion Trap": 0,
        "Medium Corrosion Trap": 0,
        "Heavy Corrosion Trap": 0,
        "Hello Carving Trap": 2,
        "Thank You Carving Trap": 2,
        "Sorry Carving Trap": 2,
        "Very Good Carving Trap": 2,
        "Immolation Trap": 0,
        "Firebomb Trap": 0,
        "Black Firebomb Trap": 0,
    },
    "medium": {
        "Poison Trap": 2,
        "Bleeding Trap": 2,
        "Curse Trap": 2,
        "Fire & Knockdown Trap": 2,
        "Toxic Trap": 2,
        "Petrification Trap": 1,
        "Slight Corrosion Trap": 1,
        "Medium Corrosion Trap": 1,
        "Heavy Corrosion Trap": 0,
        "Hello Carving Trap": 2,
        "Thank You Carving Trap": 2,
        "Sorry Carving Trap": 2,
        "Very Good Carving Trap": 2,
        "Immolation Trap": 1,
        "Firebomb Trap": 1,
        "Black Firebomb Trap": 1,
    },
    "hard": {
        "Poison Trap": 4,
        "Bleeding Trap": 4,
        "Curse Trap": 4,
        "Fire & Knockdown Trap": 4,
        "Toxic Trap": 4,
        "Petrification Trap": 4,
        "Slight Corrosion Trap": 2,
        "Medium Corrosion Trap": 2,
        "Heavy Corrosion Trap": 1,
        "Hello Carving Trap": 1,
        "Thank You Carving Trap": 1,
        "Sorry Carving Trap": 1,
        "Very Good Carving Trap": 1,
        "Immolation Trap": 2,
        "Firebomb Trap": 2,
        "Black Firebomb Trap": 2,
    },
    "good_luck": {
        "Poison Trap": 4,
        "Bleeding Trap": 4,
        "Curse Trap": 4,
        "Fire & Knockdown Trap": 4,
        "Toxic Trap": 6,
        "Petrification Trap": 6,
        "Slight Corrosion Trap": 4,
        "Medium Corrosion Trap": 4,
        "Heavy Corrosion Trap": 4,
        "Hello Carving Trap": 0,
        "Thank You Carving Trap": 0,
        "Sorry Carving Trap": 0,
        "Very Good Carving Trap": 0,
        "Immolation Trap": 5,
        "Firebomb Trap": 5,
        "Black Firebomb Trap": 5,
    },
}