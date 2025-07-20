import random
from decimal import Decimal
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Listing, Booking, Review


class Command(BaseCommand):
    help = 'Seed the database with sample listings, bookings, and reviews data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--listings',
            type=int,
            default=20,
            help='Number of listings to create (default: 20)'
        )
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Number of users to create (default: 10)'
        )
        parser.add_argument(
            '--bookings',
            type=int,
            default=30,
            help='Number of bookings to create (default: 30)'
        )
        parser.add_argument(
            '--reviews',
            type=int,
            default=50,
            help='Number of reviews to create (default: 50)'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Starting database seeding...')
        )

        # Create users
        self.create_users(options['users'])
        
        # Create listings
        self.create_listings(options['listings'])
        
        # Create bookings
        self.create_bookings(options['bookings'])
        
        # Create reviews
        self.create_reviews(options['reviews'])

        self.stdout.write(
            self.style.SUCCESS('Database seeding completed successfully!')
        )

    def create_users(self, count):
        """Create sample users"""
        self.stdout.write(f'Creating {count} users...')
        
        users_data = [
            {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'username': 'mike_wilson', 'email': 'mike@example.com', 'first_name': 'Mike', 'last_name': 'Wilson'},
            {'username': 'sarah_johnson', 'email': 'sarah@example.com', 'first_name': 'Sarah', 'last_name': 'Johnson'},
            {'username': 'david_brown', 'email': 'david@example.com', 'first_name': 'David', 'last_name': 'Brown'},
            {'username': 'lisa_davis', 'email': 'lisa@example.com', 'first_name': 'Lisa', 'last_name': 'Davis'},
            {'username': 'alex_taylor', 'email': 'alex@example.com', 'first_name': 'Alex', 'last_name': 'Taylor'},
            {'username': 'emma_white', 'email': 'emma@example.com', 'first_name': 'Emma', 'last_name': 'White'},
            {'username': 'ryan_miller', 'email': 'ryan@example.com', 'first_name': 'Ryan', 'last_name': 'Miller'},
            {'username': 'olivia_garcia', 'email': 'olivia@example.com', 'first_name': 'Olivia', 'last_name': 'Garcia'},
        ]

        created_users = 0
        for i in range(count):
            user_data = users_data[i % len(users_data)]
            username = f"{user_data['username']}_{i+1}" if i >= len(users_data) else user_data['username']
            email = f"user{i+1}@example.com" if i >= len(users_data) else user_data['email']
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'password': 'pbkdf2_sha256$600000$test$password'  # Simple test password
                }
            )
            if created:
                created_users += 1

        self.stdout.write(
            self.style.SUCCESS(f'Created {created_users} new users')
        )

    def create_listings(self, count):
        """Create sample listings"""
        self.stdout.write(f'Creating {count} listings...')
        
        listing_templates = [
            {
                'name': 'Cozy Downtown Apartment',
                'description': 'Beautiful apartment in the heart of downtown with modern amenities and city views.',
                'location': 'New York, NY',
                'base_price': 150
            },
            {
                'name': 'Beachfront Villa',
                'description': 'Luxurious beachfront villa with private beach access and stunning ocean views.',
                'location': 'Miami, FL',
                'base_price': 300
            },
            {
                'name': 'Mountain Cabin Retreat',
                'description': 'Rustic mountain cabin perfect for a peaceful getaway surrounded by nature.',
                'location': 'Denver, CO',
                'base_price': 120
            },
            {
                'name': 'Modern City Loft',
                'description': 'Stylish loft in trendy neighborhood with high ceilings and exposed brick.',
                'location': 'San Francisco, CA',
                'base_price': 200
            },
            {
                'name': 'Historic Townhouse',
                'description': 'Charming historic townhouse with period features and modern conveniences.',
                'location': 'Boston, MA',
                'base_price': 180
            },
        ]

        users = list(User.objects.all())
        created_listings = 0

        for i in range(count):
            template = listing_templates[i % len(listing_templates)]
            
            # Add variation to names and prices
            price_variation = random.uniform(0.8, 1.3)
            price = Decimal(str(round(template['base_price'] * price_variation, 2)))
            
            name_suffix = f" #{i+1}" if i >= len(listing_templates) else ""
            
            listing, created = Listing.objects.get_or_create(
                name=template['name'] + name_suffix,
                defaults={
                    'host': random.choice(users),
                    'description': template['description'],
                    'location': template['location'],
                    'pricepernight': price,
                }
            )
            if created:
                created_listings += 1

        self.stdout.write(
            self.style.SUCCESS(f'Created {created_listings} new listings')
        )

    def create_bookings(self, count):
        """Create sample bookings"""
        self.stdout.write(f'Creating {count} bookings...')
        
        users = list(User.objects.all())
        listings = list(Listing.objects.all())
        
        if not users or not listings:
            self.stdout.write(
                self.style.WARNING('No users or listings available for creating bookings')
            )
            return

        created_bookings = 0
        max_attempts = count * 3  # Prevent infinite loop
        attempts = 0

        while created_bookings < count and attempts < max_attempts:
            attempts += 1
            
            user = random.choice(users)
            listing = random.choice(listings)
            
            # Generate random dates (within next 6 months)
            start_date = date.today() + timedelta(days=random.randint(1, 180))
            end_date = start_date + timedelta(days=random.randint(1, 14))
            
            # Calculate total price
            nights = (end_date - start_date).days
            total_price = listing.pricepernight * nights
            
            # Check if booking already exists for these dates
            existing_booking = Booking.objects.filter(
                property=listing,
                start_date__lt=end_date,
                end_date__gt=start_date
            ).exists()
            
            if not existing_booking and user != listing.host:
                try:
                    booking = Booking.objects.create(
                        property=listing,
                        user=user,
                        start_date=start_date,
                        end_date=end_date,
                        total_price=total_price
                    )
                    created_bookings += 1
                except Exception as e:
                    continue

        self.stdout.write(
            self.style.SUCCESS(f'Created {created_bookings} new bookings')
        )

    def create_reviews(self, count):
        """Create sample reviews"""
        self.stdout.write(f'Creating {count} reviews...')
        
        users = list(User.objects.all())
        listings = list(Listing.objects.all())
        
        if not users or not listings:
            self.stdout.write(
                self.style.WARNING('No users or listings available for creating reviews')
            )
            return

        review_comments = [
            "Great place to stay! Clean and comfortable.",
            "Amazing location and beautiful views. Highly recommended!",
            "The host was very welcoming and the property exceeded expectations.",
            "Perfect for a weekend getaway. Will definitely book again!",
            "Nice place but could use some updates. Overall satisfied.",
            "Fantastic experience! The property was exactly as described.",
            "Good value for money. Clean and well-maintained.",
            "Beautiful property with excellent amenities.",
            "Had a wonderful time. The location was perfect for our needs.",
            "Lovely place with great attention to detail."
        ]

        created_reviews = 0
        max_attempts = count * 2  # Prevent infinite loop
        attempts = 0

        while created_reviews < count and attempts < max_attempts:
            attempts += 1
            
            user = random.choice(users)
            listing = random.choice(listings)
            
            # Don't let users review their own properties
            if user == listing.host:
                continue
            
            # Check if review already exists
            existing_review = Review.objects.filter(
                property=listing,
                user=user
            ).exists()
            
            if not existing_review:
                try:
                    review = Review.objects.create(
                        property=listing,
                        user=user,
                        rating=random.randint(1, 5),
                        comment=random.choice(review_comments)
                    )
                    created_reviews += 1
                except Exception as e:
                    continue

        self.stdout.write(
            self.style.SUCCESS(f'Created {created_reviews} new reviews')
        )