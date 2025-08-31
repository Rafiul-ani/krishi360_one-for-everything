from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize db here - will be set by app.py
db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model with role-based access control"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    role = db.Column(db.String(20), nullable=False, default='farmer')  # farmer, buyer, consultant, admin
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    crops = db.relationship('Crop', backref='farmer', lazy=True)
    orders_placed = db.relationship('Order', foreign_keys='Order.buyer_id', backref='buyer', lazy=True)
    consultations_requested = db.relationship('Consultation', foreign_keys='Consultation.farmer_id', backref='farmer', lazy=True)
    consultations_provided = db.relationship('Consultation', foreign_keys='Consultation.consultant_id', backref='consultant', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Crop(db.Model):
    """Crop listing model for farmers"""
    __tablename__ = 'crops'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    variety = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    price_per_unit = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False, default='kg')  # kg, ton, piece, etc.
    quantity_available = db.Column(db.Float, nullable=False)
    harvest_date = db.Column(db.Date, nullable=True)
    location = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    is_organic = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='crop', lazy=True)
    
    def __repr__(self):
        return f'<Crop {self.name}>'

class Order(db.Model):
    """Order model for buyers"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, confirmed, shipped, delivered, cancelled
    payment_status = db.Column(db.String(20), nullable=False, default='pending')  # pending, paid, failed, refunded
    payment_method = db.Column(db.String(50), nullable=True)
    shipping_address = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.order_number}>'

class OrderItem(db.Model):
    """Order items model"""
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    
    # Foreign keys
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id'), nullable=False)
    
    def __repr__(self):
        return f'<OrderItem {self.id}>'

class Consultation(db.Model):
    """Consultation model for expert advice"""
    __tablename__ = 'consultations'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # crop_management, pest_control, soil_health, etc.
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, in_progress, completed, cancelled
    priority = db.Column(db.String(10), nullable=False, default='medium')  # low, medium, high, urgent
    response = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Integer, nullable=True)  # 1-5 stars
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Foreign keys
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    consultant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    def __repr__(self):
        return f'<Consultation {self.title}>'

class Notification(db.Model):
    """Notification model for real-time updates"""
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # order_update, consultation_response, etc.
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', backref='notifications')
    
    def __repr__(self):
        return f'<Notification {self.title}>'
