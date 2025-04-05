"""
API for the price notification service
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from notification_service import send_price_alert, send_project_inquiry, send_custom_email
from config import config

# Initialize Flask app
app = Flask(__name__)

# Load configuration
config_name = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

# Initialize CORS with permissive settings
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "ok"}), 200

@app.route('/api/v1/send-price-alert', methods=['POST', 'OPTIONS'])
def send_price_notification():
    """Send price alert notification endpoint."""
    if request.method == 'OPTIONS':
        return '', 204
        
    data = request.json
    
    # Validate request data
    required_fields = ['email', 'product_name', 'current_price', 'previous_price', 'product_url']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    try:
        result = send_price_alert(
            user_email=data['email'],
            product_name=data['product_name'],
            current_price=float(data['current_price']),
            previous_price=float(data['previous_price']),
            product_url=data['product_url'],
            image_url=data.get('image_url')
        )
        
        if result.status_code == 200:
            return jsonify({
                "success": True,
                "message": f"Price alert notification sent to {data['email']}",
                "response": result.json()
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Failed to send price alert notification",
                "response": result.json()
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

@app.route('/api/v1/send-project-inquiry', methods=['POST', 'OPTIONS'])
def send_inquiry_notification():
    """Send project inquiry notification endpoint."""
    if request.method == 'OPTIONS':
        return '', 204
        
    data = request.json
    
    # Validate request data
    required_fields = ['recipient_email', 'sender_name', 'sender_email', 'subject', 'message']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    try:
        result = send_project_inquiry(
            recipient_email=data['recipient_email'],
            sender_name=data['sender_name'],
            sender_email=data['sender_email'],
            subject=data['subject'],
            message=data['message']
        )
        
        if result.status_code == 200:
            return jsonify({
                "success": True,
                "message": f"Project inquiry notification sent to {data['recipient_email']}",
                "response": result.json()
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Failed to send project inquiry notification",
                "response": result.json()
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

@app.route('/api/v1/send-custom-email', methods=['POST', 'OPTIONS'])
def send_custom_notification():
    """Send custom email notification endpoint."""
    if request.method == 'OPTIONS':
        return '', 204
        
    data = request.json
    
    # Validate request data
    required_fields = ['email', 'subject', 'html_content']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    try:
        result = send_custom_email(
            recipient_email=data['email'],
            subject=data['subject'],
            html_content=data['html_content'],
            text_content=data.get('text_content')
        )
        
        if result.status_code == 200:
            return jsonify({
                "success": True,
                "message": f"Custom email notification sent to {data['email']}",
                "response": result.json()
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Failed to send custom email notification",
                "response": result.json()
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

# Legacy endpoint for backward compatibility
@app.route('/send-notification', methods=['POST', 'OPTIONS'])
def send_notification():
    """Legacy endpoint that redirects to price alert endpoint."""
    return send_price_notification()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)