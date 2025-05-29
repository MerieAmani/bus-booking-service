from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Bus, Route, Trip, Booking, Payment
import hashlib
from datetime import datetime
from tabulate import tabulate
import sys

def generate_password_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def print_table(items, headers):
    """Helper function to print tabular data"""
    if not items:
        print("No records found")
        return
    print(tabulate(items, headers=headers, tablefmt="grid"))
    
#USER MENU

def user_menu(db: Session):
    while True:
        print("\n=== User Operations ===")
        print("1. Create User")
        print("2. List All Users")
        print("3. View User Details")
        print("4. Update User")
        print("5. Delete User")
        print("6. View User's Bookings")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("\nCreate New User:")
            username = input("Username: ")
            if db.query(User).filter(User.username == username).first():
                print("❌ Username already exists")
                continue
            email = input("Email: ")
            password = generate_password_hash(input("Password: "))
            full_name = input("Full Name (optional): ") or None
            user = User(
                username=username,
                email=email,
                password_hash=password,
                full_name=full_name
            )
            db.add(user)
            db.commit()
            print(f"✅ User created with ID: {user.id}")

        elif choice == '2':
            users = db.query(User).all()
            print_table(
                [(u.id, u.username, u.email) for u in users],
                ["ID", "Username", "Email"]
            )

        elif choice == '3':
            user_id = int(input("Enter User ID: "))
            user = db.query(User).get(user_id)
            if user:
                print(f"\nUser Details (ID: {user.id})")
                print(f"Username: {user.username}")
                print(f"Email: {user.email}")
                print(f"Full Name: {user.full_name or 'Not provided'}")
                print(f"Total Bookings: {len(user.bookings)}")
            else:
                print("❌ User not found")

        elif choice == '4':
            user_id = int(input("Enter User ID to update: "))
            user = db.query(User).get(user_id)
            if not user:
                print("❌ User not found")
                continue
            print("\nLeave blank to keep current value")
            username = input(f"New username [{user.username}]: ") or user.username
            email = input(f"New email [{user.email}]: ") or user.email
            full_name = input(f"New full name [{user.full_name or ''}]: ") or user.full_name
            user.username = username
            user.email = email
            user.full_name = full_name or None
            db.commit()
            print("✅ User updated successfully")

        elif choice == '5':
            user_id = int(input("Enter User ID to delete: "))
            user = db.query(User).get(user_id)
            if not user:
                print("❌ User not found")
                continue
            db.delete(user)
            db.commit()
            print("✅ User deleted successfully")

        elif choice == '6':
            user_id = int(input("Enter User ID: "))
            user = db.query(User).get(user_id)
            if user:
                print(f"\nBookings for {user.username}:")
                bookings = []
                for b in user.bookings:
                    bookings.append((
                        b.id,
                        b.trip.route.origin if b.trip and b.trip.route else "N/A",
                        b.trip.route.destination if b.trip and b.trip.route else "N/A",
                        b.trip.departure_time.strftime("%Y-%m-%d %H:%M") if b.trip else "N/A",
                        b.seat_number,
                        b.status
                    ))
                print_table(
                    bookings,
                    ["Booking ID", "From", "To", "Departure", "Seat", "Status"]
                )
            else:
                print("❌ User not found")

        elif choice == '0':
            break

#BUS MENU

def bus_menu(db: Session):
    while True:
        print("\n=== Bus Operations ===")
        print("1. Add New Bus")
        print("2. List All Buses")
        print("3. View Bus Schedule")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("\nAdd New Bus:")
            number_plate = input("Number Plate: ")
            if db.query(Bus).filter(Bus.number_plate == number_plate).first():
                print("❌ Bus with this number plate already exists")
                continue
            model = input("Model: ")
            capacity = int(input("Capacity: "))
            bus = Bus(
                number_plate=number_plate,
                model=model,
                capacity=capacity
            )
            db.add(bus)
            db.commit()
            print(f"✅ Bus added with ID: {bus.id}")

        elif choice == '2':
            buses = db.query(Bus).all()
            print_table(
                [(b.id, b.number_plate, b.model, b.capacity) for b in buses],
                ["ID", "Number Plate", "Model", "Capacity"]
            )

        elif choice == '3':
            bus_id = int(input("Enter Bus ID: "))
            bus = db.query(Bus).get(bus_id)
            if bus:
                print(f"\nSchedule for Bus {bus.number_plate}:")
                trips = []
                for t in bus.trips:
                    trips.append((
                        t.id,
                        t.route.origin if t.route else "N/A",
                        t.route.destination if t.route else "N/A",
                        t.departure_time.strftime("%Y-%m-%d %H:%M"),
                        t.available_seats
                    ))
                print_table(
                    trips,
                    ["Trip ID", "From", "To", "Departure", "Available Seats"]
                )
            else:
                print("❌ Bus not found")

        elif choice == '0':
            break

