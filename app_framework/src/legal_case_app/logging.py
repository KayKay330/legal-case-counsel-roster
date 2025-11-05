"""Provides LoggingService convenience class for application logging."""

import logging
import logging.handlers
from legal_case_app.settings import Settings
import os

class LoggingService():
    """Provides logging services."""

    def __init__(self, class_name:str, logfile_prefix_name:str=None)->None:
        """Initialize instance."""
        
        self._logger = logging.getLogger(class_name)
        self._logger.propagate = False
        self._settings_dict = Settings().read_settings_file_from_location()
        self._logfile_prefix_name = logfile_prefix_name
        self.log_level = logging.ERROR
        
        if self._settings_dict['log_level'] == 'notset':
            self._logger.setLevel(logging.NOTSET)
            self.log_level = logging.NOTSET
        elif self._settings_dict['log_level'] == 'debug':
            self._logger.setLevel(logging.DEBUG)
            self.log_level = logging.debug
        elif self._settings_dict['log_level'] == 'info':
            self._logger.setLevel(logging.INFO)
            self.log_level = logging.INFO
        elif self._settings_dict['log_level'] == 'warning':
            self._logger.setLevel(logging.WARNING)
            self.log_level = logging.WARNING
        elif self._settings_dict['log_level'] == 'error':
            self._logger.setLevel(logging.ERROR)
            self.log_level = logging.ERROR
        elif self._settings_dict['log_level'] == 'critical':
            self._logger.setLevel(logging.CRITICAL)
            self.log_level = logging.CRITICAL
        else:
            self._logger.setLevel(logging.ERROR)
            self.log_level = logging.ERROR

        self._formatter = \
                logging.Formatter('%(levelname)s:%(name)s:%(asctime)s:%(message)s')

        if not self._logger.handlers:
            if self._settings_dict['log_to_console']:
                self._ch = logging.StreamHandler()
                self._ch.setLevel(logging.DEBUG)
                self._ch.setFormatter(self._formatter)
                self._logger.addHandler(self._ch)

            if self._settings_dict['log_to_file']:
                log_file = os.path.join(self._settings_dict['logs_dir'], 
                            f"{self._logfile_prefix_name}_" \
                            f"{self._settings_dict['log_filename']}")
                self._fh = logging.handlers.TimedRotatingFileHandler(log_file, 
                            when='midnight', backupCount=20)
                self._fh.setLevel(logging.DEBUG)
                self._fh.setFormatter(self._formatter)
                self._logger.addHandler(self._fh)
        

    
    def log_debug(self, message):
        """Log to debug."""
        self._logger.debug(message)

    def log_error(self, message):
        """Log to error."""
        self._logger.error(message)

    def log_info(self, message):
        """Log to info."""
        self._logger.info(message)

    def log_warning(self, message):
        """Log to warning."""
        self._logger.warning(message)

    def log_critical(self, message):
        """Log to critical."""
        self._logger.critical(message)

