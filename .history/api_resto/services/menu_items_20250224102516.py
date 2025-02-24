from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models.menu_items import MenuItem, MenuItemIngredient
from ..models.ingredients import Ingredient  # Updated import
from sqlalchemy.exc import SQLAlchemyError

def create(db: Session, request):
    # Create the menu item
    new_menu_item = MenuItem(
        dishes=request.dishes,
        category=request.category,
        calories=request.calories,
        price=request.price
    )
    
    try:
        db.add(new_menu_item)
        db.flush()  # Flush to get the menu_item_id
        
        # Create ingredient associations
        for ingredient in request.ingredients:
            ingredient_record = db.query(Ingredient).filter(Ingredient.IngredientID == ingredient.ingredient_id).first()
            if not ingredient_record:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Ingredient with id {ingredient.ingredient_id} not found"
                )
            
          
            menu_item_ingredient = MenuItemIngredient(
                menu_item_id=new_menu_item.menuItemID,
                ingredient_id=ingredient.ingredient_id,
                quantity=ingredient.quantity
            )
            db.add(menu_item_ingredient)
        
        db.commit()
        db.refresh(new_menu_item)
        return new_menu_item
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

def read_all(db: Session):
    return db.query(MenuItem).all()

def read_one(db: Session, menu_item_id: int):
    menu_item = db.query(MenuItem).filter(MenuItem.menuItemID == menu_item_id).first() 
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return menu_item

def update(db: Session, menu_item_id: int, request):
    try:
     
        menu_item = db.query(MenuItem).filter(MenuItem.menuItemID == menu_item_id).first()
        if not menu_item:
            raise HTTPException(status_code=404, detail="Menu item not found")

      
        for key, value in request.dict(exclude={'ingredients'}, exclude_unset=True).items():
            setattr(menu_item, key, value)

        if hasattr(request, 'ingredients') and request.ingredients is not None:
          
            db.query(MenuItemIngredient).filter(
                MenuItemIngredient.menu_item_id == menu_item_id
            ).delete()

        
            for ingredient in request.ingredients:
              
                ingredient_record = db.query(Ingredient).filter(
                    Ingredient.IngredientID == ingredient.ingredient_id
                ).first()
                if not ingredient_record:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Ingredient with id {ingredient.ingredient_id} not found"
                    )
                
               
                menu_item_ingredient = MenuItemIngredient(
                    menu_item_id=menu_item_id,
                    ingredient_id=ingredient.ingredient_id,
                    quantity=ingredient.quantity
                )
                db.add(menu_item_ingredient)

        db.commit()
        db.refresh(menu_item)
        return menu_item

    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

def delete(db: Session, menu_item_id: int):
    try:
       
        db.query(MenuItemIngredient).filter(
            MenuItemIngredient.menu_item_id == menu_item_id
        ).delete(synchronize_session=False)

      
        menu_item = db.query(MenuItem).filter(MenuItem.menuItemID == menu_item_id)
        if not menu_item.first():
            raise HTTPException(status_code=404, detail="Menu item not found")
            
        menu_item.delete(synchronize_session=False)
        db.commit()
        return {"message": "Menu item deleted successfully"}
        
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
