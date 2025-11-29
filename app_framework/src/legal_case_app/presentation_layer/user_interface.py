
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
            logfile_prefix_name=self.META["log_prefix"],
        )

        # Service layer (talks to DB)
        self.DB = AppServices(config)

        self._logger.log_debug(f"{inspect.currentframe().f_code.co_name}:It works!")

    # ---------- Main loop ----------

    def start(self):
        """Start main user interface."""
        self._logger.log_debug(
            f"{inspect.currentframe().f_code.co_name}: User interface started!"
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
        """Helper to print all cases (used by option 2 and 3)."""
        cases = self.DB.get_all_cases()
        if not cases:
            print("\n(No cases found.)")
            return []

        print("\n--- Cases ---")
        for c in cases:
            print(
                f"[{c['case_id']}] {c['case_name']} "
                f"(Client: {c['client_name']}, Status: {c['case_status']})"
            )
        return cases

    def _handle_view_case_with_lawyers(self):
        """Allow the user to pick a case and see all its assigned lawyers."""
        # 1. Show cases
        cases = self._handle_list_cases()
        if not cases:
            return

        # 2. Ask which case to view
        case_id_input = input(
            "\nEnter the case_id to view (or press Enter to cancel): "
        ).strip()

        if not case_id_input:
            print("Cancelled.")
            return

        try:
            case_id = int(case_id_input)
        except ValueError:
            print("Invalid case_id. Please enter a number.")
            return

        # 3. Retrieve case + lawyers from service layer
        rows = self.DB.get_case_with_lawyers(case_id)

        if not rows:
            print(f"No case found with case_id = {case_id}.")
            return

        # 4. Print case details (use the first row for case-level info)
        case = rows[0]
        print("\n--- Case Details ---")
        print(f"Case ID: {case['case_id']}")
        print(f"Case Name: {case['case_name']}")
        print(f"Client: {case['client_name']}")
        print(f"Status: {case['case_status']}")

        print("\nAssigned Lawyers:")
        has_lawyer = False
        for row in rows:
            # If no lawyer yet, the LEFT JOIN will give None values
            if row["lawyer_id"] is None:
                continue
            has_lawyer = True
            print(
                f" - {row['first_name']} {row['last_name']} "
                f"({row['specialization']}) "
                f"| Role: {row['role']} "
                f"| Billable Hours: {row['billable_hours']}"
            )

        if not has_lawyer:
            print(" (No lawyers assigned yet.)")

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

        # ✅ new: end_date prompt
        end_date = input(
            "End date (YYYY-MM-DD, optional, press Enter to skip): "
        ).strip()
        if end_date == "":
            end_date = None

        description = input("Description (optional): ").strip()
        if description == "":
            description = None

        if not case_name or not client_name or not case_status or not start_date:
            print("[!] Case name, client name, status, and start date are required.")
            return

        try:
            self.DB.add_case(
                case_name,
                client_name,
                case_status,
                start_date,
                end_date,
                description,
            )
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
