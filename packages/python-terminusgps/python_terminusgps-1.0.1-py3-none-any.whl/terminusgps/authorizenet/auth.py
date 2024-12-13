from os import getenv

from authorizenet.apicontractsv1 import merchantAuthenticationType
from authorizenet.constants import constants


def get_merchant_auth() -> merchantAuthenticationType:
    name: str = getenv("MERCHANT_AUTH_LOGIN_ID", "")
    transactionKey: str = getenv("MERCHANT_AUTH_TRANSACTION_KEY", "")
    return merchantAuthenticationType(name=name, transactionKey=transactionKey)


def get_environment(debug: bool = False) -> str:
    return constants.SANDBOX if debug else constants.PRODUCTION
