from django.test import TestCase
from django.shortcuts import reverse

from prompts.models import Adjective, Activity, Creature, Location


class TestGetPromptView(TestCase):
    """
    Tests that the get_prompt view is behaving as expected
    """

    def setUp(self):
        # create some words for the prompt generation functions
        Adjective.objects.create(
            adjective="adjective",
            determiner="an",
        )
        Activity.objects.create(
            activity="activity",
        )
        Creature.objects.create(
            creature="creature",
            determiner="a",
            plural="creatures",
        )
        Location.objects.create(
            location="location",
        )

    def test_get_get_prompt_view(self):
        # mock ajax get request
        response = self.client.get(
            reverse("get_prompt"),
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"},
        )

        self.assertIn("prompt", response.json())
        self.assertEqual(200, response.status_code)
