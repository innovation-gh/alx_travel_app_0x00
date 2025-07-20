# ALX Travel App 0x00

A Django REST API application for managing travel listings, bookings, and reviews.

## Project Structure

```
alx_travel_app/
├── listings/
│   ├── models.py              # Database models (Listing, Booking, Review)
│   ├── serializers.py         # DRF serializers for API data representation
│   ├── management/
│   │   └── commands/
│   │       └── seed.py        # Database seeding command
│   └── ...
├── manage.py
└── README.md
```

## Models

### Listing

- **listing_id**: UUID primary key
- **host**: Foreign key to User model
- **name**: Property name (max 200 characters)
- **description**: Detailed description
- **location**: Property location
- **pricepernight**: Decimal price per night
- **created_at/updated_at**: Timestamp fields

### Booking

- **booking_id**: UUID primary key
- **property**: Foreign key to Listing
- **user**: Foreign key to User (guest)
- **start_date/end_date**: Booking date range
- **total_price**: Calculated total price
- **created_at**: Timestamp
- **Constraints**: Prevents overlapping bookings, validates date range

### Review

- **review_id**: UUID primary key
- **property**: Foreign key to Listing
- **user**: Foreign key to User (reviewer)
- **rating**: Integer rating (1-5)
- **comment**: Review text
- **created_at**: Timestamp
- **Constraints**: One review per user per property

## API Serializers

### ListingSerializer

- Full CRUD serialization for Listing model
- Nested host information (read-only)
- Price validation (must be > 0)

### BookingSerializer

- Full CRUD serialization for Booking model
- Nested property and user information
- Advanced validation for date conflicts and overlapping bookings
- Automatic total price validation

### ReviewSerializer

- Full CRUD serialization for Review model
- Nested property and user information
- Rating validation (1-5 range)

## Database Seeding

The application includes a comprehensive management command for populating the database with sample data.

### Usage

```bash
# Basic seeding with default values
python manage.py seed

# Custom seeding with specific counts
python manage.py seed --listings 50 --users 20 --bookings 100 --reviews 150
```

### Command Options

- `--listings`: Number of listings to create (default: 20)
- `--users`: Number of users to create (default: 10)
- `--bookings`: Number of bookings to create (default: 30)
- `--reviews`: Number of reviews to create (default: 50)

### Sample Data

The seeder creates:

1. **Users**: Realistic user profiles with names and emails
2. **Listings**: Diverse property types across different locations:

   - Cozy Downtown Apartment (New York, NY)
   - Beachfront Villa (Miami, FL)
   - Mountain Cabin Retreat (Denver, CO)
   - Modern City Loft (San Francisco, CA)
   - Historic Townhouse (Boston, MA)

3. **Bookings**: Realistic booking scenarios with:

   - Random future dates (within 6 months)
   - Variable stay durations (1-14 days)
   - Calculated total prices
   - Conflict prevention (no overlapping bookings)

4. **Reviews**: Authentic review comments with random ratings

## Installation & Setup

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd alx_travel_app_0x00/alx_travel_app
   ```

2. **Install dependencies:**

   ```bash
   pip install django djangorestframework
   ```

3. **Run migrations:**

   ```bash
   python manage.py makemigrations listings
   python manage.py migrate
   ```

4. **Seed the database:**

   ```bash
   python manage.py seed
   ```

5. **Create a superuser (optional):**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the server:**
   ```bash
   python manage.py runserver
   ```

## Features

- **UUID Primary Keys**: All models use UUID for enhanced security
- **Data Validation**: Comprehensive validation at both model and serializer levels
- **Relationship Management**: Proper foreign key relationships with related names
- **Conflict Prevention**: Automatic detection of booking conflicts
- **Realistic Test Data**: Seeder creates meaningful, interconnected sample data
- **RESTful API**: Full CRUD operations through Django REST Framework serializers

## Database Constraints

- **Booking Conflicts**: Automatic prevention of overlapping bookings for the same property
- **Review Uniqueness**: One review per user per property
- **Date Validation**: End dates must be after start dates
- **Rating Range**: Reviews must have ratings between 1-5
- **Price Validation**: Prices must be positive values

## Next Steps

This foundation provides everything needed for:

- Creating REST API endpoints
- Implementing user authentication
- Adding advanced filtering and search
- Building a frontend interface
- Deploying to production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure data integrity
5. Submit a pull request

## License

This project is part of the ALX Software Engineering program.
