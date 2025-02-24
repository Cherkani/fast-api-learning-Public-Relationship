from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..services import ingredients as service
from ..schemas.ingredients import IngredientCreate, Ingredient, IngredientUpdate
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/ingredients",
    tags=["Ingredients"]
)


@router.post("/", response_model=Ingredient)
def create_ingredient(request: IngredientCreate, db: Session = Depends(get_db)):
    return service.create(db=db, request=request)


@router.get("/", response_model=list[Ingredient])
def read_ingredients(db: Session = Depends(get_db)):
    return service.read_all(db=db)


@router.get("/{ingredient_id}", response_model=Ingredient)
def read_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    return service.read_one(db=db, ingredient_id=ingredient_id)


@router.put("/{ingredient_id}", response_model=Ingredient)
def update_ingredient(ingredient_id: int, request: IngredientUpdate, db: Session = Depends(get_db)):
    return service.update(db=db, ingredient_id=ingredient_id, request=request)


@router.delete("/{ingredient_id}")
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    return service.delete(db=db, ingredient_id=ingredient_id)
