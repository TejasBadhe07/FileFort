from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder="../frontend", static_folder="../frontend/static")
CORS(app)

# ✅ Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../backend/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ✅ Define User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)  # Hashed password

# ✅ Create database tables
with app.app_context():
    db.create_all()

# ✅ Route to Serve Login Page
@app.route('/')
def home():
    return render_template('index.html')  # This is your login page

# ✅ Register Route (GET = Show Form, POST = Register User)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':  
        return render_template('register.html')  # Show the registration page

    # POST Request - Handle Registration
    data = request.json
    if not data.get('username') or not data.get('password'):
        return jsonify({"message": "Username & password required"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "User already exists"}), 400
    
    hashed_password = generate_password_hash(data['password'])  # Hash password
    new_user = User(username=data['username'], password_hash=hashed_password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully"}), 201


# ✅ Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()

    if user and check_password_hash(user.password_hash, data['password']):  
        return jsonify({"message": "Login successful"}), 200
    
    return jsonify({"message": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(debug=True)
