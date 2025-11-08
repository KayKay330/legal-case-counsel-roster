

CREATE USER IF NOT EXISTS 'legal_case_user'@'localhost'
IDENTIFIED BY 'SecurePass123!';

GRANT ALL PRIVILEGES ON legal_case_roster_db.* 
TO 'legal_case_user'@'localhost';

FLUSH PRIVILEGES;
