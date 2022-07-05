from django.test import TestCase

from prompts.models import Adjective, Activity, Creature, Location


class TestAdjectiveModel(TestCase):
    """
    Tests that the Adjective model behaves as expected
    """

    def setUp(self):
        Adjective.objects.create(
            adjective="adjective",
            determiner="an",
        )

    def test_adjective_string_method(self):
        adjective = Adjective.objects.get(pk=1)
        self.assertEqual(
            str(adjective),
            "adjective",
        )


class TestActivityModel(TestCase):
    """
    Tests that the Activity model behaves as expected
    """

    def setUp(self):
        Activity.objects.create(
            activity="activity",
        )

    def test_activity_string_method(self):
        activity = Activity.objects.get(pk=1)
        self.assertEqual(
            str(activity),
            "activity",
        )


class TestCreatureModel(TestCase):
    """
    Tests that the Creature model behaves as expected
    """

    def setUp(self):
        Creature.objects.create(
            creature="creature",
            determiner="a",
            plural="creatures",
        )

    def test_creature_string_method(self):
        creature = Creature.objects.get(pk=1)
        self.assertEqual(
            str(creature),
            "creature",
        )


class TestLocationModel(TestCase):
    """
    Tests that the Location model behaves as expected
    """

    def setUp(self):
        Location.objects.create(
            location="location",
        )

    def test_location_string_method(self):
        location = Location.objects.get(pk=1)
        self.assertEqual(
            str(location),
            "location",
        )
