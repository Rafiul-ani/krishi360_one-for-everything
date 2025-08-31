#!/usr/bin/env python3
"""
Database initialization script for Krishi360
Creates tables and adds sample data for testing
"""

from app import app, db
from models import User, Crop, Order, Consultation, OrderItem
from werkzeug.security import generate_password_hash
from datetime import datetime, date, timedelta
import random

def create_sample_data():
    """Create sample data for testing"""
    
    # Create sample users
    users_data = [
        {
            'username': 'admin',
            'email': 'admin@krishi360.com',
            'password': 'admin123',
            'first_name': 'Admin',
            'last_name': 'User',
            'phone': '+880-1712345678',
            'address': 'Admin Office, Krishi360 HQ, Dhaka, Bangladesh',
            'role': 'admin'
        },
        {
            'username': 'farmer1',
            'email': 'farmer1@example.com',
            'password': 'password123',
            'first_name': 'Abdul',
            'last_name': 'Rahman',
            'phone': '+880-1712345679',
            'address': 'Village Green Farm, Rajshahi, Bangladesh',
            'role': 'farmer'
        },
        {
            'username': 'farmer2',
            'email': 'farmer2@example.com',
            'password': 'password123',
            'first_name': 'Fatima',
            'last_name': 'Begum',
            'phone': '+880-1712345680',
            'address': 'Organic Fields, Sylhet, Bangladesh',
            'role': 'farmer'
        },
        {
            'username': 'buyer1',
            'email': 'buyer1@example.com',
            'password': 'password123',
            'first_name': 'Mohammad',
            'last_name': 'Hasan',
            'phone': '+880-1712345681',
            'address': 'Dhaka, Bangladesh',
            'role': 'buyer'
        },
        {
            'username': 'buyer2',
            'email': 'buyer2@example.com',
            'password': 'password123',
            'first_name': 'Rashida',
            'last_name': 'Khan',
            'phone': '+880-1712345682',
            'address': 'Chittagong, Bangladesh',
            'role': 'buyer'
        },
        {
            'username': 'consultant1',
            'email': 'consultant1@example.com',
            'password': 'password123',
            'first_name': 'Dr. Ahmed',
            'last_name': 'Ali',
            'phone': '+880-1712345683',
            'address': 'Agricultural Research Center, Dhaka, Bangladesh',
            'role': 'consultant'
        },
        {
            'username': 'consultant2',
            'email': 'consultant2@example.com',
            'password': 'password123',
            'first_name': 'Dr. Nasreen',
            'last_name': 'Sultana',
            'phone': '+880-1712345684',
            'address': 'Soil Science Institute, Dhaka, Bangladesh',
            'role': 'consultant'
        }
    ]
    
    users = []
    for user_data in users_data:
        user = User(
            username=user_data['username'],
            email=user_data['email'],
            password_hash=generate_password_hash(user_data['password']),
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            phone=user_data['phone'],
            address=user_data['address'],
            role=user_data['role']
        )
        users.append(user)
        db.session.add(user)
    
    db.session.commit()
    print("✓ Created sample users")
    
    # Get farmer users
    farmers = [u for u in users if u.role == 'farmer']
    
    # Create sample crops
    crops_data = [
        {
            'name': 'Aromatic Rice',
            'variety': 'BRRI Dhan 28',
            'description': 'Premium quality aromatic rice with long grains and fragrant smell. Grown using organic methods.',
            'price_per_unit': 65.0,
            'unit': 'kg',
            'quantity_available': 500.0,
            'harvest_date': date.today() + timedelta(days=30),
            'location': 'Rajshahi, Bangladesh',
            'is_organic': True,
            'farmer_id': farmers[0].id
        },
        {
            'name': 'Wheat',
            'variety': 'BARI Gom 25',
            'description': 'High-quality wheat grains perfect for making flour and bread.',
            'price_per_unit': 50.0,
            'unit': 'kg',
            'quantity_available': 1000.0,
            'harvest_date': date.today() + timedelta(days=45),
            'location': 'Rajshahi, Bangladesh',
            'is_organic': False,
            'farmer_id': farmers[0].id
        },
        {
            'name': 'Organic Tomatoes',
            'variety': 'Cherry Tomatoes',
            'description': 'Fresh, juicy cherry tomatoes grown without pesticides. Perfect for salads and cooking.',
            'price_per_unit': 120.0,
            'unit': 'kg',
            'quantity_available': 200.0,
            'harvest_date': date.today() + timedelta(days=15),
            'location': 'Sylhet, Bangladesh',
            'is_organic': True,
            'farmer_id': farmers[1].id
        },
        {
            'name': 'Potatoes',
            'variety': 'BARI Alu 7',
            'description': 'Fresh potatoes suitable for all cooking purposes. Good storage quality.',
            'price_per_unit': 40.0,
            'unit': 'kg',
            'quantity_available': 800.0,
            'harvest_date': date.today() + timedelta(days=20),
            'location': 'Sylhet, Bangladesh',
            'is_organic': False,
            'farmer_id': farmers[1].id
        },
        {
            'name': 'Onions',
            'variety': 'BARI Piaz 1',
            'description': 'Sharp and pungent red onions, excellent for cooking and storage.',
            'price_per_unit': 45.0,
            'unit': 'kg',
            'quantity_available': 600.0,
            'harvest_date': date.today() + timedelta(days=25),
            'location': 'Rajshahi, Bangladesh',
            'is_organic': False,
            'farmer_id': farmers[0].id
        }
    ]
    
    crops = []
    for crop_data in crops_data:
        crop = Crop(**crop_data)
        crops.append(crop)
        db.session.add(crop)
    
    db.session.commit()
    print("✓ Created sample crops")
    
    # Get buyer users
    buyers = [u for u in users if u.role == 'buyer']
    
    # Create sample orders
    orders_data = [
        {
            'order_number': 'ORD-20241201-001',
            'total_amount': 650.0,
            'status': 'delivered',
            'payment_status': 'paid',
            'payment_method': 'bKash',
            'shipping_address': '123 Dhanmondi, Dhaka, Bangladesh',
            'notes': 'Please deliver in the morning',
            'buyer_id': buyers[0].id,
            'created_at': datetime.utcnow() - timedelta(days=5)
        },
        {
            'order_number': 'ORD-20241201-002',
            'total_amount': 400.0,
            'status': 'shipped',
            'payment_status': 'paid',
            'payment_method': 'Nagad',
            'shipping_address': '456 Chittagong Port, Chittagong, Bangladesh',
            'notes': 'Handle with care',
            'buyer_id': buyers[1].id,
            'created_at': datetime.utcnow() - timedelta(days=2)
        },
        {
            'order_number': 'ORD-20241201-003',
            'total_amount': 240.0,
            'status': 'pending',
            'payment_status': 'pending',
            'payment_method': 'bKash',
            'shipping_address': '789 Gulshan, Dhaka, Bangladesh',
            'notes': '',
            'buyer_id': buyers[0].id,
            'created_at': datetime.utcnow() - timedelta(hours=2)
        }
    ]
    
    orders = []
    for order_data in orders_data:
        order = Order(**order_data)
        orders.append(order)
        db.session.add(order)
    
    db.session.commit()
    print("✓ Created sample orders")
    
    # Create sample order items
    order_items_data = [
        {
            'order_id': orders[0].id,
            'crop_id': crops[0].id,
            'quantity': 10.0,
            'unit_price': 65.0,
            'total_price': 650.0
        },
        {
            'order_id': orders[1].id,
            'crop_id': crops[1].id,
            'quantity': 8.0,
            'unit_price': 50.0,
            'total_price': 400.0
        },
        {
            'order_id': orders[2].id,
            'crop_id': crops[2].id,
            'quantity': 2.0,
            'unit_price': 120.0,
            'total_price': 240.0
        }
    ]
    
    for item_data in order_items_data:
        order_item = OrderItem(**item_data)
        db.session.add(order_item)
    
    db.session.commit()
    print("✓ Created sample order items")
    
    # Get consultant users
    consultants = [u for u in users if u.role == 'consultant']
    
    # Create sample consultations
    consultations_data = [
        {
            'title': 'Rice Blast Disease Treatment',
            'description': 'My rice crop is showing signs of blast disease. Need advice on treatment and prevention.',
            'category': 'pest_control',
            'status': 'completed',
            'priority': 'high',
            'response': 'Rice blast can be controlled using fungicides like Tricyclazole. Apply at the first sign of disease. For prevention, ensure proper spacing and avoid excessive nitrogen.',
            'rating': 5,
            'farmer_id': farmers[0].id,
            'consultant_id': consultants[0].id,
            'created_at': datetime.utcnow() - timedelta(days=7),
            'completed_at': datetime.utcnow() - timedelta(days=5)
        },
        {
            'title': 'Soil Testing and Fertilizer Recommendation',
            'description': 'Need help with soil testing and fertilizer recommendations for wheat cultivation.',
            'category': 'soil_health',
            'status': 'in_progress',
            'priority': 'medium',
            'response': None,
            'rating': None,
            'farmer_id': farmers[1].id,
            'consultant_id': consultants[1].id,
            'created_at': datetime.utcnow() - timedelta(days=3)
        },
        {
            'title': 'Organic Farming Certification',
            'description': 'Interested in getting organic certification for my farm. What are the requirements?',
            'category': 'certification',
            'status': 'pending',
            'priority': 'low',
            'response': None,
            'rating': None,
            'farmer_id': farmers[0].id,
            'consultant_id': None,
            'created_at': datetime.utcnow() - timedelta(days=1)
        }
    ]
    
    for consultation_data in consultations_data:
        consultation = Consultation(**consultation_data)
        db.session.add(consultation)
    
    db.session.commit()
    print("✓ Created sample consultations")

def main():
    """Main function to initialize database"""
    with app.app_context():
        print("Initializing Krishi360 database...")
        
        # Create all tables
        db.create_all()
        print("✓ Created database tables")
        
        # Check if data already exists
        if User.query.first():
            print("⚠ Database already contains data. Skipping sample data creation.")
            return
        
        # Create sample data
        create_sample_data()
        
        print("\n🎉 Database initialization completed successfully!")
        print("\nSample accounts created:")
        print("Admin: admin / admin123")
        print("Farmer: farmer1 / password123")
        print("Buyer: buyer1 / password123")
        print("Consultant: consultant1 / password123")
        print("\nYou can now run the application with: python app.py")

if __name__ == '__main__':
    main()
