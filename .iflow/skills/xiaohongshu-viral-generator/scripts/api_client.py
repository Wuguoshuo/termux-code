"""
AI API Client for Xiaohongshu Viral Generator
Handles image generation API calls to various AI providers
"""

import os
import time
import base64
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pathlib import Path
import requests

logger = logging.getLogger(__name__)


class BaseAPIClient(ABC):
    """Abstract base class for AI API clients."""
    
    @abstractmethod
    def generate_image(self, prompt: str, **kwargs) -> str:
        """Generate an image from a text prompt.
        
        Args:
            prompt: Text description of the image
            **kwargs: Additional parameters
            
        Returns:
            URL or path to the generated image
        """
        pass


class OpenAIClient(BaseAPIClient):
    """OpenAI DALL-E 3 API client."""
    
    def __init__(self, api_key: str = None, model: str = "dall-e-3", 
                 size: str = "1024x1536", quality: str = "standard"):
        """
        Initialize OpenAI API client.
        
        Args:
            api_key: OpenAI API key
            model: Model name (dall-e-2, dall-e-3)
            size: Image size (1024x1024, 1024x1536, etc.)
            quality: Image quality (standard, hd)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.size = size
        self.quality = quality
        self.base_url = "https://api.openai.com/v1"
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not set. Please set it in config or environment.")
    
    def _call_api(self, endpoint: str, payload: Dict) -> Dict:
        """Make API call to OpenAI."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{self.base_url}/{endpoint}",
            headers=headers,
            json=payload,
            timeout=120
        )
        
        response.raise_for_status()
        return response.json()
    
    def generate_image(self, prompt: str, style: str = None, count: int = 1) -> str:
        """
        Generate image using DALL-E 3.
        
        Args:
            prompt: Image description
            style: Optional style modifier
            count: Number of images to generate (DALL-E 3 only supports 1)
            
        Returns:
            URL to the generated image
        """
        # Enhance prompt for better results
        enhanced_prompt = self._enhance_prompt(prompt, style)
        
        payload = {
            "model": self.model,
            "prompt": enhanced_prompt,
            "n": min(count, 1),  # DALL-E 3 only supports 1
            "size": self.size,
            "quality": self.quality,
            "response_format": "url"
        }
        
        logger.info(f"Generating image with DALL-E 3...")
        response = self._call_api("images/generations", payload)
        
        image_url = response["data"][0]["url"]
        logger.info(f"Image generated successfully: {image_url}")
        
        return image_url
    
    def _enhance_prompt(self, prompt: str, style: str = None) -> str:
        """Enhance prompt for better image generation."""
        # Add小红书风格 modifiers
        modifiers = []
        
        if style:
            style_modifiers = {
                'modern minimalist': "modern minimalist style, clean design, high quality",
                'cute and fresh': "cute and fresh style, vibrant colors, cheerful mood",
                'warm vintage': "warm vintage style, nostalgic feel, soft colors",
                'tech blue': "tech blue style, modern technology, professional",
                'nature green': "nature green style, fresh and natural, peaceful"
            }
            modifiers.append(style_modifiers.get(style, style))
        
        # Add common modifiers for小红书 content
        modifiers.extend([
            "high quality photography",
            "professional lighting",
            "sharp focus",
            "Xiaohongshu style"
        ])
        
        enhanced = f"{prompt} - {', '.join(modifiers)}"
        return enhanced
    
    def download_image(self, url: str, save_path: str) -> str:
        """
        Download image from URL and save to file.
        
        Args:
            url: Image URL
            save_path: Local path to save the image
            
        Returns:
            Path to saved image
        """
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        logger.info(f"Image saved to: {save_path}")
        return save_path


