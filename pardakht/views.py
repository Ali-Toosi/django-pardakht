import importlib
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from pardakht import gateways
from pardakht.decorators import payment_exists, payment_not_started
from pardakht.models import Payment
import logging


@login_required
def go_login(request):
    return redirect(request.build_absolute_uri())


@payment_exists
@payment_not_started
def start_payment(request, slug):
    payment = Payment.objects.get(slug=slug)
    payment.state = Payment.STATE_OPENED
    payment.save()

    gways = list()
    for gway in gateways.actives:
        if getattr(settings, str(gway+'_merchant_id').upper(), None) not in [None, '']:
            gway_module = importlib.import_module('pardakht.gateways.'+gway)
            gways.append({'name': gway_module.name, 'display_name': gway_module.display_name})

    return render(request, 'pardakht/start_payment.html', {'payment': payment, 'gateways': gways})


@payment_exists
@payment_not_started
def select_gateway(request, slug, gateway):
    if gateway not in gateways.actives:
        raise Http404

    payment = Payment.objects.get(slug=slug)

    if request.user.is_authenticated:
        payment.user = request.user
    elif payment.login_required:
        return go_login(request)

    gateway_module = importlib.import_module('.'.join([gateways.__name__, gateway]))
    token = gateway_module.get_token(request, payment)
    if token is None:
        return render(request, 'pardakht/errors/none_token.html')
    payment.state = Payment.STATE_BANK
    payment.token = token
    payment.save()
    return render(request, 'pardakht/redirect_form.html', {
        'url': gateway_module.redirect_url(payment),
        'data': gateway_module.redirect_data(request, payment)
    })


@csrf_exempt
@payment_exists
def called_back(request, slug, gateway):
    payment = Payment.objects.get(slug=slug)
    if payment.verification_done():
        return render(request, 'pardakht/errors/verified_before.html')
    if payment.user is None and request.user.is_authenticated:
        payment.user = request.user
        payment.save()
    gateway_module = importlib.import_module('.'.join([gateways.__name__, gateway]))
    gateway_module.verify(request, payment)
    if payment.callable_module is not None and payment.callable_name is not None:
        user_module = importlib.import_module(payment.callable_module)
        return_function = getattr(user_module, payment.callable_name)
        try:
            return_function(payment)
        except Exception as e:
            lg = logging.getLogger(__name__)
            lg.warning("Something went wrong with given callback function")
            lg.warning(str(e))

    return render(request, 'pardakht/payment_result.html', {'payment': payment})
