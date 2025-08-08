from fastapi import APIRouter, Request, Depends, HTTPException, status, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Dict, Any

from app.models.items import (
    FoodItem, Cart, AddItemRequest, CartResponse, 
    FoodCategory, ErrorResponse
)
from app.services.store_service import StoreService, StoreException
from app.dependencies import (
    get_shopping_cart, update_shopping_cart, 
    get_store_service, sanitize_input, validate_session
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/store", tags=["store"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def store_page(
    request: Request,
    _: bool = Depends(validate_session),
    cart: Cart = Depends(get_shopping_cart),
    store_service: StoreService = Depends(get_store_service)
):
    """Display the main store page"""
    try:
        menu_items = store_service.get_all_items()
        junk_items = store_service.get_items_by_category(FoodCategory.JUNK_FOOD)
        healthy_items = store_service.get_items_by_category(FoodCategory.HEALTHY_FOOD)

        return templates.TemplateResponse("index.html", {
            "request": request,
            "menu_items": menu_items,
            "junk_items": junk_items,
            "healthy_items": healthy_items,
            "cart_count": cart.item_count,
            "cart_total": cart.total_cost
        })
    except Exception as e:
        logger.error(f"Error loading store page: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load store page"
        )

@router.post("/add-item", response_model=CartResponse)
async def add_item(
    item_request: AddItemRequest,
    request: Request,                     # <-- gives access to app.state
    cart: dict = Depends(get_shopping_cart),
):
    service = request.app.state.store_service   # direct access
    item = service.get_item(item_request.item_name)

    cart["items"].append(item.name)
    cart["images"].append(item.image)
    cart["total_cost"] += item.price
    cart["item_count"] += 1

    return CartResponse(
        items=cart["items"],
        total_cost=cart["total_cost"],
        item_count=cart["item_count"],
        message=f"Added {item.name} to cart",
    )


@router.post("/add-item-form", response_class=HTMLResponse)
async def add_item_form_handler(
    request: Request,
    item_name: str = Form(...),
    cart: Cart = Depends(get_shopping_cart),
    store_service: StoreService = Depends(get_store_service)
):
    """Handle form submission for adding items (for HTML forms)"""
    try:
        # Sanitize input
        clean_item_name = sanitize_input(item_name)

        # Special handling for action button
        if clean_item_name == "action":
            # Redirect to checkout
            from fastapi.responses import RedirectResponse
            return RedirectResponse(url="/checkout", status_code=status.HTTP_302_FOUND)

        # Get the item and add to cart
        item = store_service.get_item(clean_item_name)
        cart.add_item(item)
        store_service.validate_cart(cart)
        update_shopping_cart(request, cart)

        # Return updated page
        menu_items = store_service.get_all_items()
        junk_items = store_service.get_items_by_category(FoodCategory.JUNK_FOOD)
        healthy_items = store_service.get_items_by_category(FoodCategory.HEALTHY_FOOD)

        return templates.TemplateResponse("index.html", {
            "request": request,
            "menu_items": menu_items,
            "junk_items": junk_items,
            "healthy_items": healthy_items,
            "cart_count": cart.item_count,
            "cart_total": cart.total_cost,
            "message": f"Added {item.name} to cart!"
        })

    except StoreException as e:
        logger.warning(f"Form error adding item: {e.message}")
        # Return page with error
        menu_items = store_service.get_all_items()
        return templates.TemplateResponse("index.html", {
            "request": request,
            "menu_items": menu_items,
            "cart_count": cart.item_count,
            "cart_total": cart.total_cost,
            "error": e.message
        })


@router.get("/menu", response_model=Dict[str, FoodItem])
async def get_menu(store_service: StoreService = Depends(get_store_service)):
    """Get the complete menu"""
    try:
        return store_service.get_all_items()
    except Exception as e:
        logger.error(f"Error getting menu: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve menu"
        )


@router.get("/cart", response_model=CartResponse)
async def get_cart(cart: Cart = Depends(get_shopping_cart)):
    """Get current cart contents"""
    return CartResponse(
        items=cart.items,
        total_cost=cart.total_cost,
        item_count=cart.item_count,
        message="Current cart contents"
    )