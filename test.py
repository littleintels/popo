import requests,json

"""
url = 'https://api.nowpayments.io/v1/status'
urr = 'https://api.nowpayments.io/v1/currencies' 
headers = {
            'x-api-key': "5W96A4J-WC74CGY-NV703FQ-DY03MS0"
}
uii = 'https://api.nowpayments.io/v1/min-amount?currency_from=btc&currency_to=trx&fiat_equivalent=usd' 

hh = 'https://api.nowpayments.io/v1/estimate?amount=3999.5000&currency_from=usd&currency_to=btc' 

pay =  'https://api.nowpayments.io/v1/payment' 

head ={
        'x-api-key': "5W96A4J-WC74CGY-NV703FQ-DY03MS0",
        'Content-Type': 'application/json' 
}
data = {
         "price_amount": 3999.5,
         "price_currency": "usd",
         "pay_currency": "btc",
         "ipn_callback_url": "https://nowpayments.io",
}

print(requests.get(hh,headers=headers).json())

"""



import hmac
import hashlib
from requests import Session, Request
from urllib import parse


class CoinPayment:
    """
     Api helper for coinpayments.net API
    """

    def __init__(self, publicKey=None, privateKey=None, ipn=None):
        self.privateKey = "9A56491E0cF12B75efe79915b395901Ddc3d9d4290c01a944Cb42f29D90b56c7"
        self.data = {
            "version": "1",
            "cmd": "",
            "key": "9b2464f227905618c08a089b9e6505d716565439f59d19ecf4a3a610174a4064",
            "format": "json",
            "ipn_url": ipn
        }
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

    def createHmac(self, data):
        result = hmac.new(bytearray(self.privateKey, 'utf-8'),
                          data.encode("utf-8"), hashlib.sha512).hexdigest()
        return result

    def sendData(self, **kwargs):
        """
        send data to coinpayments API
        """
        URL = "https://www.coinpayments.net/api.php"
        rs = Session()
        req = Request("POST", URL, data=kwargs, headers=self.headers)
        preppend = req.prepare()
        preppend.headers["hmac"] = self.createHmac(preppend.body)
        result = rs.send(preppend)
        if result.status_code == 200 and result.headers["Content-type"] == "application/json":
            return result.json()

    # Informational Commands
    def getBasicAccount(self):
        """
        https://www.coinpayments.net/apidoc-get-basic-info
        """
        self.data["cmd"] = "get_basic_info"
        return self.sendData(**self.data)

    def getExchangeRates(self):
        """
        https://www.coinpayments.net/apidoc-rates
        """
        self.data["cmd"] = "rates"
        self.data["short"] = "1"
        return self.sendData(**self.data)

    def getCoinBallance(self):
        """
        https://www.coinpayments.net/apidoc-balances
        """
        self.data["cmd"] = "balances"
        return self.sendData(**self.data)

    def getDepositAddress(self, currency):
        """
        https://www.coinpayments.net/apidoc-get-deposit-address
        """
        self.data["cmd"] = "get_deposit_address"
        self.data["currency"] = currency
        return self.sendData(**self.data)

    #
    # Receiving Payments
    def createTransaction(self, **kwargs):
        """
        https://www.coinpayments.net/apidoc-create-transaction
        """
        self.data["cmd"] = "create_transaction"
        self.data.update(kwargs)
        return self.sendData(**self.data)

    def getCallbackAddress(self, currency):
        """
        untuk transaksi komersil
        jadi setiap user mendapatakn alamat cripto
        yang berbeda-beda
        https://www.coinpayments.net/apidoc-get-callback-address
        """
        self.data["cmd"] = "get_callback_address"
        self.data["currency"] = currency
        return self.sendData(**self.data)

    def getTxInfo(self, full=0, txid=[]):
        """
        https://www.coinpayments.net/apidoc-get-tx-info
        """
        if len(txid) > 1:
            self.data["cmd"] = "get_tx_info_multi"
            self.data["txid"] = "|".join(x for x in txid)
        else:
            self.data["cmd"] = "get_tx_info"
            self.data["txid"] = txid[0]
        self.data["full"] = full
        return self.sendData(**self.data)

    def getTxList(self, **kwargs):
        """
        https://www.coinpayments.net/apidoc-get-tx-ids
        """
        self.data["cmd"] = "get_tx_ids"
        self.data.update(kwargs)
        return self.sendData(**self.data)

    # Withdrawals/Transfers
    def createTransfer(self, **kwargs):
        """
        https://www.coinpayments.net/apidoc-create-transfer
        """
        self.data["cmd"] = "create_transfer"
        self.data.update(kwargs)
        return self.sendData(**self.data)

    def createWithdrawal(self, **kwargs):
        """
        https://www.coinpayments.net/apidoc-create-withdrawal
        """
        self.data["cmd"] = "create_withdrawal"
        self.data.update(kwargs)
        return self.sendData(**self.data)

    def ConversionCoins(self):
        """
        https://www.coinpayments.net/apidoc-convert
        """
        self.data["cmd"] = "convert"
        self.data.update(kwargs)
        return self.sendData(**self.data)

    def ConversionLimits(self, **kwargs):
        """
        from	The cryptocurrency to convert from. (BTC, LTC, etc.)
        to	The cryptocurrency to convert to. (BTC, LTC, etc.)
        https://www.coinpayments.net/apidoc-convert-limits
        """
        self.data["cmd"] = "convert_limits"
        self.data.update(kwargs)
        return self.sendData(**self.data)

    def getWithdrawalHistory(self, **kwargs):
        """
        limit	The maximum number of withdrawals to return from 1-100. (default: 25)
        start	What withdrawals # to start from (for iteration/pagination.) (default: 0, starts with your newest withdrawals.)
        newer	Return withdrawals submitted at the given Unix timestamp or later. (default: 0)
        https://www.coinpayments.net/apidoc-get-withdrawal-history
        """
        self.data["cmd"] = "get_withdrawal_history"
        self.data.update(kwargs)
        return self.sendData(**self.data)

    def getWithdrawalInfo(self, wid):
        """
        https://www.coinpayments.net/apidoc-get-withdrawal-info
        """
        self.data["cmd"] = "get_withdrawal_info"
        self.data["id"] = wid
        return self.sendData(**self.data)

    def getConversionInfo(self, cid):
        """
        https://www.coinpayments.net/apidoc-get-conversion-info
        """
        self.data["cmd"] = "get_conversion_info"
        self.data["id"] = cid
        return self.sendData(**self.data)

telo = CoinPayment()
#best = telo.getCallbackAddress(currency="btc")
b = telo.getBasicAccount()
print(b)