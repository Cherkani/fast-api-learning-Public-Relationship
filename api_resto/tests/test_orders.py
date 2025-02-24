import pytest
from fastapi.testclient import TestClient
import time
from decimal import Decimal
from api_resto.tests.conftest import client, test_db  # Updated import

def test_create_order(client):
    timestamp = int(time.time())
    customer_data = {
        "name": f"Test Customer {timestamp}",
        "email": f"test{timestamp}@example.com",
        "address": "123 Test St",
        "phone_number": f"+1234567890{timestamp}"[:20]  # At least 10 chars, max 20
    }
    
    customer_response = client.post("/customers/", json=customer_data)
    print("Customer Response:", customer_response.text)  # Changed to print full response
    assert customer_response.status_code == 200, f"Customer creation failed with response: {customer_response.text}"
    response_data = customer_response.json()
    assert "id" in response_data, f"No id in response: {response_data}"
    customer_id = response_data["id"]
    
    
    menu_item_data = {
        "dishes": f"Test Dish {timestamp}",
        "category": "Main",
        "calories": 500,
        "price": 9.99,
        "ingredients": []
    }
    
    menu_item_response = client.post("/menu_items/", json=menu_item_data)
    menu_item_id = menu_item_response.json()["menuItemID"]
   
    order_data = {
        "customer_id": customer_id,
        "total_price": 19.99,
        "status": "pending",
        "tracking_number": f"TRK{timestamp}",
        "menu_items": [
            {
                "menu_item_id": menu_item_id,
                "quantity": 2
            }
        ]
    }
    
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == customer_id
    assert "id" in data

