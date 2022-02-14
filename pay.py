import json
import requests

class NowPayments():
    """pyNowPayments API by https://t.me/i49Y47 """
    def __init__(self, ipn_url='https://api.nowpayments.io/v1', format='json', api_url='https://api.nowpayments.io/v1'):
        self.privateKey = "9CYAYWB-H4PMAST-K4SQY5K-3G1XH1N"
        self.ipn_url = ipn_url
        self.format = format
        self.url = api_url

    def getAPIStatus(self):
        """Method to get information about the current state of the API Server.
        If everything is OK, you will receive an "OK" message.
        Otherwise, you'll see some error"""

        data = {}
        headers = {}

        Res = requests.get(self.url+'/status', headers=headers, data=data)
        return Res.json()

    def getAvailableCurrencies(self):
        """Method for obtaining information about the cryptocurrencies available for payments.
        This depends on the cryptocurrency you choose for your particular store"""

        data = {}
        headers = {'x-api-key': self.privateKey}

        Res = requests.get(self.url+'/currencies', headers=headers, data=data)
        return Res.json()

    def getEstimatePrice(self, amount: int, currency_from: str = 'usd', currency_to: str = 'btc'):
        """Method for calculating the approximate price in cryptocurrency for a given value in Fiat currency.
        You will need to provide the initial cost in the Fiat currency (amount, currency_from) and 
        the necessary cryptocurrency (currency_to) 
        Currently following fiat currencies are available: usd, eur, nzd, brl, gbp."""
        
        data = {}
        params = {'amount': amount, 'currency_from': currency_from, 'currency_to': currency_to}
        headers = {'x-api-key': self.privateKey}
        
        Res = requests.get(self.url+'/estimate', params=params, headers=headers, data=data)
        return Res.json()

    def createPayment(self, price_amount: int, price_currency: str, pay_currency: str, **params):
        """Method to Creates payment
        
        price_amount (required) - The fiat equivalent of the price to be paid in crypto.
        If the pay_amount parameter is left empty, our system will automatically convert this fiat price into its crypto equivalent
        
        price_currency (required) - The fiat currency in which the price_amount is specified (usd, eur, etc).

        pay_currency (required) - the crypto currency in which the pay_amount is specified (btc, eth, etc). 
        NOTE: some of the currencies require a Memo, Destination Tag, etc., to complete a payment (AVA, EOS, BNBMAINNET, XLM, XRP). 
        This is unique for each payment. This ID is received in “payin_extra_id” parameter of the response. 
        Payments made without "payin_extra_id" cannot be detected automatically.

        pay_amount (optional) - the amount that users have to pay for the order stated in crypto. 
        You can either specify it yourself, or we will automatically convert the amount you indicated in price_amount.

        ipn_callback_url (Not Required : Defauld IPN from client config will be used) - url to receive callbacks, 
        should contain "http" or "https", eg. "https://nowpayments.io"
        
        order_id (optional) - inner store order ID, e.g. "RGDBP-21314" [Str]

        order_description (optional) - inner store order description, e.g. "Apple Macbook Pro 2019 x 1"

        purchase_id (optional) - id of purchase for which you want to create aother payment, only used for several payments for one order

        payout_address (optional) - usually the funds will go to the address you specify in your Personal account. 
        In case you want to receive funds on another address, you can specify it in this parameter.
        
        payout_currency (optional) - currency of your external payout_address, required when payout_adress is specified.
        
        payout_extra_id(optional) - extra id or memo or tag for external payout_address.
        
        fixed_rate(optional) - boolean, can be true or false. Required for fixed-rate exchanges.
        
        Here the list of avalable statuses of payment:

        waiting - waiting for the customer to send the payment. The initial status of each payment.
        confirming - the transaction is being processed on the blockchain. Appears when NOWPayments detect the funds from the user on the blockchain.
        confirmed - the process is confirmed by the blockchain. Customer’s funds have accumulated enough confirmations.
        sending - the funds are being sent to your personal wallet. We are in the process of sending the funds to you.
        partially_paid - it shows that the customer sent the less than the actual price. Appears when the funds have arrived in your wallet.
        finished - the funds have reached your personal address and the payment is finished.
        failed - the payment wasn't completed due to the error of some kind.
        refunded - the funds were refunded back to the user.
        expired - the user didn't send the funds to the specified address in the 24 hour time window."""
        
        params.update({
            "price_amount": price_amount,
            "price_currency": price_currency,
            "pay_currency": pay_currency,
            "ipn_callback_url": self.ipn_url,
        })

        headers = {
            'x-api-key': self.privateKey,
            'Content-Type': 'application/json'
        }

        Res = requests.post(self.url+'/payment', headers=headers, data=json.dumps(params))
        return Res.json()

    def getPaymentStatus(self, payment_id):
        """Get the actual information about the payment. 
        You need to provide the ID of the payment in the request.

        NOTE! You should make the get payment status request with the same 
        API key that you used in the create payment request. 
        Here is the list of avalable statuses:

        waiting - waiting for the customer to send the payment. The initial status of each payment.
        confirming - the transaction is being processed on the blockchain. Appears when NOWPayments detect the funds from the user on the blockchain.
        confirmed - the process is confirmed by the blockchain. Customer’s funds have accumulated enough confirmations.
        sending - the funds are being sent to your personal wallet. We are in the process of sending the funds to you.
        partially_paid - it shows that the customer sent the less than the actual price. Appears when the funds have arrived in your wallet.
        finished - the funds have reached your personal address and the payment is finished.
        failed - the payment wasn't completed due to the error of some kind.
        refunded - the funds were refunded back to the user.
        expired - the user didn't send the funds to the specified address in the 24 hour time window.

        Additional info:

        outcome_amount - this parameter shows the amount that will be (or is already) received on your Outcome Wallet once the transaction is settled.
        outcome_currency - this parameter shows the currency in which the transaction will be settled.
        invoice_id - this parameter shows invoice ID from which the payment was created"""

        data = {}
        headers = {'x-api-key': self.privateKey}

        Res = requests.get(self.url+f'/payment/{payment_id}', headers=headers, data=data)
        return Res.json()

    def getMinimumAmount(self, currency_from, **params):
        """Get the minimum payment amount for a specific pair.

        currency_from (required)

        currency_to (optional)

        You can provide both currencies in the pair or just currency_from, 
        and we will calculate the minimum payment amount for currency_from and currency 
        which you have specified as the outcome in the Store Settings.

        In the case of several outcome wallets we will calculate the minimum amount 
        in the same way we route your payment to a specific wallet."""

        url = "https://api.nowpayments.io/v1/min-amount?currency_from=eth&currency_to=trx"

        data = {}
        params.update({'currency_from': currency_from})
        headers = {'x-api-key': self.privateKey}

        Res = requests.get(self.url+'/min-amount', params=params, headers=headers, data=data)
        return Res.json()

    def getPaymentsList(self, **params):
        """Returns the entire list of all transactions, created with certain API key. 
        
        The list of optional parameters:

        limit - number of records in one page. (possible values: from 1 to 500)
        page - the page number you want to get (possible values: from 0 to page count - 1)
        sortBy - sort the received list by a paramenter. Set to created_at by default (possible values: 
            payment_id, 
            payment_status, 
            pay_address, 
            price_amount, 
            price_currency, 
            pay_amount, 
            actually_paid, 
            pay_currency, 
            order_id, 
            order_description, 
            purchase_id, 
            outcome_amount, 
            outcome_currency)
        orderBy - display the list in ascending or descending order. Set to asc by default (possible values: asc, desc)
        dateFrom - select the displayed period start date (date format: YYYY-MM-DD or yy-MM-ddTHH:mm:ss.SSSZ).
        dateTo - select the displayed period end date (date format: YYYY-MM-DD or yy-MM-ddTHH:mm:ss.SSSZ)."""
        
        data = {}
        headers = {'x-api-key': self.privateKey}

        Res = requests.get(self.url+'/payment', params=params, headers=headers, data=data)
        return Res.json()
    
    def createInvoice(self, price_amount: int, price_currency: str, **params):
        """Method to Creates an invoice. the customer is required to follow the generated url to complete the payment. Request fields:

        price_amount (required) 
            - the amount that users have to pay for the order stated in fiat currency. 
            In case you do not indicate the price in crypto, our system will automatically convert this fiat amount into its crypto equivalent. 
        
        price_currency (required) 
            - the fiat currency in which the price_amount is specified (usd, eur, etc).

        pay_currency (optional) 
            - the crypto currency in which the pay_amount is specified (btc, eth, etc).
            If not specified, can be chosen on the invoice_url
        
        ipn_callback_url (optional) 
            - url to receive callbacks, should contain "http" or "https", eg. "https://nowpayments.io"

        order_id (optional)     
            - internal store order ID, e.g. "RGDBP-21314"
        
        order_description (optional) 
            - internal store order description, e.g. "Apple Macbook Pro 2019 x 1"
        
        success_url(optional) 
            - url where the customer will be redirected after successful payment.
        
        cancel_url(optional) 
            - url where the customer will be redirected after failed payment."""

        params.update({
            "price_amount": price_amount, 
            "price_currency": price_currency
        })

        headers = {
            'x-api-key': self.privateKey,
            'Content-Type': 'application/json',
            'charset' : 'utf-8'
        }

        Res = requests.post(self.url+'/invoice', headers=headers, data=json.dumps(params))
        return Res.json()
    
    
