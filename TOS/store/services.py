
# `requests` is not required for this mock service implementation.
# In a real integration, install requests and uncomment the API call below.

# import requests

def trigger_external_payment(order_id, amount):
    """
    Mock logic for a Third-Party Payment Gateway API.
    """
    print(f"Connecting to Payment API for Order {order_id}...")
    # In a real app: response = requests.post('https://api.stripe.com/v1/...', data=...)
    return True

def send_external_email(order_email, order_id):
    """
    Mock logic for a Third-Party Email Service API.
    """
    print(f"Sending Confirmation Email for Order {order_id} to {order_email}...")
    # In a real app: Send email via SendGrid/Mailgun API
    return True