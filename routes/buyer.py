from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_required, current_user
from models import Crop, Order, OrderItem, User, db
from datetime import datetime
import uuid

bp = Blueprint('buyer', __name__, url_prefix='/buyer')

@bp.route('/dashboard')
@login_required
def dashboard():
    """Buyer dashboard with overview statistics"""
    if current_user.role != 'buyer':
        flash('Access denied. Buyer role required.', 'error')
        return redirect(url_for('index'))
    
    # Get buyer's orders
    orders = Order.query.filter_by(buyer_id=current_user.id).order_by(Order.created_at.desc()).all()
    
    # Get featured crops (recent active crops)
    featured_crops = Crop.query.filter_by(is_active=True).order_by(Crop.created_at.desc()).limit(6).all()
    
    # Calculate statistics
    total_orders = len(orders)
    pending_orders = len([o for o in orders if o.status == 'pending'])
    completed_orders = len([o for o in orders if o.status == 'delivered'])
    total_spent = sum([o.total_amount for o in orders if o.payment_status == 'paid'])
    
    return render_template('buyer/dashboard.html', 
                         orders=orders,
                         featured_crops=featured_crops,
                         stats={
                             'total_orders': total_orders,
                             'pending_orders': pending_orders,
                             'completed_orders': completed_orders,
                             'total_spent': total_spent
                         })

@bp.route('/crops')
@login_required
def browse_crops():
    """Browse available crops"""
    if current_user.role != 'buyer':
        flash('Access denied. Buyer role required.', 'error')
        return redirect(url_for('index'))
    
    # Get filter parameters
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    location = request.args.get('location', '')
    organic_only = request.args.get('organic_only') == 'on'
    
    # Build query
    query = Crop.query.filter_by(is_active=True)
    
    if search:
        query = query.filter(Crop.name.contains(search) | Crop.description.contains(search))
    
    if location:
        query = query.filter(Crop.location.contains(location))
    
    if organic_only:
        query = query.filter_by(is_organic=True)
    
    crops = query.order_by(Crop.created_at.desc()).all()
    
    return render_template('buyer/browse_crops.html', crops=crops, 
                         search=search, location=location, organic_only=organic_only)

@bp.route('/crops/<int:crop_id>')
@login_required
def crop_details(crop_id):
    """View crop details"""
    if current_user.role != 'buyer':
        flash('Access denied. Buyer role required.', 'error')
        return redirect(url_for('index'))
    
    crop = Crop.query.filter_by(id=crop_id, is_active=True).first_or_404()
    return render_template('buyer/crop_details.html', crop=crop)

@bp.route('/cart')
@login_required
def cart():
    """View shopping cart"""
    if current_user.role != 'buyer':
        flash('Access denied. Buyer role required.', 'error')
        return redirect(url_for('index'))
    
    # Get cart from session
    cart = session.get('cart', {})
    cart_items = []
    total_amount = 0
    
    for crop_id, quantity in cart.items():
        crop = Crop.query.filter_by(id=crop_id, is_active=True).first()
        if crop and quantity > 0:
            item_total = crop.price_per_unit * quantity
            cart_items.append({
                'crop': crop,
                'quantity': quantity,
                'total': item_total
            })
            total_amount += item_total
    
    return render_template('buyer/cart.html', cart_items=cart_items, total_amount=total_amount)

@bp.route('/cart/add', methods=['POST'])
@login_required
def add_to_cart():
    """Add item to cart"""
    if current_user.role != 'buyer':
        flash('Access denied. Buyer role required.', 'error')
        return redirect(url_for('index'))
    
    crop_id = int(request.form['crop_id'])
    quantity = float(request.form['quantity'])
    
    crop = Crop.query.filter_by(id=crop_id, is_active=True).first_or_404()
    
    if quantity > crop.quantity_available:
        flash(f'Only {crop.quantity_available} {crop.unit} available!', 'error')
        return redirect(url_for('buyer.crop_details', crop_id=crop_id))
    
    # Initialize cart if not exists
    if 'cart' not in session:
        session['cart'] = {}
    
    # Add to cart
    if str(crop_id) in session['cart']:
        session['cart'][str(crop_id)] += quantity
    else:
        session['cart'][str(crop_id)] = quantity
    
    session.modified = True
    flash(f'Added {quantity} {crop.unit} of {crop.name} to cart!', 'success')
    return redirect(url_for('buyer.cart'))

@bp.route('/cart/update', methods=['POST'])
@login_required
def update_cart():
    """Update cart item quantity"""
    if current_user.role != 'buyer':
        flash('Access denied. Buyer role required.', 'error')
        return redirect(url_for('index'))
    
    crop_id = request.form['crop_id']
    quantity = float(request.form['quantity'])
    
    if quantity <= 0:
        # Remove from cart
        session['cart'].pop(crop_id, None)
    else:
        crop = Crop.query.filter_by(id=crop_id, is_active=True).first()
        if crop and quantity <= crop.quantity_available:
            session['cart'][crop_id] = quantity
        else:
            flash(f'Only {crop.quantity_available} {crop.unit} available!', 'error')
    
    session.modified = True
    return redirect(url_for('buyer.cart'))

