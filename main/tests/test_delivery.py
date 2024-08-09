from datetime import datetime,timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session,sessionmaker

from .. import models,schemas
from ..database import get_db,Base
from ..app import app
from ..routers.auth import get_current_user
from .test_auth import test_get_db
from main.routers.auth import create_access_token

if not hasattr(app,"dependency_overrides"):
    app.dependency_overrides={}

#creating current user for delivery feature
def new_current_user():
    return schemas.User(id=1,name="delivery",email="delivery@gmail.com",role="delivery_partner",mobile=9898,address="vtp",password="delivery",is_available=True)

app.dependency_overrides[get_db]=test_get_db
app.dependency_overrides[get_current_user]=new_current_user

#creating client for requesting to APIs
@pytest.fixture(scope="module")
def client():
    yield TestClient(app)

#testing delivery status update
def test_delivery_status_update(client):
    response=client.put("/delivery/deliveries/1/status",json={"status": "on_vehicle"})
    assert response.status_code==200

#testing delivery status close
def test_delivery_close(client):
    response=client.put("/delivery/deliveries/1/close",json={"status": "on_vehicle","comment":"super delivery"})
    assert response.status_code==200

