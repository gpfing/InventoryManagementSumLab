# Unit tests for OpenFoodFacts API interactions
import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import api_client


class TestSearchProductByBarcode:
    """Test search_product_by_barcode function"""
    
    @patch('api_client.requests.get')
    def test_search_by_barcode_success(self, mock_get):
        """Test successful product search by barcode"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'status': 1,
            'product': {
                'product_name': 'Test Product',
                'brands': 'Test Brand',
                'ingredients_text': 'Test ingredients',
                'categories': 'Food',
                'image_url': 'http://example.com/image.jpg'
            }
        }
        mock_get.return_value = mock_response
        
        result = api_client.search_product_by_barcode('123456789')
        
        assert result is not None
        assert result['product_name'] == 'Test Product'
        assert result['brands'] == 'Test Brand'
        assert result['barcode'] == '123456789'
        assert result['ingredients_text'] == 'Test ingredients'
        assert result['categories'] == 'Food'
        assert result['image_url'] == 'http://example.com/image.jpg'
    
    @patch('api_client.requests.get')
    def test_search_by_barcode_not_found(self, mock_get):
        """Test product not found by barcode"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'status': 0
        }
        mock_get.return_value = mock_response
        
        result = api_client.search_product_by_barcode('999999999')
        
        assert result is None
    
    @patch('api_client.requests.get')
    def test_search_by_barcode_api_error(self, mock_get):
        """Test handling API error"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        
        result = api_client.search_product_by_barcode('123456789')
        
        assert result is None
    
    @patch('api_client.requests.get')
    def test_search_by_barcode_connection_error(self, mock_get):
        """Test handling connection error"""
        mock_get.side_effect = api_client.requests.exceptions.ConnectionError()
        
        result = api_client.search_product_by_barcode('123456789')
        
        assert result is None
    
    @patch('api_client.requests.get')
    def test_search_by_barcode_timeout(self, mock_get):
        """Test handling timeout error"""
        mock_get.side_effect = api_client.requests.exceptions.Timeout()
        
        result = api_client.search_product_by_barcode('123456789')
        
        assert result is None
    
    @patch('api_client.requests.get')
    def test_search_by_barcode_missing_fields(self, mock_get):
        """Test handling missing fields in API response"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'status': 1,
            'product': {
                'product_name': 'Minimal Product'
                # Other fields missing
            }
        }
        mock_get.return_value = mock_response
        
        result = api_client.search_product_by_barcode('123456789')
        
        assert result is not None
        assert result['product_name'] == 'Minimal Product'
        assert result['brands'] == ''
        assert result['ingredients_text'] == ''
        assert result['categories'] == ''


class TestSearchProductsByName:
    """Test search_products_by_name function"""
    
    @patch('api_client.requests.get')
    def test_search_by_name_success(self, mock_get):
        """Test successful product search by name"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'count': 2,
            'page': 1,
            'page_size': 10,
            'products': [
                {
                    'product_name': 'Product 1',
                    'brands': 'Brand 1',
                    'ingredients_text': 'Ingredients 1',
                    'code': '111',
                    'categories': 'Food',
                    'image_url': 'http://example.com/1.jpg'
                },
                {
                    'product_name': 'Product 2',
                    'brands': 'Brand 2',
                    'ingredients_text': 'Ingredients 2',
                    'code': '222',
                    'categories': 'Beverage',
                    'image_url': 'http://example.com/2.jpg'
                }
            ]
        }
        mock_get.return_value = mock_response
        
        result = api_client.search_products_by_name('milk')
        
        assert result is not None
        assert result['count'] == 2
        assert result['page'] == 1
        assert len(result['products']) == 2
        assert result['products'][0]['product_name'] == 'Product 1'
        assert result['products'][0]['barcode'] == '111'
        assert result['products'][1]['product_name'] == 'Product 2'
    
    @patch('api_client.requests.get')
    def test_search_by_name_no_results(self, mock_get):
        """Test search with no results"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'count': 0,
            'page': 1,
            'page_size': 10,
            'products': []
        }
        mock_get.return_value = mock_response
        
        result = api_client.search_products_by_name('nonexistentproduct')
        
        assert result is not None
        assert result['count'] == 0
        assert result['products'] == []
    
    @patch('api_client.requests.get')
    def test_search_by_name_with_pagination(self, mock_get):
        """Test search with custom pagination"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'count': 50,
            'page': 2,
            'page_size': 5,
            'products': []
        }
        mock_get.return_value = mock_response
        
        result = api_client.search_products_by_name('milk', page=2, page_size=5)
        
        assert result is not None
        assert result['page'] == 2
        assert result['page_size'] == 5
        
        # Verify correct parameters were passed
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert call_args[1]['params']['page'] == 2
        assert call_args[1]['params']['page_size'] == 5
    
    @patch('api_client.requests.get')
    def test_search_by_name_api_error(self, mock_get):
        """Test handling API error"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        
        result = api_client.search_products_by_name('milk')
        
        assert result is None
    
    @patch('api_client.requests.get')
    def test_search_by_name_connection_error(self, mock_get):
        """Test handling connection error"""
        mock_get.side_effect = api_client.requests.exceptions.ConnectionError()
        
        result = api_client.search_products_by_name('milk')
        
        assert result is None
