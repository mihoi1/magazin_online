# 🛒 Django Online Shop

This is an online shop project built with Django that offers essential e-commerce features such as a shopping cart, order placement with payment and delivery options, and order history for authenticated users.

## Features

* View available products in the store

* Shopping cart linked to the user and stored in the database

* Manually add products to the cart as a user

* Checkout with:
  - Choice of payment method: Online with Credit Card / Cash on Delivery
  - Choice of delivery method: Courier / EasyBox Locker
  
* Order status management:
  - Pending
  - Delivered
  - Cancelled

* Order history for each user

* User authentication and registration

* Total price display for each order


##  Setup & Run Instructions

### 1. Clone the repository

```
git clone https://github.com/mihoi1/magazin_online.git
cd magazin_online
```

###  2. Create and activate a virtual environment
Windows:

```
python -m venv venv
venv\Scripts\activate
```

macOS / Linux:

```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```
pip install django
```

### 4. Apply migrations

```
python manage.py migrate
```

### 5. Create a superuser (optional)

```
python manage.py createsuperuser
```

### 6. Run the development server

```
python manage.py runserver
```

Then open: http://127.0.0.1:8000


>[!NOTE]
>* The project uses SQLite by default, which is fine for development and testing but not recommended for production.
>* User authentication is handled via Django’s built-in auth system.
