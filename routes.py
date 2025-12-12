# API routes for inventory management
# RESTful endpoints: GET, POST, PATCH, DELETE
from flask import Blueprint, request, jsonify
import data
import api_client

inventory_bp = Blueprint('inventory', __name__)


@inventory_bp.route('/inventory', methods=['GET'])
def get_all_inventory():
    """
    GET /inventory → Fetch all items
    Returns all items in the inventory
    """
    return jsonify({
        "status": "success",
        "count": len(data.inventory),
        "data": data.inventory
    }), 200


@inventory_bp.route('/inventory/<int:item_id>', methods=['GET'])
def get_inventory_item(item_id):
    """
    GET /inventory/<id> → Fetch a single item
    Returns a specific item by ID
    """
    item = next((item for item in data.inventory if item['id'] == item_id), None)
    
    if item is None:
        return jsonify({
            "status": "error",
            "message": f"Item with id {item_id} not found"
        }), 404
    
    return jsonify({
        "status": "success",
        "data": item
    }), 200


@inventory_bp.route('/inventory', methods=['POST'])
def add_inventory_item():
    """
    POST /inventory → Add a new item
    Creates a new inventory item
    Expected JSON body: product_name, brands, ingredients_text, quantity, price, barcode
    Optional: fetch_from_api (boolean) - if true and barcode is provided, fetch data from OpenFoodFacts
    """
    if not request.json:
        return jsonify({
            "status": "error",
            "message": "Request must be JSON"
        }), 400
    
    # Check if we should fetch data from OpenFoodFacts API
    fetch_from_api = request.json.get('fetch_from_api', False)
    barcode = request.json.get('barcode', '')
    
    # If fetch_from_api is true and barcode is provided, get data from API
    if fetch_from_api and barcode:
        api_data = api_client.search_product_by_barcode(barcode)
        
        if api_data:
            # Merge API data with user provided data (user data takes precedence)
            new_item = {
                "id": data.next_id,
                "product_name": request.json.get('product_name', api_data.get('product_name', '')),
                "brands": request.json.get('brands', api_data.get('brands', '')),
                "ingredients_text": request.json.get('ingredients_text', api_data.get('ingredients_text', '')),
                "quantity": request.json.get('quantity', 0),
                "price": request.json.get('price', 0.0),
                "barcode": barcode
            }
        else:
            return jsonify({
                "status": "error",
                "message": f"Product with barcode {barcode} not found in OpenFoodFacts API"
            }), 404
    else:
        # Standard validation for manual entry
        required_fields = ['product_name', 'brands', 'quantity', 'price']
        missing_fields = [field for field in required_fields if field not in request.json]
        
        if missing_fields:
            return jsonify({
                "status": "error",
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400
        
        # Create new item manually
        new_item = {
            "id": data.next_id,
            "product_name": request.json['product_name'],
            "brands": request.json['brands'],
            "ingredients_text": request.json.get('ingredients_text', ''),
            "quantity": request.json['quantity'],
            "price": request.json['price'],
            "barcode": barcode
        }
    
    data.inventory.append(new_item)
    data.next_id += 1
    
    return jsonify({
        "status": "success",
        "message": "Item added successfully",
        "data": new_item
    }), 201


@inventory_bp.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_inventory_item(item_id):
    """
    PATCH /inventory/<id> → Update an item
    Updates specific fields of an inventory item
    """
    item = next((item for item in data.inventory if item['id'] == item_id), None)
    
    if item is None:
        return jsonify({
            "status": "error",
            "message": f"Item with id {item_id} not found"
        }), 404
    
    if not request.json:
        return jsonify({
            "status": "error",
            "message": "Request must be JSON"
        }), 400
    
    # Update only provided fields
    updatable_fields = ['product_name', 'brands', 'ingredients_text', 'quantity', 'price', 'barcode']
    
    for field in updatable_fields:
        if field in request.json:
            item[field] = request.json[field]
    
    return jsonify({
        "status": "success",
        "message": "Item updated successfully",
        "data": item
    }), 200


@inventory_bp.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_inventory_item(item_id):
    """
    DELETE /inventory/<id> → Remove an item
    Deletes an item from the inventory
    """
    item = next((item for item in data.inventory if item['id'] == item_id), None)
    
    if item is None:
        return jsonify({
            "status": "error",
            "message": f"Item with id {item_id} not found"
        }), 404
    
    data.inventory.remove(item)
    
    return jsonify({
        "status": "success",
        "message": f"Item with id {item_id} deleted successfully"
    }), 200


@inventory_bp.route('/api/search/barcode/<barcode>', methods=['GET'])
def search_by_barcode(barcode):
    """
    GET /api/search/barcode/<barcode> → Search OpenFoodFacts by barcode
    Returns product information from OpenFoodFacts API
    """
    if not barcode:
        return jsonify({
            "status": "error",
            "message": "Barcode is required"
        }), 400
    
    product_data = api_client.search_product_by_barcode(barcode)
    
    if product_data is None:
        return jsonify({
            "status": "error",
            "message": f"Product with barcode {barcode} not found"
        }), 404
    
    return jsonify({
        "status": "success",
        "data": product_data
    }), 200


@inventory_bp.route('/api/search/name', methods=['GET'])
def search_by_name():
    """
    GET /api/search/name?q=<product_name>&page=<page>&page_size=<size>
    Search OpenFoodFacts by product name
    Returns list of matching products
    """
    product_name = request.args.get('q')
    
    if not product_name:
        return jsonify({
            "status": "error",
            "message": "Query parameter 'q' is required"
        }), 400
    
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    
    search_results = api_client.search_products_by_name(product_name, page, page_size)
    
    if search_results is None:
        return jsonify({
            "status": "error",
            "message": "Error searching for products"
        }), 500
    
    return jsonify({
        "status": "success",
        "data": search_results
    }), 200


@inventory_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "status": "error",
        "message": "Resource not found"
    }), 404


@inventory_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500
