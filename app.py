#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# Recommended to suppress warnings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


# Home page
@app.route('/')
def home():
    return render_template('index.html')


# Add a user (admin)
@app.route('/add_user')
def add_user():
    try:
        if not User.query.filter_by(username='admin').first():
            new_user = User(username='admin', email='admin@example.com')
            db.session.add(new_user)
            db.session.commit()
            return "User added!"
        return "User already exists."
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {e}"


# List all users
@app.route('/users')
def list_users():
    users = User.query.all()
    return '<br>'.join([f"User: {u.username}, Email: {u.email}" for u in users])


# Update a user
@app.route('/update_user')
def update_user():
    try:
        user = User.query.filter_by(username='admin').first()
        if user:
            user.email = 'new_admin@example.com'
            db.session.commit()
            return "User updated!"
        return "User not found."
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {e}"


# Delete a user
@app.route('/delete_user')
def delete_user():
    try:
        user = User.query.filter_by(username='admin').first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return "User deleted!"
        return "User not found."
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {e}"


# Debug query route (only for dev)
@app.route('/debug_queries')
def debug_queries():
    user_with_gmail = User.query.filter(
    User.email.endswith('@gmail.com')).all()
    user_username = User.query.order_by(User.username).all()
    first_2 = User.query.limit(2).all()
    total = User.query.count()
    return f"""
    Total users: {total}<br>
    First 2 users: {[u.username for u in first_2]}<br>
    Users with Gmail: {[u.email for u in user_with_gmail]}<br>
    Ordered by username: {[u.username for u in user_username]}<br>
    """


# Initialize database
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
