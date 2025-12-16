"""Unit tests for AI Integration"""
import unittest
import asyncio
from src.ai.openrouter_client import OpenRouterClient, AIResponse


class TestAIIntegration(unittest.TestCase):
    """Test AI integration"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = OpenRouterClient(api_key=None)  # Will use fallback
    
    def test_client_initialization(self):
        """Test client initialization"""
        self.assertIsNotNone(self.client)
        self.assertIsNotNone(self.client.model)
    
    def test_fallback_recommendation(self):
        """Test fallback recommendations"""
        light_data = {'lux': 100, 'status': 'low'}
        user_context = {'screen_brightness': 50}
        
        result = self.client._get_fallback_recommendation(light_data, user_context)
        
        self.assertIsInstance(result, AIResponse)
        self.assertIsNotNone(result.recommendation)
        self.assertGreater(len(result.action_items), 0)
    
    def test_fallback_strain_advice(self):
        """Test fallback strain advice"""
        result = self.client._get_fallback_strain_advice(
            screen_time=10.0,
            break_compliance=40.0,
            symptoms=['eye fatigue', 'headache']
        )
        
        self.assertIsInstance(result, AIResponse)
        self.assertEqual(result.warning_level, 'high')
    
    def test_fallback_exercise(self):
        """Test fallback exercise recommendation"""
        exercise = self.client._get_fallback_exercise(
            time_since_break=35,
            strain_level='high'
        )
        
        self.assertIsInstance(exercise, str)
        self.assertGreater(len(exercise), 0)
    
    def test_cache_functionality(self):
        """Test response caching"""
        light_data = {'lux': 300, 'status': 'optimal'}
        user_context = {}
        
        # First call
        result1 = self.client._get_fallback_recommendation(light_data, user_context)
        cache_key = 'light_300'
        self.client.cache[cache_key] = (result1, result1.timestamp)
        
        # Check cache
        self.assertIn(cache_key, self.client.cache)
        
        # Clear cache
        self.client.clear_cache()
        self.assertEqual(len(self.client.cache), 0)


if __name__ == '__main__':
    unittest.main()
