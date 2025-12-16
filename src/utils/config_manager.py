"""Configuration Manager for EyeCare AI Agent"""
import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional
from dotenv import load_dotenv
import os


class ConfigManager:
    """Professional configuration management with validation"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        
        # Load environment variables
        load_dotenv()
        
        # Set config path
        if config_path:
            self.config_path = Path(config_path)
        else:
            self.config_path = Path(__file__).parent.parent.parent / 'config.json'
        
        # User config directory
        self.user_config_dir = Path.home() / '.eyecare_agent'
        self.user_config_dir.mkdir(parents=True, exist_ok=True)
        
        self.user_config_path = self.user_config_dir / 'user_config.json'
        
        # Load configurations
        self.config = self._load_config()
        self.user_config = self._load_user_config()
        
    def _load_config(self) -> Dict:
        """Load main configuration file"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.logger.info(f"Loaded config from {self.config_path}")
                    return config
            else:
                self.logger.warning(f"Config file not found: {self.config_path}")
                return self._get_default_config()
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            return self._get_default_config()
    
    def _load_user_config(self) -> Dict:
        """Load user-specific configuration"""
        try:
            if self.user_config_path.exists():
                with open(self.user_config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            self.logger.error(f"Error loading user config: {e}")
            return {}
    
    def _get_default_config(self) -> Dict:
        """Return default configuration"""
        return {
            "app_settings": {
                "app_name": "EyeCare AI Pro",
                "version": "1.0.0",
                "minimize_to_tray": True
            },
            "break_settings": {
                "work_interval_minutes": 20,
                "break_duration_seconds": 20,
                "enable_breaks": True
            },
            "light_monitoring": {
                "enabled": True,
                "camera_index": 0,
                "check_interval_seconds": 30
            },
            "ai_settings": {
                "enabled": True,
                "model": "meta-llama/llama-3.1-8b-instruct"
            },
            "ui_settings": {
                "theme": "dark",
                "window_width": 900,
                "window_height": 700
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value with dot notation support"""
        # Check user config first (overrides)
        value = self._get_nested(self.user_config, key)
        if value is not None:
            return value
        
        # Then check main config
        value = self._get_nested(self.config, key)
        if value is not None:
            return value
        
        # Check environment variables
        env_key = key.upper().replace('.', '_')
        env_value = os.getenv(env_key)
        if env_value is not None:
            return env_value
        
        return default
    
    def _get_nested(self, data: Dict, key: str) -> Any:
        """Get nested dictionary value using dot notation"""
        keys = key.split('.')
        value = data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return None
        
        return value
    
    def set(self, key: str, value: Any, save: bool = True):
        """Set configuration value"""
        keys = key.split('.')
        config = self.user_config
        
        # Navigate to nested location
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set value
        config[keys[-1]] = value
        
        if save:
            self.save_user_config()
    
    def save_user_config(self):
        """Save user configuration to file"""
        try:
            with open(self.user_config_path, 'w', encoding='utf-8') as f:
                json.dump(self.user_config, f, indent=2, ensure_ascii=False)
            self.logger.info("User config saved successfully")
        except Exception as e:
            self.logger.error(f"Error saving user config: {e}")
    
    def get_api_key(self) -> Optional[str]:
        """Get OpenRouter API key"""
        return os.getenv('OPENROUTER_API_KEY') or self.get('ai_settings.api_key')
    
    def get_model(self) -> str:
        """Get AI model name"""
        return os.getenv('OPENROUTER_MODEL') or self.get('ai_settings.model', 'meta-llama/llama-3.1-8b-instruct')
    
    def reset_to_defaults(self):
        """Reset user config to defaults"""
        self.user_config = {}
        self.save_user_config()
        self.logger.info("Configuration reset to defaults")
