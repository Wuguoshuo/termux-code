"""
Image Generator for Xiaohongshu Viral Generator
Uses AI APIs to generate social media images
"""

import os
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

from api_client import APIManager, create_api_client

logger = logging.getLogger(__name__)


class ImageGenerator:
    """Generates images for Xiaohongshu posts using AI."""
    
    # 主题配置
    THEMES = {
        'modern minimalist': {
            'name': '现代简约',
            'description': 'Clean and professional look',
            'colors': ['#FFFFFF', '#F5F5F5', '#E0E0E0', '#424242'],
            'fonts': {'header': 'Arial', 'body': 'Arial'}
        },
        'cute and fresh': {
            'name': '可爱清新',
            'description': 'Vibrant and cheerful',
            'colors': ['#FFB6C1', '#98FB98', '#87CEEB', '#DDA0DD'],
            'fonts': {'header': 'Comic Sans MS', 'body': 'Arial'}
        },
        'warm vintage': {
            'name': '温暖复古',
            'description': 'Nostalgic and cozy',
            'colors': ['#DEB887', '#F5DEB3', '#8B4513', '#D2691E'],
            'fonts': {'header': 'Georgia', 'body': 'Georgia'}
        },
        'tech blue': {
            'name': '科技蓝',
            'description': 'Modern and professional',
            'colors': ['#1E90FF', '#4169E1', '#00BFFF', '#191970'],
            'fonts': {'header': 'Arial', 'body': 'Arial'}
        },
        'nature green': {
            'name': '自然绿',
            'description': 'Fresh and natural',
            'colors': ['#90EE90', '#3CB371', '#228B22', '#006400'],
            'fonts': {'header': 'Arial', 'body': 'Arial'}
        }
    }
    
    def __init__(self, config: Dict[str, Any] = None, api_manager: APIManager = None):
        """
        Initialize image generator.
        
        Args:
            config: Configuration dictionary
            api_manager: APIManager instance for AI API calls
        """
        self.config = config or {}
        self.api_manager = api_manager or self._create_api_manager()
        self.output_dir = self.config.get('output_dir', './output')
        self.default_size = self.config.get('size', '1024x1536')
        self.default_quality = self.config.get('quality', 95)
    
    def _create_api_manager(self) -> Optional[APIManager]:
        """Create API manager from config."""
        try:
            return APIManager(self.config)
        except Exception as e:
            logger.warning(f"Failed to create API manager: {e}")
            return None
    
    def get_available_themes(self) -> List[str]:
        """Get list of available image themes."""
        return list(self.THEMES.keys())
    
    def get_theme_info(self, theme: str) -> Dict[str, Any]:
        """Get information about a specific theme."""
        return self.THEMES.get(theme, self.THEMES['modern minimalist'])
    
    def generate_cover_image(self, title: str, topic: str, 
                             style: str = 'modern minimalist') -> Optional[str]:
        """
        Generate cover image for a post.
        
        Args:
            title: Post title
            topic: Content topic
            style: Visual theme
            
        Returns:
            Path to generated image or None if failed
        """
        if not self.api_manager:
            logger.error("No API manager available for image generation")
            return self._create_placeholder_image(title, topic, style)
        
        # Generate AI prompt
        prompt = self._build_cover_prompt(title, topic, style)
        
        # Generate image
        date_str = self._get_date_string()
        save_path = Path(self.output_dir) / date_str / f"cover_image.png"
        
        result = self.api_manager.generate_image(
            prompt=prompt,
            style=style,
            save_path=str(save_path)
        )
        
        if result:
            logger.info(f"Cover image generated: {result}")
            return result
        
        # Fallback to placeholder
        return self._create_placeholder_image(title, topic, style)
    
    def generate_post_images(self, body: str, topic: str, 
                             count: int = 4) -> List[str]:
        """
        Generate multiple post images based on body content.
        
        Args:
            body: Post body content
            topic: Content topic
            count: Number of images to generate
            
        Returns:
            List of paths to generated images
        """
        images = []
        
        # Extract key points from body for image prompts
        key_points = self._extract_key_points(body)
        
        for i in range(min(count, len(key_points))):
            prompt = self._build_content_prompt(key_points[i], topic)
            style = self._select_complementary_style(i)
            
            date_str = self._get_date_string()
            save_path = Path(self.output_dir) / date_str / f"image_{i+1}.png"
            
            result = self.api_manager.generate_image(
                prompt=prompt,
                style=style,
                save_path=str(save_path)
            )
            
            if result:
                images.append(result)
            else:
                # Create placeholder
                placeholder = self._create_placeholder_image(
                    key_points[i][:20], topic, style
                )
                if placeholder:
                    images.append(placeholder)
        
        return images
    
    def _build_cover_prompt(self, title: str, topic: str, style: str) -> str:
        """Build AI prompt for cover image."""
        theme_info = self.get_theme_info(style)
        
        prompt_parts = [
            f"Create a {style} style cover image for a social media post.",
            f"Title: {title}",
            f"Topic: {topic}",
            f"Color scheme: {', '.join(theme_info['colors'][:2])}",
            "High quality, professional photography style,",
            "Suitable for Xiaohongshu platform,",
            "Clean composition with text space"
        ]
        
        return ". ".join(prompt_parts)
    
    def _build_content_prompt(self, key_point: str, topic: str) -> str:
        """Build AI prompt for content image."""
        return (
            f"Illustration for: {key_point}. "
            f"Topic: {topic}. "
            "Social media style, clean and professional, "
            "high quality, Xiaohongshu aesthetic"
        )
    
    def _extract_key_points(self, body: str) -> List[str]:
        """Extract key points from body content for image generation."""
        # Split by newlines and filter meaningful sentences
        sentences = [
            s.strip() for s in body.split('

') 
            if len(s.strip()) > 20 and not s.strip().startswith('💡')
        ]
        return sentences[:6]  # Return up to 6 key points
    
    def _select_complementary_style(self, index: int) -> str:
        """Select a complementary style for sequential images."""
        styles = list(self.THEMES.keys())
        return styles[index % len(styles)]
    
    def _get_date_string(self) -> str:
        """Get current date string for directory naming."""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d')
    
    def _create_placeholder_image(self, text: str, topic: str, 
                                   style: str = 'modern minimalist') -> Optional[str]:
        """
        Create a placeholder image when AI generation is not available.
        
        Args:
            text: Text to display on placeholder
            topic: Content topic
            style: Visual theme
            
        Returns:
            Path to created placeholder image
        """
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            theme_info = self.get_theme_info(style)
            
            # Create image
            width, height = 1024, 1536
            bg_color = theme_info['colors'][0]
            text_color = theme_info['colors'][-1]
            
            image = Image.new('RGB', (width, height), bg_color)
            draw = ImageDraw.Draw(image)
            
            # Draw decorative elements
            draw.rectangle(
                [50, 50, width-50, height-50],
                outline=text_color,
                width=3
            )
            
            # Try to use a font, fallback to default if not available
            try:
                font = ImageFont.truetype("/system/fonts/NotoSansSC-Bold.ttf", 48)
            except:
                font = ImageFont.load_default()
            
            # Draw text (truncated if too long)
            display_text = text[:30] + "..." if len(text) > 30 else text
            
            # Calculate text position (center)
            bbox = draw.textbbox((0, 0), display_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (width - text_width) // 2
            y = (height - text_height) // 2
            
            draw.text((x, y), display_text, fill=text_color, font=font)
            
            # Add topic label
            topic_text = f"话题: {topic}"
            topic_bbox = draw.textbbox((0, 0), topic_text, font=font)
            topic_width = topic_bbox[2] - topic_bbox[0]
            
            draw.text(
                ((width - topic_width) // 2, height - 150),
                topic_text,
                fill=text_color,
                font=font
            )
            
            # Save image
            date_str = self._get_date_string()
            output_path = Path(self.output_dir) / date_str / "cover_image.png"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            image.save(str(output_path), quality=95)
            logger.info(f"Placeholder image created: {output_path}")
            
            return str(output_path)
            
        except ImportError:
            logger.error("PIL not available, cannot create placeholder image")
            return None
        except Exception as e:
            logger.error(f"Failed to create placeholder image: {e}")
            return None
    
    def generate_all_images(self, post: Dict[str, Any], 
                            output_dir: str = None) -> Dict[str, Any]:
        """
        Generate all images for a complete post.
        
        Args:
            post: Generated post dictionary
            output_dir: Output directory path
            
        Returns:
            Dictionary with image paths
        """
        output_dir = output_dir or self.output_dir
        images = {}
        
        # Generate cover image
        cover_path = self.generate_cover_image(
            post['title'],
            post['topic'],
            post.get('image_style', 'modern minimalist')
        )
        if cover_path:
            images['cover'] = cover_path
        
        # Generate post images
        post_images = self.generate_post_images(
            post['body'],
            post['topic'],
            count=4
        )
        images['post'] = post_images
        
        return images
