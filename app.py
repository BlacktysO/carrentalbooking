from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Sample data (replace with a database in production)
cars = [
    {"id": 1, "make": "Toyota", "model": "Camry", "year": 2022, "daily_price": 50, "is_available": True},
    {"id": 2, "make": "Honda", "model": "Civic", "year": 2023, "daily_price": 45, "is_available": True},
]

customers = []
bookings = []

# Homepage
@app.route("/")
def index():
    return render_template("index.html")

# Available Cars
@app.route("/cars")
def show_cars():
    return render_template("cars.html", cars=cars)

# Register Customer
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        customer_id = int(request.form["customer_id"])
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]

        # Check if customer already exists
        if any(cust["id"] == customer_id for cust in customers):
            flash("Customer ID already exists!", "error")
            return redirect(url_for("register"))

        # Add new customer
        customers.append({
            "id": customer_id,
            "name": name,
            "email": email,
            "phone": phone
        })
        flash("Customer registered successfully!", "success")
        return redirect(url_for("index"))

    return render_template("register.html")

# Create Booking
@app.route("/book", methods=["GET", "POST"])
def book():
    if request.method == "POST":
        customer_id = int(request.form["customer_id"])
        car_id = int(request.form["car_id"])
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        # Find car and customer
        car = next((car for car in cars if car["id"] == car_id), None)
        customer = next((cust for cust in customers if cust["id"] == customer_id), None)

        if not car or not car["is_available"]:
            flash("Car not available!", "error")
            return redirect(url_for("book"))

        if not customer:
            flash("Customer not found!", "error")
            return redirect(url_for("book"))

        # Calculate total price
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        days = (end - start).days
        total_price = days * car["daily_price"]

        # Add booking
        bookings.append({
            "car": car,
            "customer": customer,
            "start_date": start_date,
            "end_date": end_date,
            "total_price": total_price
        })

        # Mark car as unavailable
        car["is_available"] = False
        flash(f"Booking successful! Total: ${total_price}", "success")
        return redirect(url_for("index"))

    return render_template("book.html", cars=cars, customers=customers)

if __name__ == "__main__":
    app.run(debug=True)