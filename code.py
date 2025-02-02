import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Car Class
class Car:
    def __init__(self, car_id, make, model, year, daily_price):
        self.car_id = car_id
        self.make = make
        self.model = model
        self.year = year
        self.daily_price = daily_price
        self.is_available = True

    def __str__(self):
        return f"{self.year} {self.make} {self.model} (${self.daily_price}/day)"

# Customer Class
class Customer:
    def __init__(self, customer_id, name, email, phone):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone

    def __str__(self):
        return f"{self.name} ({self.email})"

# Booking Class
class Booking:
    def __init__(self, car, customer, start_date, end_date):
        self.car = car
        self.customer = customer
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d")
        self.total_price = self.calculate_price()

    def calculate_price(self):
        days = (self.end_date - self.start_date).days
        return days * self.car.daily_price

    def __str__(self):
        return (f"Booking: {self.car}\n"
                f"Customer: {self.customer}\n"
                f"Dates: {self.start_date.strftime('%Y-%m-%d')} to {self.end_date.strftime('%Y-%m-%d')}\n"
                f"Total: ${self.total_price}")

# Car Rental System Class
class CarRentalSystem:
    def __init__(self):
        self.cars = []
        self.customers = []
        self.bookings = []

    def add_car(self, car):
        self.cars.append(car)

    def add_customer(self, customer):
        self.customers.append(customer)

    def search_available_cars(self):
        return [car for car in self.cars if car.is_available]

    def create_booking(self, customer_id, car_id, start_date, end_date):
        customer = next((c for c in self.customers if c.customer_id == customer_id), None)
        car = next((c for c in self.cars if c.car_id == car_id), None)

        if not car or not car.is_available:
            return "Car not available"
        if not customer:
            return "Customer not found"

        booking = Booking(car, customer, start_date, end_date)
        car.is_available = False
        self.bookings.append(booking)
        return booking

# GUI Application
class CarRentalApp:
    def __init__(self, root):
        self.root = root
        self.system = CarRentalSystem()
        self.root.title("Car Rental Booking System")
        self.root.geometry("800x600")

        # Initialize sample data
        self._initialize_sample_data()

        # Create tabs
        self.tab_control = ttk.Notebook(root)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab3 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text="Available Cars")
        self.tab_control.add(self.tab2, text="Register Customer")
        self.tab_control.add(self.tab3, text="Create Booking")
        self.tab_control.pack(expand=1, fill="both")

        # Available Cars Tab
        self.car_tree = ttk.Treeview(self.tab1, columns=("ID", "Make", "Model", "Year", "Price"), show="headings")
        self.car_tree.heading("ID", text="ID")
        self.car_tree.heading("Make", text="Make")
        self.car_tree.heading("Model", text="Model")
        self.car_tree.heading("Year", text="Year")
        self.car_tree.heading("Price", text="Price/Day")
        self.car_tree.pack(fill="both", expand=True)
        self.update_car_list()

        # Register Customer Tab
        ttk.Label(self.tab2, text="Customer ID:").grid(row=0, column=0, padx=10, pady=10)
        self.customer_id_entry = ttk.Entry(self.tab2)
        self.customer_id_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.tab2, text="Name:").grid(row=1, column=0, padx=10, pady=10)
        self.name_entry = ttk.Entry(self.tab2)
        self.name_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.tab2, text="Email:").grid(row=2, column=0, padx=10, pady=10)
        self.email_entry = ttk.Entry(self.tab2)
        self.email_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(self.tab2, text="Phone:").grid(row=3, column=0, padx=10, pady=10)
        self.phone_entry = ttk.Entry(self.tab2)
        self.phone_entry.grid(row=3, column=1, padx=10, pady=10)

        ttk.Button(self.tab2, text="Register", command=self.register_customer).grid(row=4, column=0, columnspan=2, pady=10)

        # Create Booking Tab
        ttk.Label(self.tab3, text="Customer ID:").grid(row=0, column=0, padx=10, pady=10)
        self.booking_customer_id_entry = ttk.Entry(self.tab3)
        self.booking_customer_id_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.tab3, text="Car ID:").grid(row=1, column=0, padx=10, pady=10)
        self.booking_car_id_entry = ttk.Entry(self.tab3)
        self.booking_car_id_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.tab3, text="Start Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=10)
        self.start_date_entry = ttk.Entry(self.tab3)
        self.start_date_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(self.tab3, text="End Date (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=10)
        self.end_date_entry = ttk.Entry(self.tab3)
        self.end_date_entry.grid(row=3, column=1, padx=10, pady=10)

        ttk.Button(self.tab3, text="Create Booking", command=self.create_booking).grid(row=4, column=0, columnspan=2, pady=10)

    def _initialize_sample_data(self):
        self.system.add_car(Car(1, "Toyota", "Camry", 2022, 50))
        self.system.add_car(Car(2, "Honda", "Civic", 2023, 45))
        self.system.add_customer(Customer(101, "John Doe", "john@example.com", "555-1234"))

    def update_car_list(self):
        for row in self.car_tree.get_children():
            self.car_tree.delete(row)
        for car in self.system.search_available_cars():
            self.car_tree.insert("", "end", values=(car.car_id, car.make, car.model, car.year, car.daily_price))

    def register_customer(self):
        try:
            customer_id = int(self.customer_id_entry.get())
            name = self.name_entry.get()
            email = self.email_entry.get()
            phone = self.phone_entry.get()

            if not name or not email or not phone:
                messagebox.showwarning("Input Error", "Please fill all fields")
                return

            self.system.add_customer(Customer(customer_id, name, email, phone))
            messagebox.showinfo("Success", "Customer registered successfully!")
        except ValueError:
            messagebox.showerror("Input Error", "Invalid customer ID")

    def create_booking(self):
        try:
            customer_id = int(self.booking_customer_id_entry.get())
            car_id = int(self.booking_car_id_entry.get())
            start_date = self.start_date_entry.get()
            end_date = self.end_date_entry.get()

            result = self.system.create_booking(customer_id, car_id, start_date, end_date)
            if isinstance(result, Booking):
                messagebox.showinfo("Success", "Booking created successfully!")
                self.update_car_list()
            else:
                messagebox.showerror("Error", result)
        except ValueError:
            messagebox.showerror("Input Error", "Invalid input values")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = CarRentalApp(root)
    root.mainloop()