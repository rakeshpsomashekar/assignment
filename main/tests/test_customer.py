from datetime import datetime,timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session,sessionmaker
from sqlalchemy import create_engine


from .. import models,schemas
from ..database import get_db,Base
from ..app import app
from ..routers.auth import get_current_user
from .test_auth import testengine,test_get_db
from main.routers.auth import create_access_token

if not hasattr(app,"dependency_overrides"):
    app.dependency_overrides={}

#creating current user for customer page
def new_current_user():
    return schemas.User(id=1,name="testcustomer",email="testcustomer@gmail.com",role="customer",mobile=9898,address="vtp",password="testcostomer",is_available=True)

app.dependency_overrides[get_db]=test_get_db
app.dependency_overrides[get_current_user]=new_current_user

#creating client for requesting to APIs
@pytest.fixture(scope="module")
def client():
    yield TestClient(app)


#testing get pizzas feature
def test_get_pizzas(client):
    response=client.get("/customer/pizzas/")
    assert response.status_code==200
    assert response.json()[0]["name"]=="paneer"
    
#testing filtered pizzas
def test_filter_pizzas(client):
    response=client.get("/customer/pizzas/",params={"category":"small"})
    assert response.status_code==200
    
#testing add to cart feature
def test_add_to_cart(client):
    response=client.post("/customer/cart",json={
  "pizza_id": 1,
  "quantity": 2 })
    assert response.status_code==200
    assert response.json()["pizza_id"]==1
    assert response.json()["quantity"]==2

#testing checkout/order feature
def test_checkout_cart(client):
    response=client.post("/customer/checkout/",params={"payment_type":"credit_card","delivery_address":"banglore"})
    assert response.status_code==200

#testing get all orders feature
def test_get_orders(client):
    response=client.post("/customer/orders/")
    assert response.status_code==200
   

#testing get cart items feature
def test_get_cart_items(client):
    response=client.post("/customer/cartitems/")
    assert response.status_code==200


#testing remove cart pizza
def test_remove_cart_pizza(client):
    response=client.delete("customer/cart/1")
    assert response.status_code==200

#testing creat all cart items feature
def test_clear_cart(client):
    response=client.delete("customer/cart/")
    assert response.status_code==200

#testing delivery rating feature
def test_delivery_rating(client):
    response=client.post("customer/delivery_rating/",json={
  "order_id": 1,
  "order_rating": 5,
  "order_comment": "delicious",
  "delivery_partner_rating": 5

})
    assert response.status_code==200

#testing payment details feature
def test_payment_details(client):
    response=client.post("customer/payment_details/1")
    assert response.status_code==200