#ROUTE MENU

def route_menu(db: Session):
    while True:
        print("\n=== Route Operations ===")
        print("1. Add New Route")
        print("2. List All Routes")
        print("3. View Route Trips")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("\nAdd New Route:")
            origin = input("Origin: ")
            destination = input("Destination: ")
            if db.query(Route).filter(
                Route.origin == origin,
                Route.destination == destination
            ).first():
                print("❌ Route already exists")
                continue
            distance_km = int(input("Distance (km): "))
            estimated_duration = input("Estimated Duration (e.g., '6 hours'): ")
            route = Route(
                origin=origin,
                destination=destination,
                distance_km=distance_km,
                estimated_duration=estimated_duration
            )
            db.add(route)
            db.commit()
            print(f"✅ Route added with ID: {route.id}")

        elif choice == '2':
            routes = db.query(Route).all()
            print_table(
                [(r.id, r.origin, r.destination, f"{r.distance_km}km", r.estimated_duration) 
                 for r in routes],
                ["ID", "From", "To", "Distance", "Duration"]
            )

        elif choice == '3':
            route_id = int(input("Enter Route ID: "))
            route = db.query(Route).get(route_id)
            if route:
                print(f"\nTrips for {route.origin} → {route.destination}:")
                trips = []
                for t in route.trips:
                    trips.append((
                        t.id,
                        t.bus.number_plate if t.bus else "N/A",
                        t.departure_time.strftime("%Y-%m-%d %H:%M"),
                        t.arrival_time.strftime("%Y-%m-%d %H:%M"),
                        t.available_seats
                    ))
                print_table(
                    trips,
                    ["Trip ID", "Bus", "Departure", "Arrival", "Available Seats"]
                )
            else:
                print("❌ Route not found")

        elif choice == '0':
            break

#TRIP MENU

def trip_menu(db: Session):
    while True:
        print("\n=== Trip Operations ===")
        print("1. Schedule New Trip")
        print("2. List All Trips")
        print("3. View Trip Details")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("\nSchedule New Trip:")
            routes = db.query(Route).all()
            print("\nAvailable Routes:")
            print_table(
                [(r.id, r.origin, r.destination) for r in routes],
                ["ID", "From", "To"]
            )
            route_id = int(input("Select Route ID: "))
            buses = db.query(Bus).all()
            print("\nAvailable Buses:")
            print_table(
                [(b.id, b.number_plate, b.model, b.capacity) for b in buses],
                ["ID", "Number Plate", "Model", "Capacity"]
            )
            bus_id = int(input("Select Bus ID: "))
            departure_time = datetime.strptime(
                input("Departure (YYYY-MM-DD HH:MM): "),
                "%Y-%m-%d %H:%M"
            )
            arrival_time = datetime.strptime(
                input("Arrival (YYYY-MM-DD HH:MM): "),
                "%Y-%m-%d %H:%M"
            )
            bus = db.query(Bus).get(bus_id)
            if not bus:
                print("❌ Bus not found")
                continue
            trip = Trip(
                route_id=route_id,
                bus_id=bus_id,
                departure_time=departure_time,
                arrival_time=arrival_time,
                available_seats=bus.capacity
            )
            db.add(trip)
            db.commit()
            print(f"✅ Trip scheduled with ID: {trip.id}")

        elif choice == '2':
            trips = db.query(Trip).all()
            print("\nAll Scheduled Trips:")
            trip_data = []
            for t in trips:
                trip_data.append((
                    t.id,
                    t.route.origin if t.route else "N/A",
                    t.route.destination if t.route else "N/A",
                    t.bus.number_plate if t.bus else "N/A",
                    t.departure_time.strftime("%Y-%m-%d %H:%M"),
                    t.available_seats
                ))
            print_table(
                trip_data,
                ["Trip ID", "From", "To", "Bus", "Departure", "Available Seats"]
            )

        elif choice == '3':
            trip_id = int(input("Enter Trip ID: "))
            trip = db.query(Trip).get(trip_id)
            if trip:
                print(f"\nTrip Details (ID: {trip.id})")
                print(f"Route: {trip.route.origin if trip.route else 'N/A'} → {trip.route.destination if trip.route else 'N/A'}")
                print(f"Bus: {trip.bus.number_plate if trip.bus else 'N/A'}")
                print(f"Departure: {trip.departure_time}")
                print(f"Arrival: {trip.arrival_time}")
                print(f"Available Seats: {trip.available_seats}")
            else:
                print("❌ Trip not found")

        elif choice == '0':
            break

