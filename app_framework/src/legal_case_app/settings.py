"""Manage applicaion settings."""

import json
import platform
from pathlib import Path

class Settings():
    """Manage application settings."""

    def __init__(self, default_settings_filename:str='app_settings.json'):
        """Initialize instance."""
        self._default_settings_filename = default_settings_filename

    def create_settings_json_file(self, 
                                filename:str='app_settings.json') -> dict:
        """Create default settings file if none exists."""
        if not isinstance(filename, str):
            filename = self._default_settings_filename

        settings = {}

        match platform.system():
            case 'Windows':
                settings['logs_dir'] = 'logs'
                settings['log_filename'] = 'app.log'
                settings['log_level'] = 'debug'
                settings['log_to_console'] = True
                settings['log_to_file'] = True
                settings['deployed_to_production'] = False
                
            case _:
                settings['logs_dir'] = 'logs'
                settings['log_filename'] = 'app.log'
                settings['log_level'] = 'debug'
                settings['log_to_console'] = True
                settings['log_to_file'] = True
                settings['deployed_to_production'] = False    
        try:
            with open(filename, 'w') as f:
                f.write(json.dumps(settings))
        except Exception as e:
            raise Exception(f'{e}')
        return settings


    def read_settings_file_from_location(self, 
                                        filename:str='app_settings.json')->dict:
        """Read settings file and return dictionary.
        If settings file does not exist create default settings file.
        """
        settings = {}
        try:
            with open(filename, 'r') as f:
                settings = json.loads(f.read())
        except Exception as e:
            settings = self.create_settings_json_file(filename)

        return settings



