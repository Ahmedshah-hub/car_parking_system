from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'YUADbOb2Wl0aeJTMfXtoOZhP   ')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///parking.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Parking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_number = db.Column(db.String(20), unique=True, nullable=False)
    vehicle_type = db.Column(db.String(20), nullable=False) 
    entry_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico')

@app.route('/api/park', methods=['POST'])
def park_vehicle():
    data = request.get_json()
    vehicle_number = data.get('vehicle_number')
    vehicle_type = data.get('vehicle_type')
    
    if not vehicle_number:
        return jsonify({'error': 'Vehicle number is required'}), 400
        
    try:
        new_parking = Parking(
            vehicle_number=vehicle_number,
            vehicle_type=vehicle_type,
            entry_time=datetime.utcnow()
        )
        db.session.add(new_parking)
        db.session.commit()
        return jsonify({'message': 'Vehicle parked successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Vehicle already parked'}), 400

@app.route('/api/exit', methods=['POST'])
def exit_vehicle():
    data = request.get_json()
    vehicle_number = data.get('vehicle_number')
    
    if not vehicle_number:
        return jsonify({'error': 'Vehicle number is required'}), 400
        
    parking = Parking.query.filter_by(vehicle_number=vehicle_number).first()
    if parking:
        db.session.delete(parking)
        db.session.commit()
        return jsonify({'message': 'Vehicle exited successfully'}), 200
    return jsonify({'error': 'Vehicle not found'}), 404

@app.route('/api/status')
def get_status():
    parkings = Parking.query.all()
    return jsonify([{
        'vehicle_number': p.vehicle_number,
        'vehicle_type': p.vehicle_type,
        'entry_time': p.entry_time.strftime('%Y-%m-%d %H:%M:%S')
    } for p in parkings])

# For local development
if __name__ == '__main__':
    app.run(debug=True)