#BOOKING MENU

def booking_menu(db: Session):
    while True:
        print("\n=== Booking Operations ===")
        print("1. Create Booking")
        print("2. List All Bookings")
        print("3. Cancel Booking")
        print("4. View Booking Details")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("\nCreate New Booking:")
            users = db.query(User).all()
            print("\nUsers:")
            print_table(
                [(u.id, u.username) for u in users],
                ["ID", "Username"]
            )
            user_id = int(input("Select User ID: "))
            trips = db.query(Trip).all()
            print("\nAvailable Trips:")
            trip_data = []
            for t in trips:
                trip_data.append((
                    t.id,
                    t.route.origin if t.route else "N/A",
                    t.route.destination if t.route else "N/A",
                    t.departure_time.strftime("%Y-%m-%d %H:%M"),
                    t.available_seats
                ))
            print_table(
                trip_data,
                ["Trip ID", "From", "To", "Departure", "Available Seats"]
            )
            trip_id = int(input("Select Trip ID: "))
            trip = db.query(Trip).get(trip_id)
            if not trip:
                print("❌ Trip not found")
                continue
            available_seats = set(range(1, trip.bus.capacity + 1)) - {
                b.seat_number for b in trip.bookings
            }
            print(f"\nAvailable seats: {sorted(available_seats)}")
            seat_number = int(input("Select seat number: "))
            if seat_number not in available_seats:
                print("❌ Seat not available")
                continue
            booking = Booking(
                user_id=user_id,
                trip_id=trip_id,
                seat_number=seat_number,
                status="confirmed"
            )
            db.add(booking)
            payment_amount = trip.route.distance_km * 2.5 if trip.route else 0
            payment = Payment(
                booking=booking,
                amount=payment_amount,
                status="pending"
            )
            db.add(payment)
            db.commit()
            print(f"✅ Booking created! ID: {booking.id}")
            print(f"Payment due: {payment_amount:.2f}")

        elif choice == '2':
            bookings = db.query(Booking).all()
            print("\nAll Bookings:")
            booking_data = []
            for b in bookings:
                booking_data.append((
                    b.id,
                    b.user.username if b.user else "N/A",
                    f"{b.trip.route.origin if b.trip and b.trip.route else 'N/A'} → {b.trip.route.destination if b.trip and b.trip.route else 'N/A'}",
                    b.trip.departure_time.strftime("%Y-%m-%d %H:%M") if b.trip else "N/A",
                    b.seat_number,
                    b.status
                ))
            print_table(
                booking_data,
                ["Booking ID", "User", "Route", "Departure", "Seat", "Status"]
            )

        elif choice == '3':
            booking_id = int(input("Enter Booking ID to cancel: "))
            booking = db.query(Booking).get(booking_id)
            if not booking:
                print("❌ Booking not found")
                continue
            booking.status = "cancelled"
            db.commit()
            print("✅ Booking cancelled")

        elif choice == '4':
            booking_id = int(input("Enter Booking ID: "))
            booking = db.query(Booking).get(booking_id)
            if booking:
                print(f"\nBooking Details (ID: {booking.id})")
                print(f"User: {booking.user.username if booking.user else 'N/A'}")
                print(f"Route: {booking.trip.route.origin if booking.trip and booking.trip.route else 'N/A'} → {booking.trip.route.destination if booking.trip and booking.trip.route else 'N/A'}")
                print(f"Departure: {booking.trip.departure_time.strftime('%Y-%m-%d %H:%M') if booking.trip else 'N/A'}")
                print(f"Seat: {booking.seat_number}")
                print(f"Status: {booking.status}")
            else:
                print("❌ Booking not found")

        elif choice == '0':
            break

