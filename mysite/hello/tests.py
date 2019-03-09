from django.test import Client, TestCase

# Create your tests here.
from .models import Airport, Flight, Passenger

class ModelsTestCase(TestCase):
    def setUp(self):
        """This code runs before running any test, built in to TestCase
        Shown below another way of creating instances of classes"""


        a1 = Airport.objects.create(code="AAA", city="city A")
        a2 = Airport.objects.create(code="BBB", city="city B")

        Flight.objects.create(origin=a1, destination=a2, duration=100)
        Flight.objects.create(origin=a1, destination=a1, duration=200)
        Flight.objects.create(origin=a1, destination=a2, duration=-100)

    def test_departures_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(), 3)

    def test_arival_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(), 1)

    def test_valid_flight(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=100)
        self.assertTrue(f.is_valid_flight())

    def test_invalid_flight(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1, duration=200)
        self.assertFalse(f.is_valid_flight())

    def test_invalid_flight(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=-100)
        self.assertFalse(f.is_valid_flight())

    def test_index(self):
        """client gives direct access to the context of the webpage to make it easier to test"""
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["flights"].count(), 3)

    def test_valid_flight_page(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)

        c= Client()
        response = c.get(f"/{f.id}")
        self.assertEqual(response.status_code, 200)

    def test_invalid_flight(self):
        max_id = Flight.objects.all().order_by('id')[0].id

        c = Client()
        response = c.get(f"{max_id + 1}")
        self.assertEqual(response.status_code, 404)

    def test_passenger(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Dilly", last="Cento")
        f.passengers.add(p)

        c = Client()
        response = c.get(f'/{f.id}')
        self.assertEqual(response.context['passengers'].count(), 1)
