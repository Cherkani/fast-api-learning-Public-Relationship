from fastapi.testclient import TestClient
from api_resto.main import app
import time

client = TestClient(app)

def test_create_customer():

    timestamp = int(time.time())
    payload = {
        "name": "Aymen Cherkani",
        "email": f"cherkani{timestamp}@example.com",
        "address": "address test",
        "phone_number": f"333-{timestamp}"  
    }

    # POST
    response = client.post("/customers/", json=payload)
    if response.status_code != 200:
        print(f"Response body: {response.text}")  
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert "id" in data

    #  GET 
    customer_id = data["id"]
    get_response = client.get(f"/customers/{customer_id}")
    assert get_response.status_code == 200
    retrieved_data = get_response.json()
    assert retrieved_data["name"] == payload["name"]