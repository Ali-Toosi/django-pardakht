from django.urls import path
from . import views

app_name = 'pardakht'
urlpatterns = [
    path('p/<slug>/', views.start_payment, name='start_payment'),
    path('t/<slug>/<gateway>/', views.select_gateway, name='select_gateway'),
    path('r/<slug>/<gateway>', views.called_back, name='callback_url')
]
