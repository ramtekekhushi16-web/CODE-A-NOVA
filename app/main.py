from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query
from app.database import get_connection, init_db
from app.schemas import ProductCreate, ProductUpdate, StockUpdate

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="CODE-A-NOVA Product Inventory API",
    description="REST API to manage products, quantities, search, and stock updates.",
    version="1.0.0",
    lifespan=lifespan
)

def row_to_dict(row):
    return dict(row) if row else None

@app.get("/")
def home():
    return {"message": "Product Inventory API is running", "docs": "/docs"}

@app.post("/products", status_code=201)
def add_product(product: ProductCreate):
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO products (name, category, description, quantity, price)
               VALUES (?, ?, ?, ?, ?)""",
            (product.name, product.category, product.description, product.quantity, product.price)
        )
        row = conn.execute("SELECT * FROM products WHERE id = ?", (cur.lastrowid,)).fetchone()
        return row_to_dict(row)

@app.get("/products")
def list_products(
    search: str | None = Query(default=None, description="Search product name"),
    category: str | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100)
):
    sql = "SELECT * FROM products WHERE 1=1"
    params = []
    if search:
        sql += " AND name LIKE ?"
        params.append(f"%{search}%")
    if category:
        sql += " AND category LIKE ?"
        params.append(f"%{category}%")
    count_sql = sql.replace("SELECT *", "SELECT COUNT(*)")
    with get_connection() as conn:
        total = conn.execute(count_sql, params).fetchone()[0]
        rows = conn.execute(
            sql + " ORDER BY id DESC LIMIT ? OFFSET ?",
            (*params, limit, skip)
        ).fetchall()
    return {"total": total, "skip": skip, "limit": limit,
            "products": [row_to_dict(row) for row in rows]}

@app.get("/products/{product_id}")
def get_product(product_id: int):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Product not found")
    return row_to_dict(row)

@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductUpdate):
    updates = product.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields supplied for update")
    updates["updated_at"] = __import__("datetime").datetime.now().isoformat(timespec="seconds")
    assignments = ", ".join(f"{key} = ?" for key in updates)
    values = list(updates.values()) + [product_id]
    with get_connection() as conn:
        cur = conn.execute(f"UPDATE products SET {assignments} WHERE id = ?", values)
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        row = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    return row_to_dict(row)

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully", "product_id": product_id}

@app.patch("/products/{product_id}/stock")
def update_stock(product_id: int, stock: StockUpdate):
    with get_connection() as conn:
        row = conn.execute("SELECT quantity FROM products WHERE id = ?", (product_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Product not found")
        new_quantity = row["quantity"] + stock.quantity_change
        if new_quantity < 0:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        conn.execute(
            "UPDATE products SET quantity = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (new_quantity, product_id)
        )
        updated = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    return {"message": "Stock updated successfully", "product": row_to_dict(updated)}
