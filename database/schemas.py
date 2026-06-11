from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    avatar_url: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RestaurantBase(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    address: str
    delivery_time: str
    delivery_price: float = Field(ge=0)
    rating: float = Field(default=0, ge=0, le=5)
    is_open: bool = True


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(RestaurantBase):
    pass


class RestaurantResponse(RestaurantBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CategoryBase(BaseModel):
    title: str
    icon_url: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FoodBase(BaseModel):
    restaurant_id: int
    category_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    price: float = Field(gt=0)
    old_price: Optional[float] = Field(default=None, ge=0)
    image_url: Optional[str] = None
    calories: Optional[int] = Field(default=None, ge=0)
    rating: float = Field(default=0, ge=0, le=5)
    is_popular: bool = False
    is_available: bool = True


class FoodCreate(FoodBase):
    pass


class FoodUpdate(FoodBase):
    pass


class FoodResponse(FoodBase):
    id: int
    created_at: datetime
    restaurant: Optional[RestaurantResponse] = None
    category: Optional[CategoryResponse] = None

    model_config = ConfigDict(from_attributes=True)


class CartItemBase(BaseModel):
    food_id: int
    quantity: int = Field(default=1, ge=1)


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(BaseModel):
    quantity: int = Field(ge=1)


class CartItemResponse(BaseModel):
    id: int
    user_id: int
    food_id: int
    quantity: int
    created_at: datetime
    food: FoodResponse

    model_config = ConfigDict(from_attributes=True)


class CartResponse(BaseModel):
    items: list[CartItemResponse]
    total_items: int
    subtotal: float


class AddressBase(BaseModel):
    title: str
    city: str
    street: str
    building: str
    apartment: Optional[str] = None
    is_default: bool = False


class AddressCreate(AddressBase):
    pass


class AddressUpdate(AddressBase):
    pass


class AddressResponse(AddressBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderCreate(BaseModel):
    address_id: int
    payment_method: str


class OrderStatusUpdate(BaseModel):
    status: str


class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    food_id: int
    quantity: int
    price: float
    food: Optional[FoodResponse] = None

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    id: int
    user_id: int
    address_id: int
    total_price: float
    delivery_price: float
    status: str
    payment_method: str
    created_at: datetime
    items: list[OrderItemResponse]
    address: Optional[AddressResponse] = None

    model_config = ConfigDict(from_attributes=True)


class ReviewBase(BaseModel):
    restaurant_id: int
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewResponse(ReviewBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    food_id: int
    created_at: datetime
    food: FoodResponse

    model_config = ConfigDict(from_attributes=True)


class HomeResponse(BaseModel):
    categories: list[CategoryResponse]
    popular_foods: list[FoodResponse]
    open_restaurants: list[RestaurantResponse]
    recommended_foods: list[FoodResponse]
