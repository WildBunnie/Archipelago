import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

from test.general import setup_multiworld

from worlds.dark_souls_2 import DarkSouls2World


ARCHIPELAGO_SEED = 8675309
HASH_SEEDS = ("1", "2")
PROBE_MARKER = "FILLER_HASHSEED_RESULT="
SELECTION_COUNT = 64


class _ChoiceRecorder:
    def __init__(self, delegate):
        self.delegate = delegate
        self.populations = []

    def choice(self, population):
        snapshot = tuple(population)
        self.populations.append(snapshot)
        return self.delegate.choice(snapshot)


def _make_world(game_version: str) -> DarkSouls2World:
    multiworld = setup_multiworld(
        DarkSouls2World,
        steps=(),
        seed=ARCHIPELAGO_SEED,
        options={"game_version": game_version},
    )
    return multiworld.worlds[1]


def _probe_current_process() -> None:
    payload = {}
    for game_version in ("sotfs", "vanilla"):
        world = _make_world(game_version)
        recorder = _ChoiceRecorder(world.random)
        world.random = recorder
        selections = tuple(
            world.get_filler_item_name()
            for _ in range(SELECTION_COUNT)
        )

        if len(recorder.populations) != SELECTION_COUNT:
            raise RuntimeError(
                f"Expected {SELECTION_COUNT} world RNG choices for {game_version}, "
                f"got {len(recorder.populations)}."
            )
        first_population = recorder.populations[0]
        if any(population != first_population for population in recorder.populations[1:]):
            raise RuntimeError(f"Filler candidates changed during the {game_version} probe.")

        payload[game_version] = {
            "candidates": first_population,
            "selections": selections,
        }

    print(PROBE_MARKER + json.dumps(payload, sort_keys=True))


class TestFillerHashSeedEvidence(unittest.TestCase):
    @staticmethod
    def _sequence_digest(sequence) -> str:
        encoded = json.dumps(sequence, ensure_ascii=False).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def _run_probe(self, hash_seed: str):
        repository_root = Path(__file__).resolve().parents[3]
        environment = os.environ.copy()
        environment["PYTHONHASHSEED"] = hash_seed
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "worlds.dark_souls_2.test.filler_hashseed_evidence",
                "--probe",
            ],
            cwd=repository_root,
            env=environment,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            0,
            result.returncode,
            f"Hash-seed probe {hash_seed} failed.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}",
        )
        result_lines = [
            line.split(PROBE_MARKER, 1)[1]
            for line in result.stdout.splitlines()
            if PROBE_MARKER in line
        ]
        self.assertEqual(
            1,
            len(result_lines),
            f"Hash-seed probe {hash_seed} emitted an unexpected result.\nSTDOUT:\n{result.stdout}",
        )
        return json.loads(result_lines[0])

    def test_same_seed_candidates_and_selections_ignore_pythonhashseed(self) -> None:
        first_payload = self._run_probe(HASH_SEEDS[0])
        second_payload = self._run_probe(HASH_SEEDS[1])
        self.assertEqual({"sotfs", "vanilla"}, set(first_payload))
        self.assertEqual(set(first_payload), set(second_payload))

        for game_version in sorted(first_payload):
            with self.subTest(game_version=game_version):
                first_candidates = first_payload[game_version]["candidates"]
                second_candidates = second_payload[game_version]["candidates"]
                if first_candidates != second_candidates:
                    self.fail(
                        f"{game_version} candidate sequence changed between PYTHONHASHSEED "
                        f"{HASH_SEEDS[0]} ({self._sequence_digest(first_candidates)}) and "
                        f"{HASH_SEEDS[1]} ({self._sequence_digest(second_candidates)})."
                    )

                first_selections = first_payload[game_version]["selections"]
                second_selections = second_payload[game_version]["selections"]
                if first_selections != second_selections:
                    self.fail(
                        f"{game_version} selected-name sequence changed between PYTHONHASHSEED "
                        f"{HASH_SEEDS[0]} ({self._sequence_digest(first_selections)}) and "
                        f"{HASH_SEEDS[1]} ({self._sequence_digest(second_selections)})."
                    )


if __name__ == "__main__":
    if sys.argv[1:] != ["--probe"]:
        raise SystemExit("Expected --probe.")
    _probe_current_process()
