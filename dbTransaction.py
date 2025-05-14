import mysql.connector
from tkinter import messagebox

class dbTransactions:
    def __init__(self, host, user, password, dbname):
        self.host = host
        self.user = user
        self.password = password
        self.dbname = dbname
        self.connection = None

        self.connectDatabase()
        self.createTables()

    def connectDatabase(self):
        try:
            db = mysql.connector.connect(host=self.host, user=self.user, password=self.password)
            cursor = db.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.dbname}")
            db.close()
            self.connection = mysql.connector.connect(
                host=self.host, user=self.user, password=self.password, database=self.dbname
            )
            messagebox.showinfo("Database", "Connected to database successfully!")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Error: {e}")

    def createTables(self):
        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                id_number VARCHAR(15) UNIQUE,
                dob DATE,
                address TEXT,
                phone VARCHAR(15) UNIQUE,
                job VARCHAR(50),
                license_class VARCHAR(5),
                marital_status VARCHAR(20),
                education VARCHAR(50)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bikes (
                bike_id INT AUTO_INCREMENT PRIMARY KEY,
                type VARCHAR(50),
                brand VARCHAR(50),
                model VARCHAR(50),
                year YEAR,
                fuel_type VARCHAR(20),
                gear_type VARCHAR(20),
                engine_power VARCHAR(20),
                engine_capacity VARCHAR(20),
                color VARCHAR(30),
                engine_no VARCHAR(20) UNIQUE,
                chassis_no VARCHAR(20) UNIQUE,
                daily_rent INT,
                rental_status VARCHAR(20),
                usage_status VARCHAR(20)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rentals (
                rental_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT,
                bike_id INT,
                days INT,
                destination VARCHAR(100),
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                FOREIGN KEY (bike_id) REFERENCES bikes(bike_id)
            )
        """)

        self.connection.commit()

    def setCustomer(self, first, last, idno, dob, address, phone, job, license_class, marital, education):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO customers 
            (first_name, last_name, id_number, dob, address, phone, job, license_class, marital_status, education)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (first, last, idno, dob, address, phone, job, license_class, marital, education))
        self.connection.commit()

    def getCustomers(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT customer_id, first_name, last_name FROM customers")
        return cursor.fetchall()

    def setBike(self, type_, brand, model, year, fuel, gear, power, engine_cap, color, engine_no, chassis_no, daily_fee, rent_status, usage_status):
        cursor = self.connection.cursor()
        try:
            year = int(year)  # Convert to int to avoid MySQL YEAR error
        except:
            messagebox.showerror("Input Error", "Year must be a 4-digit number.")
            return
        cursor.execute("""
            INSERT INTO bikes
            (type, brand, model, year, fuel_type, gear_type, engine_power, engine_capacity, color, engine_no, chassis_no, daily_rent, rental_status, usage_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (type_, brand, model, year, fuel, gear, power, engine_cap, color, engine_no, chassis_no, daily_fee, rent_status, usage_status))
        self.connection.commit()

    def getBikes(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT bike_id, brand, model FROM bikes WHERE rental_status='Available' AND usage_status='Usable'")
        return cursor.fetchall()

    def getFee(self, bike_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT daily_rent FROM bikes WHERE bike_id = %s", (bike_id,))
        return cursor.fetchall()

    def setRent(self, customer_id, bike_id, days, destination):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO rentals (customer_id, bike_id, days, destination)
            VALUES (%s, %s, %s, %s)
        """, (customer_id, bike_id, days, destination))
        self.connection.commit()

    def getRentals(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT b.bike_id, b.brand, b.model, c.first_name, c.last_name, r.days, r.days * b.daily_rent, r.rental_id
            FROM rentals r
            JOIN customers c ON r.customer_id = c.customer_id
            JOIN bikes b ON r.bike_id = b.bike_id
        """)
        return cursor.fetchall()

    def updateRent(self, bike_id):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE bikes SET rental_status = 'Not Available' WHERE bike_id = %s", (bike_id,))
        self.connection.commit()

    def returnBike(self, rental_id, bike_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM rentals WHERE rental_id = %s", (rental_id,))
        cursor.execute("UPDATE bikes SET rental_status = 'Available' WHERE bike_id = %s", (bike_id,))
        self.connection.commit()

    def searchCustomer(self, name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT first_name, license_class FROM customers WHERE first_name LIKE %s", (name + "%",))
        return cursor.fetchall()
