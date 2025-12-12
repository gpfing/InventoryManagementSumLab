# CLI frontend to interact with the Flask API
# Allows users to add, view, update, delete inventory items
import requests
import sys

# API base URL
API_BASE_URL = "http://localhost:5000"


def print_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("="*50)
    print("1. View all inventory items")
    print("2. View single inventory item")
    print("3. Add new inventory item")
    print("4. Update inventory item")
    print("5. Delete inventory item")
    print("6. Search product on OpenFoodFacts (by barcode)")
    print("7. Search product on OpenFoodFacts (by name)")
    print("8. Exit")
    print("="*50)


def get_user_choice():
    """Get and validate user menu choice"""
    try:
        choice = input("\nEnter your choice (1-8): ").strip()
        return choice
    except (EOFError, KeyboardInterrupt):
        print("\n\nExiting...")
        sys.exit(0)


def view_all_inventory():
    """View all inventory items"""
    print("\n--- All Inventory Items ---")
    try:
        response = requests.get(f"{API_BASE_URL}/inventory")
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('data', [])
            
            if not items:
                print("No items in inventory.")
                return
            
            print(f"\nTotal items: {data.get('count', 0)}\n")
            for item in items:
                print(f"ID: {item['id']}")
                print(f"  Name: {item['product_name']}")
                print(f"  Brand: {item['brands']}")
                print(f"  Quantity: {item['quantity']}")
                print(f"  Price: ${item['price']:.2f}")
                print(f"  Barcode: {item['barcode']}")
                print("-" * 40)
        else:
            print(f"Error: {response.json().get('message', 'Unknown error')}")
    
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to API server. Make sure the Flask app is running.")
    except Exception as e:
        print(f"Error: {e}")


def view_single_item():
    """View a single inventory item by ID"""
    print("\n--- View Single Item ---")
    try:
        item_id = input("Enter item ID: ").strip()
        
        if not item_id.isdigit():
            print("Error: Item ID must be a number.")
            return
        
        response = requests.get(f"{API_BASE_URL}/inventory/{item_id}")
        
        if response.status_code == 200:
            item = response.json().get('data', {})
            print("\nItem Details:")
            print(f"ID: {item['id']}")
            print(f"Name: {item['product_name']}")
            print(f"Brand: {item['brands']}")
            print(f"Ingredients: {item['ingredients_text']}")
            print(f"Quantity: {item['quantity']}")
            print(f"Price: ${item['price']:.2f}")
            print(f"Barcode: {item['barcode']}")
        else:
            print(f"Error: {response.json().get('message', 'Item not found')}")
    
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to API server. Make sure the Flask app is running.")
    except Exception as e:
        print(f"Error: {e}")


def add_inventory_item():
    """Add a new inventory item"""
    print("\n--- Add New Inventory Item ---")
    print("Choose option:")
    print("1. Add manually")
    print("2. Add from OpenFoodFacts (by barcode)")
    
    option = input("Enter choice (1-2): ").strip()
    
    try:
        if option == "1":
            # Manual entry
            product_name = input("Product name: ").strip()
            brands = input("Brand: ").strip()
            ingredients_text = input("Ingredients (optional): ").strip()
            quantity = input("Quantity: ").strip()
            price = input("Price: ").strip()
            barcode = input("Barcode (optional): ").strip()
            
            if not product_name or not brands or not quantity or not price:
                print("Error: Product name, brand, quantity, and price are required.")
                return
            
            try:
                quantity = int(quantity)
                price = float(price)
            except ValueError:
                print("Error: Quantity must be an integer and price must be a number.")
                return
            
            payload = {
                "product_name": product_name,
                "brands": brands,
                "ingredients_text": ingredients_text,
                "quantity": quantity,
                "price": price,
                "barcode": barcode
            }
            
        elif option == "2":
            # Add from API
            barcode = input("Enter barcode: ").strip()
            quantity = input("Quantity: ").strip()
            price = input("Price: ").strip()
            
            if not barcode or not quantity or not price:
                print("Error: Barcode, quantity, and price are required.")
                return
            
            try:
                quantity = int(quantity)
                price = float(price)
            except ValueError:
                print("Error: Quantity must be an integer and price must be a number.")
                return
            
            payload = {
                "barcode": barcode,
                "quantity": quantity,
                "price": price,
                "fetch_from_api": True
            }
        else:
            print("Invalid option.")
            return
        
        response = requests.post(f"{API_BASE_URL}/inventory", json=payload)
        
        if response.status_code == 201:
            data = response.json()
            print(f"\n✓ {data.get('message', 'Success')}")
            item = data.get('data', {})
            print(f"Added item: {item.get('product_name')} (ID: {item.get('id')})")
        else:
            print(f"Error: {response.json().get('message', 'Failed to add item')}")
    
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to API server. Make sure the Flask app is running.")
    except Exception as e:
        print(f"Error: {e}")


