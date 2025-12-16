"""Unit tests for Light Detection"""
import unittest
from src.hardware.camera_manager import AmbientLightDetector


class TestLightDetection(unittest.TestCase):
    """Test ambient light detection"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.detector = AmbientLightDetector(camera_index=0)
    
    def test_initialization(self):
        """Test detector initialization"""
        self.assertIsNotNone(self.detector)
        self.assertEqual(self.detector.camera_index, 0)
    
    def test_light_classification(self):
        """Test light level classification"""
        # Test very low
        status = self.detector._classify_light_level(50, 0.1, 30)
        self.assertEqual(status, 'very_low')
        
        # Test optimal
        status = self.detector._classify_light_level(400, 0.05, 40)
        self.assertEqual(status, 'optimal')
        
        # Test high
        status = self.detector._classify_light_level(1200, 0.4, 60)
        self.assertEqual(status, 'high')
    
    def test_fallback_estimation(self):
        """Test time-based fallback"""
        lux, status, metadata = self.detector._estimate_light_fallback()
        
        self.assertIsInstance(lux, float)
        self.assertIsInstance(status, str)
        self.assertIn('source', metadata)
        self.assertEqual(metadata['source'], 'time_based_fallback')
    
    def tearDown(self):
        """Clean up"""
        self.detector.release()


if __name__ == '__main__':
    unittest.main()
