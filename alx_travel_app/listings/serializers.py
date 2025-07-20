from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Listing, Booking, Review


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class ListingSerializer(serializers.ModelSerializer):
    """Serializer for Listing model"""
    
    host = UserSerializer(read_only=True)
    host_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        source='host', 
        write_only=True
    )
    
    class Meta:
        model = Listing
        fields = [
            'listing_id', 
            'host', 
            'host_id',
            'name', 
            'description', 
            'location', 
            'pricepernight', 
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['listing_id', 'created_at', 'updated_at']
    
    def validate_pricepernight(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price per night must be greater than 0")
        return value


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model"""
    
    property = ListingSerializer(read_only=True)
    property_id = serializers.PrimaryKeyRelatedField(
        queryset=Listing.objects.all(), 
        source='property', 
        write_only=True
    )
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        source='user', 
        write_only=True
    )
    
    class Meta:
        model = Booking
        fields = [
            'booking_id',
            'property',
            'property_id',
            'user',
            'user_id',
            'start_date',
            'end_date',
            'total_price',
            'created_at'
        ]
        read_only_fields = ['booking_id', 'created_at']
    
    def validate(self, data):
        """
        Check that start_date is before end_date and no overlapping bookings exist
        """
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        property_obj = data.get('property')
        
        if start_date and end_date:
            if start_date >= end_date:
                raise serializers.ValidationError(
                    "End date must be after start date"
                )
            
            # Check for overlapping bookings (exclude current instance if updating)
            overlapping_bookings = Booking.objects.filter(
                property=property_obj,
                start_date__lt=end_date,
                end_date__gt=start_date
            )
            
            # If updating, exclude current instance
            if self.instance:
                overlapping_bookings = overlapping_bookings.exclude(
                    booking_id=self.instance.booking_id
                )
            
            if overlapping_bookings.exists():
                raise serializers.ValidationError(
                    "This property is already booked for the selected dates"
                )
        
        return data
    
    def validate_total_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Total price must be greater than 0")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model"""
    
    property = ListingSerializer(read_only=True)
    property_id = serializers.PrimaryKeyRelatedField(
        queryset=Listing.objects.all(), 
        source='property', 
        write_only=True
    )
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        source='user', 
        write_only=True
    )
    
    class Meta:
        model = Review
        fields = [
            'review_id',
            'property',
            'property_id',
            'user',
            'user_id',
            'rating',
            'comment',
            'created_at'
        ]
        read_only_fields = ['review_id', 'created_at']
    
    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value