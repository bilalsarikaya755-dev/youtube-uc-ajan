import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))

from contracts import (Direction, Research, Script, render_package,
                       validate_direction, validate_script)


class ProductionChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.board = json.loads((BASE / "example" / "blackboard.json").read_text(encoding="utf-8"))

    def models(self):
        return (Research.model_validate(self.board["research"]),
                Script.model_validate(self.board["script"]),
                Direction.model_validate(self.board["direction"]))

    def test_complete_production_package(self):
        research, script, direction = self.models()
        validate_script(script, research, 240, 60)
        validate_direction(direction, script)
        result = render_package(research, script, direction)
        self.assertIn("03:40-04:00", result)
        self.assertIn("00:50-01:00", result)
        for source in research.sources:
            self.assertIn(str(source.url), result)

    def test_missing_evidence_source_stops_research(self):
        data = copy.deepcopy(self.board["research"])
        data["facts"][0]["source_ids"] = ["HAYALI_KAYNAK"]
        with self.assertRaises(ValueError):
            Research.model_validate(data)

    def test_invented_fact_stops_script(self):
        research, script, _ = self.models()
        script.sections[0].fact_ids = ["ARAŞTIRMADA_YOK"]
        with self.assertRaises(ValueError):
            validate_script(script, research, 240, 60)

    def test_wrong_duration_stops_script(self):
        data = copy.deepcopy(self.board["script"])
        data["sections"][0]["duration_seconds"] += 1
        with self.assertRaises(ValueError):
            Script.model_validate(data)

    def test_missing_shot_stops_direction(self):
        _, script, direction = self.models()
        direction.main_shots.pop()
        with self.assertRaises(ValueError):
            validate_direction(direction, script)

    def test_duplicate_shot_stops_direction(self):
        _, script, direction = self.models()
        direction.main_shots.append(direction.main_shots[0])
        with self.assertRaises(ValueError):
            validate_direction(direction, script)

    def test_markdown_cells_do_not_break_rows(self):
        research, script, direction = self.models()
        direction.main_shots[0].visual = "Önce | sonra\nYeni çekim"
        result = render_package(research, script, direction)
        self.assertIn("Önce \\| sonra Yeni çekim", result)

    def test_demo_creates_readable_files_in_path_with_spaces(self):
        with tempfile.TemporaryDirectory(prefix="uretim kontrolu ") as target:
            result = subprocess.run([sys.executable, str(BASE / "main.py"),
                                     "--demo", "--out", target], capture_output=True,
                                    text=True, encoding="utf-8", timeout=20)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("model veya web çağrısı yapılmıyor", result.stdout)
            outputs = list(Path(target).glob("*/uretim_paketi.md"))
            self.assertEqual(len(outputs), 1)
            board = json.loads(outputs[0].with_name("blackboard.json").read_text(encoding="utf-8"))
            self.assertEqual(board["metadata"]["mode"], "demo")
            self.assertEqual(board["script"]["main_duration_seconds"], 240)
            self.assertTrue(outputs[0].with_name("shorts_seslendirme.txt").is_file())


if __name__ == "__main__":
    unittest.main()
