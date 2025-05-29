from datetime import datetime, timedelta
from database import SessionLocal, Base, engine
from models.user import User
from models.bus import Bus
from models.route import Route
from models.trip import Trip
from models.booking import Booking
from models.payment import Payment

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully")

def seed_data():
    create_tables()
    
    db = SessionLocal()

    try:
        # 1.Users
        user1 = User(
            username="matthew_amani",
            email="matt@example.com",
            password_hash="password123",
            full_name="Matthew Amani"
        )
        user2 = User(
            username="kelvin_korir",
            email="kelvin@example.com",
            password_hash="password456",
            full_name="Kelvin Korir"
        )
        db.add_all([user1, user2])
        db.commit()

        # 2.Buses
        bus1 = Bus(
            number_plate="KCA123A",
            model="Scania",
            capacity=50
        )
        bus2 = Bus(
            number_plate="KDE456B",
            model="Volvo",
            capacity=45
        )
        db.add_all([bus1, bus2])
        db.commit()

        # 3.Routes
        route1 = Route(
            origin="Nairobi",
            destination="Mombasa",
            estimated_duration="6 hours",
            distance_km=500
        )
        route2 = Route(
            origin="Nairobi",
            destination="Kisumu",
            estimated_duration="4 hours",
            distance_km=300
        )
        db.add_all([route1, route2])
        db.commit()

        # 4.Trips
        trip1 = Trip(
            route_id=route1.id,
            bus_id=bus1.id,
            departure_time=datetime.now() + timedelta(days=1),
            arrival_time=datetime.now() + timedelta(days=1, hours=6),
            available_seats=50
        )
        trip2 = Trip(
            route_id=route2.id,
            bus_id=bus2.id,
            departure_time=datetime.now() + timedelta(days=2),
            arrival_time=datetime.now() + timedelta(days=2, hours=4),
            available_seats=45
        )
        db.add_all([trip1, trip2])
        db.commit()

        # 5.Bookings
        booking1 = Booking(
            user_id=user1.id,
            trip_id=trip1.id,
            seat_number=5,
            status="confirmed"
        )
        booking2 = Booking(
            user_id=user2.id,
            trip_id=trip2.id,
            seat_number=10,
            status="confirmed"
        )
        db.add_all([booking1, booking2])
        db.commit()

        # 6.Payments
        payment1 = Payment(
            booking_id=booking1.id,
            amount=1200.00,
            status="paid",
            method="mpesa"
        )
        payment2 = Payment(
            booking_id=booking2.id,
            amount=800.00,
            status="pending",
            method="cash"
        )
        db.add_all([payment1, payment2])
        db.commit()

        print("✅ Database seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding data: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()