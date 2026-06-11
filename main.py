from fastapi import FastAPI

from api import (
    addresses,
    auth,
    cart,
    categories,
    favorites,
    foods,
    home,
    orders,
    restaurants,
    reviews,
)


app = FastAPI(title="Food Delivery API")

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(restaurants.router, prefix="/api/restaurants", tags=["Restaurants"])
app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])
app.include_router(foods.router, prefix="/api/foods", tags=["Foods"])
app.include_router(cart.router, prefix="/api/cart", tags=["Cart"])
app.include_router(orders.router, prefix="/api/orders", tags=["Orders"])
app.include_router(addresses.router, prefix="/api/addresses", tags=["Addresses"])
app.include_router(favorites.router, prefix="/api/favorites", tags=["Favorites"])
app.include_router(reviews.router, prefix="/api/reviews", tags=["Reviews"])
app.include_router(home.router, prefix="/api/home", tags=["Home"])


@app.get("/health")
def health_check():
    return {"status": "ok"}
