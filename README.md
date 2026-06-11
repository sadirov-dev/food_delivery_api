# Food Delivery API

Figma link: [Food Delivery App Community](https://www.figma.com/design/q59eRKNrM6W6oIzUG20JRj/Food-Delivery-App--Community-?node-id=223-3474&p=f&t=rMJz3ryN2sea5pjq-0)

## Description

Simple backend project for a food delivery app built with FastAPI. The project includes authentication, restaurants, categories, foods, cart, orders, addresses, favorites, reviews, home page data, SQLite database, Alembic migrations, and Docker support.

## Technologies

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Alembic
- Pydantic
- JWT Auth
- Uvicorn
- Docker

## Project structure

```text
food_delivery_api/
├── api/
├── database/
├── services/
├── alembic/
├── config.py
├── main.py
├── requirements.txt
├── README.md
├── alembic.ini
├── .env.example
├── .gitignore
├── Dockerfile
└── docker-compose.yml
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## .env example

```env
DATABASE_URL=sqlite:///./food_delivery.db
SECRET_KEY=change-this-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=60
ALGORITHM=HS256
```

## Migrations

```bash
alembic revision --autogenerate -m "initial"
alembic upgrade head
```

## Run locally

```bash
uvicorn main:app --reload
```

API:
- Swagger: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/health`

## Run with Docker

```bash
cp .env.example .env
docker compose up --build
```

## Endpoints

### Auth
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`

### Restaurants
- `POST /api/restaurants`
- `GET /api/restaurants`
- `GET /api/restaurants/{id}`
- `PUT /api/restaurants/{id}`
- `DELETE /api/restaurants/{id}`

### Categories
- `POST /api/categories`
- `GET /api/categories`
- `GET /api/categories/{id}`
- `PUT /api/categories/{id}`
- `DELETE /api/categories/{id}`

### Foods
- `POST /api/foods`
- `GET /api/foods`
- `GET /api/foods/{id}`
- `PUT /api/foods/{id}`
- `DELETE /api/foods/{id}`

Filters for `GET /api/foods`:
- `search`
- `restaurant_id`
- `category_id`
- `min_price`
- `max_price`
- `is_popular`
- `is_available`

### Cart
- `POST /api/cart/items`
- `GET /api/cart`
- `PATCH /api/cart/items/{id}`
- `DELETE /api/cart/items/{id}`
- `DELETE /api/cart/clear`

### Orders
- `POST /api/orders`
- `GET /api/orders`
- `GET /api/orders/{id}`
- `PATCH /api/orders/{id}/status`

### Addresses
- `POST /api/addresses`
- `GET /api/addresses`
- `GET /api/addresses/{id}`
- `PUT /api/addresses/{id}`
- `DELETE /api/addresses/{id}`

### Favorites
- `POST /api/favorites/{food_id}`
- `GET /api/favorites`
- `DELETE /api/favorites/{food_id}`

### Reviews
- `POST /api/reviews`
- `GET /api/reviews`
- `GET /api/reviews/{id}`
- `DELETE /api/reviews/{id}`

### Home
- `GET /api/home`

### Health
- `GET /health`

## GitHub

Repository: [food_delivery_api](https://github.com/sadirov-dev/food_delivery_api.git)

```bash
git init
git branch -M main
git remote add origin https://github.com/sadirov-dev/food_delivery_api.git
git add .
git commit -m "Initial FastAPI food delivery backend"
git push -u origin main
```

## AWS EC2 deploy commands

```bash
sudo apt update
sudo apt install -y git docker.io docker-compose-v2
sudo systemctl enable --now docker
sudo usermod -aG docker $USER

git clone https://github.com/sadirov-dev/food_delivery_api.git
cd food_delivery_api
cp .env.example .env
sudo docker compose up --build -d
docker compose ps
```
