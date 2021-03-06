from .views import TicketOnSaleViewSet
from .views import InviteViewSet
from .views import BookingViewSet
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


ticket_detail = TicketOnSaleViewSet.as_view({
  'get': 'retrieve',
  'put': 'update',
  'delete': 'destroy'
})

ticket_list = TicketOnSaleViewSet.as_view({
  # 'get': 'list',
  'post': 'create'
})

booking = BookingViewSet.as_view({
  'get': 'list',
  'post': 'create',
})

booking_detail = BookingViewSet.as_view({
  'delete': 'destroy'
})

invite_friends = InviteViewSet.as_view({
  'post': 'invite'
})

urlpatterns = format_suffix_patterns([
  path('<int:pk>/', ticket_detail, name='ticket-detail'),
  path('', ticket_list, name='ticket-list'),
  path('booking/', booking, name='booking-list'),
  path('booking/<int:pk>/', booking_detail, name='booking-detail'),
  path('invite/<int:pk>/', invite_friends, name='invite-friends')
])
