import json
import os
import sys
from pathlib import Path

APP_NAME = "ScreenTranslator"
CONFIG_FILE_NAME = "settings.json"
API_KEY_ENV_VAR = "OPENAI_API_KEY"

DEFAULT_CONFIG = {
    "source_lang": "English",
    "target_lang": "Japanese",
    "openai_api_key": "",
    "auto_copy": False,
}


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


class ConfigManager:
    def __init__(self, settings_file=None):
        self._custom_settings_file = settings_file is not None
        self.settings_path = Path(settings_file) if settings_file else self.get_default_settings_path()
        self.settings_file = str(self.settings_path)
        self.config = DEFAULT_CONFIG.copy()

        if not self._custom_settings_file:
            self.migrate_legacy_config()

        self.load_config()

    @classmethod
    def get_settings_dir(cls) -> Path:
        local_appdata = os.environ.get("LOCALAPPDATA")
        if local_appdata:
            return Path(local_appdata) / APP_NAME
        return Path.home() / "AppData" / "Local" / APP_NAME

    @classmethod
    def get_default_settings_path(cls) -> Path:
        return cls.get_settings_dir() / CONFIG_FILE_NAME

    @staticmethod
    def get_legacy_settings_path() -> Path:
        if getattr(sys, "frozen", False):
            return Path(sys.executable).resolve().parent / CONFIG_FILE_NAME
        return _project_root() / CONFIG_FILE_NAME

    def migrate_legacy_config(self):
        legacy_path = self.get_legacy_settings_path()

        try:
            if self.settings_path.exists() or not legacy_path.exists():
                return
            if legacy_path.resolve() == self.settings_path.resolve():
                return
        except OSError:
            return

        try:
            raw_text = legacy_path.read_text(encoding="utf-8").strip()
            if not raw_text:
                return
            loaded = json.loads(raw_text)
        except (OSError, json.JSONDecodeError):
            return

        if not isinstance(loaded, dict):
            return

        self.settings_path.parent.mkdir(parents=True, exist_ok=True)
        self.settings_path.write_text(
            json.dumps(loaded, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )

    def load_config(self):
        self.config = DEFAULT_CONFIG.copy()

        if not self.settings_path.exists():
            return

        try:
            raw_text = self.settings_path.read_text(encoding="utf-8").strip()
        except OSError:
            return

        if not raw_text:
            return

        try:
            loaded = json.loads(raw_text)
        except json.JSONDecodeError:
            return

        if isinstance(loaded, dict):
            self.config.update(loaded)

    def save_config(self):
        try:
            self.settings_path.parent.mkdir(parents=True, exist_ok=True)
            self.settings_path.write_text(
                json.dumps(self.config, indent=4, ensure_ascii=False),
                encoding="utf-8",
            )
        except OSError as exc:
            print(f"Error saving config: {exc}")

    def get(self, key):
        return self.config.get(key, DEFAULT_CONFIG.get(key))

    def set(self, key, value):
        self.config[key] = value
        self.save_config()

    def get_api_key(self):
        return os.environ.get(API_KEY_ENV_VAR) or self.get("openai_api_key")
