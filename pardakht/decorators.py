from django.http import Http404
from django.shortcuts import render
from pardakht.models import Payment


def payment_not_started(old_function):
    def new_function(request, slug, *args, **kwargs):
        try:
            payment = Payment.objects.get(slug=slug)
            if payment.state not in [Payment.STATE_OPENED, Payment.STATE_CREATED]:
                return render(request, 'pardakht/errors/started_before.html')
            else:
                return old_function(request, slug, *args, **kwargs)
        except Payment.DoesNotExist:
            raise Http404
    return new_function


def payment_exists(old_function):
    def new_function(request, slug, *args, **kwargs):
        try:
            payment = Payment.objects.get(slug=slug)
            return old_function(request, slug, *args, **kwargs)
        except Payment.DoesNotExist:
            raise Http404
    return new_function
