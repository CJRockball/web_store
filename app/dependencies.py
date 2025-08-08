from fastapi import Request, Depends, HTTPException, status
from app.models.items import Cart, CartItem
from app.services.store_service import store_service, StoreService
from app.config import get_settings, Settings
import nh3
import logging

logger = logging.getLogger(__name__)


def get_shopping_cart(request: Request) -> Cart:
    """Get or create shopping cart from session"""
    try:
        if "cart" not in request.session:
            request.session["cart"] = {
                "items": [],
                "total_cost": 0,
                "item_count": 0
            }
            logger.info("Created new shopping cart session")
        
        cart_data = request.session["cart"]
        
        # FIX: Properly reconstruct Cart with CartItem objects
        cart = Cart()
        
        # Convert dict items back to CartItem objects
        cart.items = [
            CartItem(**item_dict) 
            for item_dict in cart_data.get("items", [])
        ]
        cart.total_cost = cart_data.get("total_cost", 0)
        cart.item_count = cart_data.get("item_count", 0)
        
        return cart
        
    except Exception as e:
        logger.error(f"Error getting shopping cart: {str(e)}")
        return Cart()


def update_shopping_cart(request: Request, cart: Cart) -> None:
    """Update shopping cart in session"""
    try:
        request.session["cart"] = {
            "items": [item.model_dump() for item in cart.items],  # Use model_dump() instead of dict()
            "total_cost": cart.total_cost,
            "item_count": cart.item_count
        }
        logger.debug(f"Updated cart with {cart.item_count} items")
    except Exception as e:
        logger.error(f"Error updating shopping cart: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update shopping cart"
        )


def get_store_service() -> StoreService:
    """Dependency to get store service"""
    return store_service


def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent XSS"""
    if not text:
        return ""
    return nh3.clean(text.strip())


def validate_session(request: Request) -> bool:
    """Validate session integrity"""
    if not hasattr(request, 'session'):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Session not available"
        )
    return True


async def get_current_settings() -> Settings:
    """Get current application settings"""
    return get_settings()
