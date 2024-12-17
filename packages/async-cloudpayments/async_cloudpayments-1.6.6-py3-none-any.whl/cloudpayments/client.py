import aiohttp
from aiohttp import ClientSession
from .errors import CloudPaymentsError, PaymentError
from .models import Order, Receipt, Secure3d, Subscription, Transaction
from .utils import format_date, format_datetime
from .enums import WebhookType  # Исправленный импорт для WebhookType

class CloudPayments(object):
    URL = 'https://api.cloudpayments.ru/'

    def __init__(self, public_id, api_secret):
        self.public_id = public_id
        self.api_secret = api_secret
        self._session = None  # Атрибут для хранения сессии

    @property
    def session(self):
        # Если сессия ещё не инициализирована, создаём её
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session

    async def _send_request(self, endpoint: str, params=None, request_id=None):
        """Метод отправки запроса с использованием сессии."""
        auth = aiohttp.BasicAuth(self.public_id, self.api_secret)

        headers = None
        if request_id is not None:
            headers = {'X-Request-ID': request_id}

        async with self.session.post(self.URL + endpoint, json=params, auth=auth, headers=headers) as response:
            response_json = await response.json()
            return response_json

    async def test(self, request_id=None):
        """Метод для тестирования подключения."""
        response = await self._send_request('test', request_id=request_id)

        if not response['Success']:
            raise CloudPaymentsError(response)
        return response['Message']

    async def get_transaction(self, transaction_id):
        """Получить информацию о транзакции по её id."""
        params = {'TransactionId': transaction_id}
        response = await self._send_request('payments/get', params)
        if 'Model' in response.keys():
            return Transaction.from_dict(response['Model'])
        else:
            raise CloudPaymentsError(response)

    async def charge_card(self, cryptogram, amount, currency, name, ip_address,
                          invoice_id=None, description=None, account_id=None, email=None, data=None,
                          require_confirmation=False, service_fee=None):
        """Метод для charge card"""
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

        endpoint = ('payments/cards/auth' if require_confirmation else 'payments/cards/charge')
        response = await self._send_request(endpoint, params)

        if response['Success']:
            return Transaction.from_dict(response['Model'])
        if response['Message']:
            raise CloudPaymentsError(response)
        if 'ReasonCode' in response['Model']:
            raise PaymentError(response)
        return Secure3d.from_dict(response['Model'])

    async def finish_3d_secure_authentication(self, transaction_id, pa_res):
        """Завершение аутентификации 3D Secure"""
        params = {
            'TransactionId': transaction_id,
            'PaRes': pa_res
        }
        response = await self._send_request('payments/cards/post3ds', params)

        if response['Success']:
            return Transaction.from_dict(response['Model'])
        raise PaymentError(response)

    async def charge_token(self, token, account_id, amount, currency, ip_address=None,
                           invoice_id=None, description=None, email=None, data=None, tr_initiator_code: int = 1,
                           require_confirmation=False):
        """Метод для charge token"""
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

        endpoint = ('payments/tokens/auth' if require_confirmation else 'payments/tokens/charge')
        response = await self._send_request(endpoint, params)

        if response['Success']:
            return Transaction.from_dict(response['Model'])
        if 'Model' in response and 'ReasonCode' in response['Model']:
            raise PaymentError(response)
        raise CloudPaymentsError(response)

    async def confirm_payment(self, transaction_id, amount, data=None):
        """Метод для подтверждения оплаты"""
        params = {
            'Amount': amount,
            'TransactionId': transaction_id
        }

        if data is not None:
            params['JsonData'] = data

        response = await self._send_request('payments/confirm', params)

        if not response['Success']:
            raise CloudPaymentsError(response)

    async def void_payment(self, transaction_id):
        """Метод для отмены транзакции"""
        params = {'TransactionId': transaction_id}
        response = await self._send_request('payments/void', params)

        if not response['Success']:
            raise CloudPaymentsError(response)

    async def refund(self, transaction_id, amount, request_id=None):
        """Метод для возврата средств"""
        params = {
            'Amount': amount,
            'TransactionId': transaction_id
        }
        response = await self._send_request('payments/refund', params, request_id)

        if not response['Success']:
            raise CloudPaymentsError(response)

        return response['Model']['TransactionId']

    async def topup(self, token, amount, account_id, currency, invoice_id=None):
        """Метод для пополнения счета"""
        params = {
            'Token': token,
            'Amount': amount,
            'AccountId': account_id,
            'Currency': currency
        }
        if invoice_id is not None:
            params['InvoiceId'] = invoice_id
        response = await self._send_request('payments/cards/topup', params)

        if response['Success']:
            return Transaction.from_dict(response['Model'])

        raise CloudPaymentsError(response)

    async def find_payment(self, invoice_id):
        """Поиск платежа по InvoiceId"""
        params = {'InvoiceId': invoice_id}
        response = await self._send_request('payments/find', params)

        if response['Success']:
            return Transaction.from_dict(response['Model'])
        raise CloudPaymentsError(response)

    async def list_payments(self, date, timezone=None):
        """Получить список платежей"""
        params = {'Date': format_date(date)}
        if timezone is not None:
            params['Timezone'] = timezone

        response = await self._send_request('payments/list', params)

        if response['Success']:
            return [Transaction.from_dict(item) for item in response['Model']]
        raise CloudPaymentsError(response)

    async def create_subscription(self, token, account_id, amount, currency,
                                  description, email, start_date, interval, period, require_confirmation=False,
                                  max_periods=None, customer_receipt=None):
        """Создание подписки"""
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

        response = await self._send_request('subscriptions/create', params)

        if response['Success']:
            return Subscription.from_dict(response['Model'])
        raise CloudPaymentsError(response)

    async def list_subscriptions(self, account_id):
        """Список подписок"""
        params = {'accountId': account_id}
        response = await self._send_request('subscriptions/find', params)

        if response['Success']:
            return [Subscription.from_dict(item) for item in response['Model']]
        raise CloudPaymentsError(response)

    async def get_subscription(self, subscription_id):
        """Получить подписку по id"""
        params = {'Id': subscription_id}
        response = await self._send_request('subscriptions/get', params)

        if response['Success']:
            return Subscription.from_dict(response['Model'])
        raise CloudPaymentsError(response)

    async def update_subscription(self, subscription_id, amount=None, currency=None,
                                  description=None, start_date=None, interval=None, period=None,
                                  require_confirmation=None, max_periods=None):
        """Обновление подписки"""
        params = {
            'Id': subscription_id
        }
        if description is not None:
            params['Description'] = description
        if amount is not None:
            params['Amount'] = amount
        if currency is not None:
            params['Currency'] = currency
        if start_date is not None:
            params['StartDate'] = format_datetime(start_date)
        if interval is not None:
            params['Interval'] = interval
        if period is not None:
            params['Period'] = period
        if require_confirmation is not None:
            params['RequireConfiramtion'] = require_confirmation
        if max_periods is not None:
            params['MaxPeriods'] = max_periods

        response = await self._send_request('subscriptions/update', params)

        if response['Success']:
            return Subscription.from_dict(response['Model'])
        raise CloudPaymentsError(response)

    async def cancel_subscription(self, subscription_id):
        """Отмена подписки"""
        params = {'Id': subscription_id}
        response = await self._send_request('subscriptions/cancel', params)

        if response['Success']:
            return response['Model']
        raise CloudPaymentsError(response)

    async def create_receipt(self, transaction_id, amount, items, email=None, phone=None, tax_system=None):
        """Создание чека"""
        receipt = Receipt(transaction_id, amount, items, email=email, phone=phone, tax_system=tax_system)
        params = receipt.to_dict()

        response = await self._send_request('receipts/issue', params)
        if response['Success']:
            return receipt
        raise CloudPaymentsError(response)

    async def list_receipts(self, start_date, end_date):
        """Получение списка чеков"""
        params = {'StartDate': format_datetime(start_date), 'EndDate': format_datetime(end_date)}
        response = await self._send_request('receipts/list', params)

        if response['Success']:
            return [Receipt.from_dict(item) for item in response['Model']]
        raise CloudPaymentsError(response)
