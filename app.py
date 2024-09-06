from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

# Database connection function
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='budget_tracker',
            user='root',
            password='yaatri@1830;'
        )
        return connection
    except Error as e:
        print(f"Error: '{e}'")
        return None

# Existing user registration route
@app.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.json
        fname = data['fname']
        mname = data['mname']
        lname = data['lname']
        email = data['email']
        mno = data['mno']
        username = data['uname']
        password = data['password']
        gender = data['gender']
        
        hashed_password = generate_password_hash(password)

        connection = create_connection()
        if connection is None:
            return jsonify({"message": "Failed to connect to the database"}), 500
        
        cursor = connection.cursor()
        query = """
            INSERT INTO users (fname, mname, lname, email, mno, username, password, gender) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (fname, mname, lname, email, mno, username, hashed_password, gender))
        connection.commit()

        message = "Successfully added" if cursor.rowcount > 0 else "Failed to add user"

        cursor.close()
        connection.close()

        return jsonify({"message": message}), 200

    except Exception as e:
        return jsonify({"message": "Error occurred: " + str(e)}), 500

# Existing route to add expenses
@app.route('/add_expense', methods=['POST'])
def add_expense():
    try:
        data = request.json
        category = data['category']
        amount = data['amount']
        
        if category not in ['utilities', 'entertainment', 'food', 'health', 'transport', 'other']:
            return jsonify({"message": "Invalid category"}), 400

        connection = create_connection()
        if connection is None:
            return jsonify({"message": "Failed to connect to the database"}), 500
        
        cursor = connection.cursor()
        query = f"INSERT INTO money ({category}) VALUES (%s)"
        cursor.execute(query, (amount,))
        connection.commit()

        message = "Expense added successfully" if cursor.rowcount > 0 else "Failed to add expense"

        cursor.close()
        connection.close()

        return jsonify({"message": message}), 200

    except Exception as e:
        return jsonify({"message": "Error occurred: " + str(e)}), 500

# Existing route for user login
@app.route('/login', methods=['POST'])
def login_user():
    try:
        data = request.json
        username = data['username']
        password = data['password']
        
        connection = create_connection()
        if connection is None:
            return jsonify({"message": "Failed to connect to the database"}), 500
        
        cursor = connection.cursor()
        query = "SELECT password FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[0], password):
            message = "Login successful"
        else:
            message = "Invalid username or password"

        cursor.close()
        connection.close()

        return jsonify({"message": message}), 200

    except Exception as e:
        return jsonify({"message": "Error occurred: " + str(e)}), 500

# Route to fetch data for pie chart
@app.route('/get_expense_data', methods=['GET'])
def get_expense_data():
    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"message": "Failed to connect to the database"}), 500
        
        cursor = connection.cursor()
        
        # Query to get the sum of each category
        query = """
        SELECT 
            SUM(utilities) as utilities,
            SUM(entertainment) as entertainment,
            SUM(food) as food,
            SUM(health) as health,
            SUM(transport) as transport,
            SUM(other) as other
        FROM money;
        """
        cursor.execute(query)
        result = cursor.fetchone()
        
        # Prepare the data for Google Charts
        data = [
            ["Category", "Amount"],
            ["Utilities", result[0] if result[0] else 0],
            ["Entertainment", result[1] if result[1] else 0],
            ["Food", result[2] if result[2] else 0],
            ["Health", result[3] if result[3] else 0],
            ["Transport", result[4] if result[4] else 0],
            ["Other", result[5] if result[5] else 0],
        ]
        
        cursor.close()
        connection.close()

        return jsonify(data)

    except Exception as e:
        return jsonify({"message": "Error occurred: " + str(e)}), 500

# Route to render the expense chart page
@app.route('/expense_chart')
def expense_chart():
    return render_template('expense_chart.html')

if __name__ == '__main__':
    app.run(debug=True)
