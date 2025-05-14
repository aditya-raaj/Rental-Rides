<div align="center">
  
# 🚲 Rental Rides : Bangalore Bike Rental System

A complete desktop-based DBMS project to manage bike rentals using Python, Tkinter, and MySQL.

[![Made with Python](https://img.shields.io/badge/Made%20With-Python-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/Database-MySQL-blue?style=for-the-badge&logo=mysql)](https://www.mysql.com/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-%232C3E50?style=for-the-badge)]()
[![Workbench](https://img.shields.io/badge/MySQL-Workbench-00758F?style=for-the-badge&logo=mysql)](https://www.mysql.com/products/workbench/)
[![MIT License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

![Home](https://github.com/aditya-raaj/Rental-Rides/blob/main/archive/main%20menu.png)
*(Dashboard preview showcasing Home page)*

![Rentals](https://github.com/aditya-raaj/Rental-Rides/blob/main/archive/currentRentals.png)

*(Dialog box showcasing the rentals)*



</div>


## Features

- Add, search, and manage customer records
- Add, manage, and track bikes
- Create rentals with automatic fee calculation
- Return bikes and update availability
- Attractive GUI built with Tkinter + PIL
- Modular architecture using MVC principles

---

## Tech Stack

- **Python 3.10+**
- **Tkinter** (GUI)
- **MySQL + Workbench**
- **mysql-connector-python**
- **Pillow (PIL)** for images

---

## 🔢 Database Design
This project uses a relational database schema designed in MySQL, featuring three normalized tables and proper use of primary and foreign keys to maintain integrity.

### Schema Overview
 - ```customers```: Stores customer profiles
 - ```bikes```: Stores bike inventory
 - ```rentals```: Links customers to bikes with rental metadata

### DBMS Concepts Used
1. Primary Key : ```customer_id```, ```bike_id```, ```rental_id``` uniquely identify rows
2. Foreign Key : ```rentals.customer_id → customers.customer_id``` , ```rentals.bike_id → bikes.bike_id```
3. Normalization : Data split across entities to eliminate redundancy
4. Joins : Used to fetch complete rental info with bike + customer data
5. Constraints : ```UNIQUE``` on ID number, engine no., phone
6. Data Types : Optimal types (e.g., ```YEAR```, ```VARCHAR```, ```INT```, ```DATE```)


### Key Points:
 - Rental fee is not stored but calculated live as: ```days * bikes.daily_rent```
 - Engine and chassis numbers are unique, mimicking real vehicle IDs
 - Deleting a rental frees the bike by setting its status back to "Available"


---
![Joins](https://github.com/aditya-raaj/Rental-Rides/blob/main/diagrams/connections.png)

![Tables](https://github.com/aditya-raaj/Rental-Rides/blob/main/diagrams/tables.png)

---


## 🔧 How to Install

```bash
pip install mysql-connector-python pillow
```

 Start MySQL - mySQL Workbench ( used by me )

 ---

## How to Run
1. Clone or download the repo.
2. Open main.py
3. Ensure database credentials match your MySQL setup.

Run:
```bash
python main.py
```

---
## 🙋‍♂️ Developer
- [Aditya Raj](https://www.linkedin.com/in/aditya-lin/)
