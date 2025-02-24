import pytest
from fastapi.testclient import TestClient
import time

def test_create_customer(client):
    timestamp = int(time.time())
    customer_data = {
        "name": f"Test Customer {timestamp}",
        "email": f"test{timestamp}@example.com",
        "address": "123 Test St",
        "phone_number": f"+1234567{timestamp}"
    }
    
    response = client.post("/customers/", json=customer_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == customer_data["name"]
    assert data["email"] == customer_data["email"]
    assert "id" in data

def test_get_customers(client):
    response = client.get("/customers/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_single_customer(client):
    # First create a customer
    timestamp = int(time.time())
    customer_data = {
        "name": f"Test Customer {timestamp}",
        "email": f"test{timestamp}@example.com",
        "address": "123 Test St",
        "phone_number": f"+1234567{timestamp}"
    }
    
    create_response = client.post("/customers/", json=customer_data)
    customer_id = create_response.json()["id"]
    
    # Then get the customer
    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 200
    assert response.json()["id"] == customer_id

def test_update_customer(client):
    # First create a customer
    timestamp = int(time.time())
    customer_data = {
        "name": f"Test Customer {timestamp}",
        "email": f"test{timestamp}@example.com",
        "address": "123 Test St",
        "phone_number": f"+1234567{timestamp}"
    }
    
    create_response = client.post("/customers/", json=customer_data)
    customer_id = create_response.json()["id"]
    
    # Update the customer
    update_data = {
        "name": f"Updated Customer {timestamp}",
        "address": "456 Update St"
    }
    
    response = client.put(f"/customers/{customer_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == update_data["name"]

def test_delete_customer(client):
    # First create a customer
    timestamp = int(time.time())
    customer_data = {
        "name": f"Test Customer {timestamp}",
        "email": f"test{timestamp}@example.com",
        "address": "123 Test St",
        "phone_number": f"+1234567{timestamp}"
    }
    
    create_response = client.post("/customers/", json=customer_data)
    customer_id = create_response.json()["id"]
    
    # Delete the customer
    response = client.delete(f"/customers/{customer_id}")
    assert response.status_code == 204
