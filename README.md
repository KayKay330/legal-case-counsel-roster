
# Legal Case Counsel Roster  
A modular, multi-layer Python application that manages lawyers, legal cases, and lawyer–case assignments using a MySQL backend.  
Designed using clean architecture principles with separation of concerns across **Presentation**, **Service**, **Persistence**, and **Database** layers.

---

## Project Overview
This application provides a command-line interface that allows users to:

- Create, read, update, and delete (CRUD) **lawyers**
- Create, read, update, and delete **cases**
- Assign lawyers to cases with role + billable hours
- View a complete case including all assigned lawyers
- Interact with a MySQL database via connection pooling
- Initialize the database with sample data using shell scripts

The project fulfills the full assessment requirements, including **modular design**, **service abstraction**, **database persistence**, and **complete CRUD functionality**.

---

## System Architecture  
The system is structured into four layers:

- **Presentation Layer** → UserInterface  
- **Service Layer** → AppServices  
- **Persistence Layer** → MySQLPersistenceWrapper  
- **Database Layer** → MySQL schema + tables  

---

## Features

###  Lawyer Management  
- Add new lawyers  
- List all lawyers  
- Update lawyer info  
- Safe delete (with confirmation)

### Case Management  
- Add new cases  
- List all cases  
- Update case info  
- Safe delete (with confirmation)

###  Lawyer–Case Relationship  
- Assign lawyer to a case  
- Select role and billable hours  
- View a case and all associated lawyers

### Database Layer  
- MySQL schema  
- Connection pooling  
- Database initialization via scripts  
- Fully normalized tables:
  - `lawyer`
  - `legal_case`
  - `case_lawyer_xref`

---



