from fastapi import APIRouter, Depends, HTTPException, status
from schemas import OrderModel, OrderStatus
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from models import Order, User
from authorize import authorize_user
from database import Session,engine


session = Session(bind =engine)

order_router = APIRouter(
    prefix = "/orders",
    tags = ["Orders"]
)


@order_router.get("/")
async def hello(dependencies = Depends(authorize_user)):    
    return {"message": "hello world"}

@order_router.post("/placeOrder", status_code = status.HTTP_201_CREATED)
async def place_order(order:OrderModel,Authorize:AuthJWT = Depends(authorize_user)):
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    new_order = Order(
        pizza_size=order.pizza_size,
        quantity = order.quantity
    )

    new_order.user = user
    session.add(new_order)
    session.commit()

    response = {
        "pizza_size": new_order.pizza_size,
        "quantity": new_order.quantity,
        "Order_Status": new_order.order_status,
        "id":new_order.id
    }
    return jsonable_encoder({"New_Order":response})

@order_router.get("/Orders")
async def list_all_orders(Authorize:AuthJWT=Depends(authorize_user)):
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff == True:
        order = session.query(Order).all()
        return jsonable_encoder(order)
    else :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "You are not a superuse")


@order_router.get("/order/{order_id}")
async def get_by_order_id(order_id : int ,Authorize:AuthJWT=Depends(authorize_user)):
    user = Authorize.get_jwt_subject()

    current_user = session.query(User).filter(User.username == user).first()

    if current_user.is_staff:
        order = session.query(Order).filter(Order.id == order_id).first()
        return jsonable_encoder({f"Order of id {order_id}":order})
    else : 
        return {f"Order of id{order_id} does not exist!!"}
    
@order_router.get("/user_order")
async def get_user_order(username : str ,Authorize:AuthJWT=Depends(authorize_user)):
    user = Authorize.get_jwt_subject()

    current_user = session.query(User).filter(User.username == user).first()

    if current_user.is_staff:
        return jsonable_encoder(current_user.orders)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "You are not a superuser")
    
@order_router.put("/update_order/{order_id}")
async def update_order(order_id : int, order:OrderModel, Authorize:AuthJWT=Depends(authorize_user)):
    """
    #Response Body
            id:order_update.id,
            quantity:order_update.quantity,
            pizza_size:order_update.pizza_size,
            order_status:order_update.order_status,
    """
    order_update = session.query(Order).filter(Order.id == order_id).first()

    order_update.quantity = order.quantity
    order_update.pizza_size = order.pizza_size

    session.commit()

    response={
            "id":order_update.id,
            "quantity":order_update.quantity,
            "pizza_size":order_update.pizza_size,
            "order_status":order_update.order_status,
        }
    
    return jsonable_encoder({"order_update":response})

@order_router.patch("/update_order_status")
async def update_order_status(order:OrderStatus, Authorize:AuthJWT=Depends(authorize_user)):
    user = Authorize.get_jwt_subject()

    current_user = session.query(User).filter(User.username == user).first()

    if current_user.is_staff:
        order_update = session.query(Order).filter(Order.id == order.id).first()
        order_update.order_status = order.order_status
    
    session.commit()
    return jsonable_encoder({"Order Status":order_update.order_status})

@order_router.delete("/delete_order/{order_id}")
async def delete_order(order_id : int, Authorize:AuthJWT=Depends(authorize_user)):
    order = session.query(Order).filter(Order.id == order_id).first()
    session.delete(order)
    session.commit()
    return jsonable_encoder({f"Order deleted of id {order_id}"})


    
        

        

    
