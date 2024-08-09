from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from typing import List
from .auth import get_current_user
from ..database import get_db
from .. import schemas,models
router=APIRouter()

#API to create new pizza details
@router.post("/pizzas/",response_model=schemas.PizzaResponse)
def create_pizza(pizza:schemas.Pizza,db:Session=Depends(get_db),current_user:schemas.User=Depends(get_current_user)): 
    if current_user.role!="admin":
        raise HTTPException(status_code=403,detail="not enough permissions")
    new_pizza=models.Pizza(**pizza.dict())
    db.add(new_pizza)
    db.commit()
    db.refresh(new_pizza)
    return new_pizza

#API to update pizza details
@router.put("/pizzas/{id}",response_model=schemas.PizzaResponse)
def update_pizza(id:int,pizza_update:schemas.PizzaUP,db:Session=Depends(get_db),current_user:schemas.User=Depends(get_current_user)):
    if current_user.role!="admin":
        raise HTTPException(status_code=403,detail="not enough permissions")
    pizza=db.query(models.Pizza).filter(models.Pizza.id==id).first()

    if not pizza:
        raise HTTPException(status_code=404,detail="pizza not found")

    pizza.name=pizza_update.name if pizza_update.name else pizza.name
    pizza.price=pizza_update.price if pizza_update.price else pizza.price
    pizza.description=pizza_update.description if pizza_update.description else  pizza.description
    pizza.category=pizza_update.category if pizza_update.category else pizza.category
    pizza.availability=pizza_update.availability if pizza_update.availability else pizza.availability
    db.commit()
    db.refresh(pizza)
    return pizza


#API to delete pizza 
@router.delete("/pizzas/{id}",response_model=schemas.PizzaResponse)
def delete_pizza(id:int,db:Session=Depends(get_db),current_user:schemas.User=Depends(get_current_user)):
    if current_user.role!="admin":
        raise HTTPException(status_code=403,detail="not enough permissions")
    pizza=db.query(models.Pizza).filter(models.Pizza.id==id).first()
    if not pizza:
        raise HTTPException(status_code=404,detail="pizza not found")
    if pizza:
        db.delete(pizza)
        db.commit()
        return pizza
    return None

#API to update order status
@router.put("/order-status/{order_id}",response_model=schemas.OrderResponse)
def update_order_status(id:int,status:str,db:Session=Depends(get_db),current_user:schemas.User=Depends(get_current_user)):
    if current_user.role !="admin":
        raise HTTPException(status_code=403,detail="not enough permissions")
    
    order=db.query(models.Order).filter(models.Order.id==id).first()
    if not order:
        raise HTTPException(status_code=404,detail="order not found")
    
    order.status=status
    db.commit()
    db.refresh(order)

    order_items=db.query(models.OrderItem).filter(models.OrderItem.order_id==order.id).all()

    return schemas.OrderResponse(
        id=order.id,customer_id=order.customer_id,delivery_address=order.delivery_address,delivery_partner_id=order.delivery_partner_id,status=order.status,items=[schemas.OrderItemResponse(
            id=item.id,
            order_id=item.order_id,
            pizza_id=item.pizza_id,
            quantity=item.quantity,
            price=item.price)for item in order_items],
            total_price=sum(item.price for item in order_items)
    )

