# OpenFoodFacts API integration
# Functions to fetch product details from external API
import requests

OPENFOODFACTS_API_BASE = "https://world.openfoodfacts.net/api/v2"


def search_product_by_barcode(barcode):
    """
    Search for a product by barcode using OpenFoodFacts API
    """
    try:
        url = f"{OPENFOODFACTS_API_BASE}/product/{barcode}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if product was found
            if data.get('status') == 1 and 'product' in data:
                product = data['product']
                
                # Extract relevant fields
                return {
                    'product_name': product.get('product_name', ''),
                    'brands': product.get('brands', ''),
                    'ingredients_text': product.get('ingredients_text', ''),
                    'barcode': barcode,
                    'categories': product.get('categories', ''),
                    'image_url': product.get('image_url', '')
                }
            else:
                return None
        else:
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching product data: {e}")
        return None


def search_products_by_name(product_name, page=1, page_size=10):
    """
    Search for products by name using OpenFoodFacts API
    """
    try:
        url = f"{OPENFOODFACTS_API_BASE}/search"
        params = {
            'search_terms': product_name,
            'page': page,
            'page_size': page_size,
            'json': 1
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            products = []
            for product in data.get('products', []):
                products.append({
                    'product_name': product.get('product_name', ''),
                    'brands': product.get('brands', ''),
                    'ingredients_text': product.get('ingredients_text', ''),
                    'barcode': product.get('code', ''),
                    'categories': product.get('categories', ''),
                    'image_url': product.get('image_url', '')
                })
            
            return {
                'count': data.get('count', 0),
                'page': data.get('page', 1),
                'page_size': data.get('page_size', page_size),
                'products': products
            }
        else:
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error searching products: {e}")
        return None
