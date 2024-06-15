from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
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
    return render_template("index.html")


# Run the Flask app if this file is executed directly
if __name__ == "__main__":
    app.run(debug=True)
