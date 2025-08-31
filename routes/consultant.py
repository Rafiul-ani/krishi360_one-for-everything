from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import Consultation, User, db
from datetime import datetime

bp = Blueprint('consultant', __name__, url_prefix='/consultant')

@bp.route('/dashboard')
@login_required
def dashboard():
    """Consultant dashboard with overview statistics"""
    if current_user.role != 'consultant':
        flash('Access denied. Consultant role required.', 'error')
        return redirect(url_for('index'))
    
    # Get consultations assigned to this consultant
    consultations = Consultation.query.filter_by(consultant_id=current_user.id).order_by(Consultation.created_at.desc()).all()
    
    # Get pending consultations (not yet assigned)
    pending_consultations = Consultation.query.filter_by(consultant_id=None, status='pending').order_by(Consultation.created_at.desc()).all()
    
    # Calculate statistics
    total_consultations = len(consultations)
    pending_count = len([c for c in consultations if c.status == 'pending'])
    in_progress_count = len([c for c in consultations if c.status == 'in_progress'])
    completed_count = len([c for c in consultations if c.status == 'completed'])
    
    # Calculate average rating
    rated_consultations = [c for c in consultations if c.rating is not None]
    avg_rating = sum([c.rating for c in rated_consultations]) / len(rated_consultations) if rated_consultations else 0
    
    return render_template('consultant/dashboard.html', 
                         consultations=consultations,
                         pending_consultations=pending_consultations,
                         stats={
                             'total_consultations': total_consultations,
                             'pending_count': pending_count,
                             'in_progress_count': in_progress_count,
                             'completed_count': completed_count,
                             'avg_rating': round(avg_rating, 1)
                         })

@bp.route('/consultations')
@login_required
def consultations():
    """View all consultations assigned to consultant"""
    if current_user.role != 'consultant':
        flash('Access denied. Consultant role required.', 'error')
        return redirect(url_for('index'))
    
    consultations = Consultation.query.filter_by(consultant_id=current_user.id).order_by(Consultation.created_at.desc()).all()
    return render_template('consultant/consultations.html', consultations=consultations)

@bp.route('/consultations/available')
@login_required
def available_consultations():
    """View available consultations to claim"""
    if current_user.role != 'consultant':
        flash('Access denied. Consultant role required.', 'error')
        return redirect(url_for('index'))
    
    consultations = Consultation.query.filter_by(consultant_id=None, status='pending').order_by(Consultation.created_at.desc()).all()
    return render_template('consultant/available_consultations.html', consultations=consultations)

@bp.route('/consultations/<int:consultation_id>/claim', methods=['POST'])
@login_required
def claim_consultation(consultation_id):
    """Claim a consultation request"""
    if current_user.role != 'consultant':
        flash('Access denied. Consultant role required.', 'error')
        return redirect(url_for('index'))
    
    consultation = Consultation.query.filter_by(id=consultation_id, consultant_id=None, status='pending').first_or_404()
    
    consultation.consultant_id = current_user.id
    consultation.status = 'in_progress'
    db.session.commit()
    
    flash('Consultation claimed successfully!', 'success')
    return redirect(url_for('consultant.consultation_details', consultation_id=consultation_id))

@bp.route('/consultations/<int:consultation_id>')
@login_required
def consultation_details(consultation_id):
    """View consultation details"""
    if current_user.role != 'consultant':
        flash('Access denied. Consultant role required.', 'error')
        return redirect(url_for('index'))
    
    consultation = Consultation.query.filter_by(id=consultation_id).first_or_404()
    
    # Check if consultant has access to this consultation
    if consultation.consultant_id != current_user.id and consultation.consultant_id is not None:
        flash('Access denied. This consultation is assigned to another consultant.', 'error')
        return redirect(url_for('consultant.consultations'))
    
    return render_template('consultant/consultation_details.html', consultation=consultation)

@bp.route('/consultations/<int:consultation_id>/respond', methods=['GET', 'POST'])
@login_required
def respond_consultation(consultation_id):
    """Respond to consultation request"""
    if current_user.role != 'consultant':
        flash('Access denied. Consultant role required.', 'error')
        return redirect(url_for('index'))
    
    consultation = Consultation.query.filter_by(id=consultation_id, consultant_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        response = request.form['response']
        
        consultation.response = response
        consultation.status = 'completed'
        consultation.completed_at = datetime.utcnow()
        db.session.commit()
        
        flash('Consultation response submitted successfully!', 'success')
        return redirect(url_for('consultant.consultation_details', consultation_id=consultation_id))
    
    return render_template('consultant/respond_consultation.html', consultation=consultation)

@bp.route('/consultations/<int:consultation_id>/update-status', methods=['POST'])
@login_required
def update_consultation_status(consultation_id):
    """Update consultation status"""
    if current_user.role != 'consultant':
        flash('Access denied. Consultant role required.', 'error')
        return redirect(url_for('index'))
    
    consultation = Consultation.query.filter_by(id=consultation_id, consultant_id=current_user.id).first_or_404()
    new_status = request.form['status']
    
    consultation.status = new_status
    
    if new_status == 'completed' and not consultation.completed_at:
        consultation.completed_at = datetime.utcnow()
    
    db.session.commit()
    
    flash(f'Consultation status updated to {new_status}!', 'success')
    return redirect(url_for('consultant.consultation_details', consultation_id=consultation_id))

@bp.route('/profile')
@login_required
def profile():
    """Consultant profile page"""
    if current_user.role != 'consultant':
        flash('Access denied. Consultant role required.', 'error')
        return redirect(url_for('index'))
    
    # Get consultant's statistics
    consultations = Consultation.query.filter_by(consultant_id=current_user.id).all()
    
    total_consultations = len(consultations)
    completed_consultations = len([c for c in consultations if c.status == 'completed'])
    avg_rating = 0
    
    if completed_consultations > 0:
        rated_consultations = [c for c in consultations if c.rating is not None]
        if rated_consultations:
            avg_rating = sum([c.rating for c in rated_consultations]) / len(rated_consultations)
    
    return render_template('consultant/profile.html', 
                         user=current_user,
                         stats={
                             'total_consultations': total_consultations,
                             'completed_consultations': completed_consultations,
                             'avg_rating': round(avg_rating, 1)
                         })

@bp.route('/specializations')
@login_required
def specializations():
    """Manage consultant specializations"""
    if current_user.role != 'consultant':
        flash('Access denied. Consultant role required.', 'error')
        return redirect(url_for('index'))
    
    # Get consultations by category for this consultant
    consultations = Consultation.query.filter_by(consultant_id=current_user.id).all()
    
    # Count consultations by category
    category_stats = {}
    for consultation in consultations:
        category = consultation.category
        if category not in category_stats:
            category_stats[category] = {'total': 0, 'completed': 0, 'avg_rating': 0}
        
        category_stats[category]['total'] += 1
        if consultation.status == 'completed':
            category_stats[category]['completed'] += 1
            if consultation.rating:
                # Calculate average rating for this category
                cat_consultations = [c for c in consultations if c.category == category and c.rating is not None]
                if cat_consultations:
                    category_stats[category]['avg_rating'] = sum([c.rating for c in cat_consultations]) / len(cat_consultations)
    
    return render_template('consultant/specializations.html', category_stats=category_stats)
