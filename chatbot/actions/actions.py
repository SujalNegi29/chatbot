from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import uuid

# -----------------------------
# In-memory storage (TEMP)
# -----------------------------
USER_CART = {}
USER_ORDERS = {}

# Price list
MENU_PRICES = {
    "pizza": 200,
    "burger": 120,
    "pasta": 180,
    "fries": 100
}


# -----------------------------
# Add item to cart
# -----------------------------
class ActionAddToCart(Action):

    def name(self) -> Text:
        return "action_add_to_cart"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        user_id = tracker.sender_id
        food = tracker.get_slot("food")
        quantity = tracker.get_slot("quantity")

        if not food:
            dispatcher.utter_message("❌ Please tell me what item you want to add.")
            return []

        quantity = int(quantity) if quantity else 1
        food = food.lower()

        if food not in MENU_PRICES:
            dispatcher.utter_message(f"❌ {food} is not available in the menu.")
            return []

        if user_id not in USER_CART:
            USER_CART[user_id] = {}

        USER_CART[user_id][food] = USER_CART[user_id].get(food, 0) + quantity

        dispatcher.utter_message(
            f"✅ Added {quantity} {food}(s) to your cart."
        )

        return []


# -----------------------------
# Show cart total
# -----------------------------
class ActionShowTotal(Action):

    def name(self) -> Text:
        return "action_show_total"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        user_id = tracker.sender_id
        cart = USER_CART.get(user_id)

        if not cart:
            dispatcher.utter_message("🛒 Your cart is empty.")
            return []

        total = 0
        summary = []

        for item, qty in cart.items():
            price = MENU_PRICES[item] * qty
            total += price
            summary.append(f"{item} x {qty} = ₹{price}")

        dispatcher.utter_message(
            "🧾 Your cart:\n" + "\n".join(summary) + f"\n\n💰 Total: ₹{total}"
        )

        return []


# -----------------------------
# Place order
# -----------------------------
class ActionPlaceOrder(Action):

    def name(self) -> Text:
        return "action_place_order"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        user_id = tracker.sender_id
        payment = tracker.get_slot("payment_method")
        cart = USER_CART.get(user_id)

        if not cart:
            dispatcher.utter_message("❌ Your cart is empty. Add items before ordering.")
            return []

        order_id = str(uuid.uuid4())[:8]

        USER_ORDERS[user_id] = {
            "order_id": order_id,
            "items": cart,
            "status": "Preparing"
        }

        USER_CART[user_id] = {}

        dispatcher.utter_message(
            f"🎉 Order placed successfully!\n"
            f"🆔 Order ID: {order_id}\n"
            f"💳 Payment: {payment}\n"
            f"📦 Status: Preparing"
        )

        return [SlotSet("order_id", order_id)]


# -----------------------------
# Track order
# -----------------------------
class ActionTrackOrder(Action):

    def name(self) -> Text:
        return "action_track_order"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        user_id = tracker.sender_id
        order = USER_ORDERS.get(user_id)

        if not order:
            dispatcher.utter_message("❌ No active order found.")
            return []

        dispatcher.utter_message(
            f"📦 Order ID: {order['order_id']}\n"
            f"🚚 Current Status: {order['status']}"
        )

        return []


# -----------------------------
# Reorder last order
# -----------------------------
class ActionReorderLast(Action):

    def name(self) -> Text:
        return "action_reorder_last"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        user_id = tracker.sender_id
        last_order = USER_ORDERS.get(user_id)

        if not last_order:
            dispatcher.utter_message("⚠️ You don’t have any previous orders to reorder.")
            return []

        USER_CART[user_id] = last_order["items"].copy()

        dispatcher.utter_message(
            "🔁 Your last order has been added to the cart."
        )

        return []
