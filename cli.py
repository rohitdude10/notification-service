"""
Command-line interface for the price notification service
"""
import argparse
from notification_service import send_price_alert, send_project_inquiry

def main():
    parser = argparse.ArgumentParser(description='Send notifications to users')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Price alert command
    price_parser = subparsers.add_parser('price-alert', help='Send price alert notification')
    price_parser.add_argument('--email', required=True, help='Email address of the recipient')
    price_parser.add_argument('--product', required=True, help='Name of the product')
    price_parser.add_argument('--current_price', required=True, type=float, help='Current price of the product')
    price_parser.add_argument('--previous_price', required=True, type=float, help='Previous price of the product')
    price_parser.add_argument('--url', required=True, help='URL of the product')
    price_parser.add_argument('--image', help='URL of the product image (optional)')
    
    # Project inquiry command
    inquiry_parser = subparsers.add_parser('project-inquiry', help='Send project inquiry notification')
    inquiry_parser.add_argument('--recipient', required=True, help='Email address of the recipient')
    inquiry_parser.add_argument('--name', required=True, help='Name of the sender')
    inquiry_parser.add_argument('--email', required=True, help='Email address of the sender')
    inquiry_parser.add_argument('--subject', required=True, help='Subject of the inquiry')
    inquiry_parser.add_argument('--message', required=True, help='Message body of the inquiry')
    
    args = parser.parse_args()
    
    if args.command == 'price-alert':
        result = send_price_alert(
            user_email=args.email,
            product_name=args.product,
            current_price=args.current_price,
            previous_price=args.previous_price,
            product_url=args.url,
            image_url=args.image
        )
        
        if result.status_code == 200:
            print(f"✅ Price alert notification sent successfully to {args.email}")
        else:
            print(f"❌ Failed to send price alert notification. Status code: {result.status_code}")
            print(f"Error details: {result.json()}")
    
    elif args.command == 'project-inquiry':
        result = send_project_inquiry(
            recipient_email=args.recipient,
            sender_name=args.name,
            sender_email=args.email,
            subject=args.subject,
            message=args.message
        )
        
        if result.status_code == 200:
            print(f"✅ Project inquiry notification sent successfully to {args.recipient}")
        else:
            print(f"❌ Failed to send project inquiry notification. Status code: {result.status_code}")
            print(f"Error details: {result.json()}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 