@bp.route('/cart/remove/<int:crop_id>', methods=['POST'])
@login_required
def remove_from_cart(crop_id):
    """Remove item from cart"""
    if current_user.role != 'buyer':
        flash('Access denied. Buyer role required.', 'error')
        return redirect(url_for('index'))
    
    session['cart'].pop(str(crop_id), None)
    session.modified = True
    flash('Item removed from cart!', 'success')
    return redirect(url_for('buyer.cart'))

@bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout process"""
    if current_user.role != 'buyer':
        flash('Access denied. Buyer role required.', 'error')
        return redirect(url_for('index'))
    
    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty!', 'error')
        return redirect(url_for('buyer.cart'))
    
    if request.method == 'POST':
        shipping_address = request.form['shipping_address']
        payment_method = request.form['payment_method']
        notes = request.form.get('notes', '')
        
        # Create order
        order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        total_amount = 0
        order_items = []
        
        # Calculate total and create order items
        for crop_id, quantity in cart.items():
            crop = Crop.query.filter_by(id=crop_id, is_active=True).first()
            if crop and quantity > 0:
                if quantity > crop.quantity_available:
                    flash(f'Only {crop.quantity_available} {crop.unit} of {crop.name} available!', 'error')
                    return redirect(url_for('buyer.cart'))
                
                item_total = crop.price_per_unit * quantity
                total_amount += item_total
                
                order_items.append({
                    'crop': crop,
                    'quantity': quantity,
                    'unit_price': crop.price_per_unit,
                    'total_price': item_total
                })
        
        # Create order
        order = Order(
            order_number=order_number,
            total_amount=total_amount,
            shipping_address=shipping_address,
            payment_method=payment_method,
            notes=notes,
            buyer_id=current_user.id
        )
        
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Create order items
        for item in order_items:
            order_item = OrderItem(
                order_id=order.id,
                crop_id=item['crop'].id,
                quantity=item['quantity'],
                unit_price=item['unit_price'],
                total_price=item['total_price']
            )
            db.session.add(order_item)
            
            # Update crop quantity
            item['crop'].quantity_available -= item['quantity']
        
        db.session.commit()
        
        # Clear cart
        session['cart'] = {}
        session.modified = True
        
        flash(f'Order placed successfully! Order number: {order_number}', 'success')
        return redirect(url_for('buyer.order_details', order_id=order.id))
    
    # Calculate cart total
    cart_items = []
    total_amount = 0
    
    for crop_id, quantity in cart.items():
        crop = Crop.query.filter_by(id=crop_id, is_active=True).first()
        if crop and quantity > 0:
            item_total = crop.price_per_unit * quantity
            cart_items.append({
                'crop': crop,
                'quantity': quantity,
                'total': item_total
            })
            total_amount += item_total
    
    return render_template('buyer/checkout.html', cart_items=cart_items, total_amount=total_amount)

@bp.route('/orders')
@login_required
def orders():
    """View buyer's orders"""
    if current_user.role != 'buyer':
        flash('Access denied. Buyer role required.', 'error')
        return redirect(url_for('index'))
    
    orders = Order.query.filter_by(buyer_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('buyer/orders.html', orders=orders)

@bp.route('/orders/<int:order_id>')
@login_required
def order_details(order_id):
    """View order details"""
    if current_user.role != 'buyer':
        flash('Access denied. Buyer role required.', 'error')
        return redirect(url_for('index'))
    
    order = Order.query.filter_by(id=order_id, buyer_id=current_user.id).first_or_404()
    return render_template('buyer/order_details.html', order=order)

@bp.route('/orders/<int:order_id>/cancel', methods=['POST'])
@login_required
def cancel_order(order_id):
    """Cancel order"""
    if current_user.role != 'buyer':
        flash('Access denied. Buyer role required.', 'error')
        return redirect(url_for('index'))
    
    order = Order.query.filter_by(id=order_id, buyer_id=current_user.id).first_or_404()
    
    if order.status in ['shipped', 'delivered']:
        flash('Cannot cancel order that has been shipped or delivered!', 'error')
        return redirect(url_for('buyer.order_details', order_id=order_id))
    
    order.status = 'cancelled'
    
    # Restore crop quantities
    for item in order.items:
        item.crop.quantity_available += item.quantity
    
    db.session.commit()
    
    flash('Order cancelled successfully!', 'success')
    return redirect(url_for('buyer.orders'))
