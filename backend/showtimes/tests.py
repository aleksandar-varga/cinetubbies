from rest_framework.test import APITestCase

from authentication.models import User
from authentication.serializers import TheaterAdminSerializer
from authentication.serializers import AdminSerializer

from theaters.models import Theater
from theaters.serializers import AdministrationSerializer
from theaters.serializers import PublicSerializer
from theaters.serializers import AuditoriumSerializer

from movies.models import Movie
from movies.serializers import MovieSerializer

from .models import Showtime
from .serializers import ShowtimeSerializer

class ShowtimeAPITests(APITestCase):
  test_theater_admin = {
    'username': 'admin',
    'password': '123456',
    'email': 'admin@test.com',
    'role': 'cinema_admin',
    'theater': '',
  }

  test_theater_admin2 = {
    'username': 'admin2',
    'password': '123456',
    'email': 'admin2@test.com',
    'role': 'cinema_admin',
    'theater': '',
  }

  test_fan_zone_admin = {
    'username': 'admin3',
    'password': '123456',
    'email': 'admin3@test.com',
    'role': 'fan_zone_admin',
  }

  test_system_admin = {
    'username': 'sysadmin',
    'password': '123456',
    'role': 'admin',
    'email': 'sysadmin@test.com',
  }

  test_user = {
    'username': 'username',
    'password': '123456',
    'phone': '123',
    'city': 'city'
  }

  test_theater = {
    'name': 'theater1',
    'address': 'some street',
    'kind': 'p',
    'admins': [1],
  }

  test_theater2 = {
    'name': 'theater2',
    'address': 'address',
    'kind': 'm',
    'admins': [2],
  }

  test_movie = {
    'title': 'title',
    'genre': 'genre',
    'theater': 1
  }

  test_showtime = {
    'auditorium': 1,
    'date': '2018-05-10',
    'time': '15:00',
    'price': 300,
    'movie': 1
  }

  auditorium = {
    'name': 'Sala 1',
    'theater': 1,
    'layout': '{}'
  }


  def setUp(self):
    serializer = TheaterAdminSerializer(data=self.test_theater_admin)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = TheaterAdminSerializer(data=self.test_theater_admin2)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = AdminSerializer(data=self.test_fan_zone_admin)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = AdminSerializer(data=self.test_system_admin)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = AdminSerializer(data=self.test_user)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = AdministrationSerializer(data=self.test_theater)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = AdministrationSerializer(data=self.test_theater2)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = AuditoriumSerializer(data=self.auditorium)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = MovieSerializer(data=self.test_movie)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = ShowtimeSerializer(data=self.test_showtime)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

  def login(self, user):
    response = self.client.post(
      path='http://localhost:8000/api/auth/login/',
      data = {
        'username': user['username'],
        'password': user['password']
      },
      format='json'
    )
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + response.data['token'])

  def post(self, new_showtime):
    return self.client.post(
      path='http://localhost:8000/api/showtimes/',
      data = new_showtime,
      format='json'
    )

  def delete(self, id):
    return self.client.delete(
      path='http://localhost:8000/api/showtimes/'+id+'/'
    )

  def get(self, id):
    return self.client.get(
      path='http://localhost:8000/api/showtimes/'+id+'/'
    )

  def put(self, showtime, id):
    return self.client.put(
      path='http://localhost:8000/api/showtimes/'+id+'/',
      data = showtime,
      format='json'
    )

  def test_create(self):
    new_showtime = {
      'auditorium': 1,
      'date': '2018-05-07',
      'time': '15:30',
      'price': 300,
      'movie': 1
    }

    # login and post as a user; fail
    self.login(self.test_user)
    response = self.post(new_showtime)
    self.assertEqual(response.status_code, 403)

    # login and post as a system admin; fail
    self.login(self.test_system_admin)
    response = self.post(new_showtime)
    self.assertEqual(response.status_code, 403)

    # login and post as a theater admin; pass
    self.login(self.test_theater_admin)
    response = self.post(new_showtime)
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertTrue(Showtime.objects.all().count() == 2)

    # non-existing movie; fail
    new_showtime['movie'] = 3
    response = self.post(new_showtime)
    self.assertEqual(response.status_code, 400)

  def test_destroy(self):
    # login and delete as a user; fail
    self.login(self.test_user)
    response = self.delete('1')
    self.assertTrue(response.status_code, 401)

    # log and delete in as a system admin; fail
    self.login(self.test_system_admin)
    response = self.delete('1')
    self.assertTrue(response.status_code, 401)

    # log and delete in as a theater admin; pass
    self.login(self.test_theater_admin)
    response = self.delete('1')
    self.assertTrue(response.status_code, 200)
    self.assertTrue(Showtime.objects.all().count() == 0)

    # non-existing showtime; fail
    response = self.delete('2')
    self.assertTrue(response.status_code, 404)

  def test_retrieve(self):
    response = self.get('1')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)

    # non-existing showtime; fail
    response = self.get('2')
    self.assertTrue(response.status_code, 404)

  def test_update(self):
    update_showtime = {
      'auditorium': 1,
      'date': '2018-05-07',
      'time': '15:30',
      'price': 350,
      'movie': 1
    }

    # login and put as a user; fail
    self.login(self.test_user)
    response = self.put(update_showtime, '1')
    self.assertEqual(response.status_code, 403)

    # login and put as a system admin; fail
    self.login(self.test_system_admin)
    response = self.put(update_showtime, '1')
    self.assertEqual(response.status_code, 403)

    # login and put as a theater admin; pass
    self.login(self.test_theater_admin)
    response = self.put(update_showtime, '1')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)

    # attempt put on a showtime that is not theater admin's responsibility; fail
    self.login(self.test_theater_admin2)
    response = self.put(update_showtime, '1')
    self.assertEqual(response.status_code, 403)
