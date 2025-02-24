from . import (
    orders,
    ingredients,
    menu_items,
    customers,
)

from ..dependencies.database import engine


def index():
    orders.Base.metadata.create_all(engine)
    ingredients.Base.metadata.create_all(engine)
    menu_items.Base.metadata.create_all(engine)
    customers.Base.metadata.create_all(engine)
