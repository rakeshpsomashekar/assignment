from fastapi import FastAPI

from .database import engine,Base
from .routers import auth,admin,customer,delivery

app=FastAPI()

Base.metadata.create_all(engine)

app.include_router(auth.router,prefix='/auth',tags=['AUTHENTICATION APIs'])
app.include_router(admin.router,prefix='/admin',tags=['ADMIN APIs'])
app.include_router(customer.router,prefix='/customer',tags=['CUSTOMER APIs'])
app.include_router(delivery.router,prefix='/delivery',tags=['DELIVERY_PARTNER APIs'])


@app.get('/')
def read_root():
    return {"message":"welcome to the pizza delivery API"}
