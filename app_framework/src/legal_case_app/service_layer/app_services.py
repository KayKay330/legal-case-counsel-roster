
"""Implements AppServices Class."""

from legal_case_app.application_base import ApplicationBase
from legal_case_app.persistence_layer.mysql_persistence_wrapper import MySQLPersistenceWrapper
import inspect


class AppServices(ApplicationBase):
    """AppServices Class Definition."""

    def __init__(self, config: dict) -> None:
        """Initialize AppServices and set up access to the DB connection pool."""
        # Store meta info and initialize base logger
        self.META = config["meta"]
        super().__init__(
            subclass_name=self.__class__.__name__,
            logfile_prefix_name=self.META["log_prefix"],
        )

        # Create the DB wrapper (this builds the connection pool)
        self.db = MySQLPersistenceWrapper(config)

        # Reuse the connection pool created inside the DB wrapper
        self._connection_pool = self.db.connection_pool

        self._logger.log_debug(
            f"{inspect.currentframe().f_code.co_name}: AppServices initialized. "
            f"DB Config: {self.db.DB_CONFIG}"
        )

    # ---------------------------------------------------------------------
    # Low-level helpers
    # ---------------------------------------------------------------------
    def fetch_all(self, query: str):
        """Run a SELECT query and return all rows as a list of dicts."""
        connection = self._connection_pool.get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(query)
        results = cursor.fetchall()

        cursor.close()
        connection.close()

        return results

    def execute(self, query: str, params=None):
        """Run INSERT/UPDATE/DELETE style queries."""
        connection = self._connection_pool.get_connection()
        cursor = connection.cursor()

        cursor.execute(query, params)
        connection.commit()

        cursor.close()
        connection.close()

    # ---------------------------------------------------------------------
    # High-level, app-specific methods
    # ---------------------------------------------------------------------
    def get_all_lawyers(self):
        """Return all lawyers from the database."""
        query = "SELECT * FROM lawyer;"
        return self.fetch_all(query)

    def get_all_cases(self):
        """Return all legal cases from the database."""
        query = "SELECT * FROM legal_case;"
        return self.fetch_all(query)

    def get_case_lawyers(self):
        """Return the lawyer–case relationships."""
        query = "SELECT * FROM case_lawyer_xref;"
        return self.fetch_all(query)
