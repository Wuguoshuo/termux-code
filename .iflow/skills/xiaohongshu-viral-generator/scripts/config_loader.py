"""
Configuration Loader for Xiaohongshu Viral Generator
Loads and validates configuration from config.yaml
"""

import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path


class Config:
    """Configuration manager for the viral generator."""
    
    def __init__(self, config_path: str = None):
        """
        Initialize configuration loader.
        
        Args:
            config_path: Path to config.yaml file
        """
        self.config_path = config_path or self._find_config()
        self._config: Dict[str, Any] = {}
        self._load_config()
    
    def _find_config(self) -> str:
        """Find config file in skill directory."""
        script_dir = Path(__file__).parent
        skill_dir = script_dir.parent
        config_path = skill_dir / "scripts" / "config.yaml"
        
        if config_path.exists():
            return str(config_path)
        
        return "config.yaml"
    
    def _load_config(self) -> None:
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f) or {}
        except FileNotFoundError:
            self._config = self._get_default_config()
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing config file: {e}")
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            'schedule': {
                'time': '08:00',
                'timezone': 'Asia/Shanghai',
                'auto_publish': False
            },
            'topics': {
                'categories': ['职场效率', '生活美学', '学习成长', '时间管理', '个人成长'],
                'daily_count': 1,
                'rotation_strategy': 'sequential'
            },
            'ai_image': {
                'provider': 'openai',
                'openai': {
                    'model': 'dall-e-3',
                    'size': '1024x1536',
                    'quality': 'standard'
                },
                'styles': ['modern minimalist', 'cute and fresh', 'warm vintage', 'tech blue', 'nature green']
            },
            'publishing': {
                'enabled': False,
                'auto_publish': False,
                'save_as_draft': True
            },
            'output': {
                'directory': './output',
                'format': 'markdown',
                'save_images': True,
                'image_quality': 95
            },
            'debug': {
                'preview_mode': True,
                'log_level': 'INFO'
            }
        }
    
    # Property getters
    @property
    def schedule(self) -> Dict[str, Any]:
        return self._config.get('schedule', {})
    
    @property
    def topics(self) -> Dict[str, Any]:
        return self._config.get('topics', {})
    
    @property
    def ai_image(self) -> Dict[str, Any]:
        return self._config.get('ai_image', {})
    
    @property
    def publishing(self) -> Dict[str, Any]:
        return self._config.get('publishing', {})
    
    @property
    def output(self) -> Dict[str, Any]:
        return self._config.get('output', {})
    
    @property
    def debug(self) -> Dict[str, Any]:
        return self._config.get('debug', {})
    
    # Schedule methods
    def get_schedule_time(self) -> str:
        return self.schedule.get('time', '08:00')
    
    def is_auto_publish(self) -> bool:
        return self.schedule.get('auto_publish', False)
    
    # Topics methods
    def get_topics(self) -> list:
        return self.topics.get('categories', ['职场效率'])
    
    def get_daily_count(self) -> int:
        return self.topics.get('daily_count', 1)
    
    # AI Image methods
    def get_ai_provider(self) -> str:
        return self.ai_image.get('provider', 'openai')
    
    def get_openai_config(self) -> Dict[str, Any]:
        return self.ai_image.get('openai', {})
    
    def get_image_styles(self) -> list:
        return self.ai_image.get('styles', ['modern minimalist'])
    
    # Output methods
    def get_output_dir(self) -> str:
        return self.output.get('directory', './output')
    
    def should_save_images(self) -> bool:
        return self.output.get('save_images', True)
    
    # Debug methods
    def is_preview_mode(self) -> bool:
        return self.debug.get('preview_mode', True)
    
    def get_log_level(self) -> str:
        return self.debug.get('log_level', 'INFO')
    
    # Utility methods
    def reload(self) -> None:
        """Reload configuration from file."""
        self._load_config()
    
    def save(self, path: str = None) -> None:
        """Save current configuration to file."""
        save_path = path or self.config_path
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        with open(save_path, 'w', encoding='utf-8') as f:
            yaml.dump(self._config, f, allow_unicode=True, default_flow_style=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary."""
        return self._config.copy()


# Singleton instance
_config_instance: Optional[Config] = None


def get_config(config_path: str = None) -> Config:
    """Get or create configuration singleton."""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config(config_path)
    return _config_instance


def reset_config() -> None:
    """Reset configuration singleton."""
    global _config_instance
    _config_instance = None