def update_inventory_item():
    """Update an existing inventory item"""
    print("\n--- Update Inventory Item ---")
    try:
        item_id = input("Enter item ID to update: ").strip()
        
        if not item_id.isdigit():
            print("Error: Item ID must be a number.")
            return
        
        print("\nEnter new values (press Enter to skip):")
        product_name = input("Product name: ").strip()
        brands = input("Brand: ").strip()
        ingredients_text = input("Ingredients: ").strip()
        quantity = input("Quantity: ").strip()
        price = input("Price: ").strip()
        barcode = input("Barcode: ").strip()
        
        payload = {}
        if product_name:
            payload['product_name'] = product_name
        if brands:
            payload['brands'] = brands
        if ingredients_text:
            payload['ingredients_text'] = ingredients_text
        if quantity:
            try:
                payload['quantity'] = int(quantity)
            except ValueError:
                print("Error: Quantity must be an integer.")
                return
        if price:
            try:
                payload['price'] = float(price)
            except ValueError:
                print("Error: Price must be a number.")
                return
        if barcode:
            payload['barcode'] = barcode
        
        if not payload:
            print("No updates provided.")
            return
        
        response = requests.patch(f"{API_BASE_URL}/inventory/{item_id}", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✓ {data.get('message', 'Success')}")
            item = data.get('data', {})
            print(f"Updated item: {item.get('product_name')} (ID: {item.get('id')})")
        else:
            print(f"Error: {response.json().get('message', 'Failed to update item')}")
    
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to API server. Make sure the Flask app is running.")
    except Exception as e:
        print(f"Error: {e}")


def delete_inventory_item():
    """Delete an inventory item"""
    print("\n--- Delete Inventory Item ---")
    try:
        item_id = input("Enter item ID to delete: ").strip()
        
        if not item_id.isdigit():
            print("Error: Item ID must be a number.")
            return
        
        confirm = input(f"Are you sure you want to delete item {item_id}? (y/n): ").strip().lower()
        
        if confirm != 'y':
            print("Delete cancelled.")
            return
        
        response = requests.delete(f"{API_BASE_URL}/inventory/{item_id}")
        
        if response.status_code == 200:
            print(f"\n✓ {response.json().get('message', 'Item deleted successfully')}")
        else:
            print(f"Error: {response.json().get('message', 'Failed to delete item')}")
    
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to API server. Make sure the Flask app is running.")
    except Exception as e:
        print(f"Error: {e}")


def search_by_barcode():
    """Search OpenFoodFacts by barcode"""
    print("\n--- Search OpenFoodFacts by Barcode ---")
    try:
        barcode = input("Enter barcode: ").strip()
        
        if not barcode:
            print("Error: Barcode is required.")
            return
        
        response = requests.get(f"{API_BASE_URL}/api/search/barcode/{barcode}")
        
        if response.status_code == 200:
            data = response.json().get('data', {})
            print("\nProduct found:")
            print(f"Name: {data.get('product_name')}")
            print(f"Brand: {data.get('brands')}")
            print(f"Ingredients: {data.get('ingredients_text')}")
            print(f"Categories: {data.get('categories')}")
            print(f"Barcode: {data.get('barcode')}")
            if data.get('image_url'):
                print(f"Image: {data.get('image_url')}")
        else:
            print(f"Error: {response.json().get('message', 'Product not found')}")
    
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to API server. Make sure the Flask app is running.")
    except Exception as e:
        print(f"Error: {e}")


def search_by_name():
    """Search OpenFoodFacts by product name"""
    print("\n--- Search OpenFoodFacts by Name ---")
    try:
        name = input("Enter product name: ").strip()
        
        if not name:
            print("Error: Product name is required.")
            return
        
        response = requests.get(f"{API_BASE_URL}/api/search/name", params={'q': name})
        
        if response.status_code == 200:
            data = response.json().get('data', {})
            products = data.get('products', [])
            
            if not products:
                print("No products found.")
                return
            
            print(f"\nFound {data.get('count', 0)} products (showing {len(products)}):\n")
            for idx, product in enumerate(products, 1):
                print(f"{idx}. {product.get('product_name')}")
                print(f"   Brand: {product.get('brands')}")
                print(f"   Barcode: {product.get('barcode')}")
                print(f"   Categories: {product.get('categories')}")
                print("-" * 40)
        else:
            print(f"Error: {response.json().get('message', 'Search failed')}")
    
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to API server. Make sure the Flask app is running.")
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Main CLI loop"""
    print("\nWelcome to the Inventory Management System!")
    print("Make sure the Flask API server is running on http://localhost:5000")
    
    while True:
        print_menu()
        choice = get_user_choice()
        
        if choice == '1':
            view_all_inventory()
        elif choice == '2':
            view_single_item()
        elif choice == '3':
            add_inventory_item()
        elif choice == '4':
            update_inventory_item()
        elif choice == '5':
            delete_inventory_item()
        elif choice == '6':
            search_by_barcode()
        elif choice == '7':
            search_by_name()
        elif choice == '8':
            print("\nThank you for using the Inventory Management System!")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")
        
        input("\nPress Enter to continue...")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
