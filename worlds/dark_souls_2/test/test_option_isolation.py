import unittest

from test.general import setup_multiworld

from .. import DarkSouls2World
from ..locations import locations_to_keep_unrandomized


INFINITE_LIFEGEM_LOCATION_KEY = 375400601
ORIGINAL_KEEP_UNRANDOMIZED = frozenset(locations_to_keep_unrandomized)


class TestInfiniteLifegemOptionIsolation(unittest.TestCase):
    def setUp(self) -> None:
        # Keep an expected failure against the old implementation from contaminating later tests.
        self.addCleanup(self._restore_keep_unrandomized)
        self.assertEqual(ORIGINAL_KEEP_UNRANDOMIZED, frozenset(locations_to_keep_unrandomized))
        self.assertNotIn(INFINITE_LIFEGEM_LOCATION_KEY, ORIGINAL_KEEP_UNRANDOMIZED)

    @staticmethod
    def _restore_keep_unrandomized() -> None:
        locations_to_keep_unrandomized.clear()
        locations_to_keep_unrandomized.update(ORIGINAL_KEEP_UNRANDOMIZED)

    @staticmethod
    def _make_worlds(*infinite_lifegems_values: bool):
        multiworld = setup_multiworld(
            [DarkSouls2World] * len(infinite_lifegems_values),
            steps=(),
            options=[
                {"infinite_lifegems": value}
                for value in infinite_lifegems_values
            ],
        )
        return tuple(multiworld.worlds[player] for player in multiworld.player_ids)

    @staticmethod
    def _fill_slot_data(world: DarkSouls2World):
        slot_data = world.fill_slot_data()
        preserved_location_keys = frozenset(
            location["location_key"]
            for location in slot_data["location_data"]
            if location.get("keep_unrandomized") is True
        )
        baseline_after_call = frozenset(locations_to_keep_unrandomized)
        return preserved_location_keys, baseline_after_call

    def test_enabled_output_contains_key_without_mutating_baseline(self) -> None:
        world, = self._make_worlds(True)

        preserved_keys, baseline_after_call = self._fill_slot_data(world)

        self.assertIn(INFINITE_LIFEGEM_LOCATION_KEY, preserved_keys)
        self.assertEqual(ORIGINAL_KEEP_UNRANDOMIZED, baseline_after_call)

    def test_disabled_output_omits_key_without_mutating_baseline(self) -> None:
        world, = self._make_worlds(False)

        preserved_keys, baseline_after_call = self._fill_slot_data(world)

        self.assertNotIn(INFINITE_LIFEGEM_LOCATION_KEY, preserved_keys)
        self.assertEqual(ORIGINAL_KEEP_UNRANDOMIZED, baseline_after_call)

    def test_enabled_then_disabled_does_not_leak(self) -> None:
        enabled_world, = self._make_worlds(True)
        enabled_keys, baseline_after_enabled = self._fill_slot_data(enabled_world)
        disabled_world, = self._make_worlds(False)
        disabled_keys, baseline_after_disabled = self._fill_slot_data(disabled_world)

        self.assertIn(INFINITE_LIFEGEM_LOCATION_KEY, enabled_keys)
        self.assertNotIn(INFINITE_LIFEGEM_LOCATION_KEY, disabled_keys)
        self.assertEqual(ORIGINAL_KEEP_UNRANDOMIZED, baseline_after_enabled)
        self.assertEqual(ORIGINAL_KEEP_UNRANDOMIZED, baseline_after_disabled)

    def test_disabled_then_enabled_does_not_mutate_baseline(self) -> None:
        disabled_world, = self._make_worlds(False)
        disabled_keys, baseline_after_disabled = self._fill_slot_data(disabled_world)
        enabled_world, = self._make_worlds(True)
        enabled_keys, baseline_after_enabled = self._fill_slot_data(enabled_world)

        self.assertNotIn(INFINITE_LIFEGEM_LOCATION_KEY, disabled_keys)
        self.assertIn(INFINITE_LIFEGEM_LOCATION_KEY, enabled_keys)
        self.assertEqual(ORIGINAL_KEEP_UNRANDOMIZED, baseline_after_disabled)
        self.assertEqual(ORIGINAL_KEEP_UNRANDOMIZED, baseline_after_enabled)

    def test_opposite_valued_players_are_isolated(self) -> None:
        enabled_world, disabled_world = self._make_worlds(True, False)
        enabled_keys, baseline_after_enabled = self._fill_slot_data(enabled_world)
        disabled_keys, baseline_after_disabled = self._fill_slot_data(disabled_world)

        self.assertIn(INFINITE_LIFEGEM_LOCATION_KEY, enabled_keys)
        self.assertNotIn(INFINITE_LIFEGEM_LOCATION_KEY, disabled_keys)
        self.assertEqual(ORIGINAL_KEEP_UNRANDOMIZED, baseline_after_enabled)
        self.assertEqual(ORIGINAL_KEEP_UNRANDOMIZED, baseline_after_disabled)
