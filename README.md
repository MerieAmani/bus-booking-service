# Bus Booking Service

A command-line bus booking system built with Python and SQLAlchemy. This project allows users to register, log in, and manage buses, routes, trips, bookings, and payments.

## Features

- **User Authentication:** Register and log in securely with hashed passwords.
- **Bus Management:** (Planned) Add, update, and list buses.
- **Route Management:** Add, list, update, and delete routes.
- **Trip Scheduling:** Schedule trips, assign buses, and manage seat availability.
- **Booking Operations:** (Planned) Book seats for trips.
- **Payment Processing:** Record and update payments for bookings.
- **Simple CLI Interface:** Easy-to-use text-based menus.

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/bus-booking-service.git
   cd bus-booking-service
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   If you don't have a `requirements.txt`, install the essentials:
   ```bash
   pip install sqlalchemy passlib
   ```

3. **Set up the database:**
   - The database will be created automatically on first run if using SQLite.
   - For other databases, configure `database.py` accordingly.

### Running the Application

```bash
python main.py
```

Follow the on-screen prompts to register, log in, and use the system.

## Project Structure

```
bus-booking-service/
├── main.py           # Main CLI application
├── models.py         # SQLAlchemy models
├── database.py       # Database connection/session
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Notes

- Some features (bus and booking management) are placeholders and can be extended.
- Passwords are securely hashed using `passlib`.
- Designed for educational/demo purposes.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

MIT License
