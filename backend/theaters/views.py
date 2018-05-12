from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from authentication.models import TheaterAdmin
from authentication.permissions import IsSystemAdmin
from authentication.permissions import IsTheaterOrSystemAdmin

from media_upload.defaults import DEFAULT_THEATER_IMAGE
from media_upload.models import Image
from media_upload.models import THEATER_IMAGE

from .models import Theater
from .models import Auditorium
from .models import THEATER_KIND
from .models import Voting
from .serializers import PublicSerializer
from .serializers import RestrictedSerializer
from .serializers import AdministrationSerializer
from .serializers import AuditoriumSerializer
from .permissions import IsResponsibleForTheater
from movies.serializers import MovieSerializer
from showtimes.serializers import ShowtimeSerializer
from sale_tickets.serializers import TicketOnSaleSerializer


class PublicAPI(ViewSet):
  queryset = Theater.objects.all()
  permission_classes = [AllowAny]

  def list(self, request):
    all = request.GET.get('all')
    if all:
      return Response(data=PublicSerializer(self.queryset, many=True).data)

    num = request.GET.get('num')
    paginator = Paginator(self.queryset.order_by('name'), num if num else 10)
    page = request.GET.get('page')
    theaters = paginator.get_page(page if page else 1)
    return Response(data=PublicSerializer(theaters, many=True).data)

  def retrieve(self, request, pk=None):
    theater = get_object_or_404(Theater, pk=pk)
    return Response(data=PublicSerializer(theater).data)

  @action(detail=False)
  def count(self, request):
    return Response(data=Theater.objects.count())

  @action(detail=False)
  def get_theaters(self, request):
    return Response(data=PublicSerializer(self.queryset, many=True).data)

  @action(detail=False)
  def get_theater(self, request, pk=None):
    theater_admin = TheaterAdmin.objects.get(user_ptr_id=pk)
    theater = Theater.objects.get(id=theater_admin.theater_id)
    return Response(data=PublicSerializer(theater).data)

  @action(detail=True)
  def update_rating(self, request, pk=None):
    vote, _ = Voting.objects.get_or_create(
      user_id=request.user.id,
      theater_id=pk
    )
    vote.rating = request.data['rating']
    vote.save()
    rating = Voting.objects.filter(
      theater_id=pk).aggregate(rating=Avg('rating')
    )
    voters = len(Voting.objects.filter(theater_id=pk).all())
    data = {'rating':rating,'voters':voters}
    return Response(data)

  @action(detail=True)
  def get_movies(self, request, pk=None):
    theater = Theater.objects.get(id=pk)
    movies = theater.movies.all()
    return Response(MovieSerializer(movies, many=True).data)

  @action(detail=True)
  def get_repertoire(self, request, pk=None):
    theater = Theater.objects.get(id=pk)
    movies = theater.movies.all()
    showtimes = []
    for movie in movies:
      showtime_list = list(movie.showtimes.all())
      for s in showtime_list:
        showtimes.append(s)
    return Response(ShowtimeSerializer(showtimes, many=True).data)

  @action(detail=True)
  def get_tickets_on_sale(self, request, pk=None):
    theater = get_object_or_404(Theater, id=pk)
    tickets = theater.tickets_on_sale.all()
    return Response(TicketOnSaleSerializer(tickets, many=True).data)

class RestrictedAPI(ViewSet):
  permission_classes = [
    IsAuthenticated,
    IsTheaterOrSystemAdmin,
    IsResponsibleForTheater
  ]

  def update(self, request, pk=None):
    theater = get_object_or_404(Theater, pk=pk)
    self.check_object_permissions(request, theater)
    serializer = RestrictedSerializer(
      theater, data=request.data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data)

class AdministrationAPI(ViewSet):
  permission_classes = [IsAuthenticated, IsSystemAdmin]

  def create(self, request):
    serializer = AdministrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    theater = serializer.save()

    if not theater.image:
      image = Image.objects.create(
        data = DEFAULT_THEATER_IMAGE,
        kind = THEATER_IMAGE[0]
      )
      theater.image = image
      theater.save()

    return Response(data=serializer.data)

  def update(self, request, pk=None):
    theater = get_object_or_404(Theater, pk=pk)
    admins = [
      get_object_or_404(TheaterAdmin, pk=pk) for pk in request.data['admins']
    ]
    theater.admins.set(admins)
    theater.save()
    return Response(data=AdministrationSerializer(theater).data)

  def destroy(self, request, pk=None):
    theater = get_object_or_404(Theater, pk=pk)
    theater.delete()
    return Response(
      data={'message': 'Theater {0} successfully deleted.'.format(pk)}
    )

class AuditoriumAPI(ViewSet):
  permission_classes = [IsResponsibleForTheater]

  def list(self, request, theater_id=None):
    theater = get_object_or_404(Theater, id=theater_id)
    auditoriums = theater.auditoriums.all()
    return Response(AuditoriumSerializer(auditoriums, many=True).data)

  def retrieve(self, request, theater_id=None, pk=None):
    auditorium = get_object_or_404(Auditorium, id=pk)
    return Response(AuditoriumSerializer(auditorium).data)

  def create(self, request, theater_id=None):
    theater = get_object_or_404(Theater, id=theater_id)
    self.check_object_permissions(request, theater)
    serializer = AuditoriumSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data)

  def update(self, request, theater_id=None, pk=None):
    theater = get_object_or_404(Theater, id=theater_id)
    self.check_object_permissions(request, theater)
    auditorium = get_object_or_404(Auditorium, id=pk)
    serializer = AuditoriumSerializer(auditorium, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    auditorium = serializer.save()
    return Response(data=serializer.data)

  def destroy(self, request, theater_id, pk):
    theater = get_object_or_404(Theater, pk=theater_id)
    self.check_object_permissions(request, theater)
    Auditorium.objects.get(id=pk).delete()
    return Response(data={'message': f'Auditorium {pk} successfully deleted.'})
