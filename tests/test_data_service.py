import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.data_service import DataService

class TestDataService(unittest.TestCase):
    """Test cases for DataService class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_session = Mock()
        
    @patch('services.data_service.sessionmaker')
    @patch('services.data_service.create_engine')
    def test_data_service_initialization(self, mock_engine, mock_sessionmaker):
        """Test DataService initialization"""
        mock_sessionmaker.return_value = Mock(return_value=self.mock_session)
        
        service = DataService()
        
        self.assertIsNotNone(service)
        mock_engine.assert_called_once()
        mock_sessionmaker.assert_called_once()
    
    @patch('services.data_service.sessionmaker')
    @patch('services.data_service.create_engine')
    def test_get_customer_count(self, mock_engine, mock_sessionmaker):
        """Test get_customer_count method"""
        mock_sessionmaker.return_value = Mock(return_value=self.mock_session)
        self.mock_session.query.return_value.count.return_value = 91
        
        service = DataService()
        count = service.get_customer_count()
        
        self.assertEqual(count, 91)
    
    @patch('services.data_service.sessionmaker')
    @patch('services.data_service.create_engine')
    def test_get_total_revenue(self, mock_engine, mock_sessionmaker):
        """Test get_total_revenue method"""
        mock_sessionmaker.return_value = Mock(return_value=self.mock_session)
        self.mock_session.query.return_value.scalar.return_value = 1354458.59
        
        service = DataService()
        revenue = service.get_total_revenue()
        
        self.assertEqual(revenue, 1354458.59)

if __name__ == '__main__':
    unittest.main()
