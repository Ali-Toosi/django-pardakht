# set SAMAN_MERCHANT_ID in your project settings

from django.http import HttpRequest
from zeep import Client
from django.conf import settings
from django.urls import reverse
import logging
from ..models import Payment

name = 'saman'
display_name = 'سامان'
webservice_url = "https://verify.sep.ir/payments/initpayment.asmx?WSDL"

client = Client(webservice_url)

logger = logging.getLogger(__name__)


def redirect_url(payment):
    return "https://sep.shaparak.ir/payment.aspx"


def redirect_data(request: HttpRequest, payment):
    s = str(request.build_absolute_uri(reverse('pardakht:callback_url', args=[payment.slug, name])))
    return {
        'Token': payment.token,
        'RedirectURL': s
    }


def send_request(method, *params):
    ws_method = getattr(client.service, method)
    result = ws_method(*params)
    return result


def get_token(request: HttpRequest, payment):
    merchant_id = getattr(settings, str(name+'_merchant_id').upper(), 'none')
    if merchant_id == 'none':
        logger.error('Merchant ID not in settings.\nDefine your merchant id in settings.py as '+str(name+'_merchant_id').upper())
        return None
    result = send_request(
        'RequestToken',
        merchant_id,
        payment.trace_number,
        payment.price*10,
        0, 0, 0, 0, 0, 0, "", "", 0
    )
    if result not in [None, '']:
        try:
            int_token = int(result)
            if int_token < 0:
                logger.error("Gateway returned error code {} while requesting for token".format(result))
                return None
        except ValueError:
            pass
        payment.gateway = name
        payment.save()
        return result
    else:
        logger.error("Couldn't get payment token from saman")
        return None


def verify(request, payment):
    if request.POST.get('State') not in ['OK', 'ok']:
        payment.state = payment.STATE_FAILURE
        payment.payment_result = str(request.POST.get('State'))
        payment.save()
        return

    merchant_id = getattr(settings, str(name + '_merchant_id').upper(), 'none')
    if merchant_id == 'none':
        logger.error('Merchant ID not in settings.\nDefine your merchant id in settings.py as ' + str(
            name + '_merchant_id').upper())
        return None

    if payment.trace_number != request.POST.get('ResNum'):
        logger.warning('Manipulation')
        return

    ref_number = request.POST.get('RefNum')
    if Payment.objects.filter(ref_number=ref_number).exists():
        payment.state = payment.STATE_FAILURE
        payment.payment_result = 'MANIPULATION'
        payment.save()
        return
    else:
        payment.ref_number = ref_number
        payment.save()

    verify_url = "https://verify.sep.ir/payments/referencepayment.asmx?WSDL"
    verify_client = Client(verify_url)
    verify_method = getattr(verify_client.service, 'verifyTransaction')
    verify_result = verify_method(payment.ref_number, merchant_id)

    if verify_result == 10*payment.price:
        payment.state = payment.STATE_SUCCESS
    else:
        payment.state = payment.STATE_FAILURE
    payment.verification_result = str(verify_result)
    payment.save()




