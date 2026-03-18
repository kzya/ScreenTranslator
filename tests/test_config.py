import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config_manager import ConfigManager


class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.settings_path = Path(self.temp_dir.name) / "settings.json"
        self.config_manager = ConfigManager(settings_file=self.settings_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_default_values_when_file_is_missing(self):
        self.assertEqual(self.config_manager.get("source_lang"), "English")
        self.assertEqual(self.config_manager.get("target_lang"), "Japanese")
        self.assertFalse(self.config_manager.get("auto_copy"))

    def test_set_and_get(self):
        self.config_manager.set("source_lang", "Japanese")
        self.assertEqual(self.config_manager.get("source_lang"), "Japanese")

        self.config_manager.set("auto_copy", True)
        self.assertTrue(self.config_manager.get("auto_copy"))

    def test_persistence(self):
        self.config_manager.set("target_lang", "French")

        new_manager = ConfigManager(settings_file=self.settings_path)
        self.assertEqual(new_manager.get("target_lang"), "French")

    def test_empty_file_falls_back_to_defaults(self):
        self.settings_path.write_text("", encoding="utf-8")

        manager = ConfigManager(settings_file=self.settings_path)
        self.assertEqual(manager.get("source_lang"), "English")
        self.assertEqual(manager.get("openai_api_key"), "")

    def test_invalid_json_falls_back_to_defaults(self):
        self.settings_path.write_text("{not-json", encoding="utf-8")

        manager = ConfigManager(settings_file=self.settings_path)
        self.assertEqual(manager.get("target_lang"), "Japanese")
        self.assertFalse(manager.get("auto_copy"))

    def test_env_api_key_takes_priority(self):
        self.config_manager.set("openai_api_key", "saved-key")

        with patch.dict(os.environ, {"OPENAI_API_KEY": "env-key"}, clear=False):
            self.assertEqual(self.config_manager.get_api_key(), "env-key")

    def test_legacy_settings_are_migrated_once(self):
        legacy_dir = Path(self.temp_dir.name) / "legacy"
        legacy_dir.mkdir()
        legacy_path = legacy_dir / "settings.json"
        legacy_path.write_text(
            json.dumps(
                {
                    "source_lang": "Japanese",
                    "target_lang": "English",
                    "openai_api_key": "legacy-key",
                    "auto_copy": True,
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        new_settings_path = Path(self.temp_dir.name) / "appdata" / "settings.json"

        with patch.object(ConfigManager, "get_default_settings_path", return_value=new_settings_path):
            with patch.object(ConfigManager, "get_legacy_settings_path", return_value=legacy_path):
                manager = ConfigManager()

        self.assertTrue(new_settings_path.exists())
        self.assertEqual(manager.get("source_lang"), "Japanese")
        self.assertEqual(manager.get_api_key(), "legacy-key")


if __name__ == "__main__":
    unittest.main()
