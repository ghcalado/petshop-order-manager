# 🐾 PetShop Order Manager | B2B Sales Automation

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

A high-performance CLI tool designed to bridge the gap between pet supply distributors and local retailers. This system eliminates manual order errors by automating inventory selection and generating instant checkout links via WhatsApp API.

## 🌟 Key Features

- **Dynamic Order Logic:** Real-time subtotal and total calculations for complex bulk orders.
- **Relational Persistence:** Robust data handling using SQLite, ensuring order history and product integrity.
- **WhatsApp API Integration:** Custom-built message formatting for professional B2B communication.
- **Military-Grade Security:** Zero-exposure policy for sensitive data (API numbers and passwords) using environment variables (`python-dotenv`).
- **Clean Architecture:** Modular code inspired by DRY (Don't Repeat Yourself) principles.

## 🛠️ Tech Stack

- **Language:** Python 3.x
- **Database:** SQLite3
- **Security:** Dotenv (Environment Variables)
- **Communication:** Urllib (URL Encoding for WhatsApp)

## 🚀 Quick Start

### 1. Clone & Environment
```bash
git clone [https://github.com/ghcalado/petshop-order-manager.git](https://github.com/ghcalado/petshop-order-manager.git)
cd petshop-order-manager
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
2. Install Dependencies
Bash
pip install -r requirements.txt
3. Setup Credentials (SECURITY)
Create a .env file in the root directory:

Snippet de código
SENHA_LOJISTA=your_store_password
SENHA_ADMIN=your_admin_password
NUMERO_VENDEDOR=5514999999999
4. Run the Engine
Bash
python main.py
📊 Database Schema
The system operates on three optimized tables:

produtos: Inventory management (Price, Unit, Category).

pedidos: High-level order tracking.

itens_pedido: Granular item details with foreign key relationships.

Developed with ☕ and Python by Ghabriel Calado
