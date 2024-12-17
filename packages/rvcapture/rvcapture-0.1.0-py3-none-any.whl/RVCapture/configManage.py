import json
from pathlib import Path
from RVCapture.utils import getAppName


class ConfigStore:
    def __init__(self):
        self.config_dir = Path.home() /  '.config' / getAppName()
        self.config_file = self.config_dir / 'config.json'
        self.config_dir.mkdir(parents=True, exist_ok=True)

        if not self.config_file.exists():
            self.config_file.touch()
            self.config_file.write_text("{}")

    def getCompleteConfig(self):
        try:
            with open(self.config_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def getConfig(self, key):
        config = self.getCompleteConfig()
        return config.get(key, None)
    
    def setConfig(self, key, value):
        config = self.getCompleteConfig()
        config[key] = value
        with open(self.config_file, "w") as f:
            json.dump(config, f, indent=4)

    def deleteConfig(self, key):
        config = self.getCompleteConfig()
        del config[key]
        with open(self.config_file, "w") as f:
            json.dump(config, f, indent=4) 

    def getConfigKeys(self):
        config = self.getCompleteConfig()
        return list(config.keys())
    