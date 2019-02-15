# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import requests
import json
from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet

logger = logging.getLogger(__name__)


class ActionJoke(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_joke"

    def run(self, dispatcher, tracker, domain):
        # what your action should do
        request = json.loads(requests.get('https://api.chucknorris.io/jokes/random').text)  # make an api call
        joke = request['value']  # extract a joke from returned json response
        dispatcher.utter_message(joke)  # send the message back to the user
        return []


class ActionListBanks(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_list_banks"

    def run(self, dispatcher, tracker, domain):
        # what your action should do
        location = tracker.get_slot("home_location")
        if location is not None:
            dispatcher.utter_template("utter_show_list_of_banks", tracker)
        else:
            dispatcher.utter_message("Please let me know where you are...")
        return []


class ActionReset(Action):
    def name(self):
        return 'action_reset'

    def run(self, dispatcher, tracker, domain):
        SlotSet(key="home_location", value=None)
        dispatcher.utter_message("resetting home_location slot...")
        return [SlotSet(key="home_location", value=None)]
