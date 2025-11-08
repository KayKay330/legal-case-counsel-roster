
# Legal Case Counsel Roster

Console-based, multi-layered application for managing legal cases, assigned lawyers, roles, and billable hours.

Built on top of the `it566_project_app_framework` provided for IT 566.

---

## Setup

### 1. Clone & Environment

```bash
git clone https://github.com/KayKay330/legal-case-counsel-roster.git
cd legal-case-counsel-roster/app_framework
pipenv install


### 2. Database Setup (MySQL)

cd ~/legal_case_counsel_roster/app_framework
mysql -u root -p < database/01_create_schema.sql
mysql -u root -p < database/02_create_app_user.sql
mysql -u root -p < database/03_insert_sample_data.sql


### 3. Application Database User

CREATE USER 'legal_case_user'@'localhost' IDENTIFIED BY '********';
GRANT ALL PRIVILEGES ON legal_case_roster_db.* TO 'legal_case_user'@'localhost';
FLUSH PRIVILEGES;


### 4. App Configuration

pp_framework/config/legal_case_app_config.json:

- Points to legal_case_roster_db

- Uses legal_case_user credentials

- Configures the connection pool and log prefix


### 5. Run the Application


pipenv run python src/main.py -c config/legal_case_app_config.json


On success you should see debug messages indicating:

- MySQL connection pool created

- App services initialized

- User interface started



If anything in there doesn’t match your real usernames/db names, adjust it.

### Step 2: Commit the README changes

In **Git Bash** from the project root:

```bash
cd ~/legal_case_counsel_roster
git status  # verify README.md is modified
git add README.md
git commit -m "Document database setup and run instructions"
git push origin dev-legal-case


Now your PR shows:

- schema script

- app user script

- sample data script

- config file

- documentation


*****************************************************************************************************


# it566_project_app_framework
Application framework for semester project.

## Instructions

- Create your project GitHub repository
- Clone your repository to your local machine
- Copy the contents of the app_framework directory to your repository directory
- Begin work on your project

## Create Virtual Environment with PipEnv

- pipenv --python 3.12 
- pipenv install

## Miscellaneous Notes

- **Windows Segmentation Fault when Creating MySQL Pooled Connection**
    - PROBLEM: Windows users might get a Segmentation Fault when attempting to create the MySQLConnection pool in the MySQLPersistenceWrapper class. This does not seem to affect MacOS or Linux users. The problem stems from incompatible C binaries related to the mysql-connector-python package.
    - SOLUTION: I have added a `"use_pure": true` to the configuration file's "database":"pool" section. I have modified the `MySQLPersistenceWrapper._initialize_database_connection_pool()` method to use this setting in the MySQLConnectionPool() constructor.
    - Linux and MacOS users should be able to set `"use_pure": false`.
    - Windows users can try `"use_pure": false` but if you receive the Segmentation Fault error set `"use_pure": true`.
    _ I have tested this on Windows 10 Pro, Linux Debian, and MacOS 26 and 10.15.7 Catalina 
