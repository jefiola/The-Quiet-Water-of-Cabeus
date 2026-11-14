import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi import HTTPException

from app import data_manager, main


class DataApiTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.data_dir = Path(self.directory.name)
        patcher = patch.object(data_manager, "DATA_DIR", self.data_dir)
        patcher.start()
        self.addCleanup(patcher.stop)

    def write_json(self, name, value):
        (self.data_dir / name).write_text(json.dumps(value), encoding="utf-8")

    def test_catalog_and_lookup(self):
        self.write_json("crafts.json", [{"id": "lcross"}])
        self.assertEqual(main.api_get_all_crafts()["data"], [{"id": "lcross"}])
        self.assertEqual(main.api_get_craft_by_id("lcross")["data"], {"id": "lcross"})
        with self.assertRaises(HTTPException) as error:
            main.api_get_craft_by_id("unknown")
        self.assertEqual(error.exception.status_code, 404)

    def test_empty_catalog_is_successful(self):
        self.write_json("crafts.json", [])
        self.assertEqual(main.api_get_all_crafts()["data"], [])

    def test_catalog_errors_are_not_reported_as_missing_crafts(self):
        with self.assertRaises(FileNotFoundError):
            main.api_get_all_crafts()
        (self.data_dir / "crafts.json").write_text("{", encoding="utf-8")
        with self.assertRaises(json.JSONDecodeError):
            main.api_get_craft_by_id("lcross")
        self.write_json("crafts.json", None)
        with self.assertRaises(ValueError):
            main.api_get_all_crafts()

    def test_story_missing_empty_and_invalid(self):
        with self.assertRaises(HTTPException) as error:
            main.api_get_story_chapter(1)
        self.assertEqual(error.exception.status_code, 404)
        self.write_json("lcross_chapter1.json", {})
        self.assertEqual(main.api_get_story_chapter(1)["data"], {})
        self.write_json("lcross_chapter1.json", None)
        with self.assertRaises(ValueError):
            main.api_get_story_chapter(1)
        (self.data_dir / "lcross_chapter1.json").write_text("{", encoding="utf-8")
        with self.assertRaises(json.JSONDecodeError):
            main.api_get_story_chapter(1)

    def test_missing_data_directory_is_not_a_missing_chapter(self):
        with patch.object(data_manager, "DATA_DIR", self.data_dir / "missing"):
            with self.assertRaises(FileNotFoundError):
                main.api_get_story_chapter(1)


if __name__ == "__main__":
    unittest.main()
