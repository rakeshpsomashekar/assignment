from fastapi import FastAPI,APIRouter,Depends
from pydantic import BaseModel
from typing import List,Optional
from schemas import *
import uvicorn




#auth router
auth_router=APIRouter(prefix="/auth")

#user registration API
@auth_router.post("/register/",response_model=UserResponse)
def register(user:User):
    pass    

#User login API
@auth_router.post("/login",response_model=Token)
def login():
    pass


#get curremt user by using given token
@auth_router.get("/user",response_model=UserResponse)
def get_current_user(token:str):
    pass

#API for updating user details
@auth_router.post("/user/update/",response_model=UserResponse)
def update_user_details(user_up:UserUpdate):
    pass





#admin router
admin_router=APIRouter(prefix="/admin")

#API to create new pizza details
@admin_router.post("/pizzas/",response_model=PizzaResponse)
def create_pizza(pizza:Pizza): 
    pass

#API to update pizza details
@admin_router.put("/pizzas/{id}",response_model=PizzaResponse)
def update_pizza(id:int,pizza_update:PizzaUP):
    pass

#API to delete pizza 
@admin_router.delete("/pizzas/{id}",response_model=PizzaResponse)
def delete_pizza(id:int):
    pass

#API to update order status
@admin_router.put("/order-status/{order_id}",response_model=OrderResponse)
def update_order_status(id:int,status:str):
    pass



#customer router
cust_router=APIRouter(prefix="/customer")

@cust_router.get("/pizzas/",response_model=List[PizzaResponse])
def get_pizzas():
    pass

#API to get all available pizzas based on category filter
@cust_router.get("/pizzas/filter",response_model=List[PizzaResponse])
def get_filtered_pizzas(category:str):
    pass

#API to add pizza to cart
@cust_router.post("/cart/",response_model=CartItemResponse)
def add_to_cart(item:CartItem):
    pass

#   API to checkout cart / ordering cart items
@cust_router.post("/checkout/",response_model=OrderResponse)
def checkout_cart(payment_type:str,delivery_address:str,):
    pass

#API to get all my orders history
@cust_router.post("/orders/",response_model=List[OrderResponse])
def get_orders():
    pass

#API to get all cart items
@cust_router.post("/cartitems/",response_model=List[CartItemResponse])
def get_cart_items():
    pass

#API to delete pizza from cart
@cust_router.delete("/cart/{pizza_id}",response_model=CartItemResponse)
def remove_cart_pizza(pizza_id:int):
    pass
#API to clear/remove all items from cart
@cust_router.delete("/cart/",response_model=List[CartItemResponse])
def clear_cart():
    pass

#API to give delivery rating by customer user
@cust_router.post("/delivery_rating/",response_model=RatingResponse)
def delivery_ratings(ratings:Rating):
    pass
    
#API to get payment history for a given order id
@cust_router.post("/payment_details/{orderid}",response_model=PaymentResponse)
def get_payment_details(order_id:int):
    pass



#delivery router
delivery_router=APIRouter(prefix="/delivery")

#API to get all deliveries including completed by delivery user
@delivery_router.get("/deliveries/",response_model=List[DeliveryResponse])
def get_deliveries():
    pass
#API to update status of delivery by delivery user
@delivery_router.put("/deliveries/{delivery_id}/status",response_model=DeliveryResponse)
def update_delivery_status(delivery_id:int,status:DeliveryStatus):
    pass

#API to close/complete delivery by delivery user
@delivery_router.put("/deliveries/{delivery_id}/close",response_model=DeliveryResponse)
def delivery_close(delivery_id:int,delivery_close:DeliveryComment):
    pass

app=FastAPI()
app.include_router(auth_router,tags=["AUTH"])
app.include_router(admin_router,tags=["ADMIN"])
app.include_router(cust_router,tags=["CUST"])
app.include_router(delivery_router,tags=["DELIVERY"])

@app.get('/')
def default():
    return {"message":"welcome to the API placeholder "}

if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.2",port=8080)
