from .views import Register, CreateEvents, Login, UserHolidays, UserEvent
from django.urls import path


urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path("createevent/", CreateEvents.as_view(), name='create-event'),
    path('listholidays/', UserHolidays.as_view(), name='list-holidays'),
    path('listevent/<str:data>/', UserEvent.as_view(), name='list-event'),
]