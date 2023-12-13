from database import Base
from sqlalchemy import Column, Integer, Boolean, Text, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

class User(Base):
    __tablename__ = "user"
    id = Column(Integer,primary_key = True)
    username = Column(String(25), unique = True, )
    email = Column(String(90),unique = True)
    password = Column(Text)
    is_staff = Column(Boolean, default = False)
    is_active = Column(Boolean, default = False)
    orders = relationship('Order',back_populates="user")


    def __repr__(self):
        return {"User":self.username}
    
class Order(Base):
    __tablename__ = 'orders'

    ORDER_STATUSES = (
        ("PENDING","pending"),
        ("IN-TRANSIT","in-transit"),
        ("DELIVERED","delivered")
    )


    PIZZA_SIZED = (
        ('SMALL','small'),
        ('MEDIUM','medium'),
        ('LARGE','large'),
        ('EXTRA-LARGE','extra-large')
    )

    id = Column(Integer,primary_key=True)
    quantity = Column(Integer, nullable=False)
    order_status = Column(ChoiceType(choices=ORDER_STATUSES),default="PENDING")
    pizza_size = Column(ChoiceType(PIZZA_SIZED),default="SMALL")
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship('User',back_populates="orders")


    def __repr__(self):
        return f"<Order {self.pizza_size}{self.quantity}"
    

