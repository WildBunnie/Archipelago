import unittest

from test.general import setup_multiworld

from .. import DarkSouls2World
from ..items import item_dictionary, item_list


GAME_SEED = 8675309
PLUS_FIVE_ITEM = "Blue Dagger"
PLUS_TEN_ITEM = "Dagger"
ORIGINAL_REINFORCEMENTS = tuple(item.reinforcement for item in item_list)

REINFORCED_OPTIONS = {
    "randomize_equipment_level_percentage": 100,
    "min_equipment_reinforcement_in_5": 5,
    "max_equipment_reinforcement_in_5": 5,
    "min_equipment_reinforcement_in_10": 10,
    "max_equipment_reinforcement_in_10": 10,
}
PLAIN_OPTIONS = {
    "randomize_equipment_level_percentage": 0,
}


class _RandintRecorder:
    def __init__(self, delegate):
        self.delegate = delegate
        self.calls = []

    def randint(self, lower, upper):
        self.calls.append((lower, upper))
        return self.delegate.randint(lower, upper)


class TestReinforcementIsolation(unittest.TestCase):
    def setUp(self) -> None:
        self.addCleanup(self._restore_module_reinforcements)
        self._assert_module_reinforcements_unchanged()

    @staticmethod
    def _restore_module_reinforcements() -> None:
        for item, reinforcement in zip(item_list, ORIGINAL_REINFORCEMENTS):
            item.reinforcement = reinforcement

    @staticmethod
    def _module_reinforcements():
        return tuple(item.reinforcement for item in item_list)

    def _assert_module_reinforcements_unchanged(self) -> None:
        self.assertEqual(ORIGINAL_REINFORCEMENTS, self._module_reinforcements())

    @staticmethod
    def _make_worlds(reinforced_player: int = 1):
        options = (
            [REINFORCED_OPTIONS, PLAIN_OPTIONS]
            if reinforced_player == 1
            else [PLAIN_OPTIONS, REINFORCED_OPTIONS]
        )
        multiworld = setup_multiworld(
            [DarkSouls2World, DarkSouls2World],
            steps=(),
            seed=GAME_SEED,
            options=options,
        )
        reinforced_world = multiworld.worlds[reinforced_player]
        plain_world = multiworld.worlds[3 - reinforced_player]
        return reinforced_world, plain_world

    @staticmethod
    def _item_data_by_id(world: DarkSouls2World):
        return {
            item["item_id"]: item
            for item in world.fill_slot_data()["item_data"]
        }

    def test_players_and_slot_data_are_isolated_in_both_orders(self) -> None:
        for reinforced_player in (1, 2):
            for reinforced_slot_data_first in (True, False):
                with self.subTest(
                    reinforced_player=reinforced_player,
                    reinforced_slot_data_first=reinforced_slot_data_first,
                ):
                    reinforced_world, plain_world = self._make_worlds(reinforced_player)
                    creation_order = (
                        (reinforced_world, plain_world)
                        if reinforced_player == 1
                        else (plain_world, reinforced_world)
                    )
                    created_items = {}
                    for world in creation_order:
                        created_items[(world.player, PLUS_FIVE_ITEM)] = world.create_item(PLUS_FIVE_ITEM)
                        self._assert_module_reinforcements_unchanged()
                        created_items[(world.player, PLUS_TEN_ITEM)] = world.create_item(PLUS_TEN_ITEM)
                        self._assert_module_reinforcements_unchanged()

                    repeated = reinforced_world.create_item(PLUS_TEN_ITEM)
                    self._assert_module_reinforcements_unchanged()
                    self.assertIs(
                        created_items[(reinforced_world.player, PLUS_TEN_ITEM)].data,
                        repeated.data,
                    )
                    self.assertIsNot(
                        reinforced_world._item_dictionary[PLUS_TEN_ITEM],
                        plain_world._item_dictionary[PLUS_TEN_ITEM],
                    )
                    self.assertIsNot(
                        reinforced_world._item_dictionary[PLUS_TEN_ITEM],
                        item_dictionary[PLUS_TEN_ITEM],
                    )

                    slot_order = (
                        (reinforced_world, plain_world)
                        if reinforced_slot_data_first
                        else (plain_world, reinforced_world)
                    )
                    slot_data = {}
                    for world in slot_order:
                        slot_data[world.player] = self._item_data_by_id(world)
                        self._assert_module_reinforcements_unchanged()

                    plus_five_code = item_dictionary[PLUS_FIVE_ITEM].code
                    plus_ten_code = item_dictionary[PLUS_TEN_ITEM].code
                    self.assertEqual(
                        5,
                        slot_data[reinforced_world.player][plus_five_code]["reinforcement"],
                    )
                    self.assertEqual(
                        10,
                        slot_data[reinforced_world.player][plus_ten_code]["reinforcement"],
                    )
                    self.assertEqual(
                        0,
                        slot_data[plain_world.player][plus_five_code]["reinforcement"],
                    )
                    self.assertEqual(
                        0,
                        slot_data[plain_world.player][plus_ten_code]["reinforcement"],
                    )

    def test_same_seed_item_data_is_reproducible_in_one_process(self) -> None:
        payloads = []
        for _ in range(2):
            multiworld = setup_multiworld(
                DarkSouls2World,
                steps=(),
                seed=GAME_SEED,
                options=REINFORCED_OPTIONS,
            )
            world = multiworld.worlds[1]
            world.create_item(PLUS_FIVE_ITEM)
            self._assert_module_reinforcements_unchanged()
            world.create_item(PLUS_TEN_ITEM)
            self._assert_module_reinforcements_unchanged()
            payloads.append(world.fill_slot_data()["item_data"])
            self._assert_module_reinforcements_unchanged()

        self.assertEqual(payloads[0], payloads[1])

    def test_reinforcement_rng_calls_are_unchanged(self) -> None:
        reinforced_world, plain_world = self._make_worlds()
        reinforced_recorder = _RandintRecorder(reinforced_world.random)
        plain_recorder = _RandintRecorder(plain_world.random)
        reinforced_world.random = reinforced_recorder
        plain_world.random = plain_recorder

        reinforced_world.create_item(PLUS_FIVE_ITEM)
        self._assert_module_reinforcements_unchanged()
        reinforced_world.create_item(PLUS_TEN_ITEM)
        self._assert_module_reinforcements_unchanged()
        plain_world.create_item(PLUS_FIVE_ITEM)
        self._assert_module_reinforcements_unchanged()
        plain_world.create_item(PLUS_TEN_ITEM)
        self._assert_module_reinforcements_unchanged()

        self.assertEqual(
            [(0, 99), (5, 5), (0, 99), (10, 10)],
            reinforced_recorder.calls,
        )
        self.assertEqual([(0, 99), (0, 99)], plain_recorder.calls)

    def test_item_data_schema_and_order_are_unchanged(self) -> None:
        _, plain_world = self._make_worlds()
        serialized = plain_world.fill_slot_data()["item_data"]
        self._assert_module_reinforcements_unchanged()

        self.assertEqual([item.code for item in item_list], [item["item_id"] for item in serialized])
        self.assertEqual(len(item_list), len(serialized))
        for item in serialized:
            self.assertEqual(
                {"item_id", "item_type", "is_bundle", "reinforcement"},
                set(item),
            )


if __name__ == "__main__":
    unittest.main()
