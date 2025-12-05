

-- -------------------------------------
-- Table: lawyer
-- -------------------------------------
CREATE TABLE lawyer (
    lawyer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    specialization VARCHAR(200) NOT NULL,
    email VARCHAR(200) NOT NULL UNIQUE,
    phone VARCHAR(20),
    hire_date DATE NOT NULL DEFAULT (CURDATE())
);

-- -------------------------------------
-- Table: legal_case
-- -------------------------------------
CREATE TABLE legal_case (
    case_id INT AUTO_INCREMENT PRIMARY KEY,
    case_name VARCHAR(255) NOT NULL,
    client_name VARCHAR(255) NOT NULL,
    case_status VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NULL,
    description TEXT NULL
);

-- -------------------------------------
-- Table: case_lawyer_xref
-- -------------------------------------
CREATE TABLE case_lawyer_xref (
    id INT AUTO_INCREMENT PRIMARY KEY,
    case_id INT NOT NULL,
    lawyer_id INT NOT NULL,
    role VARCHAR(100) NOT NULL,
    billable_hours DECIMAL(10,2) DEFAULT 0,

    FOREIGN KEY (case_id) REFERENCES legal_case(case_id),
    FOREIGN KEY (lawyer_id) REFERENCES lawyer(lawyer_id)
);