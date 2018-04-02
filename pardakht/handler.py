from django.urls import reverse
from pardakht.models import Payment


def create_payment(price, description=None, return_function=None, return_url=None, login_required=False):
    if return_function is not None and not callable(return_function):
        raise Exception('Non callable passed as return function')
    payment = Payment.objects.create(
        price=price,
        description=description,
        login_required=login_required,
        callable_module=return_function.__module__ if return_function is not None else None,
        callable_name=return_function.__name__ if return_function is not None else None,
        return_url=return_url
    )
    return {'payment': payment, 'link': reverse('pardakht:start_payment', args=[payment.slug])}
