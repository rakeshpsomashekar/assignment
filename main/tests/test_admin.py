from datetime import datetime,timedelta

import pytest
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import Session,sessionmaker

from .. import models,schemas
from ..database import get_db,Base
from ..app import app
from ..routers.auth import get_current_user
from main.routers.auth import create_access_token
from .test_auth import TestingSessionLocal,testengine,test_get_db

if not hasattr(app,"dependency_overrides"):
    app.dependency_overrides={}

#creating current user for testing 
def new_current_user():
    return schemas.User(id=1,name="tester",email="tester@gmail.com",role="admin",mobile=9898,address="vtp",password="tester",is_available=True)

app.dependency_overrides[get_db]=test_get_db
app.dependency_overrides[get_current_user]=new_current_user

#creating client setup for sending requests
@pytest.fixture(scope="module")
def client():
    yield TestClient(app)

#testing create new pizza feature for availability only from admin user
def test_create_pizza(client):
    response=client.post("/admin/pizzas/",json={
  "name": "onion",
  "description": "oni0n spicy",
  "category": "small",
  "price": 50,
  "availability": True
})
    assert response.status_code == 200
    data=response.json()
    assert data["name"] == "onion"
    assert data["price"] == 50

#testing update pizza feature from only admin user
def test_update_pizza(client):
    response=client.put("/admin/pizzas/1",json={"name": "paneer"})
    assert response.status_code == 200
    data=response.json()
    assert data["name"] == "paneer"

#testing delete pizza feature from only admin user
def test_delete_pizza(client):
    response=client.delete("/admin/pizzas/1")
    assert response.status_code == 200

