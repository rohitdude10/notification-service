# Email Notification Service

A simple Python service for sending email notifications using Mailjet. Supports both price tracking alerts and project inquiries.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Create a `.env` file based on the provided `.env.example`:
   ```
   cp .env.example .env
   ```

3. Add your Mailjet API credentials to the `.env` file:
   ```
   MJ_APIKEY_PUBLIC=your_mailjet_api_key_here
   MJ_APIKEY_PRIVATE=your_mailjet_api_secret_here
   SENDER_EMAIL=your_sender_email_here
   SENDER_NAME=Your Sender Name
   ```

## Development Usage

### Testing the service

You can test the service by running the notification_service.py directly:

```bash
python notification_service.py
```

### CLI Usage

The CLI supports two types of notifications: price alerts and project inquiries.

#### Price Alert

Send a price alert notification:

```bash
python cli.py price-alert --email recipient@example.com --product "Sony Headphones" --current_price 278.00 --previous_price 349.99 --url "https://example.com/product" --image "https://example.com/image.jpg"
```

#### Project Inquiry

Send a project inquiry notification:

```bash
python cli.py project-inquiry --recipient team@example.com --name "John Doe" --email john@example.com --subject "Website Development Project" --message "Hello, I'm interested in developing a new website for my business. Can you help?"
```

### API Usage

Run the Flask API server in development mode:

```bash
python api.py
```

The API supports CORS (Cross-Origin Resource Sharing) and can be accessed from any origin. The following headers are allowed:
- Content-Type
- Authorization

#### Send a Price Alert

```bash
curl -X POST http://localhost:5000/api/v1/send-price-alert \
  -H "Content-Type: application/json" \
  -d '{
    "email": "recipient@example.com",
    "product_name": "Sony Headphones",
    "current_price": 278.00,
    "previous_price": 349.99,
    "product_url": "https://example.com/product",
    "image_url": "https://example.com/image.jpg"
  }'
```

#### Send a Project Inquiry

```bash
curl -X POST http://localhost:5000/api/v1/send-project-inquiry \
  -H "Content-Type: application/json" \
  -d '{
    "recipient_email": "team@example.com",
    "sender_name": "John Doe",
    "sender_email": "john@example.com",
    "subject": "Website Development Project",
    "message": "Hello, I am interested in developing a new website for my business. Can you help?"
  }'
```

## Production Deployment

### Prerequisites

- Python 3.8 or higher
- Gunicorn
- Nginx (recommended)
- SSL certificate (recommended)

### Environment Setup

1. Set up your production environment variables:
   ```
   FLASK_ENV=production
   SECRET_KEY=your-secure-secret-key
   LOG_LEVEL=INFO
   CORS_ORIGINS=https://yourdomain.com,https://api.yourdomain.com
   ```

2. Create required directories:
   ```bash
   mkdir -p logs
   ```

### Running with Gunicorn

Start the service using Gunicorn:

```bash
gunicorn -c gunicorn.conf.py api:app
```

### Nginx Configuration

Example Nginx configuration:

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Systemd Service

Create a systemd service file `/etc/systemd/system/notification-service.service`:

```ini
[Unit]
Description=Email Notification Service
After=network.target

[Service]
User=your-user
Group=your-group
WorkingDirectory=/path/to/your/service
Environment="PATH=/path/to/your/virtualenv/bin"
ExecStart=/path/to/your/virtualenv/bin/gunicorn -c gunicorn.conf.py api:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Start the service:
```bash
sudo systemctl enable notification-service
sudo systemctl start notification-service
```

## API Endpoints

- **GET /health**: Health check endpoint
- **POST /api/v1/send-price-alert**: Send a price alert notification
  - Required fields: email, product_name, current_price, previous_price, product_url
  - Optional fields: image_url
- **POST /api/v1/send-project-inquiry**: Send a project inquiry notification
  - Required fields: recipient_email, sender_name, sender_email, subject, message
- **POST /send-notification**: Legacy endpoint that redirects to /api/v1/send-price-alert

## Security Features

- Rate limiting (50 requests per minute for price alerts, 30 for project inquiries)
- CORS protection with configurable allowed origins
- Content Security Policy (CSP) headers
- Secure cookie settings
- HTTPS enforcement
- Request size limits
- Structured logging with sensitive data filtering

## Monitoring

The service includes comprehensive logging:
- Access logs: `logs/access.log`
- Error logs: `logs/error.log`
- Application logs: `logs/app.log`

All logs are in JSON format for easy parsing and analysis.

## Error Handling

The service includes:
- Global error handler
- Structured error responses
- Detailed logging of errors
- Rate limit exceeded handling
- Input validation
- Graceful degradation 