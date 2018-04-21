from authentication.models import User
from authentication.serializers import UserSerializer
from rest_framework.response import Response
from.permissions import IsSelfOrReadOnly
from rest_framework import viewsets
from rest_framework.decorators import action
from django.utils.decorators import decorator_from_middleware
from rest_framework_jwt.settings import api_settings
from.utils import auth
from rest_framework.permissions import AllowAny, DjangoModelPermissionsOrAnonReadOnly, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes

class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [IsSelfOrReadOnly]

  @action(detail=False)
  def current_user(self, request, *args, **kwargs):
    user = request.user
    user = User.objects.get(id=user.id)
    return Response(UserSerializer(user).data)

  @action(detail=False, permission_classes=[AllowAny])
  def register(self, request, * args, ** kwargs):
    user = User.create_user(request.data)
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return Response(auth.jwt_response_payload_handler(token, user))

  def update(self, request, pk=None):
    user = User.objects.get(id=pk)
    self.check_object_permissions(request, user)
    user.__dict__.update( ** request.data)
    user.save()
    return Response(UserSerializer(user).data)

  def partial_update(self, request, pk=None):
    user = User.objects.get(id=pk)
    self.check_object_permissions(request, user)
    user.__dict__.update( ** request.data)
    user.save()
    return Response(UserSerializer(user).data)

  def destroy(self, request, pk=None):
    user = User.objects.get(id=pk)
    self.check_object_permissions(request, user)
    user.delete()
    return Response({'message': 'User successfully deleted'})
