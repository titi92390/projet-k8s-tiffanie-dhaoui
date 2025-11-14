from fastapi import FastAPI
from sqlalchemy import create_engine, text
import os

app = FastAPI()

DATABASE_URL = (
    f"postgresql://{os.environ['POSTGRES_USER']}:"
    f"{os.environ['POSTGRES_PASSWORD']}@"
    f"{os.environ['POSTGRES_HOST']}/"
    f"{os.environ['POSTGRES_DB']}"
)

engine = create_engine(DATABASE_URL)

@app.get("/")
def read_root():
    return {"message": "Bienvenue"}

@app.get("/items")
def read_items():
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM items")).fetchall()
    return {"items": [dict(row) for row in rows]}

@app.post("/items")
def add_item(name: str):
    with engine.connect() as conn:
        conn.execute(text("INSERT INTO items (name) VALUES (:name)"), {"name": name})
        conn.commit()
    return {"message": "Item ajouté", "name": name}
