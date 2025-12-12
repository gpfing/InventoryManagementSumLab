# Unit tests for CLI commands
import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from io import StringIO

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import cli


class TestViewAllInventory:
    """Test view_all_inventory function"""
    
    @patch('cli.requests.get')
    def test_view_all_inventory_success(self, mock_get):
        """Test viewing all inventory items successfully"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'status': 'success',
            'count': 2,
            'data': [
                {'id': 1, 'product_name': 'Product 1', 'brands': 'Brand 1', 
                 'quantity': 10, 'price': 5.99, 'barcode': '123'},
                {'id': 2, 'product_name': 'Product 2', 'brands': 'Brand 2', 
                 'quantity': 20, 'price': 9.99, 'barcode': '456'}
            ]
        }
        mock_get.return_value = mock_response
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            cli.view_all_inventory()
            output = fake_out.getvalue()
            assert 'Product 1' in output
            assert 'Product 2' in output
            assert 'Total items: 2' in output
    
    @patch('cli.requests.get')
    def test_view_all_inventory_empty(self, mock_get):
        """Test viewing inventory when empty"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'status': 'success',
            'count': 0,
            'data': []
        }
        mock_get.return_value = mock_response
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            cli.view_all_inventory()
            output = fake_out.getvalue()
            assert 'No items in inventory' in output
    
    @patch('cli.requests.get')
    def test_view_all_inventory_connection_error(self, mock_get):
        """Test handling connection error"""
        mock_get.side_effect = cli.requests.exceptions.ConnectionError()
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            cli.view_all_inventory()
            output = fake_out.getvalue()
            assert 'Cannot connect to API server' in output


class TestViewSingleItem:
    """Test view_single_item function"""
    
    @patch('cli.requests.get')
    @patch('builtins.input', return_value='1')
    def test_view_single_item_success(self, mock_input, mock_get):
        """Test viewing a single item successfully"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'status': 'success',
            'data': {
                'id': 1, 'product_name': 'Test Product', 'brands': 'Test Brand',
                'ingredients_text': 'Test ingredients', 'quantity': 10, 
                'price': 5.99, 'barcode': '123'
            }
        }
        mock_get.return_value = mock_response
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            cli.view_single_item()
            output = fake_out.getvalue()
            assert 'Test Product' in output
            assert 'Test Brand' in output
    
    @patch('builtins.input', return_value='abc')
    def test_view_single_item_invalid_id(self, mock_input):
        """Test viewing item with invalid ID"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            cli.view_single_item()
            output = fake_out.getvalue()
            assert 'must be a number' in output


class TestDeleteInventoryItem:
    """Test delete_inventory_item function"""
    
    @patch('cli.requests.delete')
    @patch('builtins.input', side_effect=['1', 'y'])
    def test_delete_item_success(self, mock_input, mock_delete):
        """Test deleting an item successfully"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'status': 'success',
            'message': 'Item deleted successfully'
        }
        mock_delete.return_value = mock_response
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            cli.delete_inventory_item()
            output = fake_out.getvalue()
            assert 'deleted successfully' in output
    
    @patch('builtins.input', side_effect=['1', 'n'])
    def test_delete_item_cancelled(self, mock_input):
        """Test cancelling delete operation"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            cli.delete_inventory_item()
            output = fake_out.getvalue()
            assert 'cancelled' in output


class TestSearchByBarcode:
    """Test search_by_barcode function"""
    
    @patch('cli.requests.get')
    @patch('builtins.input', return_value='123456')
    def test_search_by_barcode_success(self, mock_input, mock_get):
        """Test searching by barcode successfully"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'status': 'success',
            'data': {
                'product_name': 'Found Product',
                'brands': 'Found Brand',
                'ingredients_text': 'Ingredients',
                'categories': 'Food',
                'barcode': '123456'
            }
        }
        mock_get.return_value = mock_response
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            cli.search_by_barcode()
            output = fake_out.getvalue()
            assert 'Found Product' in output
            assert 'Found Brand' in output
    
    @patch('cli.requests.get')
    @patch('builtins.input', return_value='999999')
    def test_search_by_barcode_not_found(self, mock_input, mock_get):
        """Test searching for non-existent barcode"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            'status': 'error',
            'message': 'Product not found'
        }
        mock_get.return_value = mock_response
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            cli.search_by_barcode()
            output = fake_out.getvalue()
            assert 'not found' in output


class TestSearchByName:
    """Test search_by_name function"""
    
    @patch('cli.requests.get')
    @patch('builtins.input', return_value='milk')
    def test_search_by_name_success(self, mock_input, mock_get):
        """Test searching by name successfully"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'status': 'success',
            'data': {
                'count': 2,
                'products': [
                    {'product_name': 'Almond Milk', 'brands': 'Brand A', 
                     'barcode': '111', 'categories': 'Dairy'},
                    {'product_name': 'Soy Milk', 'brands': 'Brand B', 
                     'barcode': '222', 'categories': 'Dairy'}
                ]
            }
        }
        mock_get.return_value = mock_response
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            cli.search_by_name()
            output = fake_out.getvalue()
            assert 'Almond Milk' in output
            assert 'Soy Milk' in output
            assert 'Found 2 products' in output
