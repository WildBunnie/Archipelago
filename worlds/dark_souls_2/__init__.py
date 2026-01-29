from typing import Any, List, Mapping

from BaseClasses import (Item, ItemClassification, Location,
                         LocationProgressType, Region, Tutorial)
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_rule, set_rule

from .enums import DLC, DS2Version, ItemCategory
from .options import DarkSouls2Options, option_groups
from .locations import LocationData, locations_by_region, regions_by_location
from .items import ItemData, item_dictionary, item_list
from .regions import region_dictionary, region_list
from .rules import connection_rules, location_rules


class DS2Location(Location):
    game: str = "Dark Souls II"
    data: LocationData

    def __init__(self, player, name, address, parent, data):
        self.data = data
        super(DS2Location, self).__init__(
            player, name, address, parent
        )


class DS2Item(Item):
    game: str = "Dark Souls II"
    data: ItemData

    def __init__(self, name, classification, code, player, data):
        self.data = data
        super(DS2Item, self).__init__(
            name, classification, code, player
        )


class DarkSouls2Web(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Dark Souls II randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["WildBunnie"]
    )
    # setup_pt = Tutorial()  # TODO

    options_page = True  # TODO look into this
    game_info_languages = ['en']  # , 'pt']
    tutorials = [setup_en]
    theme = "ice"
    bug_report_page = "https://github.com/WildBunnie/DarkSoulsII-Archipelago/issues"
    options_presets = {}  # TODO
    option_groups = option_groups
    rich_text_options_doc = True
    location_descriptions = {}  # TODO
    item_descriptions = {}  # TODO


