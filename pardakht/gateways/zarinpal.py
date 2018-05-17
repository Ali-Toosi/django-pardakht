# set ZARINPAL_MERCHANT_ID and ZARIPAL_USE_ZARINGATE (optional) in your project settings

from django.http import HttpRequest
from zeep import Client
from django.conf import settings
from django.urls import reverse
import logging

name = 'zarinpal'
display_name = 'زرین‌پال'
webservice_url = 'https://www.zarinpal.com/pg/services/WebGate/wsdl'

client = Client(webservice_url)

logger = logging.getLogger(__name__)


def redirect_url(payment):
    try:
        zarin_gate = "ZarinGate" if settings.ZARINPAL_USE_ZARINGATE else ""
    except AttributeError:
        zarin_gate = ""

    return "https://www.zarinpal.com/pg/StartPay/{}/{}".format(payment.token, zarin_gate)


def redirect_data(request:HttpRequest, payment):
    return {}


def send_request(method, *params):
    ws_method = getattr(client.service, method)
    result = ws_method(*params)
    return result


def get_token(request: HttpRequest, payment):
    merchant_id = getattr(settings, str(name+'_merchant_id').upper(), 'none')
    if merchant_id == 'none':
        logger.error('Merchant ID not in settings.\nDefine your merchant id in settings.py as '+str(name+'_merchant_id').upper())
        return None
    if payment.description in [None, '']:
        logger.error("Zarinpal doesn't allow empty description for payments.")
        return None
    result = send_request(
        'PaymentRequest',
        merchant_id,
        payment.price,
        payment.description,
        '',
        '',
        request.build_absolute_uri(reverse('pardakht:callback_url', args=[payment.slug, name]))
    )
    if result.Status == 100:
        payment.gateway = name
        payment.save()
        return result.Authority
    else:
        logger.error("Couldn't get payment token from zarinpal")
        return None


def verify(request, payment):
    if request.GET.get('Status') != 'OK':
        payment.state = payment.STATE_FAILURE
        payment.payment_result = str(request.GET.get('Status'))
        payment.save()
        return

    merchant_id = getattr(settings, str(name + '_merchant_id').upper(), 'none')
    if merchant_id == 'none':
        logger.error('Merchant ID not in settings.\nDefine your merchant id in settings.py as ' + str(
            name + '_merchant_id').upper())
        return None
    result = send_request('PaymentVerification', merchant_id, payment.token, payment.price)
    if str(result.Status) in ['100', '101']:
        payment.state = payment.STATE_SUCCESS
        payment.ref_number = result.RefID
    else:
        payment.state = payment.STATE_FAILURE
    payment.verification_result = str(result.Status)
    payment.save()




