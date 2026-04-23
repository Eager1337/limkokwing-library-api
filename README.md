# 📚 Limkokwing Library Management API

**PROG315 – Object-Oriented Programming 2**  
**Assignment:** Basic API Structure with Open-Source  
**Institution:** Limkokwing University of Creative Technology – Sierra Leone  
**Semester:** 04 | March 2026 – July 2026

---

## 📌 Project Description

A RESTful API built with **Python FastAPI** for managing the Limkokwing University Sierra Leone Library. The system allows users to search for books, borrow and return them, and track overdue fines — all with support for multiple concurrent users via asynchronous programming.

---

## 🚀 Features

- 🔍 Search books by title, author, or category
- 📖 Borrow available books (with 14-day loan period)
- 🔁 Return books and calculate overdue fines
- ⚠️ View all overdue books and outstanding fines
- 🔢 Retrieve a single book by ID
- ⚡ Async/await support for handling multiple users simultaneously
- ✅ Full type annotations with Pydantic models

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11+ | Core language |
| FastAPI | Web framework |
| Uvicorn | ASGI server |
| Pydantic | Data validation & type annotations |
| Asyncio | Concurrent request handling |

---

## 📦 Installation & Setup

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/limkokwing-library-api.git
cd limkokwing-library-api

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the API server
uvicorn main:app --reload
```

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/books` | Search books by title, author, or category |
| GET | `/books/{book_id}` | Get details of a specific book |
| POST | `/borrow` | Borrow an available book |
| PUT | `/return/{borrow_id}` | Return a borrowed book |
| GET | `/overdue` | List all overdue books and fines |

---

## 📖 API Documentation

Once the server is running, visit:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 📁 Project Structure

```
limkokwing-library-api/
│
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── .gitignore           # Git ignore rules
```

---

## 🌍 SDG Alignment

This project aligns with **UN Sustainable Development Goal 4 – Quality Education**, by digitizing library access and making educational resources more accessible to all students and staff.

---

## 👤 Author

- **Student Name:** [Your Full Name]  
- **Student ID:** [Your Student ID]  
- **Email:** [your.email@limkokwing.edu.sl]  
- **GitHub:** [https://github.com/YOUR_USERNAME]

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
