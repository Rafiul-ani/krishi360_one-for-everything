from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import User, Crop, Order, Consultation, db
from datetime import datetime, timedelta
from sqlalchemy import func

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    """Decorator to require admin role"""
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Access denied. Admin role required.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard with analytics and statistics"""
    
    # User statistics
    total_users = User.query.count()
    farmers = User.query.filter_by(role='farmer').count()
    buyers = User.query.filter_by(role='buyer').count()
    consultants = User.query.filter_by(role='consultant').count()
    
    # Recent registrations (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_registrations = User.query.filter(User.created_at >= thirty_days_ago).count()
    
    # Crop statistics
    total_crops = Crop.query.count()
    active_crops = Crop.query.filter_by(is_active=True).count()
    organic_crops = Crop.query.filter_by(is_organic=True).count()
    
    # Order statistics
    total_orders = Order.query.count()
    pending_orders = Order.query.filter_by(status='pending').count()
    completed_orders = Order.query.filter_by(status='delivered').count()
    total_revenue = db.session.query(func.sum(Order.total_amount)).filter_by(payment_status='paid').scalar() or 0
    
    # Consultation statistics
    total_consultations = Consultation.query.count()
    pending_consultations = Consultation.query.filter_by(status='pending').count()
    completed_consultations = Consultation.query.filter_by(status='completed').count()
    
    # Recent activity
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    recent_consultations = Consultation.query.order_by(Consultation.created_at.desc()).limit(5).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    # Monthly revenue chart data (last 12 months)
    monthly_revenue = []
    for i in range(12):
        month_start = datetime.utcnow() - timedelta(days=30*i)
        month_end = month_start + timedelta(days=30)
        revenue = db.session.query(func.sum(Order.total_amount)).filter(
            Order.created_at >= month_start,
            Order.created_at < month_end,
            Order.payment_status == 'paid'
        ).scalar() or 0
        monthly_revenue.append({
            'month': month_start.strftime('%b %Y'),
            'revenue': float(revenue)
        })
    
    monthly_revenue.reverse()
    
    return render_template('admin/dashboard.html',
                         stats={
                             'total_users': total_users,
                             'farmers': farmers,
                             'buyers': buyers,
                             'consultants': consultants,
                             'recent_registrations': recent_registrations,
                             'total_crops': total_crops,
                             'active_crops': active_crops,
                             'organic_crops': organic_crops,
                             'total_orders': total_orders,
                             'pending_orders': pending_orders,
                             'completed_orders': completed_orders,
                             'total_revenue': total_revenue,
                             'total_consultations': total_consultations,
                             'pending_consultations': pending_consultations,
                             'completed_consultations': completed_consultations
                         },
                         recent_orders=recent_orders,
                         recent_consultations=recent_consultations,
                         recent_users=recent_users,
                         monthly_revenue=monthly_revenue)

@bp.route('/users')
@login_required
@admin_required
def users():
    """Manage users"""
    page = request.args.get('page', 1, type=int)
    role_filter = request.args.get('role', '')
    search = request.args.get('search', '')
    
    query = User.query
    
    if role_filter:
        query = query.filter_by(role=role_filter)
    
    if search:
        query = query.filter(
            (User.username.contains(search)) |
            (User.email.contains(search)) |
            (User.first_name.contains(search)) |
            (User.last_name.contains(search))
        )
    
    users = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/users.html', users=users, role_filter=role_filter, search=search)

@bp.route('/users/<int:user_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(user_id):
    """Toggle user active status"""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('Cannot deactivate your own account!', 'error')
        return redirect(url_for('admin.users'))
    
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'activated' if user.is_active else 'deactivated'
    flash(f'User {user.username} has been {status}!', 'success')
    return redirect(url_for('admin.users'))

@bp.route('/users/<int:user_id>/change-role', methods=['POST'])
@login_required
@admin_required
def change_user_role(user_id):
    """Change user role"""
    user = User.query.get_or_404(user_id)
    new_role = request.form['role']
    
    if user.id == current_user.id:
        flash('Cannot change your own role!', 'error')
        return redirect(url_for('admin.users'))
    
    user.role = new_role
    db.session.commit()
    
    flash(f'User {user.username} role changed to {new_role}!', 'success')
    return redirect(url_for('admin.users'))

@bp.route('/crops')
@login_required
@admin_required
def crops():
    """Manage crops"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    organic_filter = request.args.get('organic', '')
    
    query = Crop.query
    
    if search:
        query = query.filter(
            (Crop.name.contains(search)) |
            (Crop.description.contains(search)) |
            (Crop.location.contains(search))
        )
    
    if organic_filter == 'yes':
        query = query.filter_by(is_organic=True)
    elif organic_filter == 'no':
        query = query.filter_by(is_organic=False)
    
    crops = query.order_by(Crop.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/crops.html', crops=crops, search=search, organic_filter=organic_filter)

@bp.route('/crops/<int:crop_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_crop_status(crop_id):
    """Toggle crop active status"""
    crop = Crop.query.get_or_404(crop_id)
    crop.is_active = not crop.is_active
    db.session.commit()
    
    status = 'activated' if crop.is_active else 'deactivated'
    flash(f'Crop {crop.name} has been {status}!', 'success')
    return redirect(url_for('admin.crops'))

@bp.route('/orders')
@login_required
@admin_required
def orders():
    """Manage orders"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    payment_filter = request.args.get('payment', '')
    
    query = Order.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    if payment_filter:
        query = query.filter_by(payment_status=payment_filter)
    
    orders = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/orders.html', orders=orders, status_filter=status_filter, payment_filter=payment_filter)

@bp.route('/orders/<int:order_id>/update-status', methods=['POST'])
@login_required
@admin_required
def update_order_status(order_id):
    """Update order status"""
    order = Order.query.get_or_404(order_id)
    new_status = request.form['status']
    
    order.status = new_status
    db.session.commit()
    
    flash(f'Order {order.order_number} status updated to {new_status}!', 'success')
    return redirect(url_for('admin.orders'))

@bp.route('/consultations')
@login_required
@admin_required
def consultations():
    """Manage consultations"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    category_filter = request.args.get('category', '')
    
    query = Consultation.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    if category_filter:
        query = query.filter_by(category=category_filter)
    
    consultations = query.order_by(Consultation.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/consultations.html', consultations=consultations, 
                         status_filter=status_filter, category_filter=category_filter)

@bp.route('/consultations/<int:consultation_id>/assign', methods=['POST'])
@login_required
@admin_required
def assign_consultation(consultation_id):
    """Assign consultation to consultant"""
    consultation = Consultation.query.get_or_404(consultation_id)
    consultant_id = request.form['consultant_id']
    
    if consultant_id:
        consultant = User.query.filter_by(id=consultant_id, role='consultant').first()
        if consultant:
            consultation.consultant_id = consultant_id
            consultation.status = 'in_progress'
            db.session.commit()
            flash(f'Consultation assigned to {consultant.get_full_name()}!', 'success')
        else:
            flash('Invalid consultant selected!', 'error')
    else:
        consultation.consultant_id = None
        consultation.status = 'pending'
        db.session.commit()
        flash('Consultation unassigned!', 'success')
    
    return redirect(url_for('admin.consultations'))

@bp.route('/reports')
@login_required
@admin_required
def reports():
    """Generate reports and analytics"""
    
    # Revenue report
    total_revenue = db.session.query(func.sum(Order.total_amount)).filter_by(payment_status='paid').scalar() or 0
    
    # Top selling crops
    top_crops = db.session.query(
        Crop.name,
        func.sum(OrderItem.quantity).label('total_quantity'),
        func.sum(OrderItem.total_price).label('total_revenue')
    ).join(OrderItem).join(Order).filter(
        Order.payment_status == 'paid'
    ).group_by(Crop.name).order_by(func.sum(OrderItem.total_price).desc()).limit(10).all()
    
    # User growth over time
    user_growth = []
    for i in range(12):
        month_start = datetime.utcnow() - timedelta(days=30*i)
        month_end = month_start + timedelta(days=30)
        new_users = User.query.filter(
            User.created_at >= month_start,
            User.created_at < month_end
        ).count()
        user_growth.append({
            'month': month_start.strftime('%b %Y'),
            'users': new_users
        })
    
    user_growth.reverse()
    
    # Consultation categories
    consultation_categories = db.session.query(
        Consultation.category,
        func.count(Consultation.id).label('count')
    ).group_by(Consultation.category).all()
    
    return render_template('admin/reports.html',
                         total_revenue=total_revenue,
                         top_crops=top_crops,
                         user_growth=user_growth,
                         consultation_categories=consultation_categories)

@bp.route('/settings')
@login_required
@admin_required
def settings():
    """Admin settings"""
    return render_template('admin/settings.html')
