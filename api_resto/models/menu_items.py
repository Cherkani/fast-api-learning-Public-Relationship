from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    menuItemID = Column(Integer, primary_key=True, autoincrement=True)
    dishes = Column(String(100), nullable=False ) 
    category = Column(String(50), nullable=False )
    calories = Column(Integer, nullable=False, default=0) 
    price = Column(Float, nullable=False)  

    ingredients = relationship("MenuItemIngredient", back_populates="menu_item") 
    order_items = relationship("OrderMenuItem", back_populates="menu_item")
   

class MenuItemIngredient(Base):
    __tablename__ = "menu_item_ingredients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.menuItemID"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.IngredientID"), nullable=False)
    quantity = Column(Float, nullable=False) 


    menu_item = relationship("MenuItem", back_populates="ingredients")  
    ingredient = relationship("Ingredient", back_populates="menu_items")

