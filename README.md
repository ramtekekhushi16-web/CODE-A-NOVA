# CODE-A-NOVA — Product Inventory API

A Python FastAPI + SQLite REST API for managing an inventory of products.

## Features
- Add, view, update, and delete products
- Track product quantity
- Search by product name and category
- Pagination using `skip` and `limit`
- Stock update endpoint (add or remove stock)
- Prevents negative quantity and validates input

## Run locally

Python 3.10+ is recommended.

```bash
# 1. Create and activate a virtual environment
python -m venv venv

# Windows PowerShell
.\venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the API
uvicorn app.main:app --reload
```

Open:
- API documentation: http://127.0.0.1:8000/docs
- Root endpoint: http://127.0.0.1:8000/

The SQLite database (`inventory.db`) is created automatically on first startup.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API status |
| POST | `/products` | Add a product |
| GET | `/products` | List/search products with pagination |
| GET | `/products/{product_id}` | Get one product |
| PUT | `/products/{product_id}` | Update product details |
| DELETE | `/products/{product_id}` | Delete a product |
| PATCH | `/products/{product_id}/stock` | Add/remove stock |

## Example requests

### Add product — POST `/products`
```json
{
  "name": "Wireless Mouse",
  "category": "Electronics",
  "description": "2.4 GHz wireless mouse",
  "quantity": 25,
  "price": 499.0
}
```

### Search and paginate — GET `/products?search=mouse&skip=0&limit=10`

### Update details — PUT `/products/1`
```json
{
  "price": 449.0,
  "description": "Updated product description"
}
```

### Add 10 units — PATCH `/products/1/stock`
```json
{
  "quantity_change": 10
}
```

### Remove 3 units — PATCH `/products/1/stock`
```json
{
  "quantity_change": -3
}
```

## Suggested submission checklist
1. Run the API locally and test each endpoint in `/docs`.
2. Add screenshots of successful POST, GET, PUT, DELETE, search, and stock update requests.
3. Create a GitHub repository named `CODE-A-NOVA` and push this project.
4. Share the repository link using the official internship submission form when provided.

## Important
The internship brief says projects should be developed independently and asks interns not to use AI tools. Use this project as a learning/reference scaffold only if that complies with your coordinator's rules. Understand, test, and adapt every part yourself; do not claim work you did not independently complete.
