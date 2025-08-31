from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import Crop, Order, OrderItem, Consultation, db
from datetime import datetime, date
import os
from werkzeug.utils import secure_filename

bp = Blueprint('farmer', __name__, url_prefix='/farmer')

@bp.route('/dashboard')
@login_required
def dashboard():
    """Farmer dashboard with overview statistics"""
    if current_user.role != 'farmer':
        flash('Access denied. Farmer role required.', 'error')
        return redirect(url_for('index'))
    
    # Get farmer's crops
    crops = Crop.query.filter_by(farmer_id=current_user.id).all()
    
    # Get orders for farmer's crops
    crop_ids = [crop.id for crop in crops]
    orders = Order.query.join(OrderItem).filter(OrderItem.crop_id.in_(crop_ids)).all()
    
    # Get consultations
    consultations = Consultation.query.filter_by(farmer_id=current_user.id).all()
    
    # Calculate statistics
    total_crops = len(crops)
    active_crops = len([c for c in crops if c.is_active])
    total_orders = len(orders)
    pending_consultations = len([c for c in consultations if c.status == 'pending'])
    
    return render_template('farmer/dashboard.html', 
                         crops=crops, 
                         orders=orders,
                         consultations=consultations,
                         stats={
                             'total_crops': total_crops,
                             'active_crops': active_crops,
                             'total_orders': total_orders,
                             'pending_consultations': pending_consultations
                         })

@bp.route('/crops')
@login_required
def crops():
    """List all farmer's crops"""
    if current_user.role != 'farmer':
        flash('Access denied. Farmer role required.', 'error')
        return redirect(url_for('index'))
    
    crops = Crop.query.filter_by(farmer_id=current_user.id).order_by(Crop.created_at.desc()).all()
    return render_template('farmer/crops.html', crops=crops)

