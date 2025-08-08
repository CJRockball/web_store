import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root_endpoint():
    """Test root endpoint returns welcome page"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to Kids Web Store" in response.text


def test_store_page():
    """Test store page loads correctly"""
    response = client.get("/store/")
    assert response.status_code == 200
    assert "Kids Web Store" in response.text
    assert "Pizza" in response.text
    assert "Carrot" in response.text


def test_checkout_page():
    """Test checkout page loads correctly"""
    response = client.get("/checkout/")
    assert response.status_code == 200
    assert "Checkout" in response.text


def test_get_menu_api():
    """Test menu API endpoint"""
    response = client.get("/store/menu")
    assert response.status_code == 200
    menu = response.json()
    assert "Pizza" in menu
    assert "Carrot" in menu
    assert menu["Pizza"]["price"] == 1
    assert menu["Carrot"]["price"] == 2


def test_get_cart_api():
    """Test cart API endpoint"""
    response = client.get("/store/cart")
    assert response.status_code == 200
    cart = response.json()
    assert "items" in cart
    assert "total_cost" in cart
    assert "item_count" in cart


def test_api_info():
    """Test API info endpoint"""
    response = client.get("/api/info")
    assert response.status_code == 200
    info = response.json()
    assert "app_name" in info
    assert "version" in info
    assert "endpoints" in info


def test_clear_cart():
    """Test clearing cart"""
    response = client.delete("/checkout/clear")
    assert response.status_code == 200
    result = response.json()
    assert result["item_count"] == 0
    assert result["total_cost"] == 0
    assert "cleared" in result["message"].lower()


class TestStoreService:
    """Test store service functionality"""

    def test_add_item_to_cart(self):
        """Test adding items to cart via form"""
        # Add pizza to cart
        response = client.post(
            "/store/add-item",
            data={"item_name": "Pizza"}
        )
        assert response.status_code == 200
        result = response.json()
        assert result["item_count"] == 1
        assert result["total_cost"] == 1
        assert "Pizza" in result["message"]

    def test_add_invalid_item(self):
        """Test adding invalid item to cart"""
        response = client.post(
            "/store/add-item",
            data={"item_name": "InvalidItem"}
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_checkout_actions(self):
        """Test checkout form actions"""
        # Test return action
        response = client.post(
            "/checkout/",
            data={"action": "Return"}
        )
        assert response.status_code == 200  # Should redirect

        # Test reset action
        response = client.post(
            "/checkout/",
            data={"action": "Reset"}
        )
        assert response.status_code == 200  # Should redirect


class TestSecurity:
    """Test security features"""

    def test_input_sanitization(self):
        """Test that malicious input is sanitized"""
        response = client.post(
            "/store/add-item",
            data={"item_name": "<script>alert('xss')</script>"}
        )
        # Should return 404 for invalid item, not execute script
        assert response.status_code == 404

    def test_session_handling(self):
        """Test that sessions work correctly"""
        # Make a request to create session
        response = client.get("/store/")
        assert response.status_code == 200

        # Check that session cookies are set
        assert len(response.cookies) > 0


if __name__ == "__main__":
    pytest.main([__file__])