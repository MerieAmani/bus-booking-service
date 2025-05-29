import argparse
from tabulate import tabulate
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Trip, Booking

def handle_user(db: Session, args):
    if args.action == "create":
        user = User.create(
            db,
            username=args.username,
            email=args.email,
            password=args.password,
            full_name=args.full_name
        )
        print(f"✅ User created (ID: {user.id})")

    elif args.action == "list":
        users = db.query(User).all()
        print(tabulate(
            [(u.id, u.username, u.email) for u in users],
            headers=["ID", "Username", "Email"]
        ))

def handle_trip(db: Session, args):
    if args.action == "search":
        trips = db.query(Trip).filter(
            Trip.route.has(origin=args.origin),
            Trip.route.has(destination=args.destination),
            Trip.departure_time >= args.date
        ).all()
        
        print(tabulate(
            [(t.id, t.route.origin, t.route.destination, 
              t.departure_time, t.available_seats) for t in trips],
            headers=["ID", "From", "To", "Departure", "Seats"]
        ))

def handle_booking(db: Session, args):
    if args.action == "create":
        try:
            booking = Booking.create_booking(
                db,
                user_id=args.user_id,
                trip_id=args.trip_id,
                seat_number=args.seat
            )
            print(f"✅ Booking created (ID: {booking.id})")
            print(f"Amount due: {booking.payment.amount}")
        except ValueError as e:
            print(f"❌ Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Bus Booking System")
    subparsers = parser.add_subparsers(dest="entity", required=True)
    
    # User
    user_parser = subparsers.add_parser("user")
    user_sub = user_parser.add_subparsers(dest="action", required=True)
    
    create = user_sub.add_parser("create")
    create.add_argument("--username", required=True)
    create.add_argument("--email", required=True)
    create.add_argument("--password", required=True)
    create.add_argument("--full_name")
    
    user_sub.add_parser("list")

    # Trip 
    trip_parser = subparsers.add_parser("trip")
    trip_sub = trip_parser.add_subparsers(dest="action", required=True)
    
    search = trip_sub.add_parser("search")
    search.add_argument("--origin", required=True)
    search.add_argument("--destination", required=True)
    search.add_argument("--date", required=True)

    # Booking 
    booking_parser = subparsers.add_parser("booking")
    booking_sub = booking_parser.add_subparsers(dest="action", required=True)

    new_booking = booking_sub.add_parser("create")
    new_booking.add_argument("--user_id", type=int, required=True)
    new_booking.add_argument("--trip_id", type=int, required=True)
    new_booking.add_argument("--seat", type=int, required=True)

    args = parser.parse_args()
    db = SessionLocal()

    if args.entity == "user":
        handle_user(db, args)
    elif args.entity == "trip":
        handle_trip(db, args)
    elif args.entity == "booking":
        handle_booking(db, args)

if __name__ == "__main__":
    main()