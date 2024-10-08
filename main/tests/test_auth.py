from datetime import datetime,timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session,sessionmaker
from sqlalchemy import create_engine

from .. import models,schemas
from ..database import get_db,Base
from ..app import app
from main.routers.auth import create_access_token

testengine=create_engine("sqlite:///./test.db",connect_args={"check_same_thread":False})
TestingSessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=testengine)

def test_get_db():
    try:
        db=TestingSessionLocal()
        yield db
    finally:
        db.close()

if not hasattr(app,"dependency_overrides"):
    app.dependency_overrides={}

#creating database for testing purpose
app.dependency_overrides[get_db]=test_get_db

@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=testengine)
    yield TestClient(app)

#testing user registration
def test_register_user(client):
    response=client.post("/auth/register",json={
        "name":"delivery2",
        "mobile":9898989898,
        "address": "vtp",
        "email": "delivery2@gmail.com",
        "password": "delivery2",
        "role": "delivery_partner","is_available":True
    })
    assert response.status_code == 200
    data=response.json()
    assert data["email"] == "delivery2@gmail.com"
    assert data["name"] == "delivery2"

#testing user login
def test_login_user(client):
    
    response=client.post('/auth/login',data={
        "username":"delivery2@gmail.com","password":"delivery2"
    })

    assert response.status_code == 200
    data=response.json()
    assert "access_token" in data and "token_type" in data
    assert data["token_type"]=="Bearer"

#testing invalid login 
def test_negative_login_user(client):
    
    response=client.post('/auth/login',data={
        "username":"tester@gmail.com","password":"password"
    })

    assert response.status_code == 401
    data=response.json()
    assert data["detail"]=="incorrect credentials"


#testing current user
def test_get_current_user(client):

    log_response=client.post('/auth/login',data={
        "username":"delivery2@gmail.com","password":"delivery2"
    })
    assert log_response.status_code == 200
    token=log_response.json()['access_token']
    
    response=client.get('/auth/user',headers={"Authorization":f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"]=="delivery2@gmail.com"

