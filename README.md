# Inventory Management System

## Installation and Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Flask API Server
```bash
python app.py
```
Server runs on `http://localhost:5000`

### 3. Run the CLI (in separate terminal)
```bash
python cli.py
```

### 4. Run Tests
```bash
pytest tests/ -v
```

## API Endpoints

### Inventory Management
| Method | Endpoint | Description | Required Fields |
|--------|----------|-------------|-----------------|
| GET | `/inventory` | Fetch all items | None |
| GET | `/inventory/<id>` | Fetch single item | None |
| POST | `/inventory` | Add new item | product_name, brands, quantity, price |
| PATCH | `/inventory/<id>` | Update item | Any field(s) to update |
| DELETE | `/inventory/<id>` | Delete item | None |

### OpenFoodFacts Search
| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| GET | `/api/search/barcode/<barcode>` | Search by barcode | barcode in URL |
| GET | `/api/search/name` | Search by name | ?q=product_name |

### API Examples

**Get all inventory:**
```bash
curl http://localhost:5000/inventory
```

**Add item manually:**
```bash
curl -X POST http://localhost:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{"product_name":"Honey","brands":"Local","quantity":20,"price":7.99}'
```

**Add item from OpenFoodFacts:**
```bash
curl -X POST http://localhost:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{"barcode":"3017620422003","quantity":50,"price":2.99,"fetch_from_api":true}'
```

**Update item:**
```bash
curl -X PATCH http://localhost:5000/inventory/1 \
  -H "Content-Type: application/json" \
  -d '{"quantity":100,"price":5.99}'
```

**Delete item:**
```bash
curl -X DELETE http://localhost:5000/inventory/1
```

**Search by barcode:**
```bash
curl http://localhost:5000/api/search/barcode/3017620422003
```

**Search by name:**
```bash
curl "http://localhost:5000/api/search/name?q=nutella"
```

## CLI Usage Examples

When you run `python cli.py`, you'll see this menu:

```
1. View all inventory items
2. View single inventory item
3. Add new inventory item
4. Update inventory item
5. Delete inventory item
6. Search product on OpenFoodFacts (by barcode)
7. Search product on OpenFoodFacts (by name)
8. Exit
```

### Example Workflows

**Adding an item manually (Option 3):**
```
Enter your choice (1-8): 3
Choose option:
1. Add manually
2. Add from OpenFoodFacts (by barcode)
Enter choice (1-2): 1
Product name: Organic Honey
Brand: Local Farm
Ingredients (optional): Pure honey
Quantity: 20
Price: 7.99
Barcode (optional): 123456789
```

**Adding from OpenFoodFacts (Option 3):**
```
Enter your choice (1-8): 3
Choose option:
1. Add manually
2. Add from OpenFoodFacts (by barcode)
Enter choice (1-2): 2
Enter barcode: 3017620422003
Quantity: 50
Price: 2.99
```

**Updating an item (Option 4):**
```
Enter your choice (1-8): 4
Enter item ID to update: 1
Enter new values (press Enter to skip):
Product name: 
Brand: 
Ingredients: 
Quantity: 100
Price: 5.99
Barcode: 
```

**Searching by barcode (Option 6):**
```
Enter your choice (1-8): 6
Enter barcode: 3017620422003
```

**Searching by name (Option 7):**
```
Enter your choice (1-8): 7
Enter product name: nutella
```
