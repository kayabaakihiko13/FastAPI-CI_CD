from typing import List
from uuid import uuid4
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Data awal
ITEMS = [
    {
        "id": str(uuid4()),
        "name": "Buku Tulis",
        "description": "Barang untuk menulis",
        "price": 10000,
        "quantity": 10,
    },
    {
        "id": str(uuid4()),
        "name": "Pensil",
        "description": "Barang untuk menulis",
        "price": 2000,
        "quantity": 20,
    },
    {
        "id": str(uuid4()),
        "name": "Buku Gambar",
        "description": "Barang untuk menggambar",
        "price": 15000,
        "quantity": 5,
    },
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Message": "Hello World! FastAPI is working."}


@app.get("/items")
def read_items() -> List[dict]:
    # Mengembalikan semua item tanpa field 'id'
    return [{k: v for k, v in item.items() if k != "id"} for item in ITEMS]


@app.get("/items/{name_item}")
def call_item(name_item: str):
    for item in ITEMS:
        if (
            item["name"].lower() == name_item.lower()
        ):  # .lower() supaya pencarian tidak sensitif huruf besar/kecil
            return item

    return {"error": "Item not found"}
