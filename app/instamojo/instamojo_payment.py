from instamojo_wrapper import Instamojo
from ..config import settings


__api = Instamojo(api_key=settings.instamojo_api_key,
                auth_token=settings.instamojo_auth_token)



# Create a new Payment Request
def create_new_payment_request(amount: str, name: str, email: str, phone: str, endpoint='https://test.instamojo.com/api/1.1/'):
    response = __api.payment_request_create(
        amount=amount,
        purpose='Plantonic plant purchase',
        send_email=False,
        email=email,
        phone=phone,
        buyer_name=name,
        redirect_url="http://www.example.com/handle_redirect.py"
        )

    # print the long URL of the payment request.
    print(response)
    # print the unique ID(or payment request ID)
    # print(response['payment_request']['id'])

    import requests

    headers = { "X-Api-Key": settings.instamojo_api_key, "X-Auth-Token": settings.instamojo_auth_token}
    payload = {
    'purpose': 'Plantonic plant purchase',
    'amount': amount,
    'buyer_name': name,
    'email': email,
    'phone': phone,
    'redirect_url': 'http://www.example.com/redirect/',
    'send_email': 'False',
    'send_sms': 'False',
    'webhook': 'http://www.example.com/webhook/',
    'allow_repeated_payments': 'False',
    }
    response = requests.post("https://www.instamojo.com/api/1.1/payment-requests/", data=payload, headers=headers)

    print(response.text)