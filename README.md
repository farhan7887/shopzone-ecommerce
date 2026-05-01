# 🛒 ShopZone — Full-Stack eCommerce Platform
### COMSATS University · CSC101 · ICT Lab Project

---

## 📁 Project Structure

```
ecommerce/
├── backend/
│   ├── app.py                  ← Main Flask server (run this)
│   ├── models.py               ← Database models (5 tables)
│   ├── requirements.txt        ← Python dependencies
│   └── routes/
│       ├── auth.py             ← Register, Login, Me
│       ├── products.py         ← CRUD for products
│       ├── cart.py             ← Cart management
│       └── orders.py           ← Orders + stats
│
└── frontend/
    ├── index.html              ← Home / Product listing
    ├── product.html            ← Single product detail
    ├── cart.html               ← Shopping cart
    ├── checkout.html           ← Checkout + place order
    ├── login.html              ← Login page
    ├── register.html           ← Sign up page
    ├── orders.html             ← My orders (customer)
    ├── admin/
    │   ├── dashboard.html      ← Admin stats dashboard
    │   ├── products.html       ← Add/edit/delete products
    │   └── orders.html         ← Manage all orders
    ├── css/
    │   └── style.css           ← Full custom stylesheet
    └── js/
        └── main.js             ← API client + utilities
```

---

## 🚀 How to Run

### Step 1 — Install Python Libraries
```bash
cd backend
pip install -r requirements.txt
```

### Step 2 — Start the Backend Server
```bash
python app.py
```
You should see:
```
🚀 ShopZone Backend running at http://localhost:5000
👤 Admin login  → admin@shop.com  / admin123
👤 User login   → user@shop.com   / user123
```

### Step 3 — Open the Frontend
- Open `frontend/index.html` in your browser
- OR use **Live Server** extension in VS Code (recommended)

---

## 👤 Demo Accounts

| Role     | Email             | Password  |
|----------|-------------------|-----------|
| Customer | user@shop.com     | user123   |
| Admin    | admin@shop.com    | admin123  |

---

## 🔌 API Endpoints

### Auth
| Method | Endpoint              | Description         |
|--------|-----------------------|---------------------|
| POST   | /api/auth/register    | Create new account  |
| POST   | /api/auth/login       | Login, get JWT      |
| GET    | /api/auth/me          | Get current user    |

### Products
| Method | Endpoint                  | Description              |
|--------|---------------------------|--------------------------|
| GET    | /api/products/            | Get all products         |
| GET    | /api/products/?search=X   | Search products          |
| GET    | /api/products/?category=X | Filter by category       |
| GET    | /api/products/:id         | Get single product       |
| POST   | /api/products/            | Add product (admin)      |
| PUT    | /api/products/:id         | Edit product (admin)     |
| DELETE | /api/products/:id         | Delete product (admin)   |

### Cart
| Method | Endpoint          | Description        |
|--------|-------------------|--------------------|
| GET    | /api/cart/        | Get cart items     |
| POST   | /api/cart/        | Add item to cart   |
| PUT    | /api/cart/:id     | Update quantity    |
| DELETE | /api/cart/:id     | Remove single item |
| DELETE | /api/cart/        | Clear entire cart  |

### Orders
| Method | Endpoint                    | Description            |
|--------|-----------------------------|------------------------|
| GET    | /api/orders/                | Get my orders          |
| POST   | /api/orders/                | Place order from cart  |
| GET    | /api/orders/:id             | Get single order       |
| PUT    | /api/orders/:id/status      | Update status (admin)  |
| GET    | /api/orders/stats           | Dashboard stats (admin)|

---

## 🗄️ Database Tables

```
users        → id, name, email, password, role, created_at
products     → id, name, description, price, image, category, stock, created_at
cart         → id, user_id, product_id, quantity
orders       → id, user_id, total_price, status, address, created_at
order_items  → id, order_id, product_id, quantity, price
```

---

## 🔐 How JWT Auth Works

```
1. User registers/logs in
2. Server creates a JWT token (signed with secret key)
3. Token stored in localStorage on frontend
4. Every API request sends: Authorization: Bearer <token>
5. Server validates token → allows or rejects request
```

---

## 💡 Viva Key Points

| Topic          | Answer |
|----------------|--------|
| **Framework**  | Flask — lightweight Python web framework |
| **Database**   | SQLite via SQLAlchemy ORM |
| **Auth**       | JWT (JSON Web Token) — stateless authentication |
| **Password**   | bcrypt hashing — never stored in plain text |
| **CORS**       | Flask-CORS allows frontend to call backend API |
| **REST API**   | HTTP methods: GET (read), POST (create), PUT (update), DELETE (remove) |
| **Admin role** | role='admin' field in users table — checked on every admin endpoint |
| **Stock**      | Automatically reduced when order is placed |

---

## 🖥️ Pages Overview

| Page | URL | Access |
|------|-----|--------|
| Home | index.html | Public |
| Product Detail | product.html?id=1 | Public |
| Cart | cart.html | Logged in |
| Checkout | checkout.html | Logged in |
| My Orders | orders.html | Logged in |
| Login | login.html | Guest only |
| Register | register.html | Guest only |
| Admin Dashboard | admin/dashboard.html | Admin only |
| Admin Products | admin/products.html | Admin only |
| Admin Orders | admin/orders.html | Admin only |

---

*Built with Flask + SQLAlchemy + JWT + HTML + CSS + JavaScript*
*COMSATS University Islamabad — CSC101 Lab Project 2026*
