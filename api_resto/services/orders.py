from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import orders as model
from ..models.orders import Order , OrderMenuItem
from ..models.menu_items import MenuItem
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

def create(db: Session, request):
    new_item_order = model.Order(
        customer_id=request.customer_id, 
        total_price=request.total_price,
        status=request.status,
        tracking_number=request.tracking_number
    )
    try:
        db.add(new_item_order)
        db.flush()  
        for menu_item in request.menu_items:
            menu_item_record = db.query(MenuItem).filter(MenuItem.menuItemID == menu_item.menu_item_id).first()
            if not menu_item_record:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Ingredient with id {menu_item.menu_item_id} not found"
                )
            
          
            menu_item_ingredient = OrderMenuItem(
                order_id=new_item_order.id,
                menu_item_id=menu_item.menu_item_id,
                quantity=menu_item.quantity
            )
            db.add(menu_item_ingredient)
        db.commit()
        db.refresh(new_item_order)
        return new_item_order
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    


def read_all(db: Session):
    try:
        result = db.query(Order).all()
        return result
    except SQLAlchemyError as e:
        error_message = str(e)
        if hasattr(e, 'orig') and e.orig:
            error_message = str(e.orig)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database error: {error_message}"
        )


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id: int, request): 
    try:
        order_item = db.query(model.Order).filter(model.Order.id == item_id)  
        if not order_item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        
      
        order_item.update(request.model_dump(exclude={'menu_items'}, exclude_unset=True))

        if hasattr(request, 'menu_items') and request.menu_items is not None:
          
            db.query(OrderMenuItem).filter(
                OrderMenuItem.order_id == item_id \
            ).delete()
            
           
            for menu_item in request.menu_items:
                menu_item_record = db.query(MenuItem).filter(
                    MenuItem.menuItemID == menu_item.menu_item_id
                ).first()
                if not menu_item_record:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"menu_items with id {menu_item.menu_item_id} not found"
                    )            
                order_menu_item = OrderMenuItem(
                    order_id=item_id, 
                    menu_item_id=menu_item.menu_item_id,
                    quantity=menu_item.quantity
                )
                db.add(order_menu_item)
                
        db.commit()
        return order_item.first() 
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

def delete(db: Session, item_id: int):
    try:
        db.query(OrderMenuItem).filter(
            OrderMenuItem.order_id == item_id
        ).delete(synchronize_session=False)    
        order_item = db.query(Order).filter(Order.id == item_id)
        if not order_item.first():
            raise HTTPException(status_code=404, detail="Order not found")
            
        order_item.delete(synchronize_session=False)
        db.commit()
        return {"message": "Menu item deleted successfully"}

    except SQLAlchemyError as e:
        error_message = str(e)
        if hasattr(e, 'orig') and e.orig:
            error_message = str(e.orig)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database error: {error_message}"
        )
