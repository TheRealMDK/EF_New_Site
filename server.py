from flask import Flask, render_template, request
import smtplib
import os
from dotenv import load_dotenv

# python -m pip install -r requirements.txt

# Load environment variables from the .env file
load_dotenv("./.venv/Scripts/envvars.env")

# Initialize the Flask app
app = Flask(__name__)
# Set a secret key for CSRF protection
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")


# Define the route for the home page
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        user_subject = request.form.get("subject")
        message = request.form.get("message")

        # Email sending logic using environment variables
        smtp_server = os.environ.get("MG_SMTP_SERVER")
        smtp_username = os.environ.get("MG_SMTP_USERNAME")
        smtp_password = os.environ.get("MG_SMTP_PASSWORD")
        port = 587
        sender = "edenfitness4@gmail.com"
        receiver = "info@edenfitness.co.za"

        # Construct the email message
        subject = f"New email enquiry received."
        body = ""
        body += (f"Name: {name}\n"
                 f"Email: {email}\n"
                 f"Subject: {user_subject}\n"
                 f"Message: {message}"
                 )
        message = f"Subject: {subject}\nTo: {receiver}\nFrom: {sender}\n\n{body}"
        message = message.encode("utf-8")

        # Send the email
        try:    
            with smtplib.SMTP(smtp_server, port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(sender, receiver, message)
                # If email sent successfully, return success to client
                return "success"
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            # If email sending fails, return error to client
            return str(e), 500

    return render_template("index.html")


# Run the Flask app if this file is executed directly
if __name__ == "__main__":
    app.run(debug=True)
