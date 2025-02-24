import pytest
from fastapi.testclient import TestClient
import time

def test_create_ingredient(client):
    timestamp = int(time.time())
    ingredient_data = {
        "Name": f"Test Ingredient {timestamp}",
        "Unit": "grams",
        "Amount": 100
    }
    
    response = client.post("/ingredients/", json=ingredient_data)
    assert response.status_code == 200
    data = response.json()
    assert data["Name"] == ingredient_data["Name"]
    assert data["Unit"] == ingredient_data["Unit"]
    assert "IngredientID" in data

def test_get_ingredients(client):
    response = client.get("/ingredients/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_single_ingredient(client):
    timestamp = int(time.time())
    ingredient_data = {
        "Name": f"Test Ingredient {timestamp}",
        "Unit": "grams",
        "Amount": 100
    }
    
    create_response = client.post("/ingredients/", json=ingredient_data)
    ingredient_id = create_response.json()["IngredientID"]
    
  
    response = client.get(f"/ingredients/{ingredient_id}")
    assert response.status_code == 200
    assert response.json()["IngredientID"] == ingredient_id

def test_update_ingredient(client):
   
    timestamp = int(time.time())
    ingredient_data = {
        "Name": f"Test Ingredient {timestamp}",
        "Unit": "grams",
        "Amount": 100
    }
    
    create_response = client.post("/ingredients/", json=ingredient_data)
    ingredient_id = create_response.json()["IngredientID"]
    
  
    update_data = {
        "Name": f"Updated Ingredient {timestamp}",
        "Amount": 150
    }
    
    response = client.put(f"/ingredients/{ingredient_id}", json=update_data)
    assert response.status_code == 200
    updated_data = response.json()
    assert updated_data["Name"] == update_data["Name"]
    assert updated_data["Amount"] == update_data["Amount"]

def test_delete_ingredient(client):
   
    timestamp = int(time.time())
    ingredient_data = {
        "Name": f"Test Ingredient {timestamp}",
        "Unit": "grams",
        "Amount": 100
    }
    
    create_response = client.post("/ingredients/", json=ingredient_data)
    ingredient_id = create_response.json()["IngredientID"]
    
   
    response = client.delete(f"/ingredients/{ingredient_id}")
    assert response.status_code == 200
    
   
    get_response = client.get(f"/ingredients/{ingredient_id}")
    assert get_response.status_code == 404

def test_create_ingredient_duplicate_name(client):
  
    timestamp = int(time.time())
    ingredient_data = {
        "Name": f"Test Ingredient {timestamp}",
        "Unit": "grams",
        "Amount": 100
    }
    
  
    first_response = client.post("/ingredients/", json=ingredient_data)
    assert first_response.status_code == 200
    
   
    second_response = client.post("/ingredients/", json=ingredient_data)
    assert second_response.status_code == 400
