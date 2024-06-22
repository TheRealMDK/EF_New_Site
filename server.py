from flask import Flask, render_template, request, jsonify
import smtplib
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


# Define the route for the home page
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            data = request.get_json()  # Parse JSON data from AJAX request
            name = data.get("name")
            email = data.get("email")
            user_subject = data.get("subject")
            message = data.get("message")

            # Email sending logic using environment variables
            smtp_server = os.getenv("MG_SMTP_SERVER")
            smtp_username = os.getenv("MG_SMTP_USERNAME")
            smtp_password = os.getenv("MG_SMTP_PASSWORD")
            port = 587
            sender = "edenfitness4@gmail.com"
            receiver = "info@edenfitness.co.za"

            # Construct the email message
            subject = f"New email enquiry received: {user_subject}"
            body = f"Name: {name}\nEmail: {email}\nSubject: {user_subject}\nMessage: {message}"
            email_message = f"Subject: {subject}\nTo: {receiver}\nFrom: {sender}\n\n{body}"

            # Send the email
            with smtplib.SMTP(smtp_server, port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(sender, receiver, email_message.encode("utf-8"))

            # If email sent successfully, return success to client
            return jsonify({"message": "Email sent successfully"}), 200
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            # If email sending fails, return error to client
            return jsonify({"error": str(e)}), 500

    # Handle GET request or non-AJAX POST request
    return render_template("index.html")


# Run the Flask app if this file is executed directly
if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