#PAYMENT MENU

def payment_menu(db: Session):
    while True:
        print("\n=== Payment Operations ===")
        print("1. Process Payment")
        print("2. List All Payments")
        print("3. View Payment Details")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("\nProcess Payment:")
            payments = db.query(Payment).filter(Payment.status == "pending").all()
            if not payments:
                print("No pending payments found")
                continue
            print("\nPending Payments:")
            payment_data = []
            for p in payments:
                payment_data.append((
                    p.id,
                    p.booking.id if p.booking else "N/A",
                    p.booking.user.username if p.booking and p.booking.user else "N/A",
                    p.amount,
                    p.status
                ))
            print_table(
                payment_data,
                ["Payment ID", "Booking ID", "User", "Amount", "Status"]
            )
            payment_id = int(input("Enter Payment ID to process: "))
            payment = db.query(Payment).get(payment_id)
            if not payment:
                print("❌ Payment not found")
                continue
            payment.method = input("Payment method (cash/card/mpesa): ")
            payment.status = "paid"
            db.commit()
            print("✅ Payment processed successfully")

        elif choice == '2':
            payments = db.query(Payment).all()
            print("\nAll Payments:")
            payment_data = []
            for p in payments:
                payment_data.append((
                    p.id,
                    p.booking.id if p.booking else "N/A",
                    p.booking.user.username if p.booking and p.booking.user else "N/A",
                    p.amount,
                    p.status,
                    p.method or "N/A"
                ))
            print_table(
                payment_data,
                ["Payment ID", "Booking ID", "User", "Amount", "Status", "Method"]
            )

        elif choice == '3':
            payment_id = int(input("Enter Payment ID: "))
            payment = db.query(Payment).get(payment_id)
            if payment:
                print(f"\nPayment Details (ID: {payment.id})")
                print(f"Booking ID: {payment.booking.id if payment.booking else 'N/A'}")
                print(f"User: {payment.booking.user.username if payment.booking and payment.booking.user else 'N/A'}")
                print(f"Amount: {payment.amount}")
                print(f"Status: {payment.status}")
                print(f"Method: {payment.method or 'N/A'}")
            else:
                print("❌ Payment not found")

        elif choice == '0':
            break

#LOGIN MENU

def login_menu(db):
    while True:
        print("\n=== Welcome To Bus Booking Service ===")
        print("1. Login")
        print("2. Register")
        print("0. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            username = input("Username: ")
            password = input("Password: ")
            user = db.query(User).filter(User.username == username).first()
            if user and user.password_hash == generate_password_hash(password):
                print("✅ Login successful!")
                return user
            else:
                print("❌ Invalid credentials")
        elif choice == '2':
            print("\nRegister New User:")
            username = input("Username: ")
            if db.query(User).filter(User.username == username).first():
                print("❌ Username already exists")
                continue
            email = input("Email: ")
            password = generate_password_hash(input("Password: "))
            full_name = input("Full Name (optional): ") or None
            user = User(
                username=username,
                email=email,
                password_hash=password,
                full_name=full_name
            )
            db.add(user)
            db.commit()
            print(f"✅ User registered with ID: {user.id}")
        elif choice == '0':
            print("Goodbye!")
            sys.exit(0)
        else:
            print("❌ Invalid choice")

#MAIN MENU

def main():
    db = SessionLocal()
    try:
        current_user = login_menu(db)
        while True:
            print(f"\n=== Bus Booking System (Logged in as: {current_user.username}) ===")
            print("1. User Operations")
            print("2. Bus Operations")
            print("3. Route Operations")
            print("4. Trip Operations")
            print("5. Booking Operations")
            print("6. Payment Operations")
            print("0. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                user_menu(db)
            elif choice == '2':
                bus_menu(db)
            elif choice == '3':
                route_menu(db)
            elif choice == '4':
                trip_menu(db)
            elif choice == '5':
                booking_menu(db)
            elif choice == '6':
                payment_menu(db)
            elif choice == '0':
                print("Goodbye!")
                sys.exit(0)
            else:
                print("❌ Invalid choice, please try again")
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    main()