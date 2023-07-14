
from django.urls import path,include
from apps import views

urlpatterns = [
    path('login', views.Login.as_view()), #login for admin and user
    path('event', views.EventManagementAPI.as_view()), #event create and update
    path('event_get', views.EventFetch.as_view()), #get event list and particular event for admin and user
    path('ticket', views.BookingAPI.as_view()), # book a ticket for user and view ticket
    path('booking',views.ticket_booking),
    path('success',views.success),
    path('register',views.Register.as_view())
]