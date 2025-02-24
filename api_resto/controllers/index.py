from . import orders, ingredients, menu_items, customers


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(ingredients.router)
    app.include_router(menu_items.router)
    app.include_router(customers.router)



