
"""Implements the application user interface."""

from legal_case_app.application_base import ApplicationBase
from legal_case_app.service_layer.app_services import AppServices
import inspect


class UserInterface(ApplicationBase):
    """UserInterface Class Definition."""

    def __init__(self, config: dict) -> None:
        """Initializes object."""
        self._config_dict = config
        self.META = config["meta"]

        super().__init__(
            subclass_name=self.__class__.__name__,
            logfile_prefix_name=self.META["log_prefix"]
        )

        # Service layer (talks to DB)
        self.DB = AppServices(config)

        self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}:It works!')

    # ---------- Main loop ----------

    def start(self):
        """Start main user interface."""
        self._logger.log_debug(
            f'{inspect.currentframe().f_code.co_name}: User interface started!'
        )

        while True:
            self._print_menu()
            choice = input("Select an option: ").strip()

            if choice == "1":
                self._handle_list_lawyers()
            elif choice == "2":
                self._handle_list_cases()
            elif choice == "3":
                self._handle_view_case_with_lawyers()
            elif choice == "4":
                self._handle_add_lawyer()
            elif choice == "5":
                self._handle_add_case()
            elif choice == "6":
                self._handle_assign_lawyer_to_case()
            elif choice == "0":
                print("\nExiting Legal Case Roster. Goodbye!")
                break
            else:
                print("\n[!] Invalid option. Please try again.")

    # ---------- Menu + small helpers ----------

    def _print_menu(self):
        print("\n===== Legal Case Counsel Roster =====")
        print("1. List all lawyers")
        print("2. List all cases")
        print("3. View a case and its assigned lawyers")
        print("4. Add a new lawyer")
        print("5. Add a new case")
        print("6. Assign a lawyer to a case")
        print("0. Exit")
        print("=====================================")

    # ---------- Listing handlers ----------

    def _handle_list_lawyers(self):
        """List all lawyers in a friendly format."""
        lawyers = self.DB.get_all_lawyers()
        if not lawyers:
            print("\n(No lawyers found.)")
            return

        print("\n--- Lawyers ---")
        for row in lawyers:
            print(
                f"[{row['lawyer_id']}] "
                f"{row['first_name']} {row['last_name']} "
                f"- {row['specialization']} "
                f"({row['email']})"
            )

    def _handle_list_cases(self):
        """List all cases in a friendly format."""
        cases = self.DB.get_all_cases()
        if not cases:
            print("\n(No cases found.)")
            return

        print("\n--- Cases ---")
        for row in cases:
            print(
                f"[{row['case_id']}] "
                f"{row['case_name']} "
                f"(Client: {row['client_name']}, Status: {row['case_status']})"
            )

    # ---------- View case + lawyers ----------

    def _handle_view_case_with_lawyers(self):
        """Ask for a case_id and show case details + assigned lawyers."""
        self._handle_list_cases()
        case_id_raw = input("\nEnter the case_id to view (or press Enter to cancel): ").strip()
        if not case_id_raw:
            print("Cancelled.")
            return

        try:
            case_id = int(case_id_raw)
        except ValueError:
            print("[!] Please enter a valid numeric case_id.")
            return

        rows = self.DB.get_case_with_lawyers(case_id)
        if not rows:
            print(f"\nNo case found with case_id = {case_id}.")
            return

        # All rows contain the same case info; lawyers differ per row
        case = rows[0]
        print("\n--- Case Details ---")
        print(f"ID: {case['case_id']}")
        print(f"Name: {case['case_name']}")
        print(f"Client: {case['client_name']}")
        print(f"Status: {case['case_status']}")
        print(f"Start date: {case['start_date']}")
        print(f"End date: {case['end_date']}")
        print(f"Description: {case['description']}")

        print("\nAssigned Lawyers:")
        any_lawyers = False
        for row in rows:
            if row["lawyer_id"] is None:
                continue
            any_lawyers = True
            print(
                f"- [{row['lawyer_id']}] {row['first_name']} {row['last_name']} "
                f"({row['specialization']}) "
                f"Role: {row['role']}, Hours: {row['billable_hours']}"
            )

        if not any_lawyers:
            print("  (No lawyers assigned yet.)")

    # ---------- Add lawyer ----------

    def _handle_add_lawyer(self):
        """Prompt user and create a new lawyer record."""
        print("\n--- Add New Lawyer ---")
        first = input("First name: ").strip()
        last = input("Last name: ").strip()
        spec = input("Specialization (e.g., Family Law, Corporate Law): ").strip()
        email = input("Email: ").strip()
        phone = input("Phone (optional, press Enter to skip): ").strip()

        if not first or not last or not spec or not email:
            print("[!] First, last, specialization, and email are required.")
            return

        phone_value = phone if phone else None

        try:
            self.DB.add_lawyer(first, last, spec, email, phone_value)
            print("\n[✓] Lawyer added successfully.")
        except Exception as e:
            print(f"[!] Error adding lawyer: {e}")

    # ---------- Add case ----------

    def _handle_add_case(self):
        """Prompt user and create a new legal case."""
        print("\n--- Add New Case ---")
        case_name = input("Case name: ").strip()
        client_name = input("Client name: ").strip()
        case_status = input("Status (e.g., Open, Pending, In Progress): ").strip()
        start_date = input("Start date (YYYY-MM-DD): ").strip()
        description = input("Description (optional): ").strip()

        if not case_name or not client_name or not case_status or not start_date:
            print("[!] Case name, client name, status, and start date are required.")
            return

        desc_value = description if description else None

        try:
            self.DB.add_case(case_name, client_name, case_status, start_date, desc_value)
            print("\n[✓] Case added successfully.")
        except Exception as e:
            print(f"[!] Error adding case: {e}")

    # ---------- Assign lawyer to case ----------

    def _handle_assign_lawyer_to_case(self):
        """Assign an existing lawyer to an existing case."""
        print("\n--- Assign Lawyer to Case ---")

        # Show current lawyers and cases so the user knows the IDs
        self._handle_list_lawyers()
        self._handle_list_cases()

        lawyer_raw = input("\nEnter lawyer_id to assign: ").strip()
        case_raw = input("Enter case_id to assign them to: ").strip()
        role = input("Role (e.g., Lead, Consultant): ").strip()
        hours_raw = input("Billable hours (e.g., 5.0): ").strip()

        try:
            lawyer_id = int(lawyer_raw)
            case_id = int(case_raw)
            billable_hours = float(hours_raw)
        except ValueError:
            print("[!] Please enter valid numeric values for IDs and hours.")
            return

        if not role:
            print("[!] Role is required.")
            return

        try:
            self.DB.assign_lawyer_to_case(case_id, lawyer_id, role, billable_hours)
            print("\n[✓] Lawyer assigned to case successfully.")
        except Exception as e:
            print(f"[!] Error assigning lawyer to case: {e}")
