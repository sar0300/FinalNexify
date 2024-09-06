from flask import Flask, request, render_template, jsonify
import mysql.connector
from werkzeug.security import check_password_hash

app = Flask(__name__)

# Function to create a connection to the MySQL database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='budget_tracker',
            user='root',  # Replace with your MySQL username
            password='yaatri@1830;'  # Replace with your MySQL password
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")
        return None

# Route to handle user login
@app.route('/login', methods=['POST'])
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connect to MySQL
        connection = create_connection()
        if connection is None:
            return jsonify({"message": "Failed to connect to the database"}), 500

        try:
            cursor = connection.cursor()

            # Fetch the user data from the MySQL database
            query = "SELECT password FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()

            if result:
                stored_password = result[0]
                # Check if the password matches
                if check_password_hash(stored_password, password):
                    return render_template('login.html', message="Login Success")
                else:
                    return render_template('login.html', message="Login Failed")
            else:
                return render_template('login.html', message="Login Failed")

        finally:
            cursor.close()
            connection.close()

    # Render the login page for GET requests
    return render_template('login.html')


if __name__ == '__main__':
    app.run(port=5001, debug=True)
