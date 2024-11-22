# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import time

# Simulating drawer statuses for the example
DRAWER_STATUSES = {f"{i}": "closed" for i in range(1, 11)}

class ActionControlDrawer(Action):
    def name(self) -> Text:
        return "action_control_drawer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        drawer_number = tracker.get_slot("drawer_number")
        action = tracker.get_slot("action")

        if drawer_number and action:
            # Update drawer status (simulate hardware interaction)
            DRAWER_STATUSES[drawer_number] = "open" if action == "open" else "closed"
            dispatcher.utter_message(
                text=f"Performing {action} on drawer {drawer_number}."
            )
        else:
            dispatcher.utter_message(
                text="I couldn't identify the drawer or action. Please try again."
            )
        return []

class ActionCheckDrawerStatus(Action):
    def name(self) -> Text:
        return "action_check_drawer_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        drawer_number = tracker.get_slot("drawer_number")

        if drawer_number and drawer_number in DRAWER_STATUSES:
            status = DRAWER_STATUSES[drawer_number]
            dispatcher.utter_message(
                text=f"Drawer {drawer_number} is currently {status}."
            )
        else:
            dispatcher.utter_message(
                text="I couldn't find the status for that drawer. Please try again."
            )
        return []

class ActionToggleDrawers(Action):
    def name(self) -> Text:
        return "action_toggle_drawers"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        drawer_numbers = tracker.get_slot("drawer_number").split(", ")
        toggled_drawers = []

        for drawer in drawer_numbers:
            if drawer in DRAWER_STATUSES:
                new_status = "open" if DRAWER_STATUSES[drawer] == "closed" else "closed"
                DRAWER_STATUSES[drawer] = new_status
                toggled_drawers.append(drawer)

        dispatcher.utter_message(
            text=f"Toggled drawers: {', '.join(toggled_drawers)}."
        )
        return []

class ActionSetDrawerTimer(Action):
    def name(self) -> Text:
        return "action_set_drawer_timer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        drawer_number = tracker.get_slot("drawer_number")
        action = tracker.get_slot("action")
        duration = tracker.get_slot("duration")

        if drawer_number and action and duration:
            # Simulate setting a timer (non-blocking for demonstration)
            dispatcher.utter_message(
                text=f"Timer set for drawer {drawer_number} to {action} in {duration} seconds."
            )
        else:
            dispatcher.utter_message(
                text="I couldn't set the timer. Please provide all necessary details."
            )
        return []
