
"""Implements AppServices Class."""

from legal_case_app.application_base import ApplicationBase
from legal_case_app.persistence_layer.mysql_persistence_wrapper import MySQLPersistenceWrapper
import inspect


class AppServices(ApplicationBase):
    """AppServices Class Definition."""

    def __init__(self, config: dict) -> None:
        """Initialize AppServices and wire it to the DB wrapper."""
        self._config_dict = config
        self.META = config["meta"]

        # Set up logging through ApplicationBase
        super().__init__(
            subclass_name=self.__class__.__name__,
            logfile_prefix_name=self.META["log_prefix"],
        )

        # Create the DB wrapper (this sets up the connection pool)
        self.db = MySQLPersistenceWrapper(config)
        self._connection_pool = self.db._connection_pool

        self._logger.log_debug(
            f'{inspect.currentframe().f_code.co_name}: '
            f'AppServices initialized. DB Config: {self.db.DB_CONFIG}'
        )

    # ---------- Low-level helpers ----------

    def fetch_all(self, query: str, params=None):
        """
        Run a SELECT and return all rows as dictionaries.

        :param query: SQL SELECT statement
        :param params: tuple of parameters or None
        """
        connection = self._connection_pool.get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            return results
        finally:
            cursor.close()
            connection.close()

    def execute(self, query: str, params=None):
        """
        Run an INSERT/UPDATE/DELETE.

        :param query: SQL statement
        :param params: tuple of parameters or None
        """
        connection = self._connection_pool.get_connection()
        cursor = connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            connection.commit()
        finally:
            cursor.close()
            connection.close()

    # ---------- Existing list methods ----------

    def get_all_lawyers(self):
        """Return all lawyers."""
        query = "SELECT * FROM lawyer;"
        return self.fetch_all(query)

    def get_all_cases(self):
        """Return all cases."""
        query = "SELECT * FROM legal_case;"
        return self.fetch_all(query)

    def get_case_lawyers(self):
        """Return all rows from the case_lawyer_xref table."""
        query = "SELECT * FROM case_lawyer_xref;"
        return self.fetch_all(query)

    # ---------- New feature methods ----------

    def get_case_with_lawyers(self, case_id: int):
        """
        Return a joined view of one case and its assigned lawyers.

        If there are no lawyers yet, we still return the case details
        (because of the LEFT JOIN).
        """
        query = """
        SELECT
            lc.case_id,
            lc.case_name,
            lc.client_name,
            lc.case_status,
            lc.start_date,
            l.lawyer_id,
            l.first_name,
            l.last_name,
            l.specialization,
            cl.role,
            cl.billable_hours
        FROM legal_case lc
        LEFT JOIN case_lawyer_xref cl
            ON lc.case_id = cl.case_id
        LEFT JOIN lawyer l
            ON cl.lawyer_id = l.lawyer_id
        WHERE lc.case_id = %s;
        """
        return self.fetch_all(query, (case_id,))

    def add_lawyer(self, first_name, last_name, specialization, email, phone=None):
        """
        Insert a new lawyer. hire_date is set to today's date by MySQL.
        """
        query = """
        INSERT INTO lawyer (first_name, last_name, specialization, email, phone, hire_date)
        VALUES (%s, %s, %s, %s, %s, CURDATE());
        """
        self.execute(query, (first_name, last_name, specialization, email, phone))

    def add_case(
        self,
        case_name,
        client_name,
        case_status,
        start_date,
        end_date=None,
        description=None,
    ):
        """
        Insert a new legal case.

        start_date and end_date should be 'YYYY-MM-DD'.
        end_date is optional.
        description is optional.
        """
        query = """
        INSERT INTO legal_case
            (case_name, client_name, case_status, start_date, end_date, description)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        self.execute(
            query,
            (case_name, client_name, case_status, start_date, end_date, description),
        )

    def assign_lawyer_to_case(
        self,
        case_id: int,
        lawyer_id: int,
        role: str,
        billable_hours: float,
    ):
        """
        Link a lawyer to a case with role + billable hours.
        """
        query = """
        INSERT INTO case_lawyer_xref (case_id, lawyer_id, role, billable_hours)
        VALUES (%s, %s, %s, %s);
        """
        self.execute(query, (case_id, lawyer_id, role, billable_hours))
