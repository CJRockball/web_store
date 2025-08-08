from typing import Dict, List
from app.models.items import FoodItem, FoodCategory, Cart
import logging

logger = logging.getLogger(__name__)


class StoreException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code


class StoreService:
    def __init__(self):
        self.menu_items = self._initialize_menu()
        logger.info(f"Store service initialized with {len(self.menu_items)} items")

    def _initialize_menu(self) -> Dict[str, FoodItem]:
        """Initialize the menu with available food items"""
        return {
            "Pizza": FoodItem(
                name="Pizza", 
                price=1, 
                category=FoodCategory.JUNK_FOOD, 
                image="pizza.jpg",
                description="Delicious cheese pizza"
            ),
            "Fries": FoodItem(
                name="Fries", 
                price=1, 
                category=FoodCategory.JUNK_FOOD, 
                image="fries.jpg",
                description="Crispy golden fries"
            ),
            "Cookie": FoodItem(
                name="Cookie", 
                price=1, 
                category=FoodCategory.JUNK_FOOD, 
                image="cookie.jpg",
                description="Sweet chocolate chip cookie"
            ),
            "Hotdog": FoodItem(
                name="Hotdog", 
                price=1, 
                category=FoodCategory.JUNK_FOOD, 
                image="hotdog.jpg",
                description="Classic hotdog with mustard"
            ),
            "Chocolate": FoodItem(
                name="Chocolate", 
                price=1, 
                category=FoodCategory.JUNK_FOOD, 
                image="chocolate.jpg",
                description="Rich milk chocolate bar"
            ),
            "Carrot": FoodItem(
                name="Carrot", 
                price=2, 
                category=FoodCategory.HEALTHY_FOOD, 
                image="carrot.jpg",
                description="Fresh organic carrot"
            ),
            "Tomato": FoodItem(
                name="Tomato", 
                price=2, 
                category=FoodCategory.HEALTHY_FOOD, 
                image="tomato.jpg",
                description="Ripe red tomato"
            ),
            "Corn": FoodItem(
                name="Corn", 
                price=2, 
                category=FoodCategory.HEALTHY_FOOD, 
                image="corn.jpg",
                description="Sweet corn on the cob"
            ),
            "Tea": FoodItem(
                name="Tea", 
                price=2, 
                category=FoodCategory.HEALTHY_FOOD, 
                image="tea.jpg",
                description="Healthy herbal tea"
            ),
            "Icecream": FoodItem(
                name="Icecream", 
                price=2, 
                category=FoodCategory.JUNK_FOOD, 
                image="icecream.jpg",
                description="Vanilla ice cream cone"
            ),
        }

    def get_all_items(self) -> Dict[str, FoodItem]:
        """Get all available menu items"""
        return self.menu_items

    def get_item(self, name: str) -> FoodItem:
        """Get a specific menu item by name"""
        if name not in self.menu_items:
            logger.warning(f"Item '{name}' not found in menu")
            raise StoreException(f"Item '{name}' not found", 404)
        return self.menu_items[name]

    def get_items_by_category(self, category: FoodCategory) -> List[FoodItem]:
        """Get all items in a specific category"""
        return [item for item in self.menu_items.values() if item.category == category]

    def calculate_total(self, items: List[str]) -> int:
        """Calculate total price for a list of items"""
        total = 0
        for item_name in items:
            try:
                item = self.get_item(item_name)
                total += item.price
            except StoreException:
                logger.warning(f"Skipping unknown item: {item_name}")
                continue
        return total

    def validate_cart(self, cart: Cart, max_items: int = 50) -> bool:
        """Validate cart constraints"""
        if cart.item_count > max_items:
            raise StoreException(f"Cart cannot contain more than {max_items} items", 400)

        # Validate all items exist in menu
        for cart_item in cart.items:
            if cart_item.name not in self.menu_items:
                raise StoreException(f"Invalid item in cart: {cart_item.name}", 400)

        return True


# Singleton instance
store_service = StoreService()