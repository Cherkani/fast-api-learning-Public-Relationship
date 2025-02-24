import pytest
from fastapi.testclient import TestClient
import time

def test_create_menu_item(client):
    timestamp = int(time.time())
    menu_item_data = {
        "dishes": f"Test Dish {timestamp}",
        "category": "Main",
        "calories": 500,
        "price": 9.99,
        "ingredients": []
    }
    
    response = client.post("/menu_items/", json=menu_item_data)
    assert response.status_code == 200
    data = response.json()
    assert data["dishes"] == menu_item_data["dishes"]
    assert "menuItemID" in data

def test_get_menu_items(client):
    response = client.get("/menu_items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_single_menu_item(client):
   
    timestamp = int(time.time())
    menu_item_data = {
        "dishes": f"Test Dish {timestamp}",
        "category": "Main",
        "calories": 500,
        "price": 9.99,
        "ingredients": []
    }
    
    create_response = client.post("/menu_items/", json=menu_item_data)
    menu_item_id = create_response.json()["menuItemID"]
    
   
    response = client.get(f"/menu_items/{menu_item_id}")
    assert response.status_code == 200
    assert response.json()["menuItemID"] == menu_item_id

def test_update_menu_item(client):
   
    timestamp = int(time.time())
    menu_item_data = {
        "dishes": f"Test Dish {timestamp}",
        "category": "Main",
        "calories": 500,
        "price": 9.99,
        "ingredients": []
    }
    
    create_response = client.post("/menu_items/", json=menu_item_data)
    menu_item_id = create_response.json()["menuItemID"]
    
   
    update_data = {
        "dishes": f"Updated Dish {timestamp}",
        "price": 14.99
    }
    
    response = client.put(f"/menu_items/{menu_item_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["dishes"] == update_data["dishes"]

def test_delete_menu_item(client):
  
    timestamp = int(time.time())
    menu_item_data = {
        "dishes": f"Test Dish {timestamp}",
        "category": "Main",
        "calories": 500,
        "price": 9.99,
        "ingredients": []
    }
    
    create_response = client.post("/menu_items/", json=menu_item_data)
    menu_item_id = create_response.json()["menuItemID"]
    
 
    response = client.delete(f"/menu_items/{menu_item_id}")
    assert response.status_code == 200