@bp.route('/crops/add', methods=['GET', 'POST'])
@login_required
def add_crop():
    """Add new crop listing"""
    if current_user.role != 'farmer':
        flash('Access denied. Farmer role required.', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form['name']
        variety = request.form.get('variety', '')
        description = request.form.get('description', '')
        price_per_unit = float(request.form['price_per_unit'])
        unit = request.form['unit']
        quantity_available = float(request.form['quantity_available'])
        harvest_date_str = request.form.get('harvest_date', '')
        location = request.form['location']
        is_organic = 'is_organic' in request.form
        
        harvest_date = None
        if harvest_date_str:
            harvest_date = datetime.strptime(harvest_date_str, '%Y-%m-%d').date()
        
        crop = Crop(
            name=name,
            variety=variety,
            description=description,
            price_per_unit=price_per_unit,
            unit=unit,
            quantity_available=quantity_available,
            harvest_date=harvest_date,
            location=location,
            is_organic=is_organic,
            farmer_id=current_user.id
        )
        
        db.session.add(crop)
        db.session.commit()
        
        flash('Crop added successfully!', 'success')
        return redirect(url_for('farmer.crops'))
    
    return render_template('farmer/add_crop.html')

@bp.route('/crops/<int:crop_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_crop(crop_id):
    """Edit crop listing"""
    if current_user.role != 'farmer':
        flash('Access denied. Farmer role required.', 'error')
        return redirect(url_for('index'))
    
    crop = Crop.query.filter_by(id=crop_id, farmer_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        crop.name = request.form['name']
        crop.variety = request.form.get('variety', '')
        crop.description = request.form.get('description', '')
        crop.price_per_unit = float(request.form['price_per_unit'])
        crop.unit = request.form['unit']
        crop.quantity_available = float(request.form['quantity_available'])
        harvest_date_str = request.form.get('harvest_date', '')
        crop.location = request.form['location']
        crop.is_organic = 'is_organic' in request.form
        
        if harvest_date_str:
            crop.harvest_date = datetime.strptime(harvest_date_str, '%Y-%m-%d').date()
        else:
            crop.harvest_date = None
        
        db.session.commit()
        flash('Crop updated successfully!', 'success')
        return redirect(url_for('farmer.crops'))
    
    return render_template('farmer/edit_crop.html', crop=crop)

@bp.route('/crops/<int:crop_id>/delete', methods=['POST'])
@login_required
def delete_crop(crop_id):
    """Delete crop listing"""
    if current_user.role != 'farmer':
        flash('Access denied. Farmer role required.', 'error')
        return redirect(url_for('index'))
    
    crop = Crop.query.filter_by(id=crop_id, farmer_id=current_user.id).first_or_404()
    crop.is_active = False
    db.session.commit()
    
    flash('Crop deactivated successfully!', 'success')
    return redirect(url_for('farmer.crops'))

@bp.route('/orders')
@login_required
def orders():
    """View orders for farmer's crops"""
    if current_user.role != 'farmer':
        flash('Access denied. Farmer role required.', 'error')
        return redirect(url_for('index'))
    
    # Get farmer's crops
    crops = Crop.query.filter_by(farmer_id=current_user.id).all()
    crop_ids = [crop.id for crop in crops]
    
    # Get orders for these crops
    orders = Order.query.join(OrderItem).filter(OrderItem.crop_id.in_(crop_ids)).order_by(Order.created_at.desc()).all()
    
    return render_template('farmer/orders.html', orders=orders)

@bp.route('/orders/<int:order_id>/update-status', methods=['POST'])
@login_required
def update_order_status(order_id):
    """Update order status"""
    if current_user.role != 'farmer':
        flash('Access denied. Farmer role required.', 'error')
        return redirect(url_for('index'))
    
    order = Order.query.get_or_404(order_id)
    new_status = request.form['status']
    
    # Verify this order contains farmer's crops
    crop_ids = [crop.id for crop in Crop.query.filter_by(farmer_id=current_user.id).all()]
    order_crop_ids = [item.crop_id for item in order.items]
    
    if not any(crop_id in crop_ids for crop_id in order_crop_ids):
        flash('Access denied. This order does not contain your crops.', 'error')
        return redirect(url_for('farmer.orders'))
    
    order.status = new_status
    db.session.commit()
    
    flash(f'Order status updated to {new_status}!', 'success')
    return redirect(url_for('farmer.orders'))

@bp.route('/consultations')
@login_required
def consultations():
    """View farmer's consultation requests"""
    if current_user.role != 'farmer':
        flash('Access denied. Farmer role required.', 'error')
        return redirect(url_for('index'))
    
    consultations = Consultation.query.filter_by(farmer_id=current_user.id).order_by(Consultation.created_at.desc()).all()
    return render_template('farmer/consultations.html', consultations=consultations)

@bp.route('/consultations/add', methods=['GET', 'POST'])
@login_required
def add_consultation():
    """Request new consultation"""
    if current_user.role != 'farmer':
        flash('Access denied. Farmer role required.', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        priority = request.form['priority']
        
        consultation = Consultation(
            title=title,
            description=description,
            category=category,
            priority=priority,
            farmer_id=current_user.id
        )
        
        db.session.add(consultation)
        db.session.commit()
        
        flash('Consultation request submitted successfully!', 'success')
        return redirect(url_for('farmer.consultations'))
    
    return render_template('farmer/add_consultation.html')

@bp.route('/consultations/<int:consultation_id>/rate', methods=['POST'])
@login_required
def rate_consultation(consultation_id):
    """Rate completed consultation"""
    if current_user.role != 'farmer':
        flash('Access denied. Farmer role required.', 'error')
        return redirect(url_for('index'))
    
    consultation = Consultation.query.filter_by(id=consultation_id, farmer_id=current_user.id).first_or_404()
    rating = int(request.form['rating'])
    
    if consultation.status != 'completed':
        flash('You can only rate completed consultations.', 'error')
        return redirect(url_for('farmer.consultations'))
    
    consultation.rating = rating
    db.session.commit()
    
    flash('Thank you for your rating!', 'success')
    return redirect(url_for('farmer.consultations'))
