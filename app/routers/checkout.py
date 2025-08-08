from fastapi import APIRouter, Request, Depends, HTTPException, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List

from app.models.items import Cart, CartResponse
from app.services.store_service import StoreService, StoreException
from app.dependencies import (
    get_shopping_cart, update_shopping_cart, 
    get_store_service, validate_session
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/checkout", tags=["checkout"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def checkout_page(
    request: Request,
    cart: Cart = Depends(get_shopping_cart),
    _: bool = Depends(validate_session)
):
    """Display the checkout page"""
    try:
        return templates.TemplateResponse("checkout.html", {
            "request": request,
            "cart": cart,
            "total_cost": cart.total_cost,
            "items": cart.items,
            "item_count": cart.item_count
        })
    except Exception as e:
        logger.error(f"Error loading checkout page: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load checkout page"
        )


@router.post("/", response_class=HTMLResponse)
async def checkout_action(
    request: Request,
    action: str = Form(...),
    cart: Cart = Depends(get_shopping_cart),
    _: bool = Depends(validate_session)
):
    """Handle checkout form actions"""
    try:
        if action == "Reset":
            # Clear the cart
            cart.clear()
            update_shopping_cart(request, cart)
            logger.info("Cart reset by user")

            return RedirectResponse(
                url="/store/",
                status_code=status.HTTP_302_FOUND
            )

        elif action == "Return":
            # Return to store without clearing cart
            return RedirectResponse(
                url="/store/",
                status_code=status.HTTP_302_FOUND
            )

        elif action == "Checkout":
            # Process checkout (in a real app, this would handle payment)
            if cart.item_count == 0:
                return templates.TemplateResponse("checkout.html", {
                    "request": request,
                    "cart": cart,
                    "total_cost": cart.total_cost,
                    "items": cart.items,
                    "item_count": cart.item_count,
                    "error": "Cart is empty! Please add some items first."
                })

            # Simulate successful checkout
            order_items = cart.items.copy()
            total_paid = cart.total_cost
            cart.clear()
            update_shopping_cart(request, cart)

            logger.info(f"Checkout completed for {len(order_items)} items, total: ${total_paid}")

            return templates.TemplateResponse("checkout_success.html", {
                "request": request,
                "order_items": order_items,
                "total_paid": total_paid,
                "order_number": f"ORD{hash(str(order_items)) % 10000:04d}"
            })

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid action"
            )

    except Exception as e:
        logger.error(f"Error in checkout action: {str(e)}")
        return templates.TemplateResponse("checkout.html", {
            "request": request,
            "cart": cart,
            "total_cost": cart.total_cost,
            "items": cart.items,
            "item_count": cart.item_count,
            "error": "An error occurred. Please try again."
        })


@router.delete("/clear", response_model=CartResponse)
async def clear_cart(
    request: Request,
    cart: Cart = Depends(get_shopping_cart),
    _: bool = Depends(validate_session)
):
    """Clear the shopping cart (API endpoint)"""
    try:
        cart.clear()
        update_shopping_cart(request, cart)
        logger.info("Cart cleared via API")

        return CartResponse(
            items=cart.items,
            total_cost=cart.total_cost,
            item_count=cart.item_count,
            message="Cart cleared successfully"
        )
    except Exception as e:
        logger.error(f"Error clearing cart: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clear cart"
        )


@router.post("/remove-item")
async def remove_item_from_cart(
    request: Request,
    item_name: str = Form(...),
    cart: Cart = Depends(get_shopping_cart),
    _: bool = Depends(validate_session)
):
    """Remove an item from the cart"""
    try:
        if cart.remove_item(item_name):
            update_shopping_cart(request, cart)
            logger.info(f"Removed {item_name} from cart")
            message = f"Removed {item_name} from cart"
        else:
            message = f"Item {item_name} not found in cart"

        return templates.TemplateResponse("checkout.html", {
            "request": request,
            "cart": cart,
            "total_cost": cart.total_cost,
            "items": cart.items,
            "item_count": cart.item_count,
            "message": message
        })

    except Exception as e:
        logger.error(f"Error removing item from cart: {str(e)}")
        return templates.TemplateResponse("checkout.html", {
            "request": request,
            "cart": cart,
            "total_cost": cart.total_cost,
            "items": cart.items,
            "item_count": cart.item_count,
            "error": "Failed to remove item from cart"
        })