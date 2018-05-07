from .views import TicketOnSaleViewSet
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

urlpatterns = format_suffix_patterns([
  path('<int:pk>/', ticket_detail, name='ticket-detail'),
  path('', ticket_list, name='ticket-list')
])