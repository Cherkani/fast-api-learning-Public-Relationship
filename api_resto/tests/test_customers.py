import pytest
from fastapi.testclient import TestClient
import time
import json

def generate_valid_phone(timestamp):
    
    return f"+1{timestamp % 1000000000:09d}"

def test_create_customer(client):
    timestamp = int(time.time())
    customer_data = {
        "name": f"Test Customer {timestamp}",
        "email": f"test{timestamp}@oracle.com",
        "address": "123 Test St",
        "phone_number": generate_valid_phone(timestamp)
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
    timestamp = int(time.time())
    customer_data = {
        "name": f"Test Customer {timestamp}",
        "email": f"test{timestamp}@oracle.com",
        "address": "123 Test St",
        "phone_number": generate_valid_phone(timestamp)
    }
    
    create_response = client.post("/customers/", json=customer_data)
    assert create_response.status_code == 200
    customer_id = create_response.json()["id"]
    
    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 200
    assert response.json()["id"] == customer_id

def test_update_customer(client):
    timestamp = int(time.time())
    customer_data = {
        "name": f"Test Customer {timestamp}",
        "email": f"test{timestamp}@oracle.com",
        "address": "123 Test St",
        "phone_number": generate_valid_phone(timestamp)
    }
    
    create_response = client.post("/customers/", json=customer_data)
    assert create_response.status_code == 200
    customer_id = create_response.json()["id"]
    
    update_data = {
        "name": f"Updated Customer {timestamp}",
        "address": "456 Update St"
    }
    
    response = client.put(f"/customers/{customer_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == update_data["name"]

def test_delete_customer(client):
    timestamp = int(time.time())
    customer_data = {
        "name": f"Test Customer {timestamp}",
        "email": f"test{timestamp}@oracle.com",
        "address": "123 Test St",
        "phone_number": generate_valid_phone(timestamp)
    }
    
    create_response = client.post("/customers/", json=customer_data)
    customer_id = create_response.json()["id"]
    
    response = client.delete(f"/customers/{customer_id}")
    assert response.status_code == 204






# worse case senarios  
def test_invalid_email_format(client):
    customer_data = {
        "name": "Test Customer",
        "email": "invalid.email@gmail.com",  # Non-oracle email
        "address": "123 Test St",
        "phone_number": "+1234567890"
    }
    response = client.post("/customers/", json=customer_data)
    
    print('\n')
    print('=' * 50)
    print('TEST INVALID EMAIL RESPONSE')
    print('=' * 50)
    print('Status Code:', response.status_code)
    print('-' * 50)
    print('Response JSON:')
    print(json.dumps(response.json(), indent=2))
    print('=' * 50)
    print('\n')

    assert response.status_code == 422
    assert "oracle email" in response.json()["detail"][0]["msg"].lower()

def test_invalid_email_not_email_format(client):
    customer_data = {
        "name": "Test Customer",
        "email": "notevenanemailformat",  # Invalid email format without @
        "address": "123 Test St",
        "phone_number": "+1234567890"
    }
    response = client.post("/customers/", json=customer_data)
    
    print('\n')
    print('=' * 50)
    print('TEST INVALID EMAIL FORMAT RESPONSE')
    print('=' * 50)
    print('Status Code:', response.status_code)
    print('-' * 50)
    print('Response JSON:')
    print(json.dumps(response.json(), indent=2))
    print('=' * 50)
    print('\n')

    assert response.status_code == 422
    assert "email" in response.json()["detail"][0]["msg"].lower()

def test_invalid_phone_formats(client):
    invalid_phones = [
        "1234567890",      # Missing +
        "+123",            # Too short
        "+abcdefghijk",    # Non-numeric
        "+123456789012345678"  # Too long
    ]
    
    for phone in invalid_phones:
        customer_data = {
            "name": "Test Customer",
            "email": "test@oracle.com",
            "address": "123 Test St",
            "phone_number": phone
        }
        response = client.post("/customers/", json=customer_data)
        assert response.status_code == 422
        assert "phone number" in response.json()["detail"][0]["msg"].lower()
        


def test_duplicate_customer_email(client):
    # first customer
    customer_data = {
        "name": "Test Customer",
        "email": "test.duplicate@oracle.com",
        "address": "123 Test St",
        "phone_number": "+1234567890"
    }
    response1 = client.post("/customers/", json=customer_data)
    assert response1.status_code == 200

    # second customer with same email
    response2 = client.post("/customers/", json=customer_data)
    
    print('\n')
    print('=' * 50)
    print('TEST DUPLICATE CUSTOMER EMAIL RESPONSE')
    print('=' * 50)
    print('Status Code:', response2.status_code)
    print('-' * 50)
    print('Response JSON:')
    print(json.dumps(response2.json(), indent=2))
    print('=' * 50)
    print('\n')
    
    assert response2.status_code == 400
    error_detail = response2.json()["detail"].lower()
    assert any(phrase in error_detail for phrase in ["duplicate", "already exists"])

def test_invalid_name_with_special_chars(client):
    customer_data = {
        "name": "Test@Customer#123",
        "email": "test@oracle.com",
        "address": "123 Test St",
        "phone_number": "+1234567890"
    }
    response = client.post("/customers/", json=customer_data)
    assert response.status_code == 422
    assert "special characters" in response.json()["detail"][0]["msg"].lower()


def test_empty_fields(client):
    customer_data = {
        "name": "",
        "email": "test@oracle.com",
        "address": "",
        "phone_number": "+1234567890"
    }
    response = client.post("/customers/", json=customer_data)
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any("cannot be empty" in err["msg"].lower() for err in errors)

def test_missing_fields(client):
    customer_data = {
        "name": "Test Customer",
        "email": "test@oracle.com"
        # missing address and phone_number
    }
    response = client.post("/customers/", json=customer_data)
    assert response.status_code == 422
