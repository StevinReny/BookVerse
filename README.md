# BookVerse 📚🛒

BookVerse is an **online bookstore application built using Django** that enables users to browse a catalog of books, manage a shopping cart, place orders, and track order history. The application uses Django’s built-in authentication system and enforces role-based access control to separate customer and admin responsibilities.

---

## ✨ Key Features

### 🔐 User Management
- User registration, login, and logout
- Role-based access:
  - **Customers:** Browse books, manage cart, place orders
  - **Admins:** Manage books and orders
- Secure authentication using Django’s built-in auth system

---

### 📖 Book Catalog
- Book model with:
  - Title, Author, Genre
  - Description, Price, Stock Quantity
  - Book cover image upload
- Search functionality by title, author, or genre
- Paginated book listings for better user experience

---

### 🛒 Shopping Cart
- Add books to cart
- Remove books from cart
- Update item quantities
- Real-time total price calculation

---

### 💳 Checkout & Order Management
- Order confirmation workflow
- Orders initially marked as **Pending**
- Customers can view order history
- Admins can update order status (Pending, Shipped, Delivered)

---

### 🔒 Security & Permissions
- Admin-only access to book and order management
- Permission-protected views and templates
- Secure handling of user sessions and data

---

## 🛠️ Tech Stack

- **Backend:** Django
- **Database:** SQLite / PostgreSQL
- **Frontend:** Django Templates
- **Authentication:** Django Auth System
- **Media Handling:** Image uploads
- **Pagination & Search:** Django ORM

---

## 🎯 Project Objective

The goal of BookVerse is to demonstrate how to build a **full-featured e-commerce application using Django**, covering authentication, CRUD operations, cart management, order workflows, and permission-based access control.

---

## 📄 License
MIT License
