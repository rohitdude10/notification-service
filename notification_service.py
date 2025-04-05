"""
Send price tracking notifications to users
"""
from mailjet_rest import Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API keys from environment variables
api_key = os.getenv('MJ_APIKEY_PUBLIC')
api_secret = os.getenv('MJ_APIKEY_PRIVATE')
sender_email = os.getenv('SENDER_EMAIL', 'rohitkumardude10@gmail.com')
sender_name = os.getenv('SENDER_NAME', 'Price Tracker')

# Initialize Mailjet client
mailjet = Client(auth=(api_key, api_secret), version='v3.1')

def send_price_alert(user_email, product_name, current_price, previous_price, product_url, image_url=None):
    """
    Send a price alert notification when a product's price changes.
    
    Args:
        user_email (str): Email address of the recipient
        product_name (str): Name of the product
        current_price (float): Current price of the product
        previous_price (float): Previous price of the product
        product_url (str): URL of the product
        image_url (str, optional): URL of the product image
    """
    price_diff = previous_price - current_price
    percent_change = (price_diff / previous_price) * 100 if previous_price > 0 else 0
    
    # Determine if it's a price drop or increase
    if current_price < previous_price:
        price_message = f"Price Drop Alert: Save ${price_diff:.2f} ({percent_change:.1f}%)"
        color = "#28a745"  # Green for price drop
    else:
        price_message = f"Price Increase Alert: ${abs(price_diff):.2f} ({abs(percent_change):.1f}%)"
        color = "#dc3545"  # Red for price increase
    
    # Create email template with product information
    html_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #eee; border-radius: 5px;">
        <h2 style="color: {color};">{price_message}</h2>
        <div style="display: flex; margin-bottom: 20px;">
            {'<img src="' + image_url + '" style="max-width: 150px; max-height: 150px; margin-right: 20px;" />' if image_url else ''}
            <div>
                <h3>{product_name}</h3>
                <p>Current Price: <strong>${current_price:.2f}</strong></p>
                <p>Previous Price: <s>${previous_price:.2f}</s></p>
            </div>
        </div>
        <a href="{product_url}" style="display: inline-block; background-color: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 4px;">View Product</a>
    </div>
    """
    
    data = {
        'Messages': [
            {
                "From": {
                    "Email": sender_email,
                    "Name": sender_name
                },
                "To": [
                    {
                        "Email": user_email,
                        "Name": "Valued Customer"
                    }
                ],
                "Subject": f"Price Alert: {product_name}",
                "TextPart": f"{price_message} for {product_name}. Current price: ${current_price:.2f}, Previous price: ${previous_price:.2f}. View at: {product_url}",
                "HTMLPart": html_content
            }
        ]
    }
    
    result = mailjet.send.create(data=data)
    return result

def send_project_inquiry(recipient_email, sender_name, sender_email, subject, message):
    """
    Send a project inquiry notification.
    
    Args:
        recipient_email (str): Email address of the recipient
        sender_name (str): Name of the person sending the inquiry
        sender_email (str): Email address of the sender
        subject (str): Subject of the inquiry
        message (str): Message body of the inquiry
    """
    # Create email template with inquiry information
    html_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #eee; border-radius: 5px;">
        <h2 style="color: #007bff;">New Project Inquiry</h2>
        <div style="margin-bottom: 20px; padding: 15px; background-color: #f8f9fa; border-radius: 5px;">
            <p><strong>From:</strong> {sender_name} ({sender_email})</p>
            <p><strong>Subject:</strong> {subject}</p>
            <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #ddd;">
                <p><strong>Message:</strong></p>
                <p style="white-space: pre-line;">{message}</p>
            </div>
        </div>
        <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee; font-size: 0.9em; color: #6c757d;">
            <p>To reply to this inquiry, simply respond directly to this email.</p>
        </div>
    </div>
    """
    
    data = {
        'Messages': [
            {
                "From": {
                    "Email": sender_email,
                    "Name": sender_name
                },
                "ReplyTo": {
                    "Email": sender_email,
                    "Name": sender_name
                },
                "To": [
                    {
                        "Email": recipient_email,
                        "Name": "Project Team"
                    }
                ],
                "Subject": f"Project Inquiry: {subject}",
                "TextPart": f"New inquiry from {sender_name} ({sender_email})\n\nSubject: {subject}\n\nMessage:\n{message}",
                "HTMLPart": html_content
            }
        ]
    }
    print("mail has been send" , data)
    result = mailjet.send.create(data=data)
    print("mail has been send" , result)
    return result

def send_custom_email(recipient_email, subject, html_content, text_content=None):
    """
    Send a custom email notification with HTML content.
    
    Args:
        recipient_email (str): Email address of the recipient
        subject (str): Subject of the email
        html_content (str): HTML content of the email
        text_content (str, optional): Plain text version of the email. If not provided,
                                     a simple message will be used as fallback.
    
    Returns:
        Response from the email API
    """
    if text_content is None:
        text_content = "This email contains HTML content. Please use an email client that supports HTML to view it properly."
    
    data = {
        'Messages': [
            {
                "From": {
                    "Email": sender_email,
                    "Name": "Birthday Buddy"
                },
                "To": [
                    {
                        "Email": recipient_email,
                        "Name": "Recipient"
                    }
                ],
                "Subject": subject,
                "TextPart": text_content,
                "HTMLPart": html_content
            }
        ]
    }
    
    result = mailjet.send.create(data=data)
    
    return result

# Example usage
if __name__ == "__main__":
    # Test the email function
    result = send_price_alert(
        user_email="recipient@example.com",
        product_name="Sony WH-1000XM4 Wireless Noise Cancelling Headphones",
        current_price=278.00,
        previous_price=349.99,
        product_url="https://www.amazon.com/Sony-WH-1000XM4-Canceling-Headphones-phone-call/dp/B0863TXGM3/",
        image_url="https://m.media-amazon.com/images/I/71o8Q5XJS5L._AC_SL1500_.jpg"
    )
    print(f"Status code: {result.status_code}")
    print(f"Response: {result.json()}")
    
    # Test the project inquiry function
    result = send_project_inquiry(
        recipient_email="team@example.com",
        sender_name="John Doe",
        sender_email="john@example.com",
        subject="Website Development Project",
        message="Hello,\n\nI'm interested in developing a new e-commerce website for my business. Could you please provide me with information about your services and pricing?\n\nThank you,\nJohn"
    )
    print(f"Status code: {result.status_code}")
    print(f"Response: {result.json()}") 