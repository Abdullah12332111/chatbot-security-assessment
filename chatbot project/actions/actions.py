from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import hashlib

# Simulated database with roles
USER_DATABASE = {
    "john_doe": {"password": "5f4dcc3b5aa765d61d8327deb882cf99", "role": "user"},  # Password: "password"
    "admin": {"password": "0192023a7bbd73250516f069df18b500", "role": "admin"}  # Password: "admin123"
}

# Simulated bookings database
BOOKINGS = {
    "john_doe": {"room_type": "Single", "stay_duration": "3 nights"},
    "admin": {"room_type": "Suite", "stay_duration": "5 nights"}
}

class ActionUserLogin(Action):
    def name(self) -> Text:
        return "action_user_login"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("username")
        password = tracker.get_slot("password")

        if not username or not password:
            dispatcher.utter_message(text="Please provide both username and password.")
            return []

        hashed_password = hashlib.md5(password.encode()).hexdigest()

        if username in USER_DATABASE and USER_DATABASE[username]["password"] == hashed_password:
            role = USER_DATABASE[username]["role"]
            dispatcher.utter_message(text=f"Login successful! Welcome, {username}. Your role is {role}.")
        else:
            dispatcher.utter_message(text="Invalid username or password. Please try again.")

        return []

class ActionBookRoom(Action):
    def name(self) -> Text:
        return "action_book_room"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("username")
        room_type = tracker.get_slot("room_type")
        stay_duration = tracker.get_slot("stay_duration")

        if not username:
            dispatcher.utter_message(text="You need to log in first to book a room.")
            return []

        if not room_type:
            dispatcher.utter_message(text="What type of room would you like to book?")
            return []

        if not stay_duration:
            dispatcher.utter_message(text="How many nights will you be staying?")
            return []

        BOOKINGS[username] = {"room_type": room_type, "stay_duration": stay_duration}
        dispatcher.utter_message(text=f"Your {room_type} room has been booked for {stay_duration}.")
        return []

class ActionCancelBooking(Action):
    def name(self) -> Text:
        return "action_cancel_booking"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("username")
        requested_booking = tracker.latest_message.get("text").lower()

        if not username:
            dispatcher.utter_message(text="You need to log in first to cancel a booking.")
            return []

        # Ensure the user can only cancel their own booking
        if username not in BOOKINGS:
            dispatcher.utter_message(text="You don't have any existing bookings to cancel.")
            return []

        # Prevent users from canceling someone else's booking
        if "admin" in requested_booking and username != "admin":
            dispatcher.utter_message(text="You do not have permission to cancel another user's booking.")
            return []

        # Cancel the user's own booking
        if username in BOOKINGS:
            del BOOKINGS[username]
            dispatcher.utter_message(text=f"Your booking has been successfully canceled, {username}.")
        else:
            dispatcher.utter_message(text="You can only cancel your own booking.")

        return []

class ActionPrivilegeEscalationAttempt(Action):
    def name(self) -> Text:
        return "action_privilege_escalation_attempt"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("username")

        if not username:
            dispatcher.utter_message(text="You need to log in first.")
            return []

        # Prevent privilege escalation
        if username in USER_DATABASE and USER_DATABASE[username]["role"] != "admin":
            dispatcher.utter_message(text="Access Denied! You do not have permission to become an admin.")
        else:
            dispatcher.utter_message(text="You're already an admin.")

        return []
