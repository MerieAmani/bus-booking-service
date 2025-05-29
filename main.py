from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Bus, Route, Trip, Payment
try:
    from passlib.hash import pbkdf2_sha256
except ImportError:
    print("❌ passlib is not installed. Please install it with 'pip install passlib'")
    import sys
    sys.exit(1)
import sys
from typing import Optional

def show_main_menu():
    print("\n=== Bus Booking System ===")
    print("1. User Operations")
    print("2. Bus Operations")
    print("3. Route Operations")
    print("4. Trip Operations")
    print("5. Booking Operations")
    print("6. Payment Operations")
    print("0. Exit")
    return input("Enter your choice: ")

def login(db: Session) -> Optional[User]:
    print("\n=== Login ===")
    username = input("Username: ")
    password = input("Password: ")
    user = db.query(User).filter(User.username == username).first()
    password_hash = getattr(user, "password_hash", None)
    if not user or not password_hash or not pbkdf2_sha256.verify(password, password_hash):
        print("❌ Invalid credentials")
        return None
    print(f"✅ Welcome, {user.full_name or user.username}!")
    return user

def register(db: Session) -> Optional[User]:
    print("\n=== Register ===")
    username = input("Username: ")
    if db.query(User).filter(User.username == username).first():
        print("❌ Username already exists")
        return None
    email = input("Email: ")
    password = input("Password: ")
    full_name = input("Full Name (optional): ")
    user = User(
        username=username,
        email=email,
        password_hash=pbkdf2_sha256.hash(password),
        full_name=full_name or None
    )
    db.add(user)
    db.commit()
    print(f"✅ Registration successful! ID: {user.id}")
    return user

def user_menu(db: Session):
    print("\n=== User Operations ===")
    print("Feature not implemented yet.")

def bus_menu(db: Session):
    print("\n=== Bus Operations ===")
    print("Feature not implemented yet.")

def booking_menu(db: Session):
    print("\n=== Booking Operations ===")
    print("Feature not implemented yet.")

def route_menu(db: Session):
    while True:
        print("\n=== Route Management ===")
        print("1. Add Route")
        print("2. List Routes")
        print("3. Update Route")
        print("4. Delete Route")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            origin = input("Origin: ")
            destination = input("Destination: ")
            distance = input("Distance (km): ")
            duration = input("Estimated Duration: ")
            route = Route(
                origin=origin,
                destination=destination,
                distance_km=int(distance),
                estimated_duration=duration
            )
            db.add(route)
            db.commit()
            print(f"✅ Route added with ID: {route.id}")

        elif choice == '2':
            routes = db.query(Route).all()
            print("\n=== Routes ===")
            for route in routes:
                print(f"ID: {route.id}, {route.origin} → {route.destination}, {route.distance_km}km")

        elif choice == '0':
            break

def trip_menu(db: Session):
    while True:
        print("\n=== Trip Management ===")
        print("1. Schedule Trip")
        print("2. List Trips")
        print("3. Update Trip")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            route_id = int(input("Route ID: "))
            bus_id = int(input("Bus ID: "))
            departure = input("Departure (YYYY-MM-DD HH:MM): ")
            arrival = input("Arrival (YYYY-MM-DD HH:MM): ")
            bus = db.query(Bus).get(bus_id)
            if not bus:
                print("❌ Bus not found")
                continue
            trip = Trip(
                route_id=route_id,
                bus_id=bus_id,
                departure_time=departure,
                arrival_time=arrival,
                available_seats=bus.capacity
            )
            db.add(trip)
            db.commit()
            print(f"✅ Trip scheduled with ID: {trip.id}")

        elif choice == '2':
            trips = db.query(Trip).all()
            print("\n=== Trips ===")
            for trip in trips:
                print(f"ID: {trip.id}, Route: {trip.route.origin}→{trip.route.destination}, Bus: {trip.bus.number_plate}, Seats: {trip.available_seats}")

        elif choice == '0':
            break

def payment_menu(db: Session):
    while True:
        print("\n=== Payment Management ===")
        print("1. Process Payment")
        print("2. View Payments")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            try:
                booking_id = int(input("Booking ID: "))
                amount = float(input("Amount: "))
                method = input("Payment Method: ")
            except ValueError:
                print("❌ Invalid input")
                continue
            payment = db.query(Payment).filter(Payment.booking_id == booking_id).first()
            if payment:
                setattr(payment, "amount", amount)
                setattr(payment, "method", method)
                setattr(payment, "status", "paid")
                db.commit()
                print("✅ Payment processed")
            else:
                print("❌ Booking not found")

        elif choice == '2':
            payments = db.query(Payment).all()
            print("\n=== Payments ===")
            for payment in payments:
                print(f"ID: {payment.id}, Booking ID: {payment.booking_id}, Amount: {payment.amount}, Method: {payment.method}, Status: {payment.status}")

        elif choice == '0':
            break

def auth_menu(db: Session) -> Optional[User]:
    while True:
        print("\n=== Authentication ===")
        print("1. Login")
        print("2. Register")
        print("0. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            user = login(db)
            if user:
                return user
        elif choice == '2':
            user = register(db)
            if user:
                return user
        elif choice == '0':
            sys.exit(0)

def main():
    db = SessionLocal()
    try:
        current_user = auth_menu(db)
        if not current_user:
            return

        while True:
            choice = show_main_menu()
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
    except KeyboardInterrupt:
        print("\nGoodbye!")
    finally:
        db.close()

if __name__ == "__main__":
    main()