def test_get_orders(client):
    response = client.get("/orders/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_single_order(client):
    # Create test data first
    timestamp = int(time.time())
    customer_data = {
        "name": f"Test Customer {timestamp}",
        "email": f"test{timestamp}@example.com",
        "address": "123 Test St",
        "phone_number": f"+1234567890{timestamp}"[:20]  # At least 10 chars, max 20
    }
    
    customer_response = client.post("/customers/", json=customer_data)
    customer_id = customer_response.json()["id"]
    
    menu_item_data = {
        "dishes": f"Test Dish {timestamp}",
        "category": "Main",
        "calories": 500,
        "price": 9.99,
        "ingredients": []
    }
    
    menu_item_response = client.post("/menu_items/", json=menu_item_data)
    menu_item_id = menu_item_response.json()["menuItemID"]
    
    order_data = {
        "customer_id": customer_id,
        "total_price": 19.99,
        "status": "pending",
        "tracking_number": f"TRK{timestamp}",
        "menu_items": [{"menu_item_id": menu_item_id, "quantity": 2}]
    }
    
    create_response = client.post("/orders/", json=order_data)
    order_id = create_response.json()["id"]
    
    # Test getting the order
    get_response = client.get(f"/orders/{order_id}")
    assert get_response.status_code == 200
    order = get_response.json()
    assert order["id"] == order_id
    assert order["customer_id"] == customer_id
    assert float(order["total_price"]) == 19.99
    assert order["status"] == "pending"
    assert order["tracking_number"] == f"TRK{timestamp}"

def test_update_order(client):
    # First create a customer
    timestamp = int(time.time())
    customer_data = {
        "name": f"Test Customer {timestamp}",
        "email": f"test{timestamp}@example.com",
        "address": "123 Test St",
        "phone_number": f"+1234567890{timestamp}"[:20]  # At least 10 chars, max 20
    }
    
    customer_response = client.post("/customers/", json=customer_data)
    customer_id = customer_response.json()["id"]
    
    # Create first menu item
    menu_item_data1 = {
        "dishes": f"Test Dish 1 {timestamp}",
        "category": "Main",
        "calories": 500,
        "price": 9.99,
        "ingredients": []
    }
    
    menu_item_response1 = client.post("/menu_items/", json=menu_item_data1)
    menu_item_id1 = menu_item_response1.json()["menuItemID"]
    
    # Create second menu item for update
    menu_item_data2 = {
        "dishes": f"Test Dish 2 {timestamp}",
        "category": "Dessert",
        "calories": 300,
        "price": 5.99,
        "ingredients": []
    }
    
    menu_item_response2 = client.post("/menu_items/", json=menu_item_data2)
    menu_item_id2 = menu_item_response2.json()["menuItemID"]
    
    # Create initial order
    initial_order_data = {
        "customer_id": customer_id,
        "total_price": 19.99,
        "status": "pending",
        "tracking_number": f"TRK{timestamp}",
        "menu_items": [
            {
                "menu_item_id": menu_item_id1,
                "quantity": 2
            }
        ]
    }
    
    initial_response = client.post("/orders/", json=initial_order_data)
    assert initial_response.status_code == 200
    order_id = initial_response.json()["id"]
    
    # Update the order
    update_data = {
        "total_price": 25.99,
        "status": "processing",
        "tracking_number": f"TRK{timestamp}_updated",
        "menu_items": [
            {
                "menu_item_id": menu_item_id1,
                "quantity": 1
            },
            {
                "menu_item_id": menu_item_id2,
                "quantity": 2
            }
        ]
    }
    
    update_response = client.put(f"/orders/{order_id}", json=update_data)
    assert update_response.status_code == 200
    updated_order = update_response.json()
    
    # Verify the updates - convert both to float for comparison
    assert float(updated_order["total_price"]) == float(update_data["total_price"])
    assert updated_order["status"] == update_data["status"]
    assert updated_order["tracking_number"] == update_data["tracking_number"]
    
    # Verify the updated menu items by getting the order details
    get_response = client.get(f"/orders/{order_id}")
    assert get_response.status_code == 200
    order_details = get_response.json()
    
    # Add any additional menu item validations if your response includes menu items

def test_delete_order(client):
    # Create test data first
    timestamp = int(time.time())
    customer_data = {
        "name": f"Test Customer {timestamp}",
        "email": f"test{timestamp}@example.com",
        "address": "123 Test St",
        "phone_number": f"+1234567890{timestamp}"[:20]  # At least 10 chars, max 20
    }
    
    customer_response = client.post("/customers/", json=customer_data)
    customer_id = customer_response.json()["id"]
    
    menu_item_data = {
        "dishes": f"Test Dish {timestamp}",
        "category": "Main",
        "calories": 500,
        "price": 9.99,
        "ingredients": []
    }
    
    menu_item_response = client.post("/menu_items/", json=menu_item_data)
    menu_item_id = menu_item_response.json()["menuItemID"]
    
    order_data = {
        "customer_id": customer_id,
        "total_price": 19.99,
        "status": "pending",
        "tracking_number": f"TRK{timestamp}",
        "menu_items": [{"menu_item_id": menu_item_id, "quantity": 2}]
    }
    
    create_response = client.post("/orders/", json=order_data)
    order_id = create_response.json()["id"]
    
    # Test deleting the order
    delete_response = client.delete(f"/orders/{order_id}")
    assert delete_response.status_code == 200
    
    # Verify order is deleted
    get_response = client.get(f"/orders/{order_id}")
    assert get_response.status_code == 404

def test_order_with_invalid_menu_item(client):
    timestamp = int(time.time())
    customer_data = {
        "name": f"Test Customer {timestamp}",
        "email": f"test{timestamp}@example.com",
        "address": "123 Test St",
        "phone_number": f"+1234567890{timestamp}"[:20]  # At least 10 chars, max 20
    }
    
    customer_response = client.post("/customers/", json=customer_data)
    customer_id = customer_response.json()["id"]
    
    # Try to create order with non-existent menu item
    order_data = {
        "customer_id": customer_id,
        "total_price": 19.99,
        "status": "pending",
        "tracking_number": f"TRK{timestamp}",
        "menu_items": [{"menu_item_id": 99999, "quantity": 2}]
    }
    
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 404
