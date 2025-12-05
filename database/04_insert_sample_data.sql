

USE legal_case_roster_db;

INSERT INTO lawyer (first_name, last_name, specialization, email)
VALUES
('Jordan', 'Miles', 'Corporate Law', 'jmiles@firm.com'),
('Sara', 'Patel', 'Criminal Defense', 'spatel@firm.com'),
('David', 'Nguyen', 'Family Law', 'dnguyen@firm.com');

INSERT INTO legal_case (case_name, client_name, case_status, start_date)
VALUES
('Estate Planning: Johnson', 'Mary Johnson', 'Open', '2025-11-01'),
('Contract Dispute: Axiom Corp', 'Axiom Corp', 'In Progress', '2025-10-15'),
('Divorce Settlement: Garcia', 'Ana Garcia', 'Pending', '2025-09-20');

INSERT INTO case_lawyer_xref (case_id, lawyer_id, role, billable_hours)
VALUES
(1, 1, 'Lead', 10.5),
(2, 2, 'Lead', 25.0),
(2, 1, 'Consultant', 5.0),
(3, 3, 'Lead', 12.0);

SELECT * FROM lawyer;
SELECT * FROM legal_case;
SELECT * FROM case_lawyer_xref;
