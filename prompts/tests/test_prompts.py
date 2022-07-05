from django.test import TestCase

from prompts.models import Adjective, Activity, Creature, Location
from prompts.prompts import (
    get_word,
    adjective_creature_activity_location,
    adjective_creature_activity,
    adjective_creature,
    creature_activity_location,
    creature_activity,
    adjective_creature_location,
    creature_location,
    generate_prompt,
)


class TestPromptFunctions(TestCase):
    """
    Tests that the prompt generation functions behave as expected.
    Note: The prompt functions return randomly selected words but since only
    one word is created for each model in the setup, the returned values for
    the tests are predictable.
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

    def test_get_word_returns_requested_type(self):
        word = get_word("Adjective")
        self.assertIsInstance(word, Adjective)

    def test_adjective_creature_activity_location_function(self):
        prompt = adjective_creature_activity_location()
        self.assertEqual("an adjective creature activity location", prompt)

    def test_adjective_creature_activity_function(self):
        prompt = adjective_creature_activity()
        self.assertEqual("an adjective creature activity", prompt)

    def test_adjective_creature_function(self):
        prompt = adjective_creature()
        self.assertEqual("an adjective creature", prompt)

    def test_creature_activity_location_function(self):
        prompt = creature_activity_location()
        self.assertEqual("a creature activity location", prompt)

    def test_creature_activity_function(self):
        prompt = creature_activity()
        self.assertEqual("a creature activity", prompt)

    def test_adjective_creature_location_function(self):
        prompt = adjective_creature_location()
        self.assertEqual("an adjective creature location", prompt)

    def test_creature_location_function(self):
        prompt = creature_location()
        self.assertEqual("a creature location", prompt)

    def test_generate_prompt_returns_string(self):
        prompt = generate_prompt()
        self.assertIsInstance(prompt, str)


class TestPromptFunctionFailure(TestCase):
    """
    Tests that prompt function return False if no word can be found.
    Note: No word objects are created in the setup, so all functions fail to
    find words.
    """

    def test_adjective_creature_activity_location_returns_false_on_fail(self):
        prompt = adjective_creature_activity_location()
        self.assertFalse(prompt)

    def test_adjective_creature_activity_returns_false_on_fail(self):
        prompt = adjective_creature_activity()
        self.assertFalse(prompt)

    def test_adjective_creature_returns_false_on_fail(self):
        prompt = adjective_creature()
        self.assertFalse(prompt)

    def test_creature_activity_location_returns_false_on_fail(self):
        prompt = creature_activity_location()
        self.assertFalse(prompt)

    def test_creature_activity_returns_false_on_fail(self):
        prompt = creature_activity()
        self.assertFalse(prompt)

    def test_adjective_creature_location_returns_false_on_fail(self):
        prompt = adjective_creature_location()
        self.assertFalse(prompt)

    def test_creature_location_returns_false_on_fail(self):
        prompt = creature_location()
        self.assertFalse(prompt)
