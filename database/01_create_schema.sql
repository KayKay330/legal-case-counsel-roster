

CREATE DATABASE IF NOT EXISTS legal_case_roster_db;

USE legal_case_roster_db;

CREATE TABLE IF NOT EXISTS lawyer (
    lawyer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    specialization VARCHAR(100),
    email VARCHAR(100) UNIQUE
);

CREATE TABLE IF NOT EXISTS legal_case (
    case_id INT AUTO_INCREMENT PRIMARY KEY,
    case_name VARCHAR(100) NOT NULL,
    client_name VARCHAR(100),
    case_status VARCHAR(50),
    start_date DATE
);

CREATE TABLE IF NOT EXISTS case_lawyer_xref (
    id INT AUTO_INCREMENT PRIMARY KEY,
    case_id INT NOT NULL,
    lawyer_id INT NOT NULL,
    role VARCHAR(50),
    billable_hours DECIMAL(6,2),
    FOREIGN KEY (case_id) REFERENCES legal_case(case_id),
    FOREIGN KEY (lawyer_id) REFERENCES lawyer(lawyer_id)
);
