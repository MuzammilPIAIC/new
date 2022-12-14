
from django.urls import path
from .views import *
urlpatterns = [
#     path('',        home,   name = 'home'),
    path('',  record, name = 'record'),
    path('new_record_/',  new_record_, name = 'new_record_'),
    path('record/details/<int:id>',  record_detail, name = 'details'),
    path("record/text/<str:id>/", text, name="text"),
]
