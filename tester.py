from fastapi.testclient import TestClient
from main import app  # Pastikan mengimpor 'app' dari main.py

# Inisialisasi TestClient
client = TestClient(app)


# ─────────────────────────────────────
# 1. Test Root Endpoint (/)
# ─────────────────────────────────────
def test_read_root():
    """Test endpoint root mengembalikan pesan selamat datang"""
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"Message": "Hello World! FastAPI is working."}


# ─────────────────────────────────────
# 2. Test Get All Items (/items)
# ─────────────────────────────────────
def test_read_items():
    """Test endpoint /items mengembalikan list item TANPA field 'id'"""
    response = client.get("/items")

    assert response.status_code == 200
    data = response.json()

    # Harus berupa list
    assert isinstance(data, list)

    # Harus ada minimal 1 item (karena ada data awal)
    assert len(data) > 0

    # Pastikan field 'id' TIDAK ada di response (sesuai kode main.py)
    for item in data:
        assert "id" not in item
        # Pastikan field lain ada
        assert "name" in item
        assert "price" in item
        assert "quantity" in item


# ─────────────────────────────────────
# 3. Test Get Item By Name (Found)
# ─────────────────────────────────────
def test_call_item_found():
    """Test mencari item yang ada (case-insensitive)"""
    # Coba dengan huruf kecil
    response = client.get("/items/buku tulis")
    assert response.status_code == 200
    data = response.json()
    assert data["name"].lower() == "buku tulis"
    assert "id" in data  # Endpoint detail mengembalikan ID

    # Coba dengan huruf BESAR (uji case-insensitive)
    response = client.get("/items/PENSIL")
    assert response.status_code == 200
    data = response.json()
    assert data["name"].lower() == "pensil"


# ─────────────────────────────────────
# 4. Test Get Item By Name (Not Found)
# ─────────────────────────────────────
def test_call_item_not_found():
    """Test mencari item yang tidak ada"""
    response = client.get("/items/barang_tidak_adam")

    assert response.status_code == 200  # Kode kamu return 200 dengan error message
    data = response.json()
    assert "error" in data
    assert data["error"] == "Item not found"


# ─────────────────────────────────────
# 5. Test Edge Cases
# ─────────────────────────────────────
def test_call_item_partial_match():
    """Test memastikan pencarian harus exact match (bukan partial)"""
    # "Buku" saja tidak akan menemukan "Buku Tulis"
    response = client.get("/items/buku")
    assert response.status_code == 200
    data = response.json()

    # Seharusnya tidak ditemukan karena kode menggunakan == bukan in
    if "error" in data:
        assert data["error"] == "Item not found"


def test_items_structure():
    """Test struktur data item konsisten"""
    response = client.get("/items")
    data = response.json()

    required_fields = {"name", "description", "price", "quantity"}

    for item in data:
        # Cek semua field wajib ada
        assert required_fields.issubset(item.keys())

        # Cek tipe data
        assert isinstance(item["name"], str)
        assert isinstance(item["price"], int)
        assert isinstance(item["quantity"], int)
