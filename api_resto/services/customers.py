from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from ..models.customers import Customer
from ..schemas.customers import CustomerCreate, CustomerUpdate

def create(db: Session, request: CustomerCreate):
    try:
        new_item = Customer(
            name=request.name.strip(),
            email=request.email.lower(),
            address=request.address.strip(),
            phone_number=request.phone_number.strip()
        )
        
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        
        return new_item
        
    except IntegrityError as e:
        db.rollback()
        error_msg = str(e).lower()        
        print('****************************************')        
        print('\n')
        print(error_msg)
        print('****************************************')
        print('\n')
        if "unique constraint" in error_msg:
            if "email" in error_msg:
                detail = "Email already exists"
            elif "phone_number" in error_msg:
                detail = "Phone number already exists"
            else:
                detail = "Duplicate entry found"
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=detail
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__['orig'])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )

def read_all(db: Session):
    try:
        result = db.query(Customer).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    return result

def read_one(db: Session, item_id: int):
    try:
        item = db.query(Customer).filter(Customer.id == item_id).first()
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    return item

def update(db: Session, item_id: int, request: CustomerUpdate):
    try:
        item = db.query(Customer).filter(Customer.id == item_id)
        if not item.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
        return item.first()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )

def delete(db: Session, item_id: int):
    try:
        item = db.query(Customer).filter(Customer.id == item_id)
        if not item.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