class StabilityAIClient(BaseAPIClient):
    """Stability AI API client for Stable Diffusion."""
    
    def __init__(self, api_key: str = None, model: str = "stable-diffusion-xl"):
        """
        Initialize Stability AI API client.
        
        Args:
            api_key: Stability AI API key
            model: Model name
        """
        self.api_key = api_key or os.getenv("STABILITY_API_KEY")
        self.model = model
        self.base_url = "https://api.stability.ai/v1"
        
        if not self.api_key:
            raise ValueError("STABILITY_API_KEY not set. Please set it in config or environment.")
    
    def generate_image(self, prompt: str, style: str = None, count: int = 1) -> str:
        """
        Generate image using Stable Diffusion.
        
        Args:
            prompt: Image description
            style: Optional style modifier
            count: Number of images to generate
            
        Returns:
            Base64 encoded image data
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }
        
        payload = {
            "text_prompts": [
                {"text": self._enhance_prompt(prompt, style), "weight": 1}
            ],
            "cfg_scale": 7,
            "width": 1024,
            "height": 1536,
            "samples": count,
            "steps": 30
        }
        
        logger.info(f"Generating image with Stable Diffusion XL...")
        response = requests.post(
            f"{self.base_url}/generation/{self.model}/text-to-image",
            headers=headers,
            json=payload,
            timeout=180
        )
        
        response.raise_for_status()
        data = response.json()
        
        image_data = data["artifacts"][0]["base64"]
        logger.info(f"Image generated successfully")
        
        return image_data
    
    def _enhance_prompt(self, prompt: str, style: str = None) -> str:
        """Enhance prompt for better results."""
        modifiers = []
        
        if style:
            style_modifiers = {
                'modern minimalist': "modern minimalist, clean design, high quality photography",
                'cute and fresh': "cute and fresh, vibrant colors, cheerful, anime style",
                'warm vintage': "warm vintage, nostalgic, soft colors, film grain",
                'tech blue': "technology, blue tones, modern, professional, sleek",
                'nature green': "nature, green tones, fresh, peaceful, organic"
            }
            modifiers.append(style_modifiers.get(style, style))
        
        return f"{prompt}, {', '.join(modifiers)}"
    
    def save_base64_image(self, base64_data: str, save_path: str) -> str:
        """Save base64 image data to file."""
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        image_bytes = base64.b64decode(base64_data)
        with open(save_path, 'wb') as f:
            f.write(image_bytes)
        
        logger.info(f"Image saved to: {save_path}")
        return save_path


def create_api_client(provider: str = 'openai', **kwargs) -> BaseAPIClient:
    """
    Factory function to create API client based on provider.
    
    Args:
        provider: Provider name (openai, stability)
        **kwargs: Additional configuration
        
    Returns:
        API client instance
    """
    if provider == 'openai':
        return OpenAIClient(**kwargs)
    elif provider == 'stability':
        return StabilityAIClient(**kwargs)
    else:
        raise ValueError(f"Unknown provider: {provider}")


class APIManager:
    """Manages multiple API clients with fallback support."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize API manager.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.clients = {}
        self._init_clients()
    
    def _init_clients(self) -> None:
        """Initialize API clients from config."""
        ai_config = self.config.get('ai_image', {})
        provider = ai_config.get('provider', 'openai')
        
        if provider == 'openai':
            openai_config = ai_config.get('openai', {})
            try:
                self.clients['openai'] = OpenAIClient(
                    model=openai_config.get('model', 'dall-e-3'),
                    size=openai_config.get('size', '1024x1536'),
                    quality=openai_config.get('quality', 'standard')
                )
            except ValueError as e:
                logger.warning(f"Failed to initialize OpenAI client: {e}")
        
        if provider == 'stability':
            try:
                self.clients['stability'] = StabilityAIClient()
            except ValueError as e:
                logger.warning(f"Failed to initialize Stability client: {e}")
    
    def generate_image(self, prompt: str, style: str = None, 
                       save_path: str = None) -> Optional[str]:
        """
        Generate image using available clients.
        
        Args:
            prompt: Image description
            style: Visual style
            save_path: Local path to save image
            
        Returns:
            Path to saved image or None if failed
        """
        # Try OpenAI first, then Stability
        for provider in ['openai', 'stability']:
            if provider in self.clients:
                try:
                    client = self.clients[provider]
                    
                    if provider == 'openai':
                        image_url = client.generate_image(prompt, style)
                        if save_path:
                            return client.download_image(image_url, save_path)
                        return image_url
                    
                    elif provider == 'stability':
                        base64_data = client.generate_image(prompt, style)
                        if save_path:
                            return client.save_base64_image(base64_data, save_path)
                        return base64_data
                        
                except Exception as e:
                    logger.error(f"Image generation failed with {provider}: {e}")
                    continue
        
        logger.error("No available API clients for image generation")
        return None
