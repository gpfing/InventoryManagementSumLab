# Unit tests for API endpoints
import pytest
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
import data


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app = create_app()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client
    
    # Reset data after each test
    data.inventory = [
        {
            "id": 1,
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "ingredients_text": "Filtered water, almonds, cane sugar, sea salt, sunflower lecithin, gellan gum, natural flavor, vitamin A palmitate, vitamin D2, D-alpha-tocopherol",
            "quantity": 50,
            "price": 4.99,
            "barcode": "025293600270"
        },
        {
            "id": 2,
            "product_name": "Organic Peanut Butter",
            "brands": "Justin's",
            "ingredients_text": "Dry roasted peanuts, palm oil, sea salt",
            "quantity": 30,
            "price": 8.99,
            "barcode": "894700010014"
        },
        {
            "id": 3,
            "product_name": "Greek Yogurt",
            "brands": "Chobani",
            "ingredients_text": "Cultured nonfat milk, cane sugar, water, strawberries, natural flavors, fruit pectin, guar gum, beet juice concentrate",
            "quantity": 75,
            "price": 1.49,
            "barcode": "894700010052"
        }
    ]
    data.next_id = 4


class TestGetAllInventory:
    """Test GET /inventory endpoint"""
    
    def test_get_all_inventory_success(self, client):
        """Test retrieving all inventory items"""
        response = client.get('/inventory')
        assert response.status_code == 200
        
        json_data = response.get_json()
        assert json_data['status'] == 'success'
        assert json_data['count'] == 3
        assert len(json_data['data']) == 3
    
    def test_get_all_inventory_empty(self, client):
        """Test retrieving inventory when empty"""
        data.inventory = []
        response = client.get('/inventory')
        assert response.status_code == 200
        
        json_data = response.get_json()
        assert json_data['status'] == 'success'
        assert json_data['count'] == 0
        assert json_data['data'] == []


class TestGetSingleInventoryItem:
    """Test GET /inventory/<id> endpoint"""
    
    def test_get_item_success(self, client):
        """Test retrieving a single item by ID"""
        response = client.get('/inventory/1')
        assert response.status_code == 200
        
        json_data = response.get_json()
        assert json_data['status'] == 'success'
        assert json_data['data']['id'] == 1
        assert json_data['data']['product_name'] == 'Organic Almond Milk'
    
    def test_get_item_not_found(self, client):
        """Test retrieving non-existent item"""
        response = client.get('/inventory/999')
        assert response.status_code == 404
        
        json_data = response.get_json()
        assert json_data['status'] == 'error'
        assert 'not found' in json_data['message'].lower()


class TestAddInventoryItem:
    """Test POST /inventory endpoint"""
    
    def test_add_item_success(self, client):
        """Test adding a new item"""
        new_item = {
            "product_name": "Test Product",
            "brands": "Test Brand",
            "ingredients_text": "Test ingredients",
            "quantity": 10,
            "price": 5.99,
            "barcode": "123456789"
        }
        
        response = client.post('/inventory', json=new_item)
        assert response.status_code == 201
        
        json_data = response.get_json()
        assert json_data['status'] == 'success'
        assert json_data['data']['product_name'] == 'Test Product'
        assert json_data['data']['id'] == 4
        assert len(data.inventory) == 4
    
    def test_add_item_missing_fields(self, client):
        """Test adding item with missing required fields"""
        incomplete_item = {
            "product_name": "Test Product"
        }
        
        response = client.post('/inventory', json=incomplete_item)
        assert response.status_code == 400
        
        json_data = response.get_json()
        assert json_data['status'] == 'error'
        assert 'missing required fields' in json_data['message'].lower()
    
    def test_add_item_no_json(self, client):
        """Test adding item without JSON body"""
        response = client.post('/inventory')
        # Flask returns 415 when Content-Type is not application/json
        assert response.status_code == 415
    
    def test_add_item_with_optional_fields(self, client):
        """Test adding item with only required fields"""
        minimal_item = {
            "product_name": "Minimal Product",
            "brands": "Minimal Brand",
            "quantity": 5,
            "price": 2.99
        }
        
        response = client.post('/inventory', json=minimal_item)
        assert response.status_code == 201
        
        json_data = response.get_json()
        assert json_data['status'] == 'success'
        assert json_data['data']['ingredients_text'] == ''
        assert json_data['data']['barcode'] == ''


class TestUpdateInventoryItem:
    """Test PATCH /inventory/<id> endpoint"""
    
    def test_update_item_success(self, client):
        """Test updating an item"""
        update_data = {
            "quantity": 100,
            "price": 6.99
        }
        
        response = client.patch('/inventory/1', json=update_data)
        assert response.status_code == 200
        
        json_data = response.get_json()
        assert json_data['status'] == 'success'
        assert json_data['data']['quantity'] == 100
        assert json_data['data']['price'] == 6.99
        # Other fields should remain unchanged
        assert json_data['data']['product_name'] == 'Organic Almond Milk'
    
    def test_update_item_not_found(self, client):
        """Test updating non-existent item"""
        update_data = {"quantity": 50}
        
        response = client.patch('/inventory/999', json=update_data)
        assert response.status_code == 404
        
        json_data = response.get_json()
        assert json_data['status'] == 'error'
    
    def test_update_item_no_json(self, client):
        """Test updating without JSON body"""
        response = client.patch('/inventory/1')
        # Flask returns 415 when Content-Type is not application/json
        assert response.status_code == 415


class TestDeleteInventoryItem:
    """Test DELETE /inventory/<id> endpoint"""
    
    def test_delete_item_success(self, client):
        """Test deleting an item"""
        response = client.delete('/inventory/2')
        assert response.status_code == 200
        
        json_data = response.get_json()
        assert json_data['status'] == 'success'
        assert len(data.inventory) == 2
        
        # Verify item is actually deleted
        assert not any(item['id'] == 2 for item in data.inventory)
    
    def test_delete_item_not_found(self, client):
        """Test deleting non-existent item"""
        response = client.delete('/inventory/999')
        assert response.status_code == 404
        
        json_data = response.get_json()
        assert json_data['status'] == 'error'
