import unittest

from BaseClasses import ItemClassification
from test.general import setup_multiworld

from .. import DarkSouls2World
from ..enums import DS2Version, ItemCategory
from ..items import ItemData, item_list


GAME_SEED = 8675309
SELECTION_COUNT = 64


class _ChoiceRecorder:
    def __init__(self, delegate):
        self.delegate = delegate
        self.populations = []

    def choice(self, population):
        snapshot = tuple(population)
        self.populations.append(snapshot)
        return self.delegate.choice(snapshot)


class TestFillerSelection(unittest.TestCase):
    @staticmethod
    def _make_world(game_version: str, seed: int = GAME_SEED) -> DarkSouls2World:
        multiworld = setup_multiworld(
            DarkSouls2World,
            steps=(),
            seed=seed,
            options={"game_version": game_version},
        )
        return multiworld.worlds[1]

    @staticmethod
    def _eligible_versions_by_name():
        versions_by_name = {}
        for item in item_list:
            if (
                item.category == ItemCategory.UNIQUE
                or item.classification != ItemClassification.filler
                or item.skip
                or item.exclude
            ):
                continue
            versions_by_name.setdefault(item.name, set()).add(item.version)
        return versions_by_name

    def _record_selection_sequence(self, world: DarkSouls2World, count: int):
        original_random = world.random
        recorder = _ChoiceRecorder(original_random)
        world.random = recorder
        try:
            selections = tuple(world.get_filler_item_name() for _ in range(count))
        finally:
            world.random = original_random

        self.assertEqual(count, len(recorder.populations))
        return selections, tuple(recorder.populations)

    def test_production_candidates_are_version_correct_sorted_and_stable(self) -> None:
        versions_by_name = self._eligible_versions_by_name()
        neutral_names = {
            name for name, versions in versions_by_name.items()
            if None in versions
        }
        self.assertTrue(neutral_names)

        for game_version, selected_version, opposite_version in (
            ("sotfs", DS2Version.SOTFS, DS2Version.VANILLA),
            ("vanilla", DS2Version.VANILLA, DS2Version.SOTFS),
        ):
            with self.subTest(game_version=game_version):
                world = self._make_world(game_version)
                first_candidates = world._build_filler_item_candidates(item_list)
                second_candidates = world._build_filler_item_candidates(item_list)
                _, recorded_populations = self._record_selection_sequence(world, 1)
                recorded_candidates, = recorded_populations

                expected_names = {
                    name for name, versions in versions_by_name.items()
                    if None in versions or selected_version in versions
                }
                selected_only_names = {
                    name for name, versions in versions_by_name.items()
                    if selected_version in versions
                    and None not in versions
                    and opposite_version not in versions
                }
                opposite_only_names = {
                    name for name, versions in versions_by_name.items()
                    if opposite_version in versions
                    and None not in versions
                    and selected_version not in versions
                }

                self.assertIsInstance(first_candidates, tuple)
                self.assertEqual(first_candidates, second_candidates)
                self.assertEqual(first_candidates, recorded_candidates)
                self.assertEqual(tuple(sorted(set(first_candidates))), first_candidates)
                self.assertEqual(expected_names, set(first_candidates))
                self.assertLessEqual(neutral_names, set(first_candidates))
                self.assertLessEqual(selected_only_names, set(first_candidates))
                self.assertTrue(set(first_candidates).isdisjoint(opposite_only_names))

                if selected_version == DS2Version.SOTFS:
                    self.assertTrue(selected_only_names)

    def test_synthetic_candidates_cover_both_editions_and_existing_filters(self) -> None:
        synthetic_items = (
            ItemData(900000001, "Zulu Neutral Filler", ItemCategory.GOOD),
            ItemData(900000002, "Alpha Scholar Filler", ItemCategory.GOOD, version=DS2Version.SOTFS),
            ItemData(900000003, "Beta Vanilla Filler", ItemCategory.GOOD, version=DS2Version.VANILLA),
            ItemData(900000004, "Excluded Scholar Filler", ItemCategory.GOOD,
                     version=DS2Version.SOTFS, exclude=True),
            ItemData(900000005, "Skipped Vanilla Filler", ItemCategory.GOOD,
                     version=DS2Version.VANILLA, skip=True),
            ItemData(900000006, "Unique Neutral Filler", ItemCategory.UNIQUE),
            ItemData(900000007, "Useful Neutral Item", ItemCategory.GOOD,
                     classification=ItemClassification.useful),
        )

        scholar_world = self._make_world("sotfs")
        vanilla_world = self._make_world("vanilla")

        self.assertEqual(
            ("Alpha Scholar Filler", "Zulu Neutral Filler"),
            scholar_world._build_filler_item_candidates(synthetic_items),
        )
        self.assertEqual(
            ("Beta Vanilla Filler", "Zulu Neutral Filler"),
            vanilla_world._build_filler_item_candidates(synthetic_items),
        )

    def test_repeated_same_seed_selection_is_identical_for_each_edition(self) -> None:
        for game_version in ("sotfs", "vanilla"):
            with self.subTest(game_version=game_version):
                first_world = self._make_world(game_version)
                second_world = self._make_world(game_version)

                first_selections, first_populations = self._record_selection_sequence(
                    first_world, SELECTION_COUNT
                )
                second_selections, second_populations = self._record_selection_sequence(
                    second_world, SELECTION_COUNT
                )
                expected_candidates = first_world._build_filler_item_candidates(item_list)

                self.assertEqual(first_selections, second_selections)
                self.assertEqual(first_populations, second_populations)
                self.assertTrue(all(
                    population == expected_candidates
                    for population in first_populations
                ))
                self.assertLessEqual(set(first_selections), set(expected_candidates))
