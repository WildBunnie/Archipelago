from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Toggle


class GameVersion(Choice):
    """Set the game version you will be playing on

    - **sotfs:** You will be playing the Scholar of the First Sin version
    - **vanilla:** You will be playing the Vanilla version"""
    display_name = "Game Version"
    option_sotfs = 0
    option_vanilla = 1
    default = 0


class OldIronKingDLC(Toggle):
    """Enable Crown of the Old Iron King DLC."""
    display_name = "Enable Crown of the Old Iron King DLC"


class IvoryKingDLC(Toggle):
    """Enable Crown of the Ivory King DLC."""
    display_name = "Enable Crown of the Ivory King DLC"


class SunkenKingDLC(Toggle):
    """Enable Crown of the Sunken King DLC."""
    display_name = "Enable Crown of the Sunken King DLC"


# TODO
option_groups = [
    OptionGroup("Game Options", [
        GameVersion,
        SunkenKingDLC,
        OldIronKingDLC,
        IvoryKingDLC
    ]),
]


@dataclass
class DarkSouls2Options(PerGameCommonOptions):
    game_version: GameVersion
    sunken_king_dlc: SunkenKingDLC
    old_iron_king_dlc: OldIronKingDLC
    ivory_king_dlc: IvoryKingDLC