class DarkSouls2World(World):
    """
    PeakSouls2
    """
    game = "Dark Souls II"

    web = DarkSouls2Web()

    options_dataclass = DarkSouls2Options
    options: DarkSouls2Options

    item_name_to_id = {
        item_data.name: item_data.code
        for item_data in item_list
        if not item_data.exclude
    }

    location_name_to_id = {
        location_data.name: location_data.address
        for locations in locations_by_region.values()
        for location_data in locations
        if location_data.address != None
    }

    item_name_groups = {}
    location_name_groups = {}

    def _is_dlc_enabled(self, dlc: DLC) -> bool:
        if dlc == DLC.SUNKEN_KING and not self.options.sunken_king_dlc:
            return False
        if dlc == DLC.OLD_IRON_KING and not self.options.old_iron_king_dlc:
            return False
        if dlc == DLC.IVORY_KING and not self.options.ivory_king_dlc:
            return False
        return True

    def _is_version_selected(self, version: DS2Version) -> bool:
        if version == DS2Version.SOTFS and self.options.game_version != "sotfs":
            return False
        if version == DS2Version.VANILLA and self.options.game_version != "vanilla":
            return False
        return True

    def generate_early(self) -> None:
        pass

    def create_regions(self) -> None:
        region_lookup: dict[str, Region] = {}

        # create regions and locations
        for region_data in region_list:
            if not self._is_dlc_enabled(region_data.dlc):
                continue
            region = Region(region_data.name, self.player, self.multiworld)

            for location_data in locations_by_region[region_data.name]:
                if not self._is_version_selected(location_data.version):
                    continue
                # TODO check if user chose to remove this

                if location_data.is_event:
                    region.add_event(location_data.name)
                    continue

                location = DS2Location(
                    self.player,
                    location_data.name,
                    location_data.address,
                    region,
                    location_data,
                )

                if location_data.missable:
                    location.progress_type = LocationProgressType.EXCLUDED
                region.locations.append(location)

            self.multiworld.regions.append(region)
            region_lookup[region_data.name] = region

        # setup connections
        for region_data in region_list:
            if region_data.name not in region_lookup:
                continue
            region = region_lookup[region_data.name]
            for connection in region_data.connections:
                if connection not in region_lookup:
                    continue
                region.connect(region_lookup[connection])

        # TODO more win conditions
        victory_region = region_lookup["Throne of Want"]
        victory_loc = Location(
            self.player, "Defeat Nashandra", None, victory_region)
        victory_region.locations.append(victory_loc)

        victory_loc.place_locked_item(
            Item("Victory", ItemClassification.progression, None, self.player))
        set_rule(victory_loc, lambda state: state.can_reach_location(
            "ThroneOfWant: Soul of Nashandra", self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has(
            "Victory", self.player)

    # i don't love how this is done but i cannot come up with something better
    # TODO maybe dont allow dlc items
    def create_items(self) -> None:
        item_pool: List[DS2Item] = []
        items_added: List[str] = []

        locations_to_fill: List[DS2Location] = self.multiworld.get_unfilled_locations(
            self.player)
        max_pool_size = len(locations_to_fill)

        # Add original items from locations
        for location in locations_to_fill:
            item_data = item_dictionary[location.data.original_item_name]

            if location.data.keep_original_item:
                location.place_locked_item(self.create_item(
                    location.data.original_item_name))
                items_added.append(location.data.original_item_name)
                max_pool_size -= 1
                continue

            if item_data.skip or item_data.exclude:
                continue

            if item_data.category == ItemCategory.UNIQUE and item_data.name in items_added:
                continue

            items_added.append(item_data.name)
            item_pool.append(self.create_item(item_data.name))

        # Add missing progression items

        # We do this now instead of before the previous step because
        # if we did it before we would get two of any progression item
        # that isn't unique, which is not something we really want
        missing_progression_items = [
            item.name for item in item_list
            if item.name not in items_added
            and item.classification == ItemClassification.progression
        ]

        assert len(item_pool) + len(
            missing_progression_items) <= max_pool_size, "Item pool cannot fit all dark souls 2 progression items"

        for progression_item in missing_progression_items:
            item_pool.append(self.create_item(progression_item))

        # Fill remaining slots with filler items
        for _ in range(max_pool_size - len(item_pool)):
            item_pool.append(self.create_item(self.get_filler_item_name()))

        assert len(item_pool) == max_pool_size

        self.multiworld.itempool.extend(item_pool)

    def set_rules(self) -> None:
        for connection_rule_data in connection_rules:
            _from, _to = connection_rule_data.spot.split(" -> ")
            from_region = region_dictionary[_from]
            to_region = region_dictionary[_to]

            if not self._is_dlc_enabled(from_region.dlc):
                continue
            if not self._is_dlc_enabled(to_region.dlc):
                continue
            if not self._is_version_selected(connection_rule_data.version):
                continue

            add_rule(
                self.multiworld.get_entrance(
                    connection_rule_data.spot, self.player),
                connection_rule_data.to_collection_rule(self.player)
            )

        for location_rule_data in location_rules:
            region_name = regions_by_location[location_rule_data.spot]
            region_data = region_dictionary[region_name]

            if not self._is_dlc_enabled(region_data.dlc):
                continue
            if not self._is_version_selected(location_rule_data.version):
                continue

            add_rule(
                self.multiworld.get_location(
                    location_rule_data.spot, self.player),
                location_rule_data.to_collection_rule(self.player)
            )

    def create_item(self, name: str) -> DS2Item:
        item_data: ItemData = item_dictionary[name]
        return DS2Item(name, item_data.classification, item_data.code, self.player, item_data)

    def get_filler_item_name(self) -> str:
        filler_items = {
            item.name for item in item_list
            if item.category != ItemCategory.UNIQUE
            and not item.skip
            and not item.exclude
            and not item.version == DS2Version.SOTFS
        }
        return self.random.choice(tuple(filler_items))

    # TODO review
    def fill_slot_data(self) -> Mapping[str, Any]:
        slot_data = self.options.as_dict(
            # "death_link",
            "game_version",
            # "no_weapon_req",
            # "no_spell_req",
            # "no_armor_req",
            # "no_equip_load",
            # "randomize_starting_loadout",
            # "starting_weapon_requirement",
            # "autoequip"
        )

        # non archipelago locations that should not be randomized by the static randomizer
        keep_unrandomized = set()

        # [Event - Giant Memories] Soul of a Giant
        keep_unrandomized.add(260004000)

        # [Merchant Hag Melentia - Majula] Lifegem
        # if self.options.infinite_lifegems:
        #     keep_unrandomized.add(375400601)

        # straid trades
        keep_unrandomized.update([
            376801000, 376801001, 376801002, 376801003, 376801004, 376801005,
            376801006, 376801007, 376801008, 376801009, 376801010, 376801011,
            376801012, 376801013, 376801014, 376801015, 376801016, 376801017,
            376801100, 376801101, 376801102, 376801103, 376801104, 376801105,
            376801106, 376801107, 376801108, 376801109, 376801110, 376801111,
            376801200, 376801201, 376801202, 376801203, 376801204, 376801205,
            376801206, 376801207, 376801208, 376801209, 376801210, 376801211,
            376801212, 376801213, 376801214, 376801215, 376801216, 376801217,
            376801300, 376801301, 376801302, 376801303, 376801304, 376801305,
            376801306
        ])

        # ornifex trades
        keep_unrandomized.update([
            377601000, 377601001, 377601002, 377601003, 377601004, 377601005, 377601006, 377601007,
            377601008, 377601009, 377601010, 377601011, 377601012, 377601013, 377601014, 377601015,
            377601016, 377601017, 377601018, 377601019, 377601020, 377601021, 377601022, 377601023,
            377601024, 377601025, 377601026, 377601027, 377601028, 377601029, 377601030, 377601031,
            377601032, 377601033, 377601034, 377601035, 377601036, 377601037, 377601100, 377601101,
            377601102, 377601103, 377601104, 377601105, 377601106, 377601107, 377601108, 377601109,
            377601110, 377601111, 377601112, 377601113, 377601114, 377601115, 377601116, 377601117,
            377601118, 377601119, 377601120, 377601121, 377602000, 377602001, 377602002, 377602003,
            377602004, 377602005, 377602006, 377602007, 377602008, 377602009, 377602010, 377602011,
            377602012, 377602013, 377602014, 377602015, 377602016, 377602017, 377602018, 377602019,
            377602020, 377602021, 377602022, 377602023, 377602024, 377602025, 377602026, 377602027,
            377602028, 377602029, 377602030, 377602031, 377602032, 377602033, 377602034, 377602035,
            377602036, 377602037, 377602100, 377602101, 377602102, 377602103, 377602104, 377602105,
            377602106, 377602107, 377602108, 377602109, 377602110, 377602111, 377602112, 377602113,
            377602114, 377602115, 377602116, 377602117, 377602118, 377602119, 377602120, 377602121
        ])

        # bird trades
        keep_unrandomized.update([
            250000000, 250000001, 250000002, 250000100,
            250000101, 250000102, 250000202, 250000303
        ])

        # new game plus
        keep_unrandomized.update([
            101040500, 101190001, 101193000, 102210501, 102210601, 102210602, 102213001, 184700000,
            184710000, 200154001, 200309701, 200324001, 200326001, 200332001, 200333001, 200501001,
            200503001, 200504001, 200603001, 200607001, 200619101, 200626001, 200675010, 200862001,
            210026001, 210026031, 210045001, 210045002, 210105021, 210105041, 210106061, 210106321,
            210106371, 210145061, 210146051, 210146181, 210146381, 210156031, 210156161, 210165041,
            210166191, 210166421, 210166441, 210175021, 210176171, 210176221, 210176231, 210176461,
            210185001, 210185071, 210185081, 210186021, 210186071, 210195001, 210196111, 210196211,
            210236021, 210236071, 210236131, 210275021, 210276041, 210276061, 210315001, 210316041,
            210316101, 210325001, 210326081, 210326101, 210326141, 210326191, 210335021, 210335031,
            210336011, 210336041, 210346031, 210346091, 220105001, 220106011, 220106061, 220106111,
            220106141, 220115051, 220116011, 220116171, 220215011, 220215021, 220215041, 220216021,
            220216061, 220246011, 220246111, 220246121, 220246151, 260008110, 260044001, 372110007,
            372110008, 372110105, 372110300, 372110301, 372110302, 376100259, 376100260, 376100261,
            376100262, 377200208, 377200209, 377200210, 377200211, 378300603, 378500603
        ])

        # maughlin restocks
        keep_unrandomized.update(
            [376100219, 376100220, 376100221, 376100222, 376100223, 376100224, 376100225, 376100226])

        archipelago_ids_to_location_key = {}
        location_key_to_archipelago_ids = {}
        for locations in locations_by_region.values():
            for location_data in locations:
                if location_data.is_event:
                    continue
                unique_id = location_data.ds2_id + \
                    location_data.location_type.value  # TODO support events

                # archipelago to location id
                archipelago_ids_to_location_key[location_data.address] = unique_id

                # location to archipelago id
                if unique_id not in location_key_to_archipelago_ids:
                    location_key_to_archipelago_ids[unique_id] = [
                        location_data.address]
                else:
                    location_key_to_archipelago_ids[unique_id].append(
                        location_data.address)

        item_bundles = set()
        reinforcements = {}
        for item in item_list:
            if item.bundle:
                item_bundles.add(item.code)
            if item.reinforcement != 0:
                reinforcements[item.code] = item.reinforcement

        slot_data["archipelago_id_to_location_key"] = archipelago_ids_to_location_key
        slot_data["location_key_to_archipelago_ids"] = location_key_to_archipelago_ids
        slot_data["keep_unrandomized"] = keep_unrandomized
        slot_data["item_bundles"] = item_bundles
        slot_data["reinforcements"] = reinforcements

        return slot_data
