"""
Configuration Loader for Xiaohongshu Daily Autoposter
Loads and validates configuration from config.yaml
"""

import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path


class Config:
    """Configuration manager for the autoposter."""
    
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
        # Look for config.yaml in the same directory as this script
        script_dir = Path(__file__).parent
        skill_dir = script_dir.parent
        config_path = skill_dir / "scripts" / "config.yaml"
        
        if config_path.exists():
            return str(config_path)
        
        # Fallback to current directory
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
            'posting': {
                'default_time': '08:00',
                'timezone': 'Asia/Shanghai',
                'output_dir': './output'
            },
            'content': {
                'topics': ['职场效率', '生活美学', '学习成长'],
                'templates': 'viral',
                'min_length': 300,
                'max_length': 800,
                'title_count': 5
            },
            'image': {
                'default_theme': 'vibrant',
                'dimensions': '1000x1500',
                'quality': 95,
                'format': 'PNG'
            },
            'scheduler': {
                'enabled': True,
                'log_level': 'INFO',
                'log_file': './logs/scheduler.log'
            },
            'output': {
                'date_format': '%Y-%m-%d',
                'include_metadata': True,
                'include_title_options': True,
                'create_zip': False
            }
        }
    
    # Property getters for different sections
    @property
    def posting(self) -> Dict[str, Any]:
        return self._config.get('posting', {})
    
    @property
    def content(self) -> Dict[str, Any]:
        return self._config.get('content', {})
    
    @property
    def image(self) -> Dict[str, Any]:
        return self._config.get('image', {})
    
    @property
    def scheduler(self) -> Dict[str, Any]:
        return self._config.get('scheduler', {})
    
    @property
    def output(self) -> Dict[str, Any]:
        return self._config.get('output', {})
    
    @property
    def themes(self) -> Dict[str, Any]:
        return self._config.get('themes', {})
    
    # Specific value getters
    def get_posting_time(self) -> str:
        return self.posting.get('default_time', '08:00')
    
    def get_timezone(self) -> str:
        return self.posting.get('timezone', 'Asia/Shanghai')
    
    def get_output_dir(self) -> str:
        return self.posting.get('output_dir', './output')
    
    def get_topics(self) -> list:
        return self.content.get('topics', ['职场效率'])
    
    def get_template_style(self) -> str:
        return self.content.get('templates', 'viral')
    
    def get_image_theme(self) -> str:
        return self.image.get('default_theme', 'vibrant')
    
    def get_image_dimensions(self) -> tuple:
        dims = self.image.get('dimensions', '1000x1500')
        width, height = map(int, dims.split('x'))
        return width, height
    
    def get_image_quality(self) -> int:
        return self.image.get('quality', 95)
    
    def get_image_format(self) -> str:
        return self.image.get('format', 'PNG')
    
    def is_scheduler_enabled(self) -> bool:
        return self.scheduler.get('enabled', True)
    
    def get_log_level(self) -> str:
        return self.scheduler.get('log_level', 'INFO')
    
    def get_log_file(self) -> str:
        return self.scheduler.get('log_file', './logs/scheduler.log')
    
    # Theme-related methods
    def get_theme_colors(self, theme_name: str) -> list:
        """Get color palette for a theme."""
        theme = self.themes.get(theme_name, {})
        return theme.get('colors', ['#FF6B6B', '#4ECDC4'])
    
    def get_theme_fonts(self, theme_name: str) -> dict:
        """Get font settings for a theme."""
        theme = self.themes.get(theme_name, {})
        return theme.get('fonts', {'header': 'Arial', 'body': 'Arial'})
    
    def get_available_themes(self) -> list:
        """Get list of available theme names."""
        return list(self.themes.keys())
    
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


# Singleton instance for easy access
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
