from django.urls import path
from myapp.views import process_pdf, form_view
from . import views

urlpatterns = [
    path('', form_view, name='form_view'),
    path('process_pdf/', process_pdf, name='process_pdf'),
    path('get_templates_list/', views.get_templates_list, name='get_templates_list'),
]
