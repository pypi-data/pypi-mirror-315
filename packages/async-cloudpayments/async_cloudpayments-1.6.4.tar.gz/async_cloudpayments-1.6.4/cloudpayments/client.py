import decimal
import aiohttp
import asyncio
from aiohttp import ClientSession
from requests.auth import HTTPBasicAuth

from .errors import CloudPaymentsError, PaymentError
from .models import Order, Receipt, Secure3d, Subscription, Transaction
from .utils import format_date, format_datetime


class CloudPayments(object):
    URL = 'https://api.cloudpayments.ru/'

    def __init__(self, public_id, api_secret):
        self.public_id = public_id
        self.api_secret = api_secret

    async def _send_request(self, session: ClientSession, endpoint: str, params=None, request_id=None):
        auth = aiohttp.BasicAuth(self.public_id, self.api_secret)

        headers = None
        if request_id is not None:
            headers = {'X-Request-ID': request_id}

        async with session.post(self.URL + endpoint, json=params, auth=auth, headers=headers) as response:
            response_json = await response.json()
            return response_json

    async def test(self, session: ClientSession, request_id=None):
        response = await self._send_request(session, 'test', request_id=request_id)

        if not response['Success']:
            raise CloudPaymentsError(response)
        return response['Message']

    async def get_transaction(self, session: ClientSession, transaction_id):
        """Get transaction info by its id."""
        params = {'TransactionId': transaction_id}
        response = await self._send_request(session, 'payments/get', params)
        if 'Model' in response.keys():
            return Transaction.from_dict(response['Model'])
        else:
            raise CloudPaymentsError(response)

    async def charge_card(self, session: ClientSession, cryptogram, amount, currency, name, ip_address,
                          invoice_id=None, description=None, account_id=None, email=None, data=None,
                          require_confirmation=False, service_fee=None):
        params = {
            'Amount': amount,
            'Currency': currency,
            'IpAddress': ip_address,
            'Name': name,
            'CardCryptogramPacket': cryptogram
        }
        if invoice_id is not None:
            params['InvoiceId'] = invoice_id
        if description is not None:
            params['Description'] = description
        if account_id is not None:
            params['AccountId'] = account_id
        if email is not None:
            params['Email'] = email
        if service_fee is not None:
            params['PayerServiceFee'] = service_fee
        if data is not None:
            params['JsonData'] = data

        endpoint = ('payments/cards/auth' if require_confirmation else
                    'payments/cards/charge')
        response = await self._send_request(session, endpoint, params)

        if response['Success']:
            return Transaction.from_dict(response['Model'])
        if response['Message']:
            raise CloudPaymentsError(response)
        if 'ReasonCode' in response['Model']:
            raise PaymentError(response)
        return Secure3d.from_dict(response['Model'])

    async def finish_3d_secure_authentication(self, session: ClientSession, transaction_id, pa_res):
        params = {
            'TransactionId': transaction_id,
            'PaRes': pa_res
        }
        response = await self._send_request(session, 'payments/cards/post3ds', params)

        if response['Success']:
            return Transaction.from_dict(response['Model'])
        raise PaymentError(response)

    async def charge_token(self, session: ClientSession, token, account_id, amount, currency, ip_address=None,
                           invoice_id=None, description=None, email=None, data=None, tr_initiator_code: int = 1,
                           require_confirmation=False):
        params = {
            'Amount': amount,
            'Currency': currency,
            'AccountId': account_id,
            'Token': token,
            'TrInitiatorCode': tr_initiator_code
        }
        if invoice_id is not None:
            params['InvoiceId'] = invoice_id
        if description is not None:
            params['Description'] = description
        if ip_address is not None:
            params['IpAddress'] = ip_address
        if email is not None:
            params['Email'] = email
        if data is not None:
            params['JsonData'] = data

        endpoint = ('payments/tokens/auth' if require_confirmation else
                    'payments/tokens/charge')
        response = await self._send_request(session, endpoint, params)
        if response['Success']:
            return Transaction.from_dict(response['Model'])
        if 'Model' in response and 'ReasonCode' in response['Model']:
            raise PaymentError(response)
        raise CloudPaymentsError(response)

    async def confirm_payment(self, session: ClientSession, transaction_id, amount, data=None):
        params = {
            'Amount': amount,
            'TransactionId': transaction_id
        }

        if data is not None:
            params['JsonData'] = data

        response = await self._send_request(session, 'payments/confirm', params)

        if not response['Success']:
            raise CloudPaymentsError(response)

    async def void_payment(self, session: ClientSession, transaction_id):
        params = {'TransactionId': transaction_id}
        response = await self._send_request(session, 'payments/void', params)

        if not response['Success']:
            raise CloudPaymentsError(response)

    async def refund(self, session: ClientSession, transaction_id, amount, request_id=None):
        params = {
            'Amount': amount,
            'TransactionId': transaction_id
        }
        response = await self._send_request(session, 'payments/refund', params, request_id)

        if not response['Success']:
            raise CloudPaymentsError(response)

        return response['Model']['TransactionId']

    async def topup(self, session: ClientSession, token, amount, account_id, currency, invoice_id=None):
        params = {
            'Token': token,
            'Amount': amount,
            'AccountId': account_id,
            'Currency': currency
        }
        if invoice_id is not None:
            params['InvoiceId'] = invoice_id
        response = await self._send_request(session, 'payments/cards/topup', params)

        if response['Success']:
            return Transaction.from_dict(response['Model'])

        raise CloudPaymentsError(response)

    async def find_payment(self, session: ClientSession, invoice_id):
        params = {'InvoiceId': invoice_id}
        response = await self._send_request(session, 'payments/find', params)

        if response['Success']:
            return Transaction.from_dict(response['Model'])
        raise CloudPaymentsError(response)

    async def list_payments(self, session: ClientSession, date, timezone=None):
        params = {'Date': format_date(date)}
        if timezone is not None:
            params['Timezone'] = timezone

        response = await self._send_request(session, 'payments/list', params)

        if response['Success']:
            return [Transaction.from_dict(item) for item in response['Model']]
        raise CloudPaymentsError(response)

    async def create_subscription(self, session: ClientSession, token, account_id, amount, currency,
                                  description, email, start_date, interval, period, require_confirmation=False,
                                  max_periods=None, customer_receipt=None):
        params = {
            'Token': token,
            'AccountId': account_id,
            'Description': description,
            'Email': email,
            'Amount': amount,
            'Currency': currency,
            'RequireConfiramtion': require_confirmation,
            'StartDate': format_datetime(start_date),
            'Interval': interval,
            'Period': period,
        }
        if max_periods is not None:
            params['MaxPeriods'] = max_periods
        if customer_receipt is not None:
            params['CustomerReceipt'] = customer_receipt

        response = await self._send_request(session, 'subscriptions/create', params)

        if response['Success']:
            return Subscription.from_dict(response['Model'])
        raise CloudPaymentsError(response)

    async def list_subscriptions(self, session: ClientSession, account_id):
        params = {'accountId': account_id}
        response = await self._send_request(session, 'subscriptions/find', params)

        if response['Success']:
            return [Subscription.from_dict(item) for item in response['Model']]
        raise CloudPaymentsError(response)

    async def get_subscription(self, session: ClientSession, subscription_id):
        params = {'Id': subscription_id}
        response = await self._send_request(session, 'subscriptions/get', params)

        if response['Success']:
            return Subscription.from_dict(response['Model'])
        raise CloudPaymentsError(response)

    async def update_subscription(self, session: ClientSession, subscription_id, amount=None, currency=None,
                                  description=None, start_date=None, interval=None, period=None,
                                  require_confirmation=None, max_periods=None):
        params = {
            'Id': subscription_id
        }
        if description is not None:
            params['Description'] = description
        if amount is not None:
            params['Amount'] = amount
        if currency is not None:
            params['Currency'] = currency
        if require_confirmation is not None:
            params['RequireConfirmation'] = require_confirmation
        if start_date is not None:
            params['StartDate'] = format_datetime(start_date)
        if interval is not None:
            params['Interval'] = interval
        if period is not None:
            params['Period'] = period
        if max_periods is not None:
            params['MaxPeriods'] = max_periods

        response = await self._send_request(session, 'subscriptions/update', params)

        if response['Success']:
            return Subscription.from_dict(response['Model'])
        raise CloudPaymentsError(response)

    async def cancel_subscription(self, session: ClientSession, subscription_id):
        params = {'Id': subscription_id}

        response = await self._send_request(session, 'subscriptions/cancel', params)

        if not response['Success']:
            raise CloudPaymentsError(response)

    async def create_order(self, session: ClientSession, amount, currency, description, email=None,
                           send_email=None, require_confirmation=None, invoice_id=None, account_id=None,
                           phone=None, send_sms=None, send_whatsapp=None, culture_info=None, data=None):
        params = {
            'Amount': amount,
            'Currency': currency,
            'Description': description,
        }
        if email is not None:
            params['Email'] = email
        if require_confirmation is not None:
            params['RequireConfirmation'] = require_confirmation
        if send_email is not None:
            params['SendEmail'] = send_email
        if invoice_id is not None:
            params['InvoiceId'] = invoice_id
        if account_id is not None:
            params['AccountId'] = account_id
        if phone is not None:
            params['Phone'] = phone
        if send_sms is not None:
            params['SendSms'] = send_sms
        if send_whatsapp is not None:
            params['SendWhatsApp'] = send_whatsapp
        if culture_info is not None:
            params['CultureInfo'] = culture_info
        if  data is not None:
            params['JsonData'] = data

        response = await self._send_request(session, 'orders/create', params)

        if response['Success']:
            return Order.from_dict(response['Model'])
        raise CloudPaymentsError(response)

    async def create_receipt(self, session: ClientSession, inn, receipt_type, customer_receipt,
                             invoice_id=None, account_id=None, request_id=None):
        if isinstance(customer_receipt, Receipt):
            customer_receipt = customer_receipt.to_dict()

        params = {
            'Inn': inn,
            'Type': receipt_type,
            'CustomerReceipt': customer_receipt,
        }
        if invoice_id is not None:
            params['InvoiceId'] = invoice_id
        if account_id is not None:
            params['AccountId'] = account_id

        response = await self._send_request(session, 'kkt/receipt', params, request_id)

        if not response['Success']:
            raise CloudPaymentsError(response)
        return response['Model']['Id']

    async def get_receipt(self, session: ClientSession, receipt_id):
        params = {'Id': receipt_id}
        response = await self._send_request(session, 'kkt/receipt/get', params)

        if response['Success']:
            return Receipt.from_dict(response['Model'])
        raise CloudPaymentsError(response)

    async def update_webhook(self, session: ClientSession, webhook_type: WebhookType, address, is_enabled: bool = True,
                             method="GET", encoding="UTF8", format_notifications="CloudPayments"):
        params = {
            'IsEnabled': is_enabled,
            'Address': address,
            'HttpMethod': method,
            'Encoding': encoding,
            'Format': format_notifications
        }
        response = await self._send_request(session, f'site/notifications/{webhook_type}/update', params)
        if response['Success']:
            return response
        raise CloudPaymentsError(response)
