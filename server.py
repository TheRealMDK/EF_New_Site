from flask import Flask, render_template, request, jsonify, session
import secrets
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from waitress import serve

# python -m pip install -r requirements.txt

# Load environment variables from the .env file
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)
# Set a secret key for CSRF protection
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

@app.before_request
def generate_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)

# Define the route for the home page
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            data = request.get_json()  # Parse JSON data from AJAX request
            csrf_token = data.get("csrf_token")
            if csrf_token != session.get('csrf_token'):
                return jsonify({"error": "CSRF token mismatch"}), 403
            name = data.get("name")
            number = data.get("number")
            email = data.get("email")
            user_subject = data.get("subject")
            user_message = data.get("message")

            # Email sending logic using environment variables
            smtp_server = "mail.edenfitness.co.za"
            smtp_username = "website@edenfitness.co.za"
            smtp_password = os.getenv("EF_SMTP_PASSWORD")
            port = 465
            sender_email = "website@edenfitness.co.za"
            receiver_email = "accounts@edenfitness.co.za"

            # Construct the email message
            subject = f"{user_subject}"
            body = f"Name: {name}\nNumber: {number}\nEmail: {email}\n\n{user_message}"
            
            # Create a multipart message and set headers
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = receiver_email
            message['Subject'] = subject

            # Add body to email
            message.attach(MIMEText(body, 'plain'))

            # Secure SSL context
            context = ssl.create_default_context()

            # Send the email
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(smtp_username, smtp_password)
                server.sendmail(sender_email, receiver_email, message.as_string())
                print('Email sent successfully!')

            # If email sent successfully, return success to client
            return jsonify({"message": "Email sent successfully"}), 200
        
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            # If email sending fails, return error to client
            return jsonify({"error": str(e)}), 500

    # Handle GET request or non-AJAX POST request
    return render_template("index.html", csrf_token=session.get('csrf_token'))


# Run the Flask app if this file is executed directly
if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
