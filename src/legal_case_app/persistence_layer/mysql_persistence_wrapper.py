
"""Defines the MySQLPersistenceWrapper class."""

from legal_case_app.application_base import ApplicationBase
from mysql import connector
from mysql.connector.pooling import MySQLConnectionPool
import inspect
import json


class MySQLPersistenceWrapper(ApplicationBase):
    """Implements the MySQLPersistenceWrapper class."""

    def __init__(self, config: dict) -> None:
        """Initializes object."""
        self._config_dict = config
        self.META = config["meta"]
        self.DATABASE = config["database"]

        super().__init__(
            subclass_name=self.__class__.__name__,
            logfile_prefix_name=self.META["log_prefix"],
        )

        self._logger.log_debug(
            f"{inspect.currentframe().f_code.co_name}:It works!"
        )

        # ---------- Database Configuration Constants ----------
        self.DB_CONFIG = {}
        self.DB_CONFIG["database"] = self.DATABASE["connection"]["config"]["database"]
        self.DB_CONFIG["user"] = self.DATABASE["connection"]["config"]["user"]
        self.DB_CONFIG["password"] = self.DATABASE["connection"]["config"]["password"]
        self.DB_CONFIG["host"] = self.DATABASE["connection"]["config"]["host"]
        self.DB_CONFIG["port"] = self.DATABASE["connection"]["config"]["port"]

        self._logger.log_debug(
            f'{inspect.currentframe().f_code.co_name}: '
            f'DB Connection Config Dict: {self.DB_CONFIG}'
        )

        # ---------- Database Connection ----------
        # Create the pool and expose it both as _connection_pool and connection_pool
        self._connection_pool = self._initialize_database_connection_pool(
            self.DB_CONFIG
        )
        # This is what AppServices is using: self.db.connection_pool
        self.connection_pool = self._connection_pool

        # (Old constant from the framework – not used right now, but harmless)
        self.SELECT_ALL_EMPLOYEES = (
            "SELECT id, first_name, middle_name, last_name"
        )

    # ---------- Private Utility Methods ----------

    def _initialize_database_connection_pool(
        self, config: dict
    ) -> MySQLConnectionPool:
        """Initializes database connection pool."""
        try:
            self._logger.log_debug("Creating connection pool...")
            cnx_pool = MySQLConnectionPool(
                pool_name=self.DATABASE["pool"]["name"],
                pool_size=self.DATABASE["pool"]["size"],
                pool_reset_session=self.DATABASE["pool"]["reset_session"],
                use_pure=self.DATABASE["pool"]["use_pure"],
                **config,
            )
            self._logger.log_debug(
                f"{inspect.currentframe().f_code.co_name}: "
                f"Connection pool successfully created!"
            )
            return cnx_pool
        except connector.Error as err:
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: "
                f"Problem creating connection pool: {err}"
            )
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: "
                f"Check DB cnfg:\n{json.dumps(self.DATABASE)}"
            )
        except Exception as e:
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: "
                f"Problem creating connection pool: {e}"
            )
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: "
                f"Check DB conf:\n{json.dumps(self.DATABASE)}"
            )

    # ---------- Convenience Methods (optional, for debugging/demo) ----------

    def test_connection(self):
        """
        Simple test query to validate DB connectivity.
        Used by AppServices or directly in tests if needed.
        """
        query = "SELECT first_name, last_name FROM lawyer LIMIT 3;"
        cnx = self._connection_pool.get_connection()
        cursor = cnx.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        cnx.close()
        return results
