from sqlalchemy import Column,Integer,String,Boolean,ForeignKey,DateTime,Float,Numeric
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

#User table having relationship with order,cartitems,rating,delivery tables
class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    mobile=Column(Integer)
    address=Column(String)
    email=Column(String)
    password=Column(String)
    role=Column(String)
    is_available=Column(Boolean,default=True)

    orders=relationship("Order",back_populates="delivery_partner",foreign_keys="[Order.delivery_partner_id]")
    order=relationship("Order",back_populates="customer",foreign_keys="[Order.customer_id]")
    cart_items=relationship("CartItem",back_populates="user",uselist=False)
    ratings=relationship("Rating",back_populates="user")
    delivery=relationship("Delivery",back_populates="delivery_partner")

#Pizza table having relationship with orderitems,cartitem tables
class Pizza(Base):
    __tablename__='pizzas'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    description=Column(String)
    category=Column(String)
    price=Column(Integer)
    availability=Column(Boolean,default=True)
    
   
    order_items=relationship('OrderItem',back_populates="pizza")
    cart_items=relationship('CartItem',back_populates="pizza")

#Order table having relationship with user,payment,orderditems,deliveryrating tables
class Order(Base):
    __tablename__='orders'
    id=Column(Integer,primary_key=True,index=True)
    customer_id=Column(Integer,ForeignKey("users.id"))
    status=Column(String)
    ordered_time=Column(DateTime,default=datetime.utcnow)
    delivery_partner_id=Column(Integer,ForeignKey("users.id"))
    delivery_address=Column(String)

    delivery_partner=relationship("User",back_populates="orders",foreign_keys=[delivery_partner_id])
    customer=relationship("User",back_populates="order",foreign_keys=[customer_id])
    payment=relationship("Payment",back_populates="order")
    ordered_items=relationship("OrderItem",back_populates="order")
    delivery=relationship("Delivery",back_populates="order")
    ratings=relationship('Rating',back_populates='order')

#payment table having relationship with order table
class Payment(Base):
    __tablename__='payments'
    id=Column(Integer,primary_key=True,index=True)
    order_id=Column(Integer,ForeignKey("orders.id"),unique=True)
    payment_type=Column(String)
    
    payment_date=Column(DateTime,default=datetime.utcnow)
    price=Column(Integer)
    order=relationship("Order",back_populates='payment')

#Orderitem table having relationship with order,pizza table
class OrderItem(Base):
    __tablename__='order_items'
    id=Column(Integer,primary_key=True,index=True)
    order_id=Column(Integer,ForeignKey("orders.id"))
    pizza_id=Column(Integer,ForeignKey("pizzas.id"))
    quantity=Column(String)
    price=Column(Integer)
    

    order=relationship("Order",back_populates='ordered_items')
    pizza=relationship("Pizza",back_populates='order_items')

#Cartitems table having relationship with user,pizza table
class CartItem(Base):
    __tablename__='cart_items'
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"))

    pizza_id=Column(Integer,ForeignKey("pizzas.id"))
    quantity=Column(Integer)
    price=Column(Integer)

    user=relationship("User",back_populates='cart_items')
    pizza=relationship("Pizza",back_populates='cart_items')

#Delivery table having relationship with order,user tables
class Delivery(Base):
    __tablename__='deliveries'
    id=Column(Integer,primary_key=True,index=True)
    order_id=Column(Integer,ForeignKey("orders.id"),unique=True)
    delivery_partner_id=Column(Integer,ForeignKey("users.id"))
    start_time=Column(DateTime,default=datetime.utcnow)
    end_time=Column(DateTime)
    status=Column(String,default="pending")
    comment=Column(String)

    order=relationship("Order",back_populates="delivery",foreign_keys=[order_id])
    delivery_partner=relationship("User",back_populates="delivery",foreign_keys=[delivery_partner_id])

#Rating table having relationship with user,order tables
class Rating(Base):
    __tablename__='ratings'
    id=Column(Integer,primary_key=True,index=True)
    order_id=Column(Integer,ForeignKey("orders.id"))
    user_id=Column(Integer,ForeignKey("users.id"))
    order_rating=Column(Integer)
    order_comment=Column(String)
    delivery_partner_rating=Column(Integer)

    user=relationship("User",back_populates='ratings')
    order=relationship("Order",back_populates='ratings')
