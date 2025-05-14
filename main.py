from tkinter import *
from tkinter import messagebox, ttk
from dbTransaction import dbTransactions
from PIL import Image, ImageTk

db = None

# Main Window
mainWindow = Tk()
mainWindow.title("Bangalore Bike Rental | Main Menu")
mainWindow.geometry("1080x720+10+10")
mainWindow.resizable(False, False)
mainWindow.configure(background="light yellow")

# Connect DB
try:
    db = dbTransactions("localhost", "root", "Aditya@2003", "bike_rental_db")
except Exception as e:
    messagebox.showwarning("Database Error", f"Failed to connect to database!\n{e}")
    db = None

myFont = ("Arial", 12, "bold")

# Add Customer
def customerScreen():
    window = Toplevel()
    window.title("Add Customer")
    window.geometry("700x350+150+150")

    def saveCustomer():
        if db:
            db.setCustomer(
                name_var.get(), surname_var.get(), id_var.get(), dob_var.get(),
                address_var.get(), phone_var.get(), job_var.get(), license_var.get(),
                marital_var.get(), education_var.get()
            )
            messagebox.showinfo("Success", "Customer added.")
            window.destroy()
        else:
            messagebox.showerror("Error", "Database not connected.")

    # Input vars
    name_var, surname_var, id_var = StringVar(), StringVar(), StringVar()
    dob_var, address_var, phone_var = StringVar(), StringVar(), StringVar()
    job_var, license_var, marital_var, education_var = StringVar(), StringVar(), StringVar(), StringVar()

    fields = [
        ("First Name", name_var), ("Last Name", surname_var), ("ID Number", id_var),
        ("Date of Birth (YYYY-MM-DD)", dob_var), ("Address", address_var), ("Phone Number", phone_var),
        ("Occupation", job_var), ("License Class", license_var),
        ("Marital Status", marital_var), ("Education Level", education_var)
    ]

    for i, (label, var) in enumerate(fields):
        Label(window, text=label).grid(row=i, column=0)
        Entry(window, textvariable=var).grid(row=i, column=1)

    Button(window, text="Save Customer", command=saveCustomer).grid(row=len(fields), columnspan=2, pady=10)
    window.mainloop()

# Add Bike
def addBikeScreen():
    window = Toplevel()
    window.title("Add Bike")
    window.geometry("400x600+100+100")

    def saveBike():
        if db:
            db.setBike(
                type_var.get(), brand_var.get(), model_var.get(), year_var.get(),
                fuel_var.get(), gear_var.get(), power_var.get(), engine_var.get(),
                color_var.get(), engine_no_var.get(), chassis_no_var.get(),
                daily_fee_var.get(), rent_status_var.get(), usage_status_var.get()
            )
            messagebox.showinfo("Saved", "Bike saved.")
            window.destroy()
        else:
            messagebox.showerror("Error", "Database not connected.")

    # Inputs
    type_var, brand_var, model_var, year_var = StringVar(), StringVar(), StringVar(), StringVar()
    fuel_var, gear_var, power_var, engine_var = StringVar(), StringVar(), StringVar(), StringVar()
    color_var, engine_no_var, chassis_no_var = StringVar(), StringVar(), StringVar()
    daily_fee_var = IntVar()
    rent_status_var, usage_status_var = StringVar(), StringVar()

    fields = [
        ("Bike Type", type_var), ("Brand", brand_var), ("Model", model_var),
        ("Year", year_var), ("Fuel Type", fuel_var), ("Gear Type", gear_var),
        ("Engine Power", power_var), ("Engine Capacity", engine_var),
        ("Color", color_var), ("Engine Number", engine_no_var),
        ("Chassis Number", chassis_no_var), ("Daily Rent Fee", daily_fee_var),
        ("Rent Status (Available/Not Available)", rent_status_var),
        ("Usage Status (Usable/Not Usable)", usage_status_var)
    ]

    for i, (label, var) in enumerate(fields):
        Label(window, text=label).grid(row=i, column=0, pady=3, padx=5, sticky=W)
        Entry(window, textvariable=var).grid(row=i, column=1, pady=3, padx=5)

    Button(window, text="Save Bike", command=saveBike).grid(row=len(fields), columnspan=2, pady=10)
    window.mainloop()

