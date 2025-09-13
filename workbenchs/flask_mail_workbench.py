#!/usr/bin/env python3
"""
Flask-Mail Workbench

A standalone script to test Flask-Mail functionality.
Run this file directly to start a Flask server with an endpoint for sending test emails.

Usage:
1. Set environment variables for email configuration or edit the defaults below
2. Run this script: python flask_mail_workbench.py
3. Send a POST request to http://localhost:5000/send-email with JSON body:
   {
     "recipient": "your-email@example.com",
     "subject": "Test Email",
     "body": "This is a test email from Flask-Mail workbench."
   }

Environment variables:
- MAIL_SERVER: SMTP server (default: smtp.gmail.com)
- MAIL_PORT: SMTP port (default: 587)
- MAIL_USE_TLS: Use TLS (default: True)
- MAIL_USERNAME: Your email username
- MAIL_PASSWORD: Your email password or app password
- MAIL_DEFAULT_SENDER: Default sender email
"""

import os
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Configure Flask-Mail
app.config.update(
    MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_USE_TLS=os.getenv("MAIL_USE_TLS", "True").lower() == "true",
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_DEFAULT_SENDER=os.getenv("MAIL_DEFAULT_SENDER")
)

# Initialize Flask-Mail
mail = Mail(app)

@app.route('/send-email', methods=['POST'])
def send_email():
    """
    Send a test email using Flask-Mail
    
    Expected JSON body:
    {
        "recipient": "recipient@example.com",
        "subject": "Test Email",
        "body": "This is a test email."
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "message": "No JSON data provided"}), 400
            
        recipient = data.get('recipient')
        subject = data.get('subject', 'Test Email from Flask-Mail Workbench')
        body = data.get('body', 'This is a test email from Flask-Mail workbench.')
        
        if not recipient:
            return jsonify({"success": False, "message": "Recipient email is required"}), 400
            
        # Create message
        msg = Message(
            subject=subject,
            recipients=[recipient],
            body=body
        )
        
        # Send email
        mail.send(msg)
        
        return jsonify({
            "success": True,
            "message": f"Email sent successfully to {recipient}"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Failed to send email",
            "error": str(e)
        }), 500

@app.route('/')
def index():
    """Simple index page with instructions"""
    return """
    <html>
        <head>
            <title>Flask-Mail Workbench</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
                pre { background: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }
            </style>
        </head>
        <body>
            <h1>Flask-Mail Workbench</h1>
            <p>Use this endpoint to test sending emails with Flask-Mail:</p>
            
            <h3>Send a test email:</h3>
            <pre>
POST /send-email
Content-Type: application/json

{
    "recipient": "your-email@example.com",
    "subject": "Test Email",
    "body": "This is a test email from Flask-Mail workbench."
}
            </pre>
            
            <h3>Example using curl:</h3>
            <pre>
curl -X POST http://localhost:5000/send-email \\
     -H "Content-Type: application/json" \\
     -d '{"recipient": "your-email@example.com", "subject": "Test Email", "body": "This is a test email."}'
            </pre>
        </body>
    </html>
    """

if __name__ == '__main__':
    # Check if mail configuration is set
    if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
        print("WARNING: Mail username or password not set. Set MAIL_USERNAME and MAIL_PASSWORD environment variables.")
        
    # Print configuration (without password)
    print("Mail Configuration:")
    print(f"  MAIL_SERVER: {app.config['MAIL_SERVER']}")
    print(f"  MAIL_PORT: {app.config['MAIL_PORT']}")
    print(f"  MAIL_USE_TLS: {app.config['MAIL_USE_TLS']}")
    print(f"  MAIL_USERNAME: {app.config['MAIL_USERNAME']}")
    print(f"  MAIL_DEFAULT_SENDER: {app.config['MAIL_DEFAULT_SENDER']}")
    
    # Run the Flask app
    app.run(debug=True)
