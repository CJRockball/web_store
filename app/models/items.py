from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import Enum


class FoodCategory(str, Enum):
    JUNK_FOOD = "junk"
    HEALTHY_FOOD = "healthy"


class FoodItem(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    price: int = Field(..., gt=0, description="Price must be positive")
    category: FoodCategory
    image: str = Field(..., pattern=r".*\.(jpg|png|gif)$")
    description: Optional[str] = Field(None, max_length=200)

    @validator('name')
    def name_must_be_alphanumeric_with_spaces(cls, v):
        if not v.replace(' ', '').isalnum():
            raise ValueError('Name must contain only alphanumeric characters and spaces')
        return v.title()


class CartItem(BaseModel):
    name: str
    price: int
    image: str
    quantity: int = 1


class Cart(BaseModel):
    items: List[CartItem] = []
    total_cost: int = 0
    item_count: int = 0

    def add_item(self, food_item: FoodItem) -> None:
        # Check if item already exists in cart
        for cart_item in self.items:
            if cart_item.name == food_item.name:
                cart_item.quantity += 1
                self.total_cost += food_item.price
                self.item_count += 1
                return

        # Add new item
        new_cart_item = CartItem(
            name=food_item.name,
            price=food_item.price,
            image=food_item.image
        )
        self.items.append(new_cart_item)
        self.total_cost += food_item.price
        self.item_count += 1

    def remove_item(self, item_name: str) -> bool:
        for i, cart_item in enumerate(self.items):
            if cart_item.name == item_name:
                self.total_cost -= cart_item.price * cart_item.quantity
                self.item_count -= cart_item.quantity
                del self.items[i]
                return True
        return False

    def clear(self) -> None:
        self.items = []
        self.total_cost = 0
        self.item_count = 0


class AddItemRequest(BaseModel):
    item_name: str = Field(..., min_length=1, max_length=50)


class RemoveItemRequest(BaseModel):
    item_name: str = Field(..., min_length=1, max_length=50)


class CartResponse(BaseModel):
    items: List[CartItem]
    total_cost: int
    item_count: int
    message: str = ""


class ErrorResponse(BaseModel):
    error: str
    status_code: int