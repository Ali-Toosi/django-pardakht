django-pardakht
===============

**What's this?**

You can use this app to create payments in your django project via Iranian gateways. (Right now only Zarinpal and Saman are available but the rest are coming soon)

**How does it work?**

You ask the app for a new payment and it will give you a link on your own site that you can redirect users to it in order to have a payment.

.. image:: http://img.majidonline.com/pic/321293/1.png

.. image:: http://img.majidonline.com/pic/321294/2.png

.. image:: http://img.majidonline.com/pic/321295/3.png


**Installation**

1. ``pip install django-pardakht``

2. Add ``pardakht`` to your ``INSTALLED_APPS``

3. ``python manage.py migrate``

4. Add ``pardakht`` urls to your project's urls.

::

    from pardakht import urls as pardakht_urls
    urlpatterns = [
        ...
    
        url(r'^<SOME_URL>/', include(pardakht_urls)),
    
        ...
    ]

5. For any gateway you use, add GATEWAY_MERCHANT_ID in your project settings. For example if you are going to use zarinpal, You need to add ``ZARINPAL_MERCHANT_ID`` in your settings with value set to your zarinpal merchant ID or if you are using saman gateway, You need to add ``SAMAN_MERCHANT_ID`` in your settings.


**Usage**

There is a payment model that app uses to handle payments. Every payment you create needs 5 initial parameters.

1. ``price``:  Price of the payment.

2. ``description``:  Short description about this payment. Necessary for some gateways such as Zarinpal.

3. ``return_function``:  A callable object (function) that will get called after payment is done with the payment object as it's input. It's optional and can be None.

4. ``return_url``:  A url for user to come back where he left off on your site. It's optional and can be None.

5. ``login_required``:  Must be True if user who is paying should be authenticated. If you're going to use this you have to set LOGIN_URL in project settings.

To create a payment:

::

    from pardakht import handler
    result = handler.create_payment(
        price,
        description,
        return_function,
        return_url,
        login_required
    )

This will create a payment and returns a dict containing payment object and a link to pay it:

::

    result['payment']   #  Created payment object
    result['link']      #  Link for paying this payment that you should redirect your user to

**Extra notes**

This app handles all steps of payment including UI parts.

It uses semantic-ui so if you want to use it you need to serve app's static files.

But of course you can override templates to use your own templates with your own UI design.


**Configurations**

If you are using ZarinGate to send users directly to the bank payment page, set `ZARINPAL_USE_ZARINGATE` to `True` in your project settings.


