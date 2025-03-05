from django.core.management import call_command
from django.test import TestCase
from weddingwrangle.models import Guest, Position, RSVPStatus, Title
from weddingwrangle.views import RSVPView

class GuestTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("loaddata", "weddingwrangle/initial_data.json")
        cls.groom = Position.objects.get(id=1)
        cls.mr_title = Title.objects.get(id=1)
        cls.rsvp_status = RSVPStatus.objects.get(id=4)
        cls.luke = Guest.objects.create(
            first_name="Luke", 
            surname="Skywalker", 
            position=cls.groom, 
            title=cls.mr_title,
            rsvp_status=cls.rsvp_status,
            rsvp_link="ao4eiflaiwj"
        )
        cls.han = Guest.objects.create(
            first_name="Han", 
            surname="Solo", 
            position=cls.groom, 
            title=cls.mr_title,
            rsvp_status=cls.rsvp_status,
            rsvp_link="8o4ekfKabwd"
        )

    def test_fetching_guests(self):
        self.assertEqual(self.luke.surname, "Skywalker")
        self.assertEqual(self.han.surname, "Solo")

    def test_guest_rsvp_status(self):
        self.assertEqual(self.luke.rsvp_status.id, 4)
        self.assertEqual(self.han.rsvp_status.id, 4)
