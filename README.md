
# E-commerce Platform Project

This project aims to create an e-commerce platform specific to clothing products. It provides the foundation for an extensible and versatile platform, focusing primarily on robust user authentication, secure payment integration, and containerized deployment.


## Features

- Secure User Registration: Implemented a secure user registration system incorporating email verification and JWT token-based authorization for ensuring trusted user access and safeguarding user data.
- Payment Integration via Stripe: Successfully integrated and tested Stripe payment system, allowing simulated transactions within the e-commerce platform for demonstration and future transactional capability.
- Containerized Deployment: Utilized Docker to containerize the project, including PostgreSQL, ensuring seamless deployment and management within containerized environments, facilitating scalability and efficient resource management.


## Tech Stack

**Backend:** Python, Django, Rest Framework

**Database:** PostgreSQL

**Other Tools:** Docker, Stripe API


## Installation

Prerequisites

    Python latest version
    Docker 

Clone the repository:
```bash 
git clone git@github.com:asefdevs/E-Commerce.git

```
Set up a virtual environment:

```bash
  python3 -m venv myvenv 
  source myenv/bin/activate
```

    
## Usage

Run Docker Compose:

```bash

sudo docker-compose up --build

```


You can access with link:

http://localhost:8000/


## 🔗 Endpoints and Features


User Account Operations:

        Register: http://0.0.0.0:8000/api/account/register/
        Verify Email: http://0.0.0.0:8000/api/account/verify_email/'token will be here'
        Login: http://0.0.0.0:8000/api/account/login/
        User Profile Details: http://0.0.0.0:8000/api/account/profile/detail/
        Change Profile Photo: http://0.0.0.0:8000/api/account/profile/photo_update/


E-commerce Store Functions:

        Products List: http://0.0.0.0:8000/api/store/products/
        Product Details: http://0.0.0.0:8000/api/store/products/<int:pk>/
        Add Product: http://0.0.0.0:8000/api/store/add-product/
        Categories List: http://0.0.0.0:8000/api/store/categories/
        Category Details: http://0.0.0.0:8000/api/store/categories/<int:id>/


Shopping Cart, Favorites, and Orders:

        Shopping Cart Items: http://0.0.0.0:8000/api/shopping/cartitems/
        Add Item to Cart: http://0.0.0.0:8000/api/shopping/add_item/
        Cart Item Details: http://0.0.0.0:8000/api/shopping/cartitems/<int:pk>/
        Add to Favorites: http://0.0.0.0:8000/api/shopping/add_favorites/
        Favorites List: http://0.0.0.0:8000/api/shopping/favorites/
        Favorites Item Details: http://0.0.0.0:8000/api/shopping/delete_favorite/<int:pk>/
        Add Order: http://0.0.0.0:8000/api/shopping/add_order/
        Recent Orders: http://0.0.0.0:8000/api/shopping/recent_orders/
        Cancel Order: http://0.0.0.0:8000/api/shopping/cancel_order/<int:pk>/
## License

[MIT](https://choosealicense.com/licenses/mit/)

