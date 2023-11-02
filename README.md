
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
    
## Usage

Run Docker Compose:

```bash

sudo docker-compose up --build

```


You can access with link:

http://localhost:8000/


## 🔗 Endpoints and Features


### User Account Operations

| Endpoint                                | HTTP Method | Description                                       |
|-----------------------------------------|-------------|---------------------------------------------------|
| /api/account/register/                  | POST        | User registration                                 |
| /api/account/verify_email/{token}/      | GET         | Verify user's email using a token                 |
| /api/account/login/                     | POST        | User login                                        |
| /api/account/profile/detail/            | GET         | Retrieve user's profile details                   |
| /api/account/profile/photo_update/      | PUT         | Update user's profile photo                       |

### E-commerce Store Functions

| Endpoint                                | HTTP Method | Description                                       |
|-----------------------------------------|-------------|---------------------------------------------------|
| /api/store/products/                    | GET         | Retrieve list of products                         |
| /api/store/products/<int:pk>/           | GET         | Retrieve details of a specific product            |
| /api/store/add-product/                 | POST        | Add a new product to the store                    |
| /api/store/categories/                  | GET         | Retrieve list of product categories               |
| /api/store/categories/<int:id>/         | GET         | Retrieve details of a specific category           |

### Shopping Cart, Favorites, and Orders

| Endpoint                                | HTTP Method | Description                                       |
|-----------------------------------------|-------------|---------------------------------------------------|
| /api/shopping/cartitems/                | GET         | Retrieve items in the shopping cart               |
| /api/shopping/add_item/                 | POST        | Add an item to the shopping cart                  |
| /api/shopping/cartitems/<int:pk>/       | GET         | Retrieve details of a specific item in the cart   |
| /api/shopping/add_favorites/            | POST        | Add items to the favorites list                   |
| /api/shopping/favorites/                | GET         | Retrieve list of favorite items                   |
| /api/shopping/delete_favorite/<int:pk>/ | DELETE      | Delete a specific favorite item                   |
| /api/shopping/add_order/                | POST        | Add an order for items in the cart                |
| /api/shopping/recent_orders/            | GET         | Retrieve list of recent orders                    |
| /api/shopping/cancel_order/<int:pk>/    | DELETE      | Cancel a specific order                           |

## License

[MIT](https://choosealicense.com/licenses/mit/)