# Rent Bike
def rentBikeScreen():
    window = Toplevel()
    window.title("Rent a Bike")
    window.geometry("500x300+150+150")

    if not db:
        messagebox.showerror("Error", "Database not connected.")
        return

    customers = db.getCustomers()
    bikes = db.getBikes()

    selected_customer = StringVar()
    selected_bike = StringVar()
    rental_days = IntVar()
    destination = StringVar()
    total_cost_var = StringVar()

    def calculateAndSave():
        cust_id = selected_customer.get().split()[0]
        bike_id = selected_bike.get().split()[0]
        days = rental_days.get()
        dest = destination.get()

        fee = db.getFee(bike_id)[0][0]
        total = fee * days
        total_cost_var.set(f"{total} INR")

        db.setRent(cust_id, bike_id, days, dest)
        db.updateRent(bike_id)

        messagebox.showinfo("Rented", f"Rental created. Total = ₹{total}")
        window.destroy()

    Label(window, text="Select Customer").pack()
    ttk.Combobox(window, textvariable=selected_customer, values=[f"{c[0]} {c[1]} {c[2]}" for c in customers]).pack()

    Label(window, text="Select Bike").pack()
    ttk.Combobox(window, textvariable=selected_bike, values=[f"{b[0]} {b[1]} {b[2]}" for b in bikes]).pack()

    Label(window, text="Number of Days").pack()
    Entry(window, textvariable=rental_days).pack()

    Label(window, text="Destination").pack()
    Entry(window, textvariable=destination).pack()

    Label(window, text="Total Fee:").pack()
    Label(window, textvariable=total_cost_var).pack()

    Button(window, text="Confirm Rental", command=calculateAndSave).pack(pady=10)
    window.mainloop()

# Return Bike
def returnBikeScreen():
    window = Toplevel()
    window.title("Return Bike")
    window.geometry("500x300+150+150")

    if not db:
        messagebox.showerror("Error", "Database not connected.")
        return

    rentals = db.getRentals()
    rental_options = [f"{r[7]}: {r[3]} {r[4]} → {r[1]} ({r[2]})" for r in rentals]
    rental_var = StringVar()

    Label(window, text="Select Rental to Return").pack(pady=10)
    combo = ttk.Combobox(window, textvariable=rental_var, values=rental_options)
    combo.pack()

    def processReturn():
        selected = rental_var.get()
        if not selected:
            messagebox.showwarning("Missing", "Select a rental to return.")
            return
        rental_id = int(selected.split(":")[0])
        bike_id = [r for r in rentals if r[7] == rental_id][0][0]
        db.returnBike(rental_id, bike_id)
        messagebox.showinfo("Returned", "Bike returned successfully.")
        window.destroy()

    Button(window, text="Return Bike", command=processReturn).pack(pady=20)
    window.mainloop()

# Rental Listing
def rentalListScreen():
    window = Toplevel()
    window.title("Current Rentals")
    window.geometry("800x600+100+100")

    if not db:
        messagebox.showerror("Error", "Database not connected.")
        return

    rentals = db.getRentals()
    for i, r in enumerate(rentals):
        bike = f"{r[1]} {r[2]}"
        customer = f"{r[3]} {r[4]}"
        days = r[5]
        cost = r[6]
        Label(window, text=f"{i+1}. {bike} rented to {customer} for {days} days. ₹{cost}", font="Arial 10").pack(anchor='w', padx=10, pady=5)

    window.mainloop()

# Search
def searchCustomerScreen():
    window = Toplevel()
    window.title("Search Customer")
    window.geometry("500x300+150+150")
    search_var = StringVar()

    def search():
        if not db:
            messagebox.showerror("Error", "Database not connected.")
            return
        results = db.searchCustomer(search_var.get())
        for r in results:
            Label(window, text=f"Name: {r[0]}, License: {r[1]}").pack(anchor='w')

    Label(window, text="Enter Name to Search:").pack()
    Entry(window, textvariable=search_var).pack()
    Button(window, text="Search", command=search).pack(pady=5)
    window.mainloop()

# Add logo/image (optional)
try:
    logo_img = Image.open("archive/bike-logo2.jpg")
    logo_img = logo_img.resize((600, 400))
    logo = ImageTk.PhotoImage(logo_img)
    Label(mainWindow, image=logo, bg="white").place(x=400, y=160)
except:
    pass

# Buttons
Button(mainWindow, text="Add Customer", command=customerScreen, font=myFont, bg="#0A2647", fg="white", width=20, height=2).place(x=100, y=150)
Button(mainWindow, text="Add Bike", command=addBikeScreen, font=myFont, bg="#0A2647", fg="white", width=20, height=2).place(x=100, y=230)
Button(mainWindow, text="Rent a Bike", command=rentBikeScreen, font=myFont, bg="#0A2647", fg="white", width=20, height=2).place(x=100, y=310)
Button(mainWindow, text="View Rentals", command=rentalListScreen, font=myFont, bg="#0A2647", fg="white", width=20, height=2).place(x=100, y=390)
Button(mainWindow, text="Search Customer", command=searchCustomerScreen, font=myFont, bg="#0A2647", fg="white", width=20, height=2).place(x=100, y=470)
Button(mainWindow, text="Return Bike", command=returnBikeScreen, font=myFont, bg="#0A2647", fg="white", width=20, height=2).place(x=100, y=550)

mainWindow.mainloop()
