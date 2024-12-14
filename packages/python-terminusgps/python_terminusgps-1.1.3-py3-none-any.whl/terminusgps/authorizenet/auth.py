from authorizenet.apicontractsv1 import merchantAuthenticationType
from authorizenet.constants import constants

from django.conf import settings


def get_merchant_auth() -> merchantAuthenticationType:
    return merchantAuthenticationType(
        name=settings.MERCHANT_AUTH_LOGIN_ID,
        transactionKey=settings.MERCHANT_AUTH_TRANSACTION_KEY,
    )


def get_environment() -> str:
    return constants.SANDBOX if settings.DEBUG else constants.PRODUCTION
