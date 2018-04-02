from django.conf.urls import url
from . import views

app_name = 'pardakht'
urlpatterns = [
    url(r'^p/(?P<slug>\w+)/$', views.start_payment, name='start_payment'),
    url(r'^t/(?P<slug>\w+)/(?P<gateway>\w+)/$', views.select_gateway, name='select_gateway'),
    url(r'^r/(?P<slug>\w+)/(?P<gateway>\w+)', views.called_back, name='callback_url')
]