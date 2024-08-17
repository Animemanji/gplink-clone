from flask import Blueprint, render_template, redirect, url_for, flash, request
    from werkzeug.security import generate_password_hash, check_password_hash
    from flask_login import login_user, logout_user, login_required, current_user
    from .models import User
    from . import db
    
    user = Blueprint('user', __name__)
    
    @user.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            email = request.form.get('email')
            username = request.form.get('username')
            password = request.form.get('password')
    
            # Check if the user already exists
            user_exists = User.query.filter_by(email=email).first()
            if user_exists:
                flash('Email address already exists', 'danger')
                return redirect(url_for('user.signup'))
    
            # Create new user
            new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
    
            # Log the user in after signup
            login_user(new_user)
            flash('Account created successfully', 'success')
            return redirect(url_for('user_dashboard.dashboard'))
    
        return render_template('signup.html')
    
    @user.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
    
            user = User.query.filter_by(email=email).first()
    
            # Check if the user exists and the password matches
            if not user or not check_password_hash(user.password, password):
                flash('Incorrect email or password', 'danger')
                return redirect(url_for('user.login'))
    
            # Log the user in
            login_user(user)
            flash('Logged in successfully', 'success')
            return redirect(url_for('user_dashboard.dashboard'))
    
        return render_template('login.html')
    
    @user.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Logged out successfully', 'success')
        return redirect(url_for('user.login'))
    
    @user.route('/profile')
    @login_required
    def profile():
        return render_template('profile.html', user=current_user